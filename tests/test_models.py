"""Tests for data models."""

import pytest
from datetime import datetime

from modelshelf.models import (
    ModelInfo,
    ModelStatus,
    ModelSize,
    BenchmarkResult,
    SystemInfo,
    DownloadProgress,
)


class TestModelInfo:
    """Test ModelInfo model."""

    def test_basic_creation(self):
        """Test basic model creation."""
        model = ModelInfo(
            id="test-model",
            name="Test Model",
            source="ollama",
        )
        assert model.id == "test-model"
        assert model.name == "Test Model"
        assert model.source == "ollama"
        assert model.status == ModelStatus.AVAILABLE

    def test_with_optional_fields(self):
        """Test model with optional fields."""
        model = ModelInfo(
            id="llama2-7b",
            name="Llama 2 7B",
            source="ollama",
            status=ModelStatus.INSTALLED,
            size="7B",
            parameters="7B",
            quantization="Q4_K_M",
            description="Test description",
            tags=["llm", "chat"],
            disk_size=4000000000,
        )
        assert model.size == "7B"
        assert model.quantization == "Q4_K_M"
        assert len(model.tags) == 2

    def test_default_values(self):
        """Test default values."""
        model = ModelInfo(id="test", name="Test", source="ollama")
        assert model.tags == []
        assert model.capabilities == []
        assert model.languages == []
        assert model.description is None


class TestBenchmarkResult:
    """Test BenchmarkResult model."""

    def test_creation(self):
        """Test benchmark result creation."""
        result = BenchmarkResult(
            model_id="test-model",
            model_name="Test Model",
            tokens_per_second=42.5,
            latency_ms=250.0,
            score=85.0,
        )
        assert result.model_id == "test-model"
        assert result.tokens_per_second == 42.5
        assert result.score == 85.0
        assert isinstance(result.timestamp, datetime)


class TestSystemInfo:
    """Test SystemInfo model."""

    def test_creation(self):
        """Test system info creation."""
        info = SystemInfo(
            platform="Linux-5.15.0",
            cpu_count=8,
            memory_total=16000000000,
            memory_available=8000000000,
            disk_total=500000000000,
            disk_free=200000000000,
            python_version="3.11.0",
            modelshelf_version="1.0.0",
        )
        assert info.cpu_count == 8
        assert info.gpu_available is False


class TestDownloadProgress:
    """Test DownloadProgress model."""

    def test_progress_calculation(self):
        """Test progress percentage calculation."""
        progress = DownloadProgress(
            model_id="test",
            total_bytes=1000,
            downloaded_bytes=500,
        )
        assert progress.progress_percent == 50.0

    def test_progress_none_total(self):
        """Test progress with no total."""
        progress = DownloadProgress(model_id="test", downloaded_bytes=500)
        assert progress.progress_percent is None
