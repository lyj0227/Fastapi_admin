import sys
from loguru import logger
from starlette.requests import Request
from fastapi import  Response,HTTPException
from datetime import datetime, timedelta, timezone
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
"""
日志中间件
"""
class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,request: Request, call_next) -> Response:
        method = request.method
        path = request.scope['path']
        http_type = request.scope['type']
        china_tz = timezone(timedelta(hours=8), 'China')
        current_time_china = datetime.now(china_tz)
        formatted_time = current_time_china.strftime('%Y-%m-%d')
        response = await call_next(request)
        logger.remove()
        code = response.status_code
        if code == 500:
            logger.add(sys.stderr, colorize=True, format=f"<red>{method} - {code}</red> - <bold><i>{path} - {http_type}</i></bold> - <blue>{current_time_china}</blue>", level="ERROR")
            logger.add(f"{formatted_time}.debug.log", rotation="1 week", enqueue=True)
            logger.error(f'{method} {code} {path} {http_type} {current_time_china}')
        else:
            logger.add(sys.stderr, colorize=True, format=f"<green>{method}- {code}</green> - <bold><i>{path} - {http_type}</i></bold> - <blue>{current_time_china}</blue>", level="INFO")
            logger.add(f"{formatted_time}.log", rotation="1 week", enqueue=True)
            logger.info(f'{method} {code} {path} {http_type} {current_time_china}')
        return response