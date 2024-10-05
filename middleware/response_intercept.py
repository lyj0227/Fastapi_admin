import json
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from api.v1.admin_user.services import creat_admin
from starlette.responses import StreamingResponse


# 响应拦截中间件
class ResponseInterceptor(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> StreamingResponse:
        response: Response = None
        try:
            response: StreamingResponse = await call_next(request)
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"code": 500, "data": None, "message": "Internal Server Error"},
            )
        await creat_admin()
        if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
            return response
        code = response.status_code
        response_body = b""
        global data
        global cleaned_data
        cleaned_data = {}
        async for chunk in response.body_iterator:
            response_body += chunk
        if response_body:
            cleaned_data = json.loads(response_body.decode("utf-8"))
        if code == 200:
            data = JSONResponse(
                status_code=code,
                content={"code": code, "message": "success", "data": cleaned_data},
            )
        else:
            error_message = cleaned_data.get("detail")
            data = JSONResponse(
                status_code=code,
                content={"code": code, "message": error_message, "data": None},
            )
        return data
