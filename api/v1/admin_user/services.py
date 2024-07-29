from .models import User
from fastapi import status
from tortoise.queryset import Q
from utils.password import password_hash
from utils.api_response import APIResponse
from tortoise.exceptions import DoesNotExist, IntegrityError


# 用户名密码校验
async def user_check(username, password):
    try:
        user = await User.get(userName=username, passWord=password_hash(password))
        return user
    except DoesNotExist:
        return APIResponse(code=status.HTTP_403_FORBIDDEN,
                           message='The user name or password is incorrect').http_error()
    except Exception as e:
        print(e, type(e))


# 创建新用户
async def create_user(username, password):
    try:
        await User(userName=username, passWord=password_hash(password)).save()
        return True
    except IntegrityError:
        return APIResponse(code=status.HTTP_401_UNAUTHORIZED, message='User creation failure').http_error()
    except Exception as e:
        print(e, type(e))


# 更新密码
async def edit_password(id: int | str, password: str, new_password: str):
    try:
        user = await User.get(Q(id=id) & Q(passWord=password_hash(password)))
        user.passWord = password_hash(new_password)
        await user.save()
        return True
    except DoesNotExist:
        return APIResponse(code=status.HTTP_401_UNAUTHORIZED, message='old password wrong').http_error()
    except Exception as e:
        print(e, type(e))

