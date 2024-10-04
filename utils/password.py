from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


# 加密函数
def password_hash(password: str) -> str:
    return pwd_context.hash(password)


# 密码校验
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        raise Exception(str(e))
