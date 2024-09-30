from config import settings
from fastapi import FastAPI
from tortoise import Tortoise


async def init_mysql(app:FastAPI):
    # 创建数据库ORM链接
    try:
        await Tortoise.init(
            db_url=f'mysql://{settings.MYSQL_USERNAME}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:'
                   f'{settings.MYSQL_POST}/{settings.MYSQL_DATABASES}',
            modules={"models": ["api.v1.admin_user.models"]},
            timezone="Asia/Shanghai"
        )
        await Tortoise.generate_schemas()
    except Exception as e:
        raise Exception(str(e))
