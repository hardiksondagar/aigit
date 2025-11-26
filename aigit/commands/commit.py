"""Commit command implementation."""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

from aigit.config import get_config
from aigit.services import ai, git

console = Console()


def commit_command(
    all: bool = typer.Option(False, "-a", "--all", help="Stage all changes before committing"),
    message_hint: str = typer.Option(None, "-m", "--message", help="Hint for AI to generate message"),
    yes: bool = typer.Option(False, "-y", "--yes", help="Skip confirmation"),
):
    """Generate AI commit message and create commit."""

    try:
        repo = git.get_repo()

        # Stage all if requested
        if all:
            console.print("[cyan]Staging all changes...[/cyan]")
            git.stage_all(repo)

        # Check for staged changes
        if not git.has_staged_changes(repo):
            console.print("[yellow]No staged changes to commit.[/yellow]")
            console.print("Use [cyan]git add[/cyan] or [cyan]aigit commit -a[/cyan] to stage changes.")
            raise typer.Exit(1)

        # Get diff
        diff = git.get_staged_diff(repo)

        if not diff:
            console.print("[yellow]No changes to commit.[/yellow]")
            raise typer.Exit(1)

        # Generate commit message
        console.print("[cyan]Generating commit message...[/cyan]")
        conventional = get_config("conventional_commits")

        try:
            commit_message = ai.generate_commit_message(diff, conventional, message_hint)
        except ValueError as e:
            console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)
        except Exception as e:
            console.print(f"[red]Failed to generate commit message:[/red] {e}")
            raise typer.Exit(1)

        # Display the message
        console.print()
        console.print(Panel(commit_message, title="Generated Commit Message", border_style="green"))
        console.print()

        # Confirm or edit
        interactive = get_config("interactive") and not yes

        if interactive:
            action = Prompt.ask(
                "Action",
                choices=["commit", "edit", "cancel"],
                default="commit"
            )

            if action == "cancel":
                console.print("[yellow]Commit cancelled.[/yellow]")
                raise typer.Exit(0)
            elif action == "edit":
                commit_message = Prompt.ask("Enter commit message", default=commit_message)

        # Create commit
        try:
            commit_hash = git.commit(commit_message, repo)
            console.print(f"[green]✓[/green] Committed as [cyan]{commit_hash}[/cyan]")
        except Exception as e:
            console.print(f"[red]Failed to commit:[/red] {e}")
            raise typer.Exit(1)

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

