<div align="center">

# 🗄️ ModelShelf

**A lightweight CLI tool for managing local AI models across multiple platforms**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-17%20passed-brightgreen)]()
[![Code Style](https://img.shields.io/badge/Code%20Style-Black-black)]()

[简体中文](#-简体中文) | [繁體中文](#-繁體中文) | [English](#-english)

</div>

---

## 🎉 项目介绍

ModelShelf 是一款专为本地 AI 模型管理而生的轻量级 CLI 工具。在 AI 大模型蓬勃发展的今天，开发者往往需要在本地部署多个模型（如 Llama、Mistral、CodeLlama 等），并通过不同的平台（Ollama、LM Studio、LocalAI）进行管理。ModelShelf 将这些分散的管理需求统一到一个优雅的命令行界面中，让模型管理变得前所未有的简单高效。

### 💡 灵感来源

本项目灵感来源于 GitHub Trending 上的 `headroom` 和 `hermes-agent` 等项目，观察到开发者在本地 AI 模型管理方面的痛点，自研开发了这款差异化工具。

### 🌟 自研差异化亮点

- **多平台统一**：业界首个同时支持 Ollama、LM Studio、LocalAI 三大主流平台的管理工具
- **交互式 TUI**：提供类似 Vim 的键盘驱动交互界面，无需记忆复杂命令
- **性能基准测试**：内置模型性能评测系统，帮助选择最优模型
- **智能搜索**：支持按名称、标签、描述多维度搜索
- **配置即代码**：YAML 配置文件，易于版本控制和团队协作

---

## ✨ 核心特性

| 特性 | 描述 | 状态 |
|------|------|------|
| 🤖 **多平台支持** | 统一管理 Ollama、LM Studio、LocalAI 模型 | ✅ |
| 🔍 **智能搜索** | 按名称、标签、描述快速定位模型 | ✅ |
| ⬇️ **一键下载** | 支持模型拉取和更新 | ✅ |
| 🗑️ **安全删除** | 带确认机制的模型删除 | ✅ |
| ⚡ **性能评测** | 内置基准测试，量化模型性能 | ✅ |
| 🖥️ **交互式 TUI** | 键盘驱动的终端用户界面 | ✅ |
| 📊 **系统监控** | 实时查看 CPU、内存、GPU 状态 | ✅ |
| ⚙️ **灵活配置** | YAML 配置文件，支持自定义源 | ✅ |
| 🎨 **美观输出** | 基于 Rich 的彩色表格和进度条 | ✅ |
| 🧪 **完整测试** | 17 个单元测试，覆盖率 47%+ | ✅ |

---

## 🚀 快速开始

### 环境要求

- **Python**: 3.9 或更高版本
- **操作系统**: Linux / macOS / Windows
- **依赖**: 详见 `pyproject.toml`

### 安装步骤

```bash
# 从 PyPI 安装（即将发布）
pip install modelshelf

# 或从源码安装
git clone https://github.com/gitstq/ModelShelf.git
cd ModelShelf
pip install -e .
```

### 基本命令

```bash
# 查看系统状态和模型源健康度
modelshelf status

# 列出所有已安装模型
modelshelf list

# 搜索模型
modelshelf search llama

# 拉取模型
modelshelf pull llama2:7b

# 删除模型
modelshelf delete llama2:7b

# 性能测试
modelshelf benchmark llama2:7b

# 查看配置
modelshelf config show
```

### 交互式 TUI

```bash
# 启动交互式界面
python -m modelshelf.tui
```

---

## 📖 详细使用指南

### 模型源配置

ModelShelf 默认支持以下模型源：

| 源名称 | 默认地址 | 说明 |
|--------|----------|------|
| Ollama | http://localhost:11434 | 最热门的本地模型运行平台 |
| LM Studio | http://localhost:1234 | 图形化模型管理工具 |
| LocalAI | http://localhost:8080 | 兼容 OpenAI API 的本地服务 |

### 添加自定义源

```bash
modelshelf config source-add --name myserver --url http://192.168.1.100:11434
```

### 配置管理

```bash
# 查看当前配置
modelshelf config show

# 修改默认源
modelshelf config set default_source lmstudio

# 删除源
modelshelf config source-remove lmstudio
```

### 输出格式

```bash
# JSON 格式输出
modelshelf list --format json

# 树形结构输出
modelshelf list --format tree

# 表格输出（默认）
modelshelf list --format table
```

---

## 💡 设计思路与迭代规划

### 技术选型原因

| 技术 | 选型理由 |
|------|----------|
| **Python 3.9+** | 生态丰富，异步支持成熟，开发者友好 |
| **Click** | 业界标准的 Python CLI 框架，命令解析强大 |
| **Rich** | 终端美化库，支持表格、进度条、树形结构 |
| **Pydantic** | 数据验证和序列化，类型安全 |
| **httpx** | 现代异步 HTTP 客户端，支持 HTTP/2 |
| **pytest** | 成熟的测试框架，插件生态丰富 |

### 后续迭代计划

- [ ] 支持更多模型源（llama.cpp、vLLM 等）
- [ ] 模型版本管理和回滚
- [ ] 批量操作和脚本化支持
- [ ] 模型推荐系统（基于硬件配置）
- [ ] Web UI 管理界面
- [ ] 模型共享和同步功能

### 社区贡献方向

欢迎提交 PR 和 Issue！详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📦 打包与部署

### 开发环境搭建

```bash
# 克隆仓库
git clone https://github.com/gitstq/ModelShelf.git
cd ModelShelf

# 安装开发依赖
make install-dev

# 运行测试
make test

# 代码格式化
make format

# 代码检查
make lint
```

### 构建发布

```bash
# 构建 wheel 包
make build

# 发布到 PyPI
make publish
```

---

## 🤝 贡献指南

### 提交规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/)：

- `feat:` 新功能
- `fix:` 修复问题
- `docs:` 文档更新
- `test:` 测试相关
- `refactor:` 代码重构

### Issue 反馈

请提供以下信息：
1. ModelShelf 版本
2. Python 版本和操作系统
3. 复现步骤
4. 期望行为 vs 实际行为

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 🌐 语言切换

- [简体中文](#-简体中文)（当前）
- [繁體中文](#-繁體中文)
- [English](#-english)

---

## 📧 联系我们

如有问题或建议，欢迎通过以下方式联系：

- 📮 Issue: [GitHub Issues](https://github.com/gitstq/ModelShelf/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/gitstq/ModelShelf/discussions)

---

<div align="center">

Made with ❤️ by ModelShelf Team

</div>
