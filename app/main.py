from fastapi import FastAPI

from app.api.routers import get_api_router

# FastAPI 应用实例
app = FastAPI(title="fastapi-langchain-playground")

# 统一挂载路由
app.include_router(get_api_router())
