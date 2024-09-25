from tortoise.contrib.fastapi import register_tortoise
from config import settings


def init_database(app):
    # 创建数据库ORM链接
    try:
        register_tortoise(
            app,
            db_url=f'mysql://{settings.MYSQL_USERNAME}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:'
                   f'{settings.MYSQL_POST}/{settings.MYSQL_DATABASES}',
            modules={"models": ["api.v1.admin_user.models"]},
            generate_schemas=True,
            add_exception_handlers=True,
        )
    except Exception as e:
        raise Exception(str(e))
