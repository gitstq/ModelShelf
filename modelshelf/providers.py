"""Model provider adapters for different local AI platforms."""

import json
from abc import ABC, abstractmethod
from typing import Any, Optional

import httpx

from .models import ModelInfo, ModelStatus


class BaseProvider(ABC):
    """Base class for model providers."""

    def __init__(self, name: str, base_url: str, timeout: int = 30) -> None:
        self.name = name
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    @abstractmethod
    async def list_models(self) -> list[ModelInfo]:
        """List available models from this provider."""
        pass

    @abstractmethod
    async def get_model(self, model_id: str) -> Optional[ModelInfo]:
        """Get specific model information."""
        pass

    @abstractmethod
    async def pull_model(self, model_id: str) -> bool:
        """Pull/download a model."""
        pass

    @abstractmethod
    async def delete_model(self, model_id: str) -> bool:
        """Delete a model."""
        pass

    @abstractmethod
    async def check_health(self) -> bool:
        """Check if the provider is available."""
        pass

    async def _request(
        self, method: str, endpoint: str, **kwargs
    ) -> Optional[dict[str, Any]]:
        """Make HTTP request to provider."""
        try:
            url = f"{self.base_url}{endpoint}"
            response = await self.client.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except (httpx.RequestError, httpx.HTTPStatusError, json.JSONDecodeError):
            return None


class OllamaProvider(BaseProvider):
    """Ollama model provider."""

    def __init__(self, base_url: str = "http://localhost:11434", timeout: int = 30) -> None:
        super().__init__("ollama", base_url, timeout)

    async def list_models(self) -> list[ModelInfo]:
        """List Ollama models."""
        data = await self._request("GET", "/api/tags")
        if not data or "models" not in data:
            return []

        models = []
        for item in data["models"]:
            model = ModelInfo(
                id=item.get("name", "").replace(":", "-"),
                name=item.get("name", ""),
                source="ollama",
                status=ModelStatus.INSTALLED,
                size=self._parse_size(item.get("details", {}).get("parameter_size", "")),
                parameters=item.get("details", {}).get("parameter_size", ""),
                quantization=item.get("details", {}).get("quantization_level", ""),
                format=item.get("details", {}).get("format", ""),
                description=item.get("description", ""),
                tags=item.get("tags", []),
                disk_size=item.get("size", 0),
                model_family=item.get("details", {}).get("family", ""),
            )
            models.append(model)
        return models

    async def get_model(self, model_id: str) -> Optional[ModelInfo]:
        """Get Ollama model details."""
        models = await self.list_models()
        for model in models:
            if model.id == model_id or model.name == model_id:
                return model
        return None

    async def pull_model(self, model_id: str) -> bool:
        """Pull Ollama model."""
        data = await self._request("POST", "/api/pull", json={"name": model_id})
        return data is not None

    async def delete_model(self, model_id: str) -> bool:
        """Delete Ollama model."""
        data = await self._request("DELETE", "/api/delete", json={"name": model_id})
        return data is not None

    async def check_health(self) -> bool:
        """Check Ollama availability."""
        data = await self._request("GET", "/api/tags")
        return data is not None

    def _parse_size(self, parameter_size: str) -> Optional[str]:
        """Parse parameter size string."""
        if not parameter_size:
            return None
        return parameter_size.upper().replace("B", "B")


class LMStudioProvider(BaseProvider):
    """LM Studio model provider."""

    def __init__(self, base_url: str = "http://localhost:1234", timeout: int = 30) -> None:
        super().__init__("lmstudio", base_url, timeout)

    async def list_models(self) -> list[ModelInfo]:
        """List LM Studio models."""
        data = await self._request("GET", "/v1/models")
        if not data or "data" not in data:
            return []

        models = []
        for item in data.get("data", []):
            model = ModelInfo(
                id=item.get("id", "").replace("/", "-"),
                name=item.get("id", ""),
                source="lmstudio",
                status=ModelStatus.INSTALLED,
                description=item.get("description", ""),
            )
            models.append(model)
        return models

    async def get_model(self, model_id: str) -> Optional[ModelInfo]:
        """Get LM Studio model."""
        models = await self.list_models()
        for model in models:
            if model.id == model_id:
                return model
        return None

    async def pull_model(self, model_id: str) -> bool:
        """LM Studio doesn't support API pull."""
        return False

    async def delete_model(self, model_id: str) -> bool:
        """LM Studio doesn't support API delete."""
        return False

    async def check_health(self) -> bool:
        """Check LM Studio availability."""
        data = await self._request("GET", "/v1/models")
        return data is not None


class LocalAIProvider(BaseProvider):
    """LocalAI model provider."""

    def __init__(self, base_url: str = "http://localhost:8080", timeout: int = 30) -> None:
        super().__init__("localai", base_url, timeout)

    async def list_models(self) -> list[ModelInfo]:
        """List LocalAI models."""
        data = await self._request("GET", "/models")
        if not data:
            return []

        models = []
        model_list = data if isinstance(data, list) else data.get("data", [])
        for item in model_list:
            model = ModelInfo(
                id=item.get("id", "").replace("/", "-"),
                name=item.get("id", ""),
                source="localai",
                status=ModelStatus.INSTALLED,
                description=item.get("description", ""),
            )
            models.append(model)
        return models

    async def get_model(self, model_id: str) -> Optional[ModelInfo]:
        """Get LocalAI model."""
        models = await self.list_models()
        for model in models:
            if model.id == model_id:
                return model
        return None

    async def pull_model(self, model_id: str) -> bool:
        """LocalAI doesn't support API pull."""
        return False

    async def delete_model(self, model_id: str) -> bool:
        """LocalAI doesn't support API delete."""
        return False

    async def check_health(self) -> bool:
        """Check LocalAI availability."""
        data = await self._request("GET", "/models")
        return data is not None


class ProviderRegistry:
    """Registry for model providers."""

    _providers: dict[str, type[BaseProvider]] = {
        "ollama": OllamaProvider,
        "lmstudio": LMStudioProvider,
        "localai": LocalAIProvider,
    }

    @classmethod
    def register(cls, name: str, provider_class: type[BaseProvider]) -> None:
        """Register a new provider."""
        cls._providers[name.lower()] = provider_class

    @classmethod
    def get_provider(cls, name: str, base_url: str, timeout: int = 30) -> BaseProvider:
        """Get provider instance by name."""
        provider_class = cls._providers.get(name.lower())
        if not provider_class:
            raise ValueError(f"Unknown provider: {name}")
        return provider_class(base_url, timeout)

    @classmethod
    def list_providers(cls) -> list[str]:
        """List registered provider names."""
        return list(cls._providers.keys())

    @classmethod
    def is_registered(cls, name: str) -> bool:
        """Check if provider is registered."""
        return name.lower() in cls._providers
