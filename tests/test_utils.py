"""Unit tests for feddup.utils"""

import shutil
import tempfile
from pathlib import Path

from feddup.utils import (
    sanitize_git_url,
    validate_source_url,
    validate_destination_url,
    cleanup_workspace,
    get_repo_size,
    humanize_size,
)


class TestSanitizeGitUrl:
    def test_adds_git_suffix(self):
        assert (
            sanitize_git_url("https://github.com/user/repo")
            == "https://github.com/user/repo.git"
        )

    def test_keeps_existing_git_suffix(self):
        assert (
            sanitize_git_url("https://github.com/user/repo.git")
            == "https://github.com/user/repo.git"
        )

    def test_strips_embedded_credentials(self):
        url = "https://oauth2:ghp_secret@github.com/user/repo.git"
        assert sanitize_git_url(url) == "https://github.com/user/repo.git"

    def test_strips_user_pass_credentials(self):
        url = "https://user:pass@github.com/user/repo.git"
        assert sanitize_git_url(url) == "https://github.com/user/repo.git"

    def test_strips_bare_token_at(self):
        url = "https://ghp_secret@github.com/user/repo.git"
        assert sanitize_git_url(url) == "https://github.com/user/repo.git"

    def test_empty_string(self):
        assert sanitize_git_url("") == ""

    def test_no_protocol_after_strip(self):
        # After stripping credentials from a bare host-path URL, the
        # protocol is restored so downstream git commands work.
        url = "oauth2:ghp_secret@github.com/user/repo"
        result = sanitize_git_url(url)
        assert result == "https://github.com/user/repo.git"


class TestValidateSourceUrl:
    def test_github_valid(self):
        assert validate_source_url("https://github.com/user/repo.git") is True

    def test_gitlab_valid(self):
        assert validate_source_url("https://gitlab.com/user/repo.git") is True

    def test_bitbucket_valid(self):
        assert validate_source_url("https://bitbucket.org/user/repo.git") is True

    def test_codeberg_valid(self):
        assert validate_source_url("https://codeberg.org/user/repo.git") is True

    def test_gitea_com_valid(self):
        assert validate_source_url("https://gitea.com/user/repo.git") is True

    def test_http_rejected(self):
        assert validate_source_url("http://github.com/user/repo.git") is False

    def test_random_host_rejected(self):
        assert validate_source_url("https://example.com/user/repo.git") is False

    def test_empty_rejected(self):
        assert validate_source_url("") is False


class TestValidateDestinationUrl:
    def test_valid_https_git(self):
        assert validate_destination_url("https://gitlab.com/user/repo.git") is True

    def test_missing_git_suffix(self):
        assert validate_destination_url("https://gitlab.com/user/repo") is False

    def test_http_rejected(self):
        assert validate_destination_url("http://gitlab.com/user/repo.git") is False

    def test_empty_rejected(self):
        assert validate_destination_url("") is False


class TestCleanupWorkspace:
    def setup_method(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.repo_dir = self.tmp / "myrepo.git"
        self.repo_dir.mkdir()
        (self.repo_dir / "config").write_text("dummy")

    def teardown_method(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_removes_existing_repo(self):
        assert cleanup_workspace(self.tmp, "myrepo") is True
        assert not self.repo_dir.exists()

    def test_missing_repo_returns_false(self):
        assert cleanup_workspace(self.tmp, "nope") is False


class TestGetRepoSize:
    def setup_method(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.repo_dir = self.tmp / "myrepo.git"
        self.repo_dir.mkdir()
        (self.repo_dir / "config").write_text("12345")
        (self.repo_dir / "objects").mkdir()

    def teardown_method(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_size_positive(self):
        size = get_repo_size(self.tmp, "myrepo")
        assert size == 5

    def test_missing_repo_zero(self):
        assert get_repo_size(self.tmp, "nope") == 0


class TestHumanizeSize:
    def test_zero(self):
        assert humanize_size(0) == "0 B"

    def test_bytes(self):
        assert humanize_size(512) == "512.0 B"

    def test_kilobytes(self):
        assert "KB" in humanize_size(2048)

    def test_megabytes(self):
        assert "MB" in humanize_size(5 * 1024 * 1024)
