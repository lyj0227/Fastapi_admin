# mdi加密模块
import hashlib


# 密码校验加密函数
def password_hash(password: str):
    has = hashlib.sha256()
    has.update(password.encode('utf-8'))
    return has.hexdigest()


