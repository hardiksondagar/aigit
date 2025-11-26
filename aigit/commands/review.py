"""Review command implementation."""

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from aigit.services import ai, git

console = Console()


def review_command():
    """AI code review of staged changes."""

    try:
        repo = git.get_repo()

        # Check for staged changes
        if not git.has_staged_changes(repo):
            console.print("[yellow]No staged changes to review.[/yellow]")
            console.print("Use [cyan]git add[/cyan] to stage changes first.")
            raise typer.Exit(1)

        # Get diff
        diff = git.get_staged_diff(repo)

        # Generate review
        console.print("[cyan]Reviewing staged changes...[/cyan]")
        console.print()

        try:
            review = ai.generate_review(diff)
        except ValueError as e:
            console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)
        except Exception as e:
            console.print(f"[red]Failed to generate review:[/red] {e}")
            raise typer.Exit(1)

        # Display review
        console.print(Panel(Markdown(review), title="Code Review", border_style="blue"))

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

