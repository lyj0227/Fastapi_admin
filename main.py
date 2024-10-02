from fastapi import FastAPI
from api.v1.main import include_router
# CORS模块
from starlette.middleware.cors import CORSMiddleware
# 环境配置
from config import settings
# 异常拦截器
from interceptors.http_intercept import ApiExceptionInterception
# 静态文件
from fastapi.staticfiles import StaticFiles
# 中间件
from middleware.logger_middleware import LoggerMiddleware
from middleware.response_intercept import ResponseInterceptor
from middleware.linkdb_middleware import LinkDBMiddleware
from fastapi_pagination import  add_pagination
# 创建app实例
app = FastAPI(
    debug=settings.DEBUG,
    title=settings.TITLE,
    summary=settings.SUMMARY,
    version=settings.VERSION,
    openapi_url=settings.OPENAPI_URL,
    responses=settings.RESPONSES,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# 异常拦截
ApiExceptionInterception(app)
# 响应体拦截中间件
app.add_middleware(ResponseInterceptor)
# 日志中间件
app.add_middleware(LoggerMiddleware)
app.add_middleware(LinkDBMiddleware)

# 分页中间件
add_pagination(app)
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
