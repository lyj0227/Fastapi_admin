from fastapi import FastAPI, status, HTTPException
from api.v1.main import include_router
# 导入CORS模块
from starlette.middleware.cors import CORSMiddleware
# # 导入数据库模块
from sql_app.database import init_database
# 导入环境配置
from config import settings
# 异常拦截
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from jwt import PyJWTError

from middleware.logger_middleware import LoggerMiddleware
from middleware.response_intercept import ResponseInterceptor


class HttpResponses(BaseModel):
    detail: str


# 创建app实例
app = FastAPI(
    debug=settings.DEBUG,
    title=settings.TITLE,
    summary=settings.SUMMARY,
    version=settings.VERSION,
    openapi_url=settings.OPENAPI_URL,
    responses={
        422: {"description": "Validation Error", "model": HttpResponses}
    }
)


# 校验异常拦截
@app.exception_handler(RequestValidationError)
def verify_intercept(request, exc):
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Validation Error",
    )


# jwt异常拦截
@app.exception_handler(PyJWTError)
def verify_intercept(request, exc):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=str(exc),
    )

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
init_database(app)
