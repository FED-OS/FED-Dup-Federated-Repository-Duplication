FROM python:3.14-slim

LABEL maintainer="Fed-Dup Team"
LABEL description="Fed-Dup - Federated Repository Duplication Engine"
LABEL version="1.0.0"

# Install Git (required for mirror operations)
RUN apt-get update && \
    apt-get install -y --no-install-recommends git curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Create workspace directory
RUN mkdir -p /app/feddup_workspace

# Expose Streamlit port
EXPOSE 8501

# Environment defaults
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    PYTHONUNBUFFERED=1 \
    TZ=UTC

# Health check against Streamlit's built-in health endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -fsS http://localhost:8501/_stcore/health || exit 1

# Run both the Streamlit UI and the background sync worker concurrently.
# The worker reads its interval from config.json (settings.auto_sync_interval).
CMD ["sh", "-c", "streamlit run app.py --server.port=8501 --server.address=0.0.0.0 & python worker.py"]
