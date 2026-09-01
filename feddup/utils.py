"""
Fed-Dup Utilities: Validation, sanitization, disk management
"""

import re
import shutil
from pathlib import Path


def sanitize_git_url(url: str) -> str:
    """Clean URL: remove any existing auth credentials and ensure .git suffix.

    Strips embedded credentials such as ``user:pass@`` or ``oauth2:token@``
    so that tokens can be injected cleanly by the engine. Also normalizes the
    URL to end with ``.git`` to satisfy ``git clone --mirror`` expectations.
    """
    if not url:
        return url
    # Capture protocol before stripping credentials so it can be restored
    protocol_match = re.match(r"^(https?://)", url)
    protocol = protocol_match.group(1) if protocol_match else "https://"
    # Strip everything up to and including the last '@' (credentials)
    if "@" in url:
        url = url.rsplit("@", 1)[1]
    # Re-attach protocol if it was lost during stripping
    if not url.startswith("https://") and not url.startswith("http://"):
        url = protocol + url
    # Normalize to https
    if url.startswith("http://"):
        url = "https://" + url[len("http://") :]
    # Ensure .git suffix
    if not url.endswith(".git"):
        url += ".git"
    return url


def validate_source_url(url: str) -> bool:
    """Only allow HTTPS GitHub/GitLab/Bitbucket/Gitea/Codeberg sources."""
    if not url or not url.startswith("https://"):
        return False
    allowed = (
        "https://github.com/",
        "https://gitlab.com/",
        "https://bitbucket.org/",
        "https://codeberg.org/",
        "https://gitea.com/",
    )
    return url.startswith(allowed)


def validate_destination_url(url: str) -> bool:
    """Validate backup destination - any HTTPS Git server."""
    if not url:
        return False
    return url.startswith("https://") and url.endswith(".git")


def cleanup_workspace(workspace_dir: Path, repo_name: str) -> bool:
    """Remove a repo's mirror cache to save disk space."""
    repo_path = workspace_dir / f"{repo_name}.git"
    if repo_path.exists():
        shutil.rmtree(repo_path, ignore_errors=True)
        return True
    return False


def get_repo_size(workspace_dir: Path, repo_name: str) -> int:
    """Get size of cached repo in bytes."""
    repo_path = workspace_dir / f"{repo_name}.git"
    if repo_path.exists():
        return sum(f.stat().st_size for f in repo_path.rglob("*") if f.is_file())
    return 0


def humanize_size(num_bytes: int) -> str:
    """Convert bytes into a human-readable string."""
    if num_bytes <= 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(num_bytes)
    idx = 0
    while size >= 1024 and idx < len(units) - 1:
        size /= 1024
        idx += 1
    return f"{size:.1f} {units[idx]}"
