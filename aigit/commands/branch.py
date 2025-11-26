"""Branch command implementation."""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

from aigit.config import get_config
from aigit.services import ai, git

console = Console()


def branch_command(
    description: str = typer.Argument(None, help="Description for branch (optional)"),
    yes: bool = typer.Option(False, "-y", "--yes", help="Skip confirmation"),
):
    """Generate AI branch name and create branch."""

    try:
        repo = git.get_repo()

        # Get context for branch name
        diff = None
        if not description:
            # Use staged changes or all changes
            if git.has_staged_changes(repo):
                diff = git.get_staged_diff(repo)
            elif git.has_unstaged_changes(repo):
                diff = git.get_unstaged_diff(repo)
            else:
                console.print("[yellow]No changes found. Please provide a description:[/yellow]")
                description = Prompt.ask("Branch description")

        # Generate branch name
        console.print("[cyan]Generating branch name...[/cyan]")

        try:
            branch_name = ai.generate_branch_name(diff, description)
        except ValueError as e:
            console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)
        except Exception as e:
            console.print(f"[red]Failed to generate branch name:[/red] {e}")
            raise typer.Exit(1)

        # Display the name
        console.print()
        console.print(Panel(branch_name, title="Generated Branch Name", border_style="green"))
        console.print()

        # Confirm or edit
        interactive = get_config("interactive") and not yes

        if interactive:
            action = Prompt.ask(
                "Action",
                choices=["create", "edit", "cancel"],
                default="create"
            )

            if action == "cancel":
                console.print("[yellow]Branch creation cancelled.[/yellow]")
                raise typer.Exit(0)
            elif action == "edit":
                branch_name = Prompt.ask("Enter branch name", default=branch_name)

        # Create and checkout branch
        try:
            git.create_branch(branch_name, repo, checkout=True)
            console.print(f"[green]✓[/green] Created and checked out branch [cyan]{branch_name}[/cyan]")
        except Exception as e:
            console.print(f"[red]Failed to create branch:[/red] {e}")
            raise typer.Exit(1)

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

