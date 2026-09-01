"""Unit tests for feddup.config"""

import json

import pytest

import feddup.config as config_module
from feddup.config import (
    load_config,
    save_config,
    add_repository,
    remove_repository,
    get_repository_count,
    get_repositories,
    get_setting,
)


@pytest.fixture(autouse=True)
def temp_config(tmp_path, monkeypatch):
    """Redirect CONFIG_FILE to a temp file for every test."""
    cfg = tmp_path / "config.json"
    monkeypatch.setattr(config_module, "CONFIG_FILE", cfg)
    return cfg


class TestLoadConfig:
    def test_missing_file_returns_defaults(self, temp_config):
        assert not temp_config.exists()
        cfg = load_config()
        assert cfg["github_token"] == ""
        assert cfg["backup_token"] == ""
        assert cfg["repositories"] == []
        assert cfg["settings"]["auto_sync_interval"] == 3600
        assert cfg["settings"]["cleanup_after_sync"] is False

    def test_loads_existing_file(self, temp_config):
        temp_config.write_text(
            json.dumps(
                {
                    "github_token": "ghp_abc",
                    "backup_token": "glpat_xyz",
                    "repositories": [{"name": "r", "source": "s", "destination": "d"}],
                    "settings": {"auto_sync_interval": 60, "cleanup_after_sync": True},
                }
            )
        )
        cfg = load_config()
        assert cfg["github_token"] == "ghp_abc"
        assert len(cfg["repositories"]) == 1

    def test_corrupt_file_returns_defaults(self, temp_config):
        temp_config.write_text("{not valid json}")
        cfg = load_config()
        assert cfg["repositories"] == []

    def test_backfills_missing_settings(self, temp_config):
        temp_config.write_text(json.dumps({"github_token": "x"}))
        cfg = load_config()
        assert cfg["settings"]["auto_sync_interval"] == 3600


class TestSaveConfig:
    def test_writes_file(self, temp_config):
        save_config({"github_token": "tok", "repositories": [], "settings": {}})
        data = json.loads(temp_config.read_text())
        assert data["github_token"] == "tok"


class TestAddRemoveRepository:
    def test_add_persists(self, temp_config):
        cfg = load_config()
        add_repository(
            cfg,
            "repo1",
            "https://github.com/u/repo.git",
            "https://gitlab.com/u/repo.git",
        )
        cfg2 = load_config()
        assert cfg2["repositories"][0]["name"] == "repo1"

    def test_remove_valid_index(self, temp_config):
        cfg = load_config()
        add_repository(cfg, "a", "s", "d")
        add_repository(cfg, "b", "s", "d")
        assert remove_repository(cfg, 0) is True
        cfg2 = load_config()
        assert cfg2["repositories"][0]["name"] == "b"

    def test_remove_invalid_index(self, temp_config):
        cfg = load_config()
        assert remove_repository(cfg, 99) is False


class TestHelpers:
    def test_count(self, temp_config):
        cfg = load_config()
        assert get_repository_count(cfg) == 0
        add_repository(cfg, "a", "s", "d")
        assert get_repository_count(load_config()) == 1

    def test_get_repositories(self, temp_config):
        cfg = load_config()
        assert get_repositories(cfg) == []

    def test_get_setting_default(self, temp_config):
        cfg = load_config()
        assert get_setting(cfg, "nonexistent", "fallback") == "fallback"
