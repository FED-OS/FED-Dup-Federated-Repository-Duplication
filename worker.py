"""
Fed-Dup Background Worker
Runs on a schedule to sync repositories automatically without the UI.

Usage:
    python worker.py            # uses interval from config.json
    python worker.py --once     # single sync then exit (great for cron/CI)
"""

import argparse
import time
from pathlib import Path

from feddup.config import load_config
from feddup.engine import duplicate_repository
from feddup.logger import get_logger

logger = get_logger("feddup.worker")
CONFIG_FILE = Path("config.json")


def sync_all(config=None):
    """Sync every configured repository once.

    Returns a list of ``(repo_name, success, message)`` tuples.
    """
    if config is None:
        config = load_config()
    gh_token = config.get("github_token", "")
    backup_token = config.get("backup_token", "")
    cleanup = config.get("settings", {}).get("cleanup_after_sync", False)

    results = []
    for repo in config.get("repositories", []):
        logger.info(f"⏳ Auto-syncing: {repo['name']}")
        success, msg = duplicate_repository(
            repo, gh_token, backup_token, cleanup=cleanup
        )
        if success:
            logger.info(f"✅ {msg}")
        else:
            logger.error(f"❌ {msg}")
        results.append((repo["name"], success, msg))
    return results


def auto_sync_loop():
    """Loop forever, syncing at the configured interval."""
    logger.info("🛡️ Fed-Dup worker started - entering sync loop")
    while True:
        try:
            config = load_config()
            interval = config.get("settings", {}).get("auto_sync_interval", 3600)
            sync_all(config)
        except Exception as e:  # noqa: BLE001
            logger.error(f"⚠️ Worker error: {e}")
        time.sleep(max(60, int(interval)))


def main():
    parser = argparse.ArgumentParser(description="Fed-Dup background sync worker")
    parser.add_argument("--once", action="store_true", help="Sync once and exit")
    args = parser.parse_args()

    if args.once:
        sync_all()
    else:
        auto_sync_loop()


if __name__ == "__main__":
    main()
