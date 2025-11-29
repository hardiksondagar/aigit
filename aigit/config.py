"""Configuration management for aigit."""

import os
from pathlib import Path
from typing import Any

import tomli
import tomli_w

CONFIG_DIR = Path.home() / ".config" / "aigit"
CONFIG_FILE = CONFIG_DIR / "config.toml"

# Supported providers and their default base URLs
PROVIDER_DEFAULTS = {
    "openai": {
        "base_url": None,  # Use OpenAI SDK default
        "requires_api_key": True,
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "requires_api_key": False,
    },
    "llamacpp": {
        "base_url": "http://localhost:8080/v1",
        "requires_api_key": False,
    },
    "vllm": {
        "base_url": "http://localhost:8000/v1",
        "requires_api_key": False,
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "requires_api_key": True,
    },
    "custom": {
        "base_url": None,  # User must specify
        "requires_api_key": True,  # Safer default
    },
}

DEFAULT_CONFIG = {
    "openai_api_key": "",
    "github_token": "",
    "model": "gpt-4o-mini",
    "conventional_commits": True,
    "auto_stage": False,
    "interactive": True,
    "provider": "openai",
    "base_url": "",
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
    provider = get_config("provider") or "openai"
    
    # Check if provider requires API key
    provider_info = PROVIDER_DEFAULTS.get(provider, PROVIDER_DEFAULTS["custom"])
    
    key = os.environ.get("OPENAI_API_KEY") or get_config("openai_api_key")
    
    # If provider doesn't require API key, return a dummy key
    if not provider_info["requires_api_key"]:
        return key or "not-needed"
    
    if not key:
        raise ValueError(
            "OpenAI API key not found. Set it with:\n"
            "  aigit config set openai_api_key <your-key>\n"
            "Or set the OPENAI_API_KEY environment variable."
        )
    return key


def get_provider_config() -> dict[str, Any]:
    """Get provider configuration including base_url and api_key."""
    provider = get_config("provider") or "openai"
    custom_base_url = get_config("base_url")
    
    # Get provider defaults
    provider_info = PROVIDER_DEFAULTS.get(provider, PROVIDER_DEFAULTS["custom"])
    
    # Custom base_url overrides provider default
    base_url = custom_base_url if custom_base_url else provider_info["base_url"]
    
    # Get API key
    api_key = get_openai_api_key()
    
    config = {
        "provider": provider,
        "api_key": api_key,
        "base_url": base_url,
        "requires_api_key": provider_info["requires_api_key"],
    }
    
    return config


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

