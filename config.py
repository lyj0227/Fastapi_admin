from pydantic_settings import BaseSettings
from functools import lru_cache

import sys
import secrets


# 创建Settings对象
class Settings(BaseSettings):
    # fastapi
    DEBUG: bool = True
    TITLE: str = "FastAPI Admin"
    SUMMARY: str = 'FastAPI Admin 是一款基于fastapi的后端项目模板'
    VERSION: str = "0.0.1"
    OPENAPI_URL: str = '/openapi.json'
    # MySQL
    MYSQL_HOST: str
    MYSQL_POST: int
    MYSQL_USERNAME: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASES: str
    # Redis
    REDIS_HOST: str
    REDIS_POST: int
    REDIS_DB: int
    # Token
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3

    class Config:
        env_file = '.env'


# 使用lru_cache只创建一次Settings对象
@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
