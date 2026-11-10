"""Tests for GitHub remote URL parsing."""

from aigit.services.git import parse_github_url


def test_ssh_url_with_git_suffix():
    assert parse_github_url("git@github.com:owner/repo.git") == ("owner", "repo")


def test_https_url_with_git_suffix():
    assert parse_github_url("https://github.com/owner/repo.git") == ("owner", "repo")


def test_https_url_without_suffix():
    assert parse_github_url("https://github.com/owner/repo") == ("owner", "repo")


def test_https_url_with_dotgit_mid_name():
    # Only a trailing ".git" is a suffix; ".git" inside the name must survive.
    assert parse_github_url("https://github.com/owner/dot.gitfiles") == ("owner", "dot.gitfiles")


def test_ssh_url_with_dotgit_mid_name():
    assert parse_github_url("git@github.com:owner/my.git.repo") == ("owner", "my.git.repo")


def test_non_github_and_empty_urls():
    assert parse_github_url("") is None
    assert parse_github_url(None) is None
    assert parse_github_url("https://gitlab.com/owner/repo.git") is None
