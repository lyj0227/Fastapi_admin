from pydantic_settings import BaseSettings
from functools import lru_cache
import sys


# 创建Settings对象
class Settings(BaseSettings):
    DEBUG: bool
    TITLE: str = "FastAPI Admin"
    SUMMARY: str = 'FastAPI Admin 是一款基于fastapi的后端项目模板'
    VERSION: str = "0.0.1"
    DOCS_URL: str
    REDOC_URL: str
    OPENAPI_URL: str
    GENERATE_SCHEMAS: bool
    ADD_EXCEPTION_HANDLERS: bool

    class Config:
        if "dev" in sys.argv:
            env_file = ".env.development"
        if "run" in sys.argv:
            env_file = ".env.production"


# 使用lru_cache只创建一次Settings对象
@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
