# Deployment Guide

This guide covers deploying Fed-Dup in production environments — including
Docker, Docker Compose, Kubernetes, reverse proxies, and security hardening.

## Table of Contents

- [Deployment Options](#deployment-options)
- [Docker Compose (Recommended)](#docker-compose-recommended)
- [Standalone Docker](#standalone-docker)
- [Kubernetes](#kubernetes)
- [Systemd Service](#systemd-service)
- [Cron / CI Deployment](#cron--ci-deployment)
- [Reverse Proxy & TLS](#reverse-proxy--tls)
- [Authentication](#authentication)
- [Persistent Storage](#persistent-storage)
- [Health Checks & Monitoring](#health-checks--monitoring)
- [Security Hardening](#security-hardening)
- [Backup & Recovery](#backup--recovery)

---

## Deployment Options

| Option              | Best For                          | Complexity |
|---------------------|-----------------------------------|------------|
| Docker Compose      | Single-host production            | Low        |
| Standalone Docker   | Quick trial / single container    | Low        |
| Kubernetes          | Scalable, cloud-native deploys    | High       |
| Systemd service     | Bare-metal / VM without Docker    | Medium     |
| Cron / CI (`--once`)| Scheduled, stateless syncs        | Low        |

---

## Docker Compose (Recommended)

The included `docker-compose.yml` is the fastest path to a production-ready
deployment.

### 1. Prepare configuration

```bash
cp config.json.example config.json
# Edit config.json with your tokens and repositories
chmod 600 config.json
```

### 2. Start the service

```bash
docker compose up -d
```

### 3. Verify health

```bash
docker compose ps
# The STATUS column should show "Up (healthy)"
```

### 4. View logs

```bash
docker compose logs -f feddup
```

The compose file:
- Maps port **8501** → host **8501**.
- Mounts `./config.json` into the container (read-write for UI edits).
- Creates a named volume `feddup_workspace` for mirror storage.
- Runs a healthcheck against `/_stcore/health`.

---

## Standalone Docker

```bash
docker build -t feddup:1.0.0 .

docker run -d \
  --name feddup \
  -p 8501:8501 \
  -v $(pwd)/config.json:/app/config.json \
  -v feddup_workspace:/app/feddup_workspace \
  --restart unless-stopped \
  feddup:1.0.0
```

Check health:
```bash
curl http://localhost:8501/_stcore/health
# Expected: "ok"
```

---

## Kubernetes

A minimal Kubernetes deployment:

### ConfigMap (non-secret settings)

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: feddup-config
data:
  auto_sync_interval: "3600"
  cleanup_after_sync: "true"
  max_parallel_syncs: "3"
```

### Secret (tokens)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: feddup-secrets
type: Opaque
stringData:
  github_token: "ghp_your_source_token"
  backup_token: "your_destination_token"
```

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: feddup
spec:
  replicas: 1
  selector:
    matchLabels:
      app: feddup
  template:
    metadata:
      labels:
        app: feddup
    spec:
      containers:
        - name: feddup
          image: feddup:1.0.0
          ports:
            - containerPort: 8501
          envFrom:
            - secretRef:
                name: feddup-secrets
            - configMapRef:
                name: feddup-config
          volumeMounts:
            - name: workspace
              mountPath: /app/feddup_workspace
          livenessProbe:
            httpGet:
              path: /_stcore/health
              port: 8501
            initialDelaySeconds: 30
            periodSeconds: 30
          readinessProbe:
            httpGet:
              path: /_stcore/health
              port: 8501
            initialDelaySeconds: 10
            periodSeconds: 10
      volumes:
        - name: workspace
          persistentVolumeClaim:
            claimName: feddup-workspace
```

### PVC

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: feddup-workspace
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

### CronJob (CI mode)

For scheduled syncs without a persistent UI:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: feddup-sync
spec:
  schedule: "0 */6 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: feddup
              image: feddup:1.0.0
              command: ["python", "worker.py", "--once"]
              envFrom:
                - secretRef:
                    name: feddup-secrets
          restartPolicy: OnFailure
```

---

## Systemd Service

For bare-metal or VM deployments without Docker:

### 1. Install Fed-Dup

Follow [INSTALL.md](INSTALL.md).

### 2. Create a systemd unit

`/etc/systemd/system/feddup.service`:

```ini
[Unit]
Description=Fed-Dup Repository Mirroring Engine
After=network.target

[Service]
Type=simple
User=feddup
Group=feddup
WorkingDirectory=/opt/fed-dup
EnvironmentFile=/opt/fed-dup/.env
ExecStart=/opt/fed-dup/.venv/bin/streamlit run app.py --server.port=8501 --server.address=127.0.0.1
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3. Create the user and set permissions

```bash
sudo useradd -r -s /bin/false -d /opt/fed-dup feddup
sudo chown -R feddup:feddup /opt/fed-dup
sudo chmod 600 /opt/fed-dup/config.json
```

### 4. Enable and start

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now feddup
sudo systemctl status feddup
```

---

## Cron / CI Deployment

For stateless, scheduled syncs using `--once`:

```cron
# Sync every 6 hours
0 */6 * * *  cd /opt/fed-dup && /opt/fed-dup/.venv/bin/python worker.py --once >> /var/log/fed-dup.log 2>&1
```

This is ideal when you don't need the web UI and just want automated
mirroring.

---

## Reverse Proxy & TLS

**Do not expose the Streamlit UI directly to the internet.** Use a reverse
proxy with TLS termination.

### Caddy (automatic TLS)

```caddyfile
feddup.example.com {
    reverse_proxy localhost:8501
}
```

### nginx

```nginx
server {
    listen 443 ssl http2;
    server_name feddup.example.com;

    ssl_certificate     /etc/ssl/certs/feddup.crt;
    ssl_certificate_key /etc/ssl/private/feddup.key;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}

server {
    listen 80;
    server_name feddup.example.com;
    return 301 https://$host$request_uri;
}
```

> **WebSocket support is required** — Streamlit uses WebSockets for live
> updates. The `Upgrade` and `Connection` headers above enable this.

---

## Authentication

Streamlit does not include built-in authentication. Add an auth layer at the
reverse proxy:

- **OAuth Proxy:** Use [oauth2-proxy](https://oauth2-proxy.github.io/) with
  GitHub, Google, or OIDC.
- **Cloudflare Access:** Zero-trust access in front of the proxy.
- **Basic Auth (nginx):** For small teams:
  ```nginx
  auth_basic "Fed-Dup";
  auth_basic_user_file /etc/nginx/.htpasswd;
  ```

---

## Persistent Storage

| Data              | Location                  | Must Persist? |
|-------------------|---------------------------|---------------|
| `config.json`     | Mounted volume / file     | ✅ Yes — all settings & tokens |
| `feddup_workspace/` | Named volume / PVC      | Optional — if `cleanup_after_sync` is true, this is just temp space. If false, mirrors accumulate here. |

For Kubernetes, use a `PersistentVolumeClaim`. For Docker Compose, the named
volume handles persistence automatically.

---

## Health Checks & Monitoring

### Health endpoint

Streamlit exposes `/_stcore/health` which returns `ok` (HTTP 200) when the
server is up.

```bash
curl http://localhost:8501/_stcore/health
```

### Docker healthcheck

The `Dockerfile` includes:
```dockerfile
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1
```

### External monitoring

Point your monitoring tool (Uptime Kuma, Pingdom, Prometheus blackbox
exporter) at the health endpoint.

### Logging

- The worker logs to stdout. In Docker, view with `docker compose logs`.
- In systemd, logs go to journald: `journalctl -u feddup -f`.
- All token substrings are redacted before logging.

---

## Security Hardening

See [SECURITY.md](SECURITY.md) for the full checklist. Key production items:

1. ✅ **TLS** — terminate TLS at the reverse proxy.
2. ✅ **Authentication** — add an auth layer (oauth2-proxy, Cloudflare Access,
   basic auth).
3. ✅ **File permissions** — `chmod 600 config.json`; run as non-root user.
4. ✅ **Token scope** — use read-only tokens for sources, scoped write tokens
   for destinations.
5. ✅ **Token rotation** — rotate regularly; use expiring tokens where
   supported.
6. ✅ **Network isolation** — restrict egress to known Git hosts only if
   possible.
7. ✅ **Resource limits** — set CPU/memory limits in Docker/K8s to prevent
   runaway syncs.
8. ✅ **Cleanup** — enable `cleanup_after_sync` to minimize disk usage.

---

## Backup & Recovery

Fed-Dup itself is a backup tool, but it also needs to be backed up:

1. **Back up `config.json`** — this is the only stateful file. Store it in a
   secrets manager or encrypted backup. It contains tokens, so treat it as a
   secret.
2. **Back up the destination repos** — your mirrored repos *are* the backup.
   Verify they are accessible and complete periodically.
3. **Recovery:** To restore, redeploy Fed-Dup and restore `config.json`. The
   workspace directory is ephemeral (it is just bare mirrors) and does not
   need to be backed up if `cleanup_after_sync` is enabled.

---

## Production Checklist

- [ ] TLS enabled at reverse proxy
- [ ] Authentication layer configured
- [ ] `config.json` permissions set to `600`
- [ ] Running as non-root user
- [ ] Token scopes minimized (read-only source, scoped write dest)
- [ ] `cleanup_after_sync` enabled (if disk space is a concern)
- [ ] Health check monitored externally
- [ ] Logs being collected and reviewed
- [ ] Resource limits set (Docker/K8s)
- [ ] `config.json` backed up to a secure location
- [ ] Destination repos verified as accessible
