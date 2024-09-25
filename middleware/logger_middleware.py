import sys
from loguru import logger
from fastapi import Request, Response
from datetime import datetime, timedelta, timezone
from starlette.middleware.base import BaseHTTPMiddleware

class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,request: Request, call_next) -> Response:
        method = request.method
        url = request.url
        response: Response = await call_next(request)
        china_tz = timezone(timedelta(hours=8), 'China')
        current_time_china = datetime.now(china_tz)
        formatted_time = current_time_china.strftime('%Y-%m-%d')
        code = response.status_code
        logger.remove()
        logger.add(sys.stderr, colorize=True, format="<green>{message}</green>", level="INFO")
        logger.add(f"{formatted_time}.log", rotation="1 week", enqueue=True)
        logger.info(f'{url} {method} {code} {current_time_china}')
        return response

