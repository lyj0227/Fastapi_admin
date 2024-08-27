from fastapi import FastAPI
from .admin_user.route import user


def include_router(app: FastAPI):
    app.include_router(user)




