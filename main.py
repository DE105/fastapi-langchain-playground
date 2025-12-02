import uvicorn


if __name__ == "__main__":
    # 便于本地快速启动：uv run python main.py
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
