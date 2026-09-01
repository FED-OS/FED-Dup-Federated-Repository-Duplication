"""Unit tests for feddup.engine

These tests avoid real network/Git operations by monkeypatching
``subprocess.run`` and the workspace directory. The goal is to verify the
control flow, validation, token redaction, and cleanup behaviour.
"""

import subprocess
from unittest.mock import patch

import pytest

import feddup.engine as engine_module
from feddup.engine import duplicate_repository

REPO = {
    "name": "demo",
    "source": "https://github.com/user/demo.git",
    "destination": "https://gitlab.com/user/demo.git",
}


@pytest.fixture(autouse=True)
def temp_workspace(tmp_path, monkeypatch):
    """Redirect the workspace dir to a temp location for every test."""
    monkeypatch.setattr(engine_module, "WORKSPACE_DIR", tmp_path)
    return tmp_path


class FakeCompletedProcess:
    def __init__(self, returncode=0, stderr=b""):
        self.returncode = returncode
        self.stderr = stderr
        self.stdout = b""


def _make_git_success(*args, **kwargs):
    return FakeCompletedProcess(0, b"")


class TestValidation:
    def test_invalid_source_returns_error(self, temp_workspace):
        repo = dict(REPO, source="https://example.com/bad.git")
        success, msg = duplicate_repository(repo, "tok", "tok")
        assert success is False
        assert "Invalid source" in msg

    def test_invalid_destination_returns_error(self, temp_workspace):
        repo = dict(REPO, destination="https://gitlab.com/user/demo")  # no .git
        success, msg = duplicate_repository(repo, "tok", "tok")
        assert success is False
        assert "destination" in msg.lower()

    def test_non_https_rejected(self, temp_workspace):
        # sanitize forces https:// but validate_source_url checks https prefix;
        # http:// source gets rejected because sanitize keeps protocol and
        # validate_source_url only allows https://
        repo = dict(REPO, source="http://github.com/user/demo.git")
        success, msg = duplicate_repository(repo, "tok", "tok")
        # http:// is not in the allowed list -> invalid source
        assert success is False


class TestHappyPath:
    def test_fresh_clone_and_push(self, temp_workspace):
        with patch(
            "feddup.engine.subprocess.run", side_effect=_make_git_success
        ) as mock_run:
            success, msg = duplicate_repository(REPO, "ghp_secret", "glpat_secret")
        assert success is True
        assert "successful" in msg
        # Two git calls: clone --mirror then push --mirror
        assert mock_run.call_count == 2
        first_args = mock_run.call_args_list[0][0][0]
        assert "clone" in first_args and "--mirror" in first_args

    def test_existing_repo_updates(self, temp_workspace):
        # Pre-create the repo dir so it takes the update path
        (temp_workspace / "demo.git").mkdir()
        with patch(
            "feddup.engine.subprocess.run", side_effect=_make_git_success
        ) as mock_run:
            success, msg = duplicate_repository(REPO, "ghp_secret", "glpat_secret")
        assert success is True
        first_args = mock_run.call_args_list[0][0][0]
        assert "remote" in first_args and "update" in first_args


class TestTokenRedaction:
    def test_error_message_redacts_tokens(self, temp_workspace):
        def _fail(*args, **kwargs):
            raise subprocess.CalledProcessError(
                1, "git", stderr=b"fatal: auth failed for ghp_secret glpat_secret"
            )

        with patch("feddup.engine.subprocess.run", side_effect=_fail):
            success, msg = duplicate_repository(REPO, "ghp_secret", "glpat_secret")
        assert success is False
        assert "ghp_secret" not in msg
        assert "glpat_secret" not in msg
        assert "***" in msg


class TestCleanup:
    def test_cleanup_removes_repo_dir(self, temp_workspace):
        (temp_workspace / "demo.git").mkdir()
        (temp_workspace / "demo.git" / "config").write_text("x")
        with patch("feddup.engine.subprocess.run", side_effect=_make_git_success):
            success, msg = duplicate_repository(REPO, "tok", "tok", cleanup=True)
        assert success is True
        assert not (temp_workspace / "demo.git").exists()

    def test_no_cleanup_keeps_repo_dir(self, temp_workspace):
        # Simulate the clone creating the repo directory by making the
        # mocked subprocess side-effect create it on the "clone" call.
        repo_dir = temp_workspace / "demo.git"

        def _git_then_mkdir(*args, **kwargs):
            cmd = args[0]
            if "clone" in cmd:
                repo_dir.mkdir(parents=True, exist_ok=True)
            return FakeCompletedProcess(0, b"")

        with patch("feddup.engine.subprocess.run", side_effect=_git_then_mkdir):
            duplicate_repository(REPO, "tok", "tok", cleanup=False)
        # Without cleanup the repo dir should remain
        assert repo_dir.exists()
