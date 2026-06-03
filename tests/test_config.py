"""Tests for configuration management."""

import os
import tempfile
from pathlib import Path

import pytest

from modelshelf.config import ConfigManager, ModelSourceConfig, AppConfig


class TestConfigManager:
    """Test ConfigManager."""

    def test_default_config(self):
        """Test default configuration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir) / "config"
            data_dir = Path(tmpdir) / "data"
            
            manager = ConfigManager()
            manager.config_dir = config_dir
            manager.data_dir = data_dir
            manager.config_file = config_dir / "config.yaml"
            
            config = manager.load_config()
            
            assert config.default_source == "ollama"
            assert len(config.sources) == 3
            assert config.auto_update_check is True

    def test_save_and_load(self):
        """Test saving and loading configuration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir) / "config"
            data_dir = Path(tmpdir) / "data"
            
            manager = ConfigManager()
            manager.config_dir = config_dir
            manager.data_dir = data_dir
            manager.config_file = config_dir / "config.yaml"
            
            config = AppConfig(default_source="lmstudio")
            manager.save_config(config)
            
            # Reset and reload
            manager._config = None
            loaded = manager.load_config()
            
            assert loaded.default_source == "lmstudio"

    def test_add_source(self):
        """Test adding a source."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir) / "config"
            data_dir = Path(tmpdir) / "data"
            
            manager = ConfigManager()
            manager.config_dir = config_dir
            manager.data_dir = data_dir
            manager.config_file = config_dir / "config.yaml"
            
            new_source = ModelSourceConfig(name="custom", url="http://localhost:9999")
            manager.add_source(new_source)
            
            config = manager.get_config()
            assert len(config.sources) == 4
            assert config.sources[-1].name == "custom"

    def test_remove_source(self):
        """Test removing a source."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir) / "config"
            data_dir = Path(tmpdir) / "data"
            
            manager = ConfigManager()
            manager.config_dir = config_dir
            manager.data_dir = data_dir
            manager.config_file = config_dir / "config.yaml"
            
            result = manager.remove_source("lmstudio")
            assert result is True
            
            config = manager.get_config()
            assert len(config.sources) == 2
            
            result = manager.remove_source("nonexistent")
            assert result is False

    def test_get_source(self):
        """Test getting a source."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir) / "config"
            data_dir = Path(tmpdir) / "data"
            
            manager = ConfigManager()
            manager.config_dir = config_dir
            manager.data_dir = data_dir
            manager.config_file = config_dir / "config.yaml"
            
            source = manager.get_source("ollama")
            assert source is not None
            assert source.name == "ollama"
            
            source = manager.get_source("nonexistent")
            assert source is None
