import sys
from loguru import logger
from fastapi import Request, Response
from datetime import datetime, timedelta, timezone


async def logger_middleware(request: Request, call_next):
    method = request.method
    url = request.url
    response: Response = await call_next(request)
    china_tz = timezone(timedelta(hours=8), 'China')
    current_time_china = datetime.now(china_tz)
    formatted_time = current_time_china.strftime('%Y-%m-%d')
    code = response.status_code
    logger.remove()
    logger.add(sys.stderr, format="{level} | {message}", level="INFO")
    logger.add(f"{formatted_time}.log", rotation="1 week", enqueue=True)
    logger.info(f'{url} {method} {code} {current_time_china}')
    return response

