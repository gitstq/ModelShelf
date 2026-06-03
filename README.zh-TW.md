<div align="center">

# 🗄️ ModelShelf

**輕量化 CLI 工具，統一管理多平台本地 AI 模型**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-17%20passed-brightgreen)]()
[![Code Style](https://img.shields.io/badge/Code%20Style-Black-black)]()

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md)

</div>

---

## 🎉 專案介紹

ModelShelf 是一款專為本地 AI 模型管理而生的輕量化 CLI 工具。在 AI 大模型蓬勃發展的今天，開發者往往需要在本地部署多個模型（如 Llama、Mistral、CodeLlama 等），並透過不同的平台（Ollama、LM Studio、LocalAI）進行管理。ModelShelf 將這些分散的管理需求統一到一個優雅的命令列介面中，讓模型管理變得前所未有的簡單高效。

### 💡 靈感來源

本專案靈感來源於 GitHub Trending 上的 `headroom` 和 `hermes-agent` 等專案，觀察到開發者在本地 AI 模型管理方面的痛點，自研開發了這款差異化工具。

### 🌟 自研差異化亮點

- **多平台統一**：業界首個同時支援 Ollama、LM Studio、LocalAI 三大主流平台的管理工具
- **互動式 TUI**：提供類似 Vim 的鍵盤驅動互動介面，無需記憶複雜命令
- **效能基準測試**：內建模型效能評測系統，協助選擇最優模型
- **智慧搜尋**：支援按名稱、標籤、描述多維度搜尋
- **配置即程式碼**：YAML 設定檔，易於版本控制和團隊協作

---

## ✨ 核心特性

| 特性 | 描述 | 狀態 |
|------|------|------|
| 🤖 **多平台支援** | 統一管理 Ollama、LM Studio、LocalAI 模型 | ✅ |
| 🔍 **智慧搜尋** | 按名稱、標籤、描述快速定位模型 | ✅ |
| ⬇️ **一鍵下載** | 支援模型拉取和更新 | ✅ |
| 🗑️ **安全刪除** | 帶確認機制的模型刪除 | ✅ |
| ⚡ **效能評測** | 內建基準測試，量化模型效能 | ✅ |
| 🖥️ **互動式 TUI** | 鍵盤驅動的終端使用者介面 | ✅ |
| 📊 **系統監控** | 即時查看 CPU、記憶體、GPU 狀態 | ✅ |
| ⚙️ **靈活配置** | YAML 設定檔，支援自訂源 | ✅ |
| 🎨 **美觀輸出** | 基於 Rich 的彩色表格和進度條 | ✅ |
| 🧪 **完整測試** | 17 個單元測試，覆蓋率 47%+ | ✅ |

---

## 🚀 快速開始

### 環境要求

- **Python**: 3.9 或更高版本
- **作業系統**: Linux / macOS / Windows
- **依賴**: 詳見 `pyproject.toml`

### 安裝步驟

```bash
# 從 PyPI 安裝（即將發布）
pip install modelshelf

# 或從原始碼安裝
git clone https://github.com/gitstq/ModelShelf.git
cd ModelShelf
pip install -e .
```

### 基本命令

```bash
# 查看系統狀態和模型源健康度
modelshelf status

# 列出所有已安裝模型
modelshelf list

# 搜尋模型
modelshelf search llama

# 拉取模型
modelshelf pull llama2:7b

# 刪除模型
modelshelf delete llama2:7b

# 效能測試
modelshelf benchmark llama2:7b

# 查看配置
modelshelf config show
```

### 互動式 TUI

```bash
# 啟動互動式介面
python -m modelshelf.tui
```

---

## 📖 詳細使用指南

### 模型源配置

ModelShelf 預設支援以下模型源：

| 源名稱 | 預設位址 | 說明 |
|--------|----------|------|
| Ollama | http://localhost:11434 | 最熱門的本地模型執行平台 |
| LM Studio | http://localhost:1234 | 圖形化模型管理工具 |
| LocalAI | http://localhost:8080 | 相容 OpenAI API 的本地服務 |

### 新增自訂源

```bash
modelshelf config source-add --name myserver --url http://192.168.1.100:11434
```

### 配置管理

```bash
# 查看目前配置
modelshelf config show

# 修改預設源
modelshelf config set default_source lmstudio

# 刪除源
modelshelf config source-remove lmstudio
```

### 輸出格式

```bash
# JSON 格式輸出
modelshelf list --format json

# 樹狀結構輸出
modelshelf list --format tree

# 表格輸出（預設）
modelshelf list --format table
```

---

## 💡 設計思路與迭代規劃

### 技術選型原因

| 技術 | 選型理由 |
|------|----------|
| **Python 3.9+** | 生態豐富，非同步支援成熟，開發者友善 |
| **Click** | 業界標準的 Python CLI 框架，命令解析強大 |
| **Rich** | 終端美化庫，支援表格、進度條、樹狀結構 |
| **Pydantic** | 資料驗證和序列化，型別安全 |
| **httpx** | 現代非同步 HTTP 客戶端，支援 HTTP/2 |
| **pytest** | 成熟的測試框架，外掛生態豐富 |

### 後續迭代計劃

- [ ] 支援更多模型源（llama.cpp、vLLM 等）
- [ ] 模型版本管理和回滾
- [ ] 批次操作和腳本化支援
- [ ] 模型推薦系統（基於硬體配置）
- [ ] Web UI 管理介面
- [ ] 模型共享和同步功能

### 社群貢獻方向

歡迎提交 PR 和 Issue！詳見 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📦 打包與部署

### 開發環境搭建

```bash
# 克隆倉庫
git clone https://github.com/gitstq/ModelShelf.git
cd ModelShelf

# 安裝開發依賴
make install-dev

# 執行測試
make test

# 程式碼格式化
make format

# 程式碼檢查
make lint
```

### 建置發布

```bash
# 建置 wheel 包
make build

# 發布到 PyPI
make publish
```

---

## 🤝 貢獻指南

### 提交規範

遵循 [Conventional Commits](https://www.conventionalcommits.org/)：

- `feat:` 新功能
- `fix:` 修復問題
- `docs:` 文件更新
- `test:` 測試相關
- `refactor:` 程式碼重構

### Issue 回饋

請提供以下資訊：
1. ModelShelf 版本
2. Python 版本和作業系統
3. 復現步驟
4. 期望行為 vs 實際行為

---

## 📄 開源協議

本專案採用 [MIT License](LICENSE) 開源協議。

---

## 🌐 語言切換

- [简体中文](README.md)
- [繁體中文](README.zh-TW.md)（目前）
- [English](README.en.md)

---

## 📧 聯絡我們

如有問題或建議，歡迎透過以下方式聯絡：

- 📮 Issue: [GitHub Issues](https://github.com/gitstq/ModelShelf/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/gitstq/ModelShelf/discussions)

---

<div align="center">

Made with ❤️ by ModelShelf Team

</div>
