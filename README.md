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
3. 运行本地服务
   ```bash
   uv run python main.py
   ```
   或直接启动 uvicorn：
   ```bash
   uv run uvicorn app.main:app --reload
   ```
   当你添加 FastAPI 应用后，可用：
   ```bash
   uv run uvicorn app:app --reload
   ```

## 目录速览
- `app/main.py`：FastAPI 应用入口，统一挂载路由
- `app/api/`：路由层，`health.py` 提供 `/health`
- `app/core/`：核心配置与依赖（`config.py`、`deps.py`）
- `app/models/`：Pydantic 数据模型
- `app/services/`：业务服务层，编排链路
- `app/chains/`：LangChain 链路/Agent 封装
- `app/utils/`：通用工具
- `main.py`：便捷启动脚本（`uv run python main.py`）
- `pyproject.toml`：项目元数据与依赖
- `uv.lock`：锁定的依赖版本
- `.python-version`：固定解释器版本

## LangChain + Gemini 最小示例
1. 确保已设置环境变量（按需替换为你的 Key）：
   ```bash
   set GOOGLE_API_KEY=你的_Gemini_Key
   ```
2. 运行最小示例（使用 `gemini-2.5-flash`）：
   ```bash
   uv run python - <<'PY'
   from app.chains.gemini import demo_chat
   print(demo_chat("用一句话介绍 FastAPI 是什么？"))
   PY
   ```
   若需自定义模型，修改 `demo_chat` 内的 `model_name` 即可。

### Gemini Agent 示例（含工具调用与结构化输出）
```bash
uv run python - <<'PY'
from app.chains.gemini_agent import demo_agent

resp = demo_agent("北京今天的天气怎样？")
print(resp)
PY
```
默认调用示例工具 `get_weather` 并以结构化数据 `WeatherAnswer` 返回。将问题替换为你的场景即可。

## 常用 uv 命令
- 添加依赖：`uv add "fastapi[standard]"`、`uv add "langchain>=1.1.0"`
- 更新依赖版本：`uv add "fastapi[standard]==0.123.0" --upgrade`
- 同步环境：`uv sync`
- 清理缓存：`uv cache clean`

## 后续可做
- 增加 FastAPI 路由与 LangChain 流水线示例
- 编写集成测试与简单健康检查端点
- 补充针对各模型提供商的配置示例与环境变量说明
