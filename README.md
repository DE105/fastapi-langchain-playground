# fastapi-langchain-playground

一个基于 FastAPI 与 LangChain 的实验项目，便于快速接入 OpenAI、Anthropic、Google GenAI 等大模型生态，集中验证链式调用、工具调用和多模型对比。

## 环境要求
- Python 3.14（已在 `.python-version` 中固定）
- 已安装 [uv](https://github.com/astral-sh/uv)
- （可选）相关大模型 API Key：`OPENAI_API_KEY`、`ANTHROPIC_API_KEY`、`GOOGLE_API_KEY`

## 快速开始
1. 同步依赖（若无虚拟环境会自动在当前目录创建 `.venv`，默认使用 Python 3.14）
   ```bash
   uv sync
   ```
   如需显式指定解释器：`uv sync --python 3.14` 或先设置 `UV_PYTHON=3.14`。
2. 激活虚拟环境（若未激活）
   ```bash
   .venv\\Scripts\\activate
   ```
3. 运行示例（当前仅示例输出）
   ```bash
   uv run python main.py
   ```
   当你添加 FastAPI 应用后，可用：
   ```bash
   uv run uvicorn app:app --reload
   ```

## 目录速览
- `main.py`：当前示例入口
- `pyproject.toml`：项目元数据与依赖
- `uv.lock`：锁定的依赖版本
- `.python-version`：固定解释器版本

## 常用 uv 命令
- 添加依赖：`uv add "fastapi[standard]"`、`uv add "langchain>=1.1.0"`
- 更新依赖版本：`uv add "fastapi[standard]==0.123.0" --upgrade`
- 同步环境：`uv sync`
- 清理缓存：`uv cache clean`

## 后续可做
- 增加 FastAPI 路由与 LangChain 流水线示例
- 编写集成测试与简单健康检查端点
- 补充针对各模型提供商的配置示例与环境变量说明
