import json
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware,StreamingResponse


# 响应拦截中间件
class ResponseInterceptor(BaseHTTPMiddleware):
    async def dispatch(self, request:Request, call_next) -> StreamingResponse:
        if request.url.path in ['/docs','/redoc','/openapi.json']:
            return response
        response:StreamingResponse = await call_next(request)
        code = response.status_code
        response_body = b""
        global data
        global cleaned_data 
        cleaned_data = {}
        async for chunk in response.body_iterator:
            response_body += chunk
        response.body_iterator = iter([response_body])
        cleaned_data = json.loads(response_body.decode("utf-8"))
        if code == 200:
            data = JSONResponse(status_code=code,content={
                "code":code,
                'message':"success",
                "data":cleaned_data
            })
        else:
            data = JSONResponse(status_code=code,content={
                "code":code,
                'message':cleaned_data['detail'],
                "data":None
            })
        return data