"""Configuration management for aigit."""

import os
from pathlib import Path
from typing import Any

import tomli
import tomli_w

CONFIG_DIR = Path.home() / ".config" / "aigit"
CONFIG_FILE = CONFIG_DIR / "config.toml"

DEFAULT_CONFIG = {
    "openai_api_key": "",
    "github_token": "",
    "model": "gpt-4o-mini",
    "conventional_commits": True,
    "auto_stage": False,
    "interactive": True,
}


def ensure_config_dir() -> None:
    """Ensure the config directory exists."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> dict[str, Any]:
    """Load configuration from file."""
    if not CONFIG_FILE.exists():
        return DEFAULT_CONFIG.copy()

    with open(CONFIG_FILE, "rb") as f:
        config = tomli.load(f)

    # Merge with defaults for any missing keys
    merged = DEFAULT_CONFIG.copy()
    merged.update(config)
    return merged


def save_config(config: dict[str, Any]) -> None:
    """Save configuration to file."""
    ensure_config_dir()
    with open(CONFIG_FILE, "wb") as f:
        tomli_w.dump(config, f)


def get_config(key: str) -> Any:
    """Get a specific config value."""
    config = load_config()
    return config.get(key)


def set_config(key: str, value: Any) -> None:
    """Set a specific config value."""
    config = load_config()

    # Type conversion for known boolean fields
    if key in ("conventional_commits", "auto_stage", "interactive"):
        if isinstance(value, str):
            value = value.lower() in ("true", "1", "yes", "on")

    config[key] = value
    save_config(config)


def get_openai_api_key() -> str:
    """Get OpenAI API key from config or environment."""
    key = os.environ.get("OPENAI_API_KEY") or get_config("openai_api_key")
    if not key:
        raise ValueError(
            "OpenAI API key not found. Set it with:\n"
            "  aigit config set openai_api_key <your-key>\n"
            "Or set the OPENAI_API_KEY environment variable."
        )
    return key


def get_github_token() -> str:
    """Get GitHub token from config or environment."""
    token = os.environ.get("GITHUB_TOKEN") or get_config("github_token")
    if not token:
        raise ValueError(
            "GitHub token not found. Set it with:\n"
            "  aigit config set github_token <your-token>\n"
            "Or set the GITHUB_TOKEN environment variable."
        )
    return token

