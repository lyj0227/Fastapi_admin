import jwt
from fastapi import Header
from datetime import datetime, timedelta
from config import settings


ALGORITHM = "HS256"


# 生成签名
def creat_token(data: dict):
    jwt_data = data.copy()
    exp = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    jwt_data.update({'exp': exp})
    return jwt.encode(jwt_data, settings.SECRET_KEY, algorithm=ALGORITHM)


# 签名解密
def verify_token(token: str | None = Header()):
    return jwt.decode(token, settings.SECRET_KEY, ALGORITHM)

