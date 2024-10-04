from pydantic_settings import BaseSettings
from pydantic import BaseModel
from functools import lru_cache
import secrets
from typing import Any


# 创建Settings对象
class Settings(BaseSettings):
    class HttpResponses(BaseModel):
        code: int
        message: str
        data: Any

    # fastapi
    DEBUG: bool = True
    TITLE: str = "FastAPI Admin"
    SUMMARY: str = """
    FastAPI Admin 是一款基于fastapi的后端项目模板
    """
    VERSION: str = "0.0.1"
    OPENAPI_URL: str = "/openapi.json"
    RESPONSES: dict[int, dict[str, str | type]] = {
        422: {"description": "Validation Error", "model": HttpResponses},
        401: {"description": "Token Error", "model": HttpResponses},
        200: {"description": "Successful Response", "model": HttpResponses},
    }
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
    # aliyun
    ACCESS_KEY_ID: str
    ACCESSKEY_SECRET: str
    # Host
    HOSTS: list[str] = ["*"]
    ORIGINS: list[str] = ["*"]
    MEDOTHS: list[str] = ["*"]
    HEADERS: list[str] = ["*"]
    CREDENTIALS: bool = False

    class Config:
        env_file = ".env"


# 使用lru_cache只创建一次Settings对象
@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
