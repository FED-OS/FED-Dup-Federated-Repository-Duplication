"""
Fed-Dup Core Engine
Federated Repository Duplication without dependencies.

The engine performs a two-phase Git mirror operation:
  1. ``git clone --mirror`` (or ``git remote update`` for cached repos)
  2. ``git push --mirror`` to the destination

All token material is injected into URLs only at the moment of subprocess
execution and is redacted from any error messages that bubble back to the
caller.
"""

import subprocess
from pathlib import Path

from feddup.utils import (
    sanitize_git_url,
    validate_source_url,
    validate_destination_url,
    cleanup_workspace,
)
from feddup.logger import get_logger

logger = get_logger(__name__)
WORKSPACE_DIR = Path("./feddup_workspace")


def _redact(message: str, *tokens: str) -> str:
    """Strip known token strings from an error message."""
    redacted = message
    for token in tokens:
        if token:
            redacted = redacted.replace(token, "***")
    return redacted


def _run_git(args: list, tokens: tuple) -> subprocess.CompletedProcess:
    """Run a git subprocess, raising CalledProcessError on non-zero exit."""
    return subprocess.run(args, check=True, capture_output=True)


def duplicate_repository(
    repo: dict, gh_token: str, backup_token: str, cleanup: bool = False
):
    """
    The main duplication engine.

    Clones --mirror from source, pushes --mirror to destination.

    Parameters
    ----------
    repo : dict
        Must contain ``name``, ``source``, and ``destination`` keys.
    gh_token : str
        Token used to authenticate against the source (read).
    backup_token : str
        Token used to authenticate against the destination (write).
    cleanup : bool
        If True, delete the local mirror cache after a successful push.

    Returns
    -------
    tuple[bool, str]
        ``(success, message)`` where message has any tokens redacted.
    """
    source = sanitize_git_url(repo["source"])
    destination = sanitize_git_url(repo["destination"])
    repo_name = repo["name"]

    logger.info(f"🔄 Starting Fed-Dup for: {repo_name}")

    # Validate before running
    if not validate_source_url(source):
        return False, f"Invalid source URL: {source}"
    if not validate_destination_url(destination):
        return False, f"Invalid destination URL: {destination}"
    if not source.startswith("https://"):
        return False, "Only HTTPS URLs are supported"

    # Inject tokens (oauth2:user@ form works for GitHub/GitLab/etc.)
    source_auth = source.replace("https://", f"https://oauth2:{gh_token}@")
    dest_auth = destination.replace("https://", f"https://oauth2:{backup_token}@")

    # Create workspace
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    repo_dir = WORKSPACE_DIR / f"{repo_name}.git"

    try:
        # Phase 1: Clone mirror or update existing
        if not repo_dir.exists():
            logger.info(f"📥 Fresh mirror clone of {repo_name}")
            _run_git(
                ["git", "clone", "--mirror", source_auth, str(repo_dir)],
                (gh_token, backup_token),
            )
        else:
            logger.info(f"🔄 Updating existing mirror of {repo_name}")
            _run_git(
                ["git", "--git-dir", str(repo_dir), "remote", "update"],
                (gh_token, backup_token),
            )

        # Phase 2: Push mirror to destination
        logger.info(f"📤 Pushing {repo_name} to backup destination")
        _run_git(
            ["git", "--git-dir", str(repo_dir), "push", "--mirror", dest_auth],
            (gh_token, backup_token),
        )

        # Phase 3: Cleanup if requested
        if cleanup:
            cleanup_workspace(WORKSPACE_DIR, repo_name)
            logger.info(f"🧹 Cleaned up workspace for {repo_name}")

        logger.info(f"✅ Fed-Dup completed: {repo_name}")
        return True, f"Fed-Dup successful for {repo_name}"

    except subprocess.CalledProcessError as e:
        error_msg = ""
        if e.stderr:
            try:
                error_msg = e.stderr.decode(errors="replace")
            except Exception:
                error_msg = str(e.stderr)
        error_msg = _redact(error_msg, gh_token, backup_token)
        logger.error(f"❌ Fed-Dup failed for {repo_name}: {error_msg}")
        return False, f"Git error: {error_msg}"
    except Exception as e:
        error_msg = _redact(str(e), gh_token, backup_token)
        logger.error(f"❌ Fed-Dup failed for {repo_name}: {error_msg}")
        return False, f"Error: {error_msg}"
