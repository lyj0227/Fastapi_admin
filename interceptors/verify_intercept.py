from fastapi import FastAPI, status, HTTPException
from fastapi.exceptions import RequestValidationError

def verify_intercept(app:FastAPI):
    @app.exception_handler(RequestValidationError)
    def verify_intercept(request, exc):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Validation Error",
        )