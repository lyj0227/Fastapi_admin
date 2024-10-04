from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, StreamingResponse
from sql_app.mysqlServe import init_mysql
from tortoise import Tortoise, connections


class LinkDBMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> StreamingResponse:
        try:
            await init_mysql()
            await Tortoise.generate_schemas()
            response: StreamingResponse = await call_next(request)
        finally:
            await connections.close_all()
        return response
