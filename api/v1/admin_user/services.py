from .models import User
from fastapi import status, HTTPException
from tortoise.queryset import Q
from utils.password import password_hash
from tortoise.exceptions import DoesNotExist, IntegrityError


# 用户名密码校验
async def user_check(username, password):
    try:
        user = await User.get(userName=username, passWord=password_hash(password))
        return user
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
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
    try:
        user = await User.get(Q(id=id) & Q(passWord=password_hash(password)))
        user.passWord = password_hash(new_password)
        await user.save()
        return True
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='old password wrong'
        )


