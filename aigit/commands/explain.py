"""Explain command implementation."""

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from aigit.services import ai, git

console = Console()


def explain_command(
    target: str = typer.Argument(None, help="Commit hash, branch, or empty for current diff"),
):
    """Explain what changed in a commit/branch/diff."""

    try:
        repo = git.get_repo()

        # Determine what to explain
        context = None
        diff = None

        if target:
            # Try to get diff for specific commit or branch
            try:
                # First try as a commit
                diff = git.get_commit_diff(repo, target)
                context = f"Commit: {target}"
            except Exception:
                # Maybe it's a branch?
                try:
                    current = git.get_current_branch(repo)
                    diff = git.get_branch_diff(repo, target)
                    context = f"Branch diff: {target}...{current}"
                except Exception:
                    console.print(f"[red]Could not find commit or branch:[/red] {target}")
                    raise typer.Exit(1)
        else:
            # Explain current changes
            if git.has_staged_changes(repo):
                diff = git.get_staged_diff(repo)
                context = "Staged changes"
            elif git.has_unstaged_changes(repo):
                diff = git.get_unstaged_diff(repo)
                context = "Unstaged changes"
            else:
                console.print("[yellow]No changes to explain.[/yellow]")
                console.print("Specify a commit hash or branch, or make some changes first.")
                raise typer.Exit(1)

        if not diff:
            console.print("[yellow]No changes found.[/yellow]")
            raise typer.Exit(1)

        # Generate explanation
        console.print(f"[cyan]Explaining {context}...[/cyan]")
        console.print()

        try:
            explanation = ai.generate_explanation(diff, context)
        except ValueError as e:
            console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)
        except Exception as e:
            console.print(f"[red]Failed to generate explanation:[/red] {e}")
            raise typer.Exit(1)

        # Display explanation
        console.print(Panel(Markdown(explanation), title="Explanation", border_style="blue"))

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

