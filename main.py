import argparse
from uvicorn import run
from fastapi import FastAPI
from api.v1 import routers
# 导入CORS模块
from fastapi.middleware.cors import CORSMiddleware
# 导入数据库模块
from sql_app.database import init_database, SqlError

app = FastAPI(title="FastAPI Admin", summary='FastAPI Admin 是一款基于fastapi的后端项目模板', version='1.0.0',docs_url='/')
# 挂在路由
try:
    for k in routers:
        app.include_router(k)
except Exception as e:
    SqlError(str(e))
# CORS配置
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建环境变量
parser = argparse.ArgumentParser(usage='env')
parser.add_argument('--env', default='dev', choices=['dev', 'pro'])
ENV = parser.parse_args()
init_database(app, ENV)
if __name__ == '__main__':
    if ENV.env == 'dev':
        run('main:app', port=8000, reload=True)
    elif ENV.env == 'pro':
        run('main:app', port=8000)
