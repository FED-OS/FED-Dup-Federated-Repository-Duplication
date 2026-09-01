"""
Fed-Dup Configuration Handler (JSON-based, No Database)
"""

import json
from pathlib import Path
from typing import Dict, List

CONFIG_FILE = Path("config.json")

DEFAULT_SETTINGS = {
    "auto_sync_interval": 3600,  # seconds
    "cleanup_after_sync": False,
    "max_parallel_syncs": 3,
}


def _default_config() -> Dict:
    """Return a fresh default configuration dictionary."""
    return {
        "github_token": "",
        "backup_token": "",
        "repositories": [],
        "settings": dict(DEFAULT_SETTINGS),
    }


def load_config() -> Dict:
    """Load config from the JSON file.

    If the file does not exist, a default config is returned so the UI can
    boot without error on first run.
    """
    if not CONFIG_FILE.exists():
        return _default_config()
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
    except (json.JSONDecodeError, OSError):
        return _default_config()

    # Backfill any missing keys for forward-compatibility
    config.setdefault("github_token", "")
    config.setdefault("backup_token", "")
    config.setdefault("repositories", [])
    settings = config.get("settings", {})
    for key, value in DEFAULT_SETTINGS.items():
        settings.setdefault(key, value)
    config["settings"] = settings
    return config


def save_config(config: Dict) -> None:
    """Save config to the JSON file with pretty indentation."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


def add_repository(config: Dict, name: str, source: str, destination: str) -> None:
    """Add a repository to the config and persist it."""
    config["repositories"].append(
        {
            "name": name,
            "source": source,
            "destination": destination,
        }
    )
    save_config(config)


def remove_repository(config: Dict, index: int) -> bool:
    """Remove a repository by index. Returns True if removed."""
    repos = config.get("repositories", [])
    if 0 <= index < len(repos):
        repos.pop(index)
        save_config(config)
        return True
    return False


def get_repository_count(config: Dict) -> int:
    """Get number of configured repositories."""
    return len(config.get("repositories", []))


def get_repositories(config: Dict) -> List[Dict]:
    """Return the list of configured repositories."""
    return config.get("repositories", [])


def get_setting(config: Dict, key: str, default=None):
    """Fetch a single setting value with a fallback default."""
    return config.get("settings", {}).get(key, default)
