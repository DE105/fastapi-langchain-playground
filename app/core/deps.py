from app.core.config import get_settings, Settings


def get_app_settings() -> Settings:
    # FastAPI Depends 可直接复用本函数获取配置
    return get_settings()
