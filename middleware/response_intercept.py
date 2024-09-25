import json
from fastapi import Request
from starlette.middleware.base import StreamingResponse
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class ResponseInterceptor(BaseHTTPMiddleware):
    async def dispatch(self, request:Request, call_next) -> StreamingResponse:
        response:StreamingResponse = await call_next(request)
        if request.url.path in ['/docs','/redoc','/openapi.json']:
            return response
        code = response.status_code
        response_body = b""
        global data
        global cleaned_data 
        cleaned_data = {}
        try:
            async for chunk in response.body_iterator:
                response_body += chunk
        except Exception as e:
            print(e)
        # 重置为普通迭代器
        try:
            response.body_iterator = iter([response_body])
            cleaned_data = json.loads(response_body.decode("utf-8"))
        except Exception as e:
            print(e)
        
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
        # 使用异步生成器返回响应体
        async def new_body_iterator():
            yield response_body
        # 设置为异步生成器
        response.body_iterator = new_body_iterator()  
        return data