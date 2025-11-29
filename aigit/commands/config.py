"""Config command implementation."""

import typer
from rich.console import Console
from rich.table import Table

from aigit import config as cfg

console = Console()

SUPPORTED_PROVIDERS = ["openai", "ollama", "llamacpp", "vllm", "openrouter", "custom"]


def config_command(
    action: str = typer.Argument(..., help="Action: set, get, or list"),
    key: str = typer.Argument(None, help="Config key"),
    value: str = typer.Argument(None, help="Config value (for set)"),
):
    """Manage aigit configuration."""

    action = action.lower()

    if action == "set":
        if not key or value is None:
            console.print("[red]Usage:[/red] aigit config set <key> <value>")
            raise typer.Exit(1)

        # Validate provider
        if key == "provider":
            if value not in SUPPORTED_PROVIDERS:
                console.print(f"[red]Error:[/red] Invalid provider '{value}'")
                console.print(f"[yellow]Supported providers:[/yellow] {', '.join(SUPPORTED_PROVIDERS)}")
                raise typer.Exit(1)

        try:
            cfg.set_config(key, value)
            console.print(f"[green]✓[/green] Set {key} = {value}")
            
            # Display helpful messages for provider configuration
            if key == "provider":
                provider_info = cfg.PROVIDER_DEFAULTS.get(value, {})
                if provider_info.get("base_url"):
                    console.print(f"[dim]Default base URL: {provider_info['base_url']}[/dim]")
                if not provider_info.get("requires_api_key", True):
                    console.print("[dim]API key not required for this provider[/dim]")
                else:
                    console.print("[yellow]⚠[/yellow]  Don't forget to set your API key: aigit config set openai_api_key <key>")
                    
            if key == "base_url" and value:
                console.print("[dim]Custom base URL will override provider default[/dim]")
                
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)

    elif action == "get":
        if not key:
            console.print("[red]Usage:[/red] aigit config get <key>")
            raise typer.Exit(1)

        try:
            val = cfg.get_config(key)
            if val is None:
                console.print(f"[yellow]Key not found:[/yellow] {key}")
            else:
                # Mask sensitive values
                if "key" in key.lower() or "token" in key.lower():
                    if val:
                        val = val[:8] + "..." if len(val) > 8 else "***"
                console.print(f"{key} = {val}")
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)

    elif action == "list":
        try:
            config = cfg.load_config()

            table = Table(title="aigit Configuration")
            table.add_column("Key", style="cyan")
            table.add_column("Value", style="green")

            for k, v in sorted(config.items()):
                # Mask sensitive values
                display_val = str(v)
                if "key" in k.lower() or "token" in k.lower():
                    if v:
                        display_val = str(v)[:8] + "..." if len(str(v)) > 8 else "***"

                table.add_row(k, display_val)

            console.print(table)
            console.print(f"\n[dim]Config file: {cfg.CONFIG_FILE}[/dim]")
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)

    else:
        console.print(f"[red]Unknown action:[/red] {action}")
        console.print("Available actions: set, get, list")
        raise typer.Exit(1)

