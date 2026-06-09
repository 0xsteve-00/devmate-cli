"""Configuration management for devmate."""

import os
from pathlib import Path
from typing import Any

import yaml


DEFAULT_CONFIG = {
    "model": "gpt-4o-mini",
    "commit": {
        "style": "conventional",  # conventional | simple | detailed
        "language": "en",
        "max_length": 72,
    },
    "shell": {
        "safety": True,  # ask before executing dangerous commands
        "os_context": True,  # include OS info in prompt for better commands
    },
}

CONFIG_FILENAME = ".devmate.yaml"


def find_config_file() -> Path | None:
    """Search for config file in current dir, then home dir."""
    # Check current directory first
    local = Path.cwd() / CONFIG_FILENAME
    if local.exists():
        return local

    # Check home directory
    home = Path.home() / CONFIG_FILENAME
    if home.exists():
        return home

    return None


def load_config() -> dict[str, Any]:
    """Load config from file, env vars, and defaults."""
    config = DEFAULT_CONFIG.copy()

    # Load from file
    config_file = find_config_file()
    if config_file:
        with open(config_file) as f:
            file_config = yaml.safe_load(f) or {}
        config = _deep_merge(config, file_config)

    # Environment variable overrides
    if api_key := os.environ.get("DEVMATE_API_KEY"):
        config["api_key"] = api_key
    if model := os.environ.get("DEVMATE_MODEL"):
        config["model"] = model

    return config


def get_api_key(config: dict[str, Any]) -> str | None:
    """Get API key from config or environment."""
    # Check config first
    if key := config.get("api_key"):
        return key

    # Check common env vars
    for env_var in ["DEVMATE_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY"]:
        if key := os.environ.get(env_var):
            return key

    return None


def init_config(path: Path | None = None) -> Path:
    """Create a default config file."""
    if path is None:
        path = Path.home() / CONFIG_FILENAME

    template = """# devmate configuration
# Docs: https://github.com/achmadyosifa/devmate-cli

# API key (or set DEVMATE_API_KEY / OPENAI_API_KEY env var)
# api_key: sk-...

# AI model to use
# Examples: gpt-4o-mini, gpt-4o, claude-sonnet-4-20250514, ollama/llama3
model: gpt-4o-mini

# Commit message settings
commit:
  style: conventional   # conventional | simple | detailed
  language: en           # en, id, etc.
  max_length: 72

# Shell assistant settings
shell:
  safety: true           # confirm before running dangerous commands
  os_context: true       # send OS info for better command suggestions
"""
    path.write_text(template)
    return path


def _deep_merge(base: dict, override: dict) -> dict:
    """Deep merge two dicts."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result
