"""Configuration management for ModelShelf."""

import os
from pathlib import Path
from typing import Optional

import yaml
from platformdirs import user_config_dir, user_data_dir
from pydantic import BaseModel, Field


class ModelSourceConfig(BaseModel):
    """Configuration for a model source."""

    name: str = Field(..., description="Source name")
    url: str = Field(..., description="Source URL")
    enabled: bool = Field(default=True, description="Whether the source is enabled")
    api_key: Optional[str] = Field(default=None, description="API key for the source")
    timeout: int = Field(default=30, description="Request timeout in seconds")


class AppConfig(BaseModel):
    """Application configuration."""

    version: str = Field(default="1.0.0", description="Config version")
    default_source: str = Field(default="ollama", description="Default model source")
    sources: list[ModelSourceConfig] = Field(
        default_factory=lambda: [
            ModelSourceConfig(name="ollama", url="http://localhost:11434"),
            ModelSourceConfig(name="lmstudio", url="http://localhost:1234"),
            ModelSourceConfig(name="localai", url="http://localhost:8080"),
        ],
        description="Model sources",
    )
    auto_update_check: bool = Field(
        default=True, description="Check for updates automatically"
    )
    log_level: str = Field(default="INFO", description="Logging level")
    max_download_retries: int = Field(default=3, description="Max download retries")
    concurrent_downloads: int = Field(default=2, description="Concurrent downloads")


class ConfigManager:
    """Manages application configuration."""

    def __init__(self) -> None:
        self.config_dir = Path(user_config_dir("modelshelf", "modelshelf"))
        self.data_dir = Path(user_data_dir("modelshelf", "modelshelf"))
        self.config_file = self.config_dir / "config.yaml"
        self._config: Optional[AppConfig] = None

    def ensure_directories(self) -> None:
        """Ensure configuration and data directories exist."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def load_config(self) -> AppConfig:
        """Load configuration from file or create default."""
        if self._config is not None:
            return self._config

        self.ensure_directories()

        if self.config_file.exists():
            with open(self.config_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            self._config = AppConfig(**data)
        else:
            self._config = AppConfig()
            self.save_config(self._config)

        return self._config

    def save_config(self, config: AppConfig) -> None:
        """Save configuration to file."""
        self.ensure_directories()
        with open(self.config_file, "w", encoding="utf-8") as f:
            yaml.dump(config.model_dump(), f, default_flow_style=False, allow_unicode=True)

    def get_config(self) -> AppConfig:
        """Get current configuration."""
        if self._config is None:
            return self.load_config()
        return self._config

    def update_config(self, **kwargs) -> AppConfig:
        """Update configuration values."""
        config = self.get_config()
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
        self.save_config(config)
        return config

    def get_source(self, name: str) -> Optional[ModelSourceConfig]:
        """Get a model source by name."""
        config = self.get_config()
        for source in config.sources:
            if source.name.lower() == name.lower():
                return source
        return None

    def add_source(self, source: ModelSourceConfig) -> None:
        """Add a new model source."""
        config = self.get_config()
        config.sources.append(source)
        self.save_config(config)

    def remove_source(self, name: str) -> bool:
        """Remove a model source by name."""
        config = self.get_config()
        original_len = len(config.sources)
        config.sources = [s for s in config.sources if s.name.lower() != name.lower()]
        if len(config.sources) < original_len:
            self.save_config(config)
            return True
        return False


# Global config manager instance
config_manager = ConfigManager()
