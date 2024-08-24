import jwt
from fastapi import Header, status, HTTPException
from datetime import datetime, timedelta
from config import settings


ALGORITHM = "HS256"


# 生成签名
def creat_token(data: dict):
    jwt_data = data.copy()
    exp = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    jwt_data.update({'exp': exp})
    return jwt.encode(jwt_data, settings.SECRET_KEY, algorithm=ALGORITHM)


# 签名解密
def verify_token(token: str | None = Header()):
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token Error"
        )
    else:
        try:
            return jwt.decode(token, settings.SECRET_KEY, ALGORITHM)
        # 抛出签名验证错误异常
        except jwt.InvalidSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token Error"
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token Error"
            )
        except jwt.DecodeError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Decode Error"
            )
        except jwt.InvalidAlgorithmError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Algorithm Error"
            )
        except jwt.InvalidKeyError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Key Error"
            )
