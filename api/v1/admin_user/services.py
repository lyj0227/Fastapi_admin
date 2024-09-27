from .models import User
from fastapi import HTTPException
from utils.password import password_hash, verify_password
from sql_app.redisServe import get_redis


# 用户名密码校验
async def user_check(username, password):
    global user
    try:
        user = await User.get(userName=username)
    except Exception:
         raise HTTPException(
            status_code=400,
            detail='用户不存在'
        )
    if verify_password(password, user.passWord) is False:
        raise HTTPException(
            status_code=400,
            detail='The user name or password is incorrect'
        )
    return user
    


# 创建新用户
async def create_user(username, password):
    try:
        await User(userName=username, passWord=password_hash(password)).save()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# 更新密码
async def edit_password(id: int | str, password: str, new_password: str):
    user = await User.get(id=id)
    if verify_password(password, user.passWord) is False:
        raise HTTPException(
            status_code=400,
            detail='old password wrong'
        )
    user.passWord = password_hash(new_password)
    await user.save()



