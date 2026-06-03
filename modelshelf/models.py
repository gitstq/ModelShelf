"""Data models for ModelShelf."""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class ModelStatus(str, Enum):
    """Model status enumeration."""

    INSTALLED = "installed"
    DOWNLOADING = "downloading"
    AVAILABLE = "available"
    ERROR = "error"
    UPDATING = "updating"


class ModelSize(str, Enum):
    """Model size category."""

    TINY = "tiny"      # < 1B
    SMALL = "small"    # 1B - 7B
    MEDIUM = "medium"  # 7B - 30B
    LARGE = "large"    # 30B - 70B
    XLARGE = "xlarge"  # > 70B


class ModelInfo(BaseModel):
    """Information about an AI model."""

    id: str = Field(..., description="Unique model identifier")
    name: str = Field(..., description="Model name")
    source: str = Field(..., description="Source platform (ollama, lmstudio, etc.)")
    status: ModelStatus = Field(default=ModelStatus.AVAILABLE, description="Model status")
    size: Optional[str] = Field(default=None, description="Model size (e.g., '7B')")
    size_category: Optional[ModelSize] = Field(default=None, description="Size category")
    parameters: Optional[str] = Field(default=None, description="Parameter count")
    quantization: Optional[str] = Field(default=None, description="Quantization level")
    format: Optional[str] = Field(default=None, description="Model format")
    description: Optional[str] = Field(default=None, description="Model description")
    tags: list[str] = Field(default_factory=list, description="Model tags")
    installed_at: Optional[datetime] = Field(default=None, description="Installation timestamp")
    updated_at: Optional[datetime] = Field(default=None, description="Last update timestamp")
    disk_size: Optional[int] = Field(default=None, description="Disk size in bytes")
    download_url: Optional[str] = Field(default=None, description="Download URL")
    version: Optional[str] = Field(default=None, description="Model version")
    license: Optional[str] = Field(default=None, description="Model license")
    author: Optional[str] = Field(default=None, description="Model author")
    homepage: Optional[str] = Field(default=None, description="Model homepage")
    capabilities: list[str] = Field(default_factory=list, description="Model capabilities")
    languages: list[str] = Field(default_factory=list, description="Supported languages")
    context_length: Optional[int] = Field(default=None, description="Context window size")
    embedding_length: Optional[int] = Field(default=None, description="Embedding dimension")

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "id": "llama2-7b",
                "name": "Llama 2 7B",
                "source": "ollama",
                "status": "installed",
                "size": "7B",
                "quantization": "Q4_K_M",
                "description": "Meta's Llama 2 7B parameter model",
                "tags": ["llm", "chat", "meta"],
            }
        }


class BenchmarkResult(BaseModel):
    """Benchmark test result."""

    model_id: str = Field(..., description="Model identifier")
    model_name: str = Field(..., description="Model name")
    timestamp: datetime = Field(default_factory=datetime.now, description="Test timestamp")
    tokens_per_second: Optional[float] = Field(default=None, description="Generation speed")
    latency_ms: Optional[float] = Field(default=None, description="First token latency")
    memory_usage_mb: Optional[float] = Field(default=None, description="Memory usage")
    cpu_usage_percent: Optional[float] = Field(default=None, description="CPU usage")
    gpu_usage_percent: Optional[float] = Field(default=None, description="GPU usage")
    test_duration: Optional[float] = Field(default=None, description="Test duration in seconds")
    prompt_tokens: Optional[int] = Field(default=None, description="Prompt token count")
    completion_tokens: Optional[int] = Field(default=None, description="Completion token count")
    total_tokens: Optional[int] = Field(default=None, description="Total token count")
    score: Optional[float] = Field(default=None, description="Overall benchmark score")


class SystemInfo(BaseModel):
    """System information."""

    platform: str = Field(..., description="Operating system")
    cpu_count: int = Field(..., description="Number of CPU cores")
    memory_total: int = Field(..., description="Total memory in bytes")
    memory_available: int = Field(..., description="Available memory in bytes")
    disk_total: int = Field(..., description="Total disk space in bytes")
    disk_free: int = Field(..., description="Free disk space in bytes")
    gpu_available: bool = Field(default=False, description="GPU availability")
    gpu_count: Optional[int] = Field(default=None, description="Number of GPUs")
    gpu_names: list[str] = Field(default_factory=list, description="GPU names")
    python_version: str = Field(..., description="Python version")
    modelshelf_version: str = Field(..., description="ModelShelf version")


class DownloadProgress(BaseModel):
    """Download progress information."""

    model_id: str = Field(..., description="Model identifier")
    total_bytes: Optional[int] = Field(default=None, description="Total bytes to download")
    downloaded_bytes: int = Field(default=0, description="Bytes downloaded")
    speed_bytes_per_second: Optional[float] = Field(default=None, description="Download speed")
    eta_seconds: Optional[float] = Field(default=None, description="Estimated time remaining")
    status: str = Field(default="pending", description="Download status")
    error: Optional[str] = Field(default=None, description="Error message if failed")

    @property
    def progress_percent(self) -> Optional[float]:
        """Calculate progress percentage."""
        if self.total_bytes and self.total_bytes > 0:
            return (self.downloaded_bytes / self.total_bytes) * 100
        return None
