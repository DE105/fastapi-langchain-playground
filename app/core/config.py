from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    app_name: str = Field("fastapi-langchain-playground", description="应用名")
    openai_api_key: str | None = Field(None, description="OpenAI API Key")
    anthropic_api_key: str | None = Field(None, description="Anthropic API Key")
    google_api_key: str | None = Field(None, description="Google GenAI API Key")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    # 通过 lru_cache 避免重复解析环境变量
    return Settings()
