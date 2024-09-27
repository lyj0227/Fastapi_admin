from fastapi import FastAPI
from api.v1.main import include_router
# 导入CORS模块
from starlette.middleware.cors import CORSMiddleware
# # 导入数据库模块
from sql_app.mysqlServe import init_mysql
# 导入环境配置
from config import settings
from middleware.logger_middleware import LoggerMiddleware
from middleware.response_intercept import ResponseInterceptor
from interceptors.verify_intercept import verify_intercept
from interceptors.token_intercept import token_intercept
# 静态文件
from fastapi.staticfiles import StaticFiles
# 创建app实例
app = FastAPI(
    debug=settings.DEBUG,
    title=settings.TITLE,
    summary=settings.SUMMARY,
    version=settings.VERSION,
    openapi_url=settings.OPENAPI_URL,
    responses=settings.RESPONSES
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# 异常拦截
verify_intercept(app)
token_intercept(app)

# 响应体拦截中间件
app.add_middleware(ResponseInterceptor)
# 日志中间件
app.add_middleware(LoggerMiddleware)

# 挂载路由
include_router(app)
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
init_mysql(app)
