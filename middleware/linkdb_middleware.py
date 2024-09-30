from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware,StreamingResponse
from sql_app.mysqlServe import init_mysql
from tortoise import Tortoise

class LinkDBMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request:Request, call_next) -> StreamingResponse:
        await init_mysql(init_mysql)
        response:StreamingResponse = await call_next(request)
        await Tortoise.close_connections()
        return response