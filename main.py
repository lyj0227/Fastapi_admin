from fastapi import FastAPI
from api.v1.main import include_router
from sql_app.mysqlServe import init_mysql

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
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi_pagination import add_pagination
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address, default_limits=["1/1 seconds"])
# 创建app实例
app = FastAPI(
    debug=settings.DEBUG,
    title=settings.TITLE,
    summary=settings.SUMMARY,
    version=settings.VERSION,
    openapi_url=settings.OPENAPI_URL,
    responses=settings.RESPONSES,
)
# 限制请求速率
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.mount("/static", StaticFiles(directory="static"), name="static")

# 异常拦截
ApiExceptionInterception(app)
# 响应体拦截中间件
app.add_middleware(ResponseInterceptor)
# 日志中间件
app.add_middleware(LoggerMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.HOSTS)
# 分页中间件
add_pagination(app)
# 挂载路由
include_router(app)
# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=settings.CREDENTIALS,
    allow_methods=settings.MEDOTHS,
    allow_headers=settings.HEADERS,
)

init_mysql(app)
