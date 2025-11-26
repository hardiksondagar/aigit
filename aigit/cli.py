"""Main CLI entry point for aigit."""

import typer
from rich.console import Console

app = typer.Typer(
    name="aigit",
    help="AI-powered Git CLI tool for smart commits, branches, and PRs",
    add_completion=True,
    no_args_is_help=True,
)
console = Console()

# Import commands
from aigit.commands.commit import commit_command
from aigit.commands.branch import branch_command
from aigit.commands.pr import pr_command
from aigit.commands.review import review_command
from aigit.commands.explain import explain_command
from aigit.commands.config import config_command

# Register commands
app.command(name="commit", help="Generate AI commit message and create commit")(commit_command)
app.command(name="branch", help="Generate AI branch name and create branch")(branch_command)
app.command(name="pr", help="Create PR with AI-generated title and description")(pr_command)
app.command(name="review", help="AI code review of staged changes")(review_command)
app.command(name="explain", help="Explain changes in commit/branch/diff")(explain_command)
app.command(name="config", help="Manage aigit configuration")(config_command)


if __name__ == "__main__":
    app()

