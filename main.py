from fastapi import FastAPI
from api.v1 import routers
# 导入CORS模块
from starlette.middleware.cors import CORSMiddleware
# 导入数据库模块
from sql_app.database import init_database
# 导入环境配置
from config import settings

# 创建app实例
app = FastAPI(
    debug=settings.DEBUG,
    title=settings.TITLE,
    summary=settings.SUMMARY,
    version=settings.VERSION,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    openapi_url=settings.OPENAPI_URL,
)


# 挂载路由
try:
    for k in routers:
        app.include_router(k)
except Exception as e:
    raise Exception(e)

# CORS配置
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 挂载数据库
init_database(app)
