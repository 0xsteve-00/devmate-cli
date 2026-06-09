"""Tests for devmate config module."""

import os
import tempfile
from pathlib import Path

from devmate.config import DEFAULT_CONFIG, init_config, load_config, _deep_merge


def test_default_config():
    """Default config should have required keys."""
    assert "model" in DEFAULT_CONFIG
    assert "commit" in DEFAULT_CONFIG
    assert "shell" in DEFAULT_CONFIG
    assert DEFAULT_CONFIG["commit"]["style"] == "conventional"


def test_deep_merge():
    """Deep merge should combine nested dicts."""
    base = {"a": 1, "b": {"c": 2, "d": 3}}
    override = {"b": {"c": 99}, "e": 5}
    result = _deep_merge(base, override)
    assert result == {"a": 1, "b": {"c": 99, "d": 3}, "e": 5}


def test_init_config():
    """Init should create a valid yaml config file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / ".devmate.yaml"
        created = init_config(path)
        assert created.exists()
        content = created.read_text()
        assert "model:" in content
        assert "commit:" in content


def test_load_config_env_override():
    """Environment variables should override config."""
    os.environ["DEVMATE_MODEL"] = "test-model"
    try:
        config = load_config()
        assert config["model"] == "test-model"
    finally:
        del os.environ["DEVMATE_MODEL"]
