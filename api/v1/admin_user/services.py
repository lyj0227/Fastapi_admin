from .models import User
from fastapi import status, HTTPException
from tortoise.queryset import Q
from utils.password import password_hash, verify_password
from tortoise.exceptions import DoesNotExist, IntegrityError


# 用户名密码校验
async def user_check(username, password):
    user = await User.get(userName=username)
    if verify_password(password, user.passWord):
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='The user name or password is incorrect'
        )


# 创建新用户
async def create_user(username, password):
    try:
        await User(userName=username, passWord=password_hash(password)).save()
        return True
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User creation failure'
        )


# 更新密码
async def edit_password(id: int | str, password: str, new_password: str):
    user = await User.get(id=id)
    if verify_password(password, user.passWord):
        user.passWord = password_hash(new_password)
        await user.save()
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='old password wrong'
        )


