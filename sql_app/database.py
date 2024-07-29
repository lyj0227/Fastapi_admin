from tortoise.contrib.fastapi import register_tortoise

GENERATE_SCHEMAS = False
ADD_EXCEPTION_HANDLERS = False


class SqlError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def init_database(app, env):
    global GENERATE_SCHEMAS
    global ADD_EXCEPTION_HANDLERS
    if env.env == 'dev':
        GENERATE_SCHEMAS = True
        ADD_EXCEPTION_HANDLERS = True
    elif env.env == 'pro':
        GENERATE_SCHEMAS = False
        ADD_EXCEPTION_HANDLERS = False
    # 创建数据库ORM链接
    try:
        register_tortoise(
            app,
            db_url='mysql://root:lyj227@localhost:3306/admin',
            modules={"models": ["api.v1.admin_user.models"]},
            generate_schemas=GENERATE_SCHEMAS,
            add_exception_handlers=ADD_EXCEPTION_HANDLERS,
        )
    except Exception as e:
        raise SqlError(str(e))
