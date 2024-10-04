from fastapi import FastAPI, HTTPException, Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from jwt import PyJWTError
from fastapi.exceptions import RequestValidationError
from tortoise.exceptions import DoesNotExist, IntegrityError


class ApiExceptionInterception:
    def __init__(self, app: FastAPI, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if app is not None:
            self.init_app(app)

    def init_app(self, app: FastAPI):
        app.add_exception_handler(RequestValidationError, handler=self.all_verify)
        app.add_exception_handler(PyJWTError, handler=self.all_jwterror)
        app.add_exception_handler(DoesNotExist, handler=self.all_doesnotexist)
        app.add_exception_handler(IntegrityError, handler=self.integrity_error)

    async def all_jwterror(self, reqiest: Request, exc: PyJWTError):
        raise HTTPException(
            status_code=401,
            detail=str(exc),
        )

    async def all_doesnotexist(self, reqiest: Request, exc: DoesNotExist):
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    async def all_verify(self, reqiest: Request, exc: RequestValidationError):
        raise HTTPException(
            status_code=422,
            detail="Validation Error",
        )

    async def all_http_error(self, reqiest: Request, exc: StarletteHTTPException):
        raise HTTPException(
            status_code=exc.status_code,
            detail=str(exc.detail),
        )

    async def all_exception_handler(self, reqiest: Request, exc: HTTPException):
        raise HTTPException(
            status_code=exc.status_code,
            detail=str(exc.detail),
        )

    async def integrity_error(self, reqiest: Request, exc: IntegrityError):
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )
