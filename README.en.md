<div align="center">

# 🗄️ ModelShelf

**A lightweight CLI tool for managing local AI models across multiple platforms**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-17%20passed-brightgreen)]()
[![Code Style](https://img.shields.io/badge/Code%20Style-Black-black)]()

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md)

</div>

---

## 🎉 Project Introduction

ModelShelf is a lightweight CLI tool designed for local AI model management. In today's booming AI landscape, developers often need to deploy multiple models locally (such as Llama, Mistral, CodeLlama, etc.) and manage them through different platforms (Ollama, LM Studio, LocalAI). ModelShelf unifies these scattered management needs into an elegant command-line interface, making model management simpler and more efficient than ever before.

### 💡 Inspiration

This project was inspired by trending projects like `headroom` and `hermes-agent` on GitHub, observing the pain points developers face in local AI model management, and independently developed this differentiated tool.

### 🌟 Differentiation Highlights

- **Multi-Platform Unification**: The industry's first management tool supporting all three major platforms: Ollama, LM Studio, and LocalAI
- **Interactive TUI**: Keyboard-driven interface similar to Vim, no need to memorize complex commands
- **Performance Benchmarking**: Built-in model performance evaluation system to help choose optimal models
- **Smart Search**: Multi-dimensional search by name, tags, and descriptions
- **Configuration as Code**: YAML configuration files for easy version control and team collaboration

---

## ✨ Core Features

| Feature | Description | Status |
|---------|-------------|--------|
| 🤖 **Multi-Platform Support** | Unified management for Ollama, LM Studio, LocalAI models | ✅ |
| 🔍 **Smart Search** | Quickly locate models by name, tags, or description | ✅ |
| ⬇️ **One-Click Download** | Support model pulling and updates | ✅ |
| 🗑️ **Safe Deletion** | Model deletion with confirmation mechanism | ✅ |
| ⚡ **Performance Benchmark** | Built-in benchmarking to quantify model performance | ✅ |
| 🖥️ **Interactive TUI** | Keyboard-driven terminal user interface | ✅ |
| 📊 **System Monitoring** | Real-time CPU, memory, and GPU status | ✅ |
| ⚙️ **Flexible Configuration** | YAML config files with custom source support | ✅ |
| 🎨 **Beautiful Output** | Colorful tables and progress bars based on Rich | ✅ |
| 🧪 **Complete Testing** | 17 unit tests with 47%+ coverage | ✅ |

---

## 🚀 Quick Start

### Requirements

- **Python**: 3.9 or higher
- **OS**: Linux / macOS / Windows
- **Dependencies**: See `pyproject.toml`

### Installation

```bash
# Install from PyPI (coming soon)
pip install modelshelf

# Or install from source
git clone https://github.com/gitstq/ModelShelf.git
cd ModelShelf
pip install -e .
```

### Basic Commands

```bash
# Check system status and source health
modelshelf status

# List all installed models
modelshelf list

# Search for models
modelshelf search llama

# Pull a model
modelshelf pull llama2:7b

# Delete a model
modelshelf delete llama2:7b

# Run benchmark
modelshelf benchmark llama2:7b

# View configuration
modelshelf config show
```

### Interactive TUI

```bash
# Launch interactive interface
python -m modelshelf.tui
```

---

## 📖 Detailed Usage Guide

### Model Source Configuration

ModelShelf supports the following model sources by default:

| Source Name | Default Address | Description |
|-------------|-----------------|-------------|
| Ollama | http://localhost:11434 | The most popular local model runtime platform |
| LM Studio | http://localhost:1234 | GUI model management tool |
| LocalAI | http://localhost:8080 | OpenAI API-compatible local service |

### Adding Custom Sources

```bash
modelshelf config source-add --name myserver --url http://192.168.1.100:11434
```

### Configuration Management

```bash
# View current configuration
modelshelf config show

# Change default source
modelshelf config set default_source lmstudio

# Remove a source
modelshelf config source-remove lmstudio
```

### Output Formats

```bash
# JSON format output
modelshelf list --format json

# Tree structure output
modelshelf list --format tree

# Table output (default)
modelshelf list --format table
```

---

## 💡 Design Philosophy & Roadmap

### Technology Choices

| Technology | Reason |
|------------|--------|
| **Python 3.9+** | Rich ecosystem, mature async support, developer-friendly |
| **Click** | Industry-standard Python CLI framework with powerful command parsing |
| **Rich** | Terminal beautification library supporting tables, progress bars, trees |
| **Pydantic** | Data validation and serialization with type safety |
| **httpx** | Modern async HTTP client with HTTP/2 support |
| **pytest** | Mature testing framework with rich plugin ecosystem |

### Future Roadmap

- [ ] Support for more model sources (llama.cpp, vLLM, etc.)
- [ ] Model version management and rollback
- [ ] Batch operations and scripting support
- [ ] Model recommendation system (based on hardware configuration)
- [ ] Web UI management interface
- [ ] Model sharing and synchronization features

### Community Contributions

PRs and Issues are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📦 Packaging & Deployment

### Development Environment Setup

```bash
# Clone repository
git clone https://github.com/gitstq/ModelShelf.git
cd ModelShelf

# Install development dependencies
make install-dev

# Run tests
make test

# Code formatting
make format

# Code linting
make lint
```

### Build & Release

```bash
# Build wheel package
make build

# Publish to PyPI
make publish
```

---

## 🤝 Contributing Guide

### Commit Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation update
- `test:` Test-related changes
- `refactor:` Code refactoring

### Issue Reporting

Please provide:
1. ModelShelf version
2. Python version and operating system
3. Steps to reproduce
4. Expected vs actual behavior

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🌐 Language Switch

- [简体中文](README.md)
- [繁體中文](README.zh-TW.md)
- [English](README.en.md) (Current)

---

## 📧 Contact Us

For questions or suggestions, please reach out through:

- 📮 Issue: [GitHub Issues](https://github.com/gitstq/ModelShelf/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/gitstq/ModelShelf/discussions)

---

<div align="center">

Made with ❤️ by ModelShelf Team

</div>
