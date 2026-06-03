"""Tests for core functionality."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from modelshelf.core import ModelShelf
from modelshelf.models import ModelInfo, ModelStatus, SystemInfo


class TestModelShelf:
    """Test ModelShelf core."""

    @pytest.fixture
    def modelshelf(self):
        """Create ModelShelf instance."""
        return ModelShelf()

    def test_format_size(self, modelshelf):
        """Test size formatting."""
        assert modelshelf.format_size(500) == "500.0 B"
        assert modelshelf.format_size(1024) == "1.0 KB"
        assert modelshelf.format_size(1024 ** 2) == "1.0 MB"
        assert modelshelf.format_size(1024 ** 3) == "1.0 GB"
        assert modelshelf.format_size(None) == "Unknown"

    def test_format_memory(self, modelshelf):
        """Test memory formatting."""
        assert modelshelf.format_memory(1024 ** 3) == "1.0 GB"
        assert modelshelf.format_memory(16 * 1024 ** 3) == "16.0 GB"

    def test_get_system_info(self, modelshelf):
        """Test system info retrieval."""
        info = modelshelf.get_system_info()
        
        assert isinstance(info, SystemInfo)
        assert info.cpu_count > 0
        assert info.memory_total > 0
        assert info.disk_total > 0
        assert info.python_version != ""
        assert info.modelshelf_version == "1.0.0"

    @pytest.mark.asyncio
    async def test_search_models(self, modelshelf):
        """Test model search."""
        # Mock the list_all_models method
        mock_models = [
            ModelInfo(id="llama2", name="Llama 2", source="ollama", tags=["llm"]),
            ModelInfo(id="codellama", name="Code Llama", source="ollama", tags=["code"]),
            ModelInfo(id="mistral", name="Mistral", source="ollama", tags=["llm"]),
        ]
        
        modelshelf.list_all_models = AsyncMock(return_value=mock_models)
        
        results = await modelshelf.search_models("llama")
        assert len(results) == 2
        assert all("llama" in m.name.lower() for m in results)

    @pytest.mark.asyncio
    async def test_search_by_tag(self, modelshelf):
        """Test search by tag."""
        mock_models = [
            ModelInfo(id="llama2", name="Llama 2", source="ollama", tags=["llm", "chat"]),
            ModelInfo(id="codellama", name="Code Llama", source="ollama", tags=["code"]),
        ]
        
        modelshelf.list_all_models = AsyncMock(return_value=mock_models)
        
        results = await modelshelf.search_models("code")
        assert len(results) == 1
        assert results[0].name == "Code Llama"
