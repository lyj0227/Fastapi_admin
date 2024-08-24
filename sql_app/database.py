from tortoise.contrib.fastapi import register_tortoise
from config import settings


class SqlError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def init_database(app):
    # 创建数据库ORM链接
    try:
        register_tortoise(
            app,
            db_url=settings.DB_URL,
            modules={"models": ["api.v1.admin_user.models"]},
            generate_schemas=settings.GENERATE_SCHEMAS,
            add_exception_handlers=settings.ADD_EXCEPTION_HANDLERS,
        )
    except Exception as e:
        raise SqlError(str(e))
