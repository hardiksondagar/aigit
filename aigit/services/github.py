"""GitHub service for PR operations."""

import webbrowser

from github import Github

from aigit.config import get_github_token
from aigit.services.git import get_repo, get_remote_url, parse_github_url


def get_client() -> Github:
    """Get GitHub client."""
    return Github(get_github_token())


def get_github_repo(repo=None):
    """Get the GitHub repository object."""
    repo = repo or get_repo()
    url = get_remote_url(repo)

    if not url:
        raise ValueError("No remote origin URL found")

    parsed = parse_github_url(url)
    if not parsed:
        raise ValueError(f"Could not parse GitHub URL: {url}")

    owner, repo_name = parsed
    client = get_client()

    return client.get_repo(f"{owner}/{repo_name}")


def create_pull_request(
    title: str,
    body: str,
    head: str,
    base: str,
    draft: bool = False,
    repo=None,
) -> dict:
    """Create a pull request on GitHub."""
    gh_repo = get_github_repo(repo)

    pr = gh_repo.create_pull(
        title=title,
        body=body,
        head=head,
        base=base,
        draft=draft,
    )

    return {
        "number": pr.number,
        "url": pr.html_url,
        "title": pr.title,
    }


def open_pr_in_browser(url: str) -> None:
    """Open a PR URL in the default browser."""
    webbrowser.open(url)

