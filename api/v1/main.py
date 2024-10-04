from fastapi import FastAPI
from .admin_user.route import user
from .upload_file.route import upload


# 路由挂载函数
def include_router(app: FastAPI):
    app.include_router(user)
    app.include_router(upload)
