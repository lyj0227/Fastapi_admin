from config import settings
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise


def init_mysql(app: FastAPI) -> None:
    # 创建数据库ORM链接
    try:
        Tortoise._init_timezone(use_tz=False, timezone="Asia/Shanghai")
        register_tortoise(
            app,
            db_url=f"mysql://{settings.MYSQL_USERNAME}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:"
            f"{settings.MYSQL_POST}/{settings.MYSQL_DATABASES}",
            modules={"models": ["api.v1.admin_user.models"]},
            generate_schemas=True,
            add_exception_handlers=True,
        )
    except Exception as e:
        raise Exception(str(e))
