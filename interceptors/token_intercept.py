from fastapi import FastAPI, status, HTTPException
from jwt import PyJWTError

def token_intercept(app:FastAPI):
    @app.exception_handler(PyJWTError)
    def verify_intercept(request, exc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )