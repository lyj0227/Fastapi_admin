import json
from .models import User,Role
from fastapi import HTTPException
from tortoise.transactions import atomic
from utils.password import password_hash, verify_password
from sql_app.redisServe import get_redis
from auth.authorization import creat_token

# 用户名密码校验
@atomic()
async def user_check(username, password):
    try:
        roles = []
        permissions = []
        user = await User.get(username=username).prefetch_related("roles__permissions")
        if verify_password(password, user.password) is False:
            raise HTTPException(
                status_code=400,
                detail='The user name or password is incorrect'
            )
        for role in user.roles:
            roles.append(role.name)
            for permission in role.permissions:
                permissions.append(permission.__dict__)
        token = creat_token({
                "user_id": user.id,
                "roles":json.dumps(roles),
                "is_admin":user.is_admin,
                "is_frozen":user.is_frozen,
                'permissions':json.dumps(permissions)
            })
        user.role = roles
        user.permissions = permissions
        data = {'userInfo':user,'authorization':token}
        return data
    except Exception as e:
         print(e)
         raise HTTPException(
            status_code=400,
            detail='The user does not exist'
        )
    


# 创建新用户
async def create_user(username, password):
    try:
        await User(username=username, password=password_hash(password)).save()
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



