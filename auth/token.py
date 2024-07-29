import jwt
import os
from fastapi import Header, status
from datetime import datetime, timedelta
from utils.api_response import APIResponse

# 使用随机字符串生成加密密钥
KEY = os.urandom(32)


# 生成签名
def creat_token(data: dict, time: float = 3):
    jwt_data = data.copy()
    exp = datetime.utcnow() + timedelta(minutes=time)
    jwt_data.update({'exp': exp})
    return jwt.encode(jwt_data, KEY, algorithm='HS256')


# 签名解密
def verify_token(token: str | None = Header()):
    if token is None:
        APIResponse(code=status.HTTP_401_UNAUTHORIZED, message="Invalid Token Error").http_error()
    else:
        try:
            return jwt.decode(token, KEY, 'HS256')
        except jwt.InvalidSignatureError:
            APIResponse(code=status.HTTP_401_UNAUTHORIZED, message="Invalid Token Error").http_error()
        except jwt.ExpiredSignatureError:
            APIResponse(code=status.HTTP_401_UNAUTHORIZED, message="Invalid Token Error").http_error()
        except jwt.DecodeError:
            APIResponse(code=status.HTTP_401_UNAUTHORIZED, message="Decode Error").http_error()
        except jwt.InvalidAlgorithmError:
            APIResponse(code=status.HTTP_401_UNAUTHORIZED, message="Invalid Algorithm Error").http_error()
        except jwt.InvalidKeyError:
            APIResponse(code=status.HTTP_401_UNAUTHORIZED, message="Invalid Key Error").http_error()
