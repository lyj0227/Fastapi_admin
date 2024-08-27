from .models import User
from fastapi import HTTPException
from utils.password import password_hash, verify_password
from tortoise.exceptions import IntegrityError


# 用户名密码校验
async def user_check(username, password):
    user = await User.get(userName=username)
    if verify_password(password, user.passWord):
        return user
    else:
        raise HTTPException(
            status_code=400,
            detail='The user name or password is incorrect'
        )


# 创建新用户
async def create_user(username, password):
    try:
        await User(userName=username, passWord=password_hash(password)).save()
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail='User creation failure'
        )


# 更新密码
async def edit_password(id: int | str, password: str, new_password: str):
    user = await User.get(id=id)
    if verify_password(password, user.passWord):
        user.passWord = password_hash(new_password)
        await user.save()
    else:
        raise HTTPException(
            status_code=400,
            detail='old password wrong'
        )


