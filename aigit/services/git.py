"""Git service for local Git operations."""

import subprocess
from pathlib import Path

from git import Repo
from git.exc import InvalidGitRepositoryError


def get_repo(path: str = ".") -> Repo:
    """Get the Git repository at the given path."""
    try:
        return Repo(path, search_parent_directories=True)
    except InvalidGitRepositoryError:
        raise ValueError(f"Not a git repository: {path}")


def get_staged_diff(repo: Repo = None) -> str:
    """Get the diff of staged changes."""
    repo = repo or get_repo()
    return repo.git.diff("--staged")


def get_unstaged_diff(repo: Repo = None) -> str:
    """Get the diff of unstaged changes."""
    repo = repo or get_repo()
    return repo.git.diff()


def get_all_diff(repo: Repo = None) -> str:
    """Get diff of all changes (staged + unstaged)."""
    repo = repo or get_repo()
    staged = get_staged_diff(repo)
    unstaged = get_unstaged_diff(repo)

    if staged and unstaged:
        return f"{staged}\n{unstaged}"
    return staged or unstaged


def get_branch_diff(repo: Repo = None, base_branch: str = None) -> str:
    """Get diff between current branch and base branch."""
    repo = repo or get_repo()
    base = base_branch or get_default_branch(repo)

    return repo.git.diff(f"{base}...HEAD")


def get_commit_diff(repo: Repo = None, commit: str = "HEAD") -> str:
    """Get diff for a specific commit."""
    repo = repo or get_repo()
    return repo.git.show(commit, "--format=", "--patch")


def get_default_branch(repo: Repo = None) -> str:
    """Detect the default branch (main or master)."""
    repo = repo or get_repo()

    # Check remote default branch
    try:
        remote_head = repo.git.symbolic_ref("refs/remotes/origin/HEAD", short=True)
        return remote_head.replace("origin/", "")
    except Exception:
        pass

    # Fallback: check if main or master exists
    branches = [ref.name for ref in repo.references]
    if "main" in branches or "origin/main" in branches:
        return "main"
    if "master" in branches or "origin/master" in branches:
        return "master"

    return "main"  # Default assumption


def get_current_branch(repo: Repo = None) -> str:
    """Get the current branch name."""
    repo = repo or get_repo()
    return repo.active_branch.name


def get_changed_files(repo: Repo = None, base_branch: str = None) -> list[str]:
    """Get list of changed files compared to base branch."""
    repo = repo or get_repo()
    base = base_branch or get_default_branch(repo)

    try:
        output = repo.git.diff("--name-only", f"{base}...HEAD")
        return [f for f in output.split("\n") if f]
    except Exception:
        return []


def get_staged_files(repo: Repo = None) -> list[str]:
    """Get list of staged files."""
    repo = repo or get_repo()
    output = repo.git.diff("--staged", "--name-only")
    return [f for f in output.split("\n") if f]


def stage_all(repo: Repo = None) -> None:
    """Stage all changes."""
    repo = repo or get_repo()
    repo.git.add("-A")


def commit(message: str, repo: Repo = None) -> str:
    """Create a commit with the given message."""
    repo = repo or get_repo()
    repo.git.commit("-m", message)
    return repo.head.commit.hexsha[:7]


def create_branch(name: str, repo: Repo = None, checkout: bool = True) -> None:
    """Create a new branch."""
    repo = repo or get_repo()

    if checkout:
        repo.git.checkout("-b", name)
    else:
        repo.git.branch(name)


def has_staged_changes(repo: Repo = None) -> bool:
    """Check if there are staged changes."""
    repo = repo or get_repo()
    return bool(get_staged_diff(repo))


def has_unstaged_changes(repo: Repo = None) -> bool:
    """Check if there are unstaged changes."""
    repo = repo or get_repo()
    return bool(get_unstaged_diff(repo))


def has_any_changes(repo: Repo = None) -> bool:
    """Check if there are any changes."""
    repo = repo or get_repo()
    return has_staged_changes(repo) or has_unstaged_changes(repo)


def get_remote_url(repo: Repo = None) -> str | None:
    """Get the remote origin URL."""
    repo = repo or get_repo()

    try:
        return repo.remotes.origin.url
    except Exception:
        return None


def parse_github_url(url: str) -> tuple[str, str] | None:
    """Parse GitHub owner and repo from remote URL."""
    if not url:
        return None

    # Handle SSH URLs: git@github.com:owner/repo.git
    if url.startswith("git@github.com:"):
        path = url.replace("git@github.com:", "").replace(".git", "")
        parts = path.split("/")
        if len(parts) == 2:
            return parts[0], parts[1]

    # Handle HTTPS URLs: https://github.com/owner/repo.git
    if "github.com" in url:
        path = url.split("github.com/")[-1].replace(".git", "")
        parts = path.split("/")
        if len(parts) >= 2:
            return parts[0], parts[1]

    return None


def push_branch(repo: Repo = None, set_upstream: bool = True) -> None:
    """Push the current branch to origin."""
    repo = repo or get_repo()
    branch = get_current_branch(repo)

    if set_upstream:
        repo.git.push("-u", "origin", branch)
    else:
        repo.git.push("origin", branch)

