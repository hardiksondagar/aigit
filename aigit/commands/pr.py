"""PR command implementation."""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

from aigit.config import get_config
from aigit.services import ai, git, github

console = Console()


def pr_command(
    base: str = typer.Option(None, "--base", "-b", help="Base branch for PR"),
    draft: bool = typer.Option(False, "--draft", help="Create as draft PR"),
    yes: bool = typer.Option(False, "-y", "--yes", help="Skip confirmation"),
    no_open: bool = typer.Option(False, "--no-open", help="Don't open PR in browser"),
):
    """Generate AI PR title/description and create pull request."""

    try:
        repo = git.get_repo()

        # Get current branch
        current_branch = git.get_current_branch(repo)

        # Get or detect base branch
        base_branch = base or git.get_default_branch(repo)

        # Check if we're on the base branch
        if current_branch == base_branch:
            console.print(f"[yellow]You're on the base branch ({base_branch}). Create a feature branch first.[/yellow]")
            raise typer.Exit(1)

        # Get diff and changed files
        diff = git.get_branch_diff(repo, base_branch)

        if not diff:
            console.print(f"[yellow]No changes between {current_branch} and {base_branch}.[/yellow]")
            raise typer.Exit(1)

        files_changed = git.get_changed_files(repo, base_branch)

        # Generate PR content
        console.print("[cyan]Generating PR title and description...[/cyan]")

        try:
            title, description = ai.generate_pr(diff, base_branch, current_branch, files_changed)
        except ValueError as e:
            console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)
        except Exception as e:
            console.print(f"[red]Failed to generate PR:[/red] {e}")
            raise typer.Exit(1)

        # Display the PR content
        console.print()
        console.print(Panel(title, title="PR Title", border_style="green"))
        console.print()
        console.print(Panel(description, title="PR Description", border_style="green"))
        console.print()
        console.print(f"[dim]Base: {base_branch} ← Head: {current_branch}[/dim]")
        console.print()

        # Confirm or edit
        interactive = get_config("interactive") and not yes

        if interactive:
            if not Confirm.ask("Create this PR?", default=True):
                console.print("[yellow]PR creation cancelled.[/yellow]")
                raise typer.Exit(0)

            if Confirm.ask("Edit title or description?", default=False):
                title = Prompt.ask("PR Title", default=title)
                console.print("PR Description (press Enter to keep current):")
                new_desc = Prompt.ask("", default="<keep current>")
                if new_desc != "<keep current>":
                    description = new_desc

        # Push branch to origin
        console.print(f"[cyan]Pushing {current_branch} to origin...[/cyan]")
        try:
            git.push_branch(repo, set_upstream=True)
        except Exception as e:
            console.print(f"[red]Failed to push branch:[/red] {e}")
            raise typer.Exit(1)

        # Create PR
        console.print("[cyan]Creating pull request...[/cyan]")
        try:
            pr_info = github.create_pull_request(
                title=title,
                body=description,
                head=current_branch,
                base=base_branch,
                draft=draft,
                repo=repo,
            )

            console.print(f"[green]✓[/green] Created PR #{pr_info['number']}: {pr_info['title']}")
            console.print(f"[cyan]{pr_info['url']}[/cyan]")

            # Open in browser
            if not no_open:
                console.print("[dim]Opening in browser...[/dim]")
                github.open_pr_in_browser(pr_info['url'])

        except ValueError as e:
            console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)
        except Exception as e:
            console.print(f"[red]Failed to create PR:[/red] {e}")
            raise typer.Exit(1)

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

