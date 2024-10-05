import json
from auth.authorization import verify_token
from .models import User, Role, Permissions
from fastapi import HTTPException
from redis import Redis
from tortoise.transactions import atomic
from .schemas import Register, CreateRole, UpdateUserInfo, Permissions as Permission
from utils.toolkit import convert_to_datetime
from auth.authorization import creat_token
from fastapi_pagination.ext.tortoise import paginate
from utils.password import password_hash, verify_password


async def user_check(username: str, password: str) -> dict:
    roles = []
    permissions = []
    user = await User.get(username=username).prefetch_related("roles__permissions")
    if verify_password(password, user.password) is False:
        raise HTTPException(
            status_code=400, detail="The user name or password is incorrect"
        )
    for role in user.roles:
        roles.append(role.name)
        for permission in role.permissions:
            permissions.append(permission.__dict__)
    token = creat_token(
        {
            "user_id": user.id,
            "roles": json.dumps(roles),
            "is_admin": user.is_admin,
            "is_frozen": user.is_frozen,
            "permissions": json.dumps(permissions),
        }
    )
    user.role = roles
    user.permissions = permissions
    data = {"userInfo": user, "Authorization": token}
    return data


@atomic()
async def create_user(register: Register) -> None:
    user = await User.create(
        username=register.username,
        password=password_hash(register.password),
        avatar=register.avatar,
        is_frozen=register.is_frozen,
        is_admin=register.is_admin,
    )
    role_ids = [k.id for k in register.role]
    roles = await Role.filter(id__in=role_ids)
    await user.roles.add(*roles)
    return None


async def create_role(createRole: CreateRole) -> None:
    await Role.create(name=createRole.name)
    return None


@atomic()
async def delete_role(id: int) -> None:
    role = await Role.get(id=id).prefetch_related("permissions", "users")
    await role.permissions.clear()
    await role.users.clear()
    await role.delete()
    return None


async def user_list(username, start_time, end_time, is_frozen, is_admin):
    users = User.all()
    data = {}
    if username:
        data["username__icontains"] = username
    if start_time:
        start_time = convert_to_datetime(start_time)
        data["registration_time__gte"] = start_time
    if end_time:
        end_time = convert_to_datetime(end_time)
        data["registration_time__lte"] = end_time
    if is_frozen is not None:
        data["is_frozen"] = is_frozen
    if is_admin is not None:
        data["is_admin"] = is_admin
    users = users.filter(**data)
    return await paginate(users)


async def user_info(id: int):
    user = await User.get(id=id).prefetch_related("roles__permissions")
    roles = []
    permissions = []
    for role in user.roles:
        roles.append(role.name)
        for permission in role.permissions:
            permissions.append(permission.__dict__)
    user.role = roles
    user.permissions = permissions
    return user


@atomic()
async def delete_user(id: int):
    user = await User.get(id=id).prefetch_related("roles__permissions")
    await user.roles.clear()
    await user.delete()
    return None


@atomic()
async def update_user_info(id: int, user_info: UpdateUserInfo):
    user = await User.get(id=id).prefetch_related("roles__permissions")
    if user_info.username:
        user.username = user_info.username
    if user_info.avatar:
        user.avatar = user_info.avatar
    if user_info.is_admin:
        user.avatar = user_info.is_admin
    if user_info.is_frozen:
        user.avatar = user_info.is_frozen
    if user_info.password:
        user.avatar = user_info.password
    if user_info.role:
        roles = []
        for k in user_info.role:
            roles.append(k.id)
        role = await Role.filter(id__in=roles)
        await user.roles.add(*role)
    await user.save()
    return None


async def create_permissions(permissions: Permission):
    await Permissions(code=permissions.code, description=permissions.description).save()
    return None


@atomic()
async def roles_join_permissions(role_id: int, permissions_id: int):
    role = await Role.get(id=role_id)
    permissions = await Permissions.get(id=permissions_id)
    await role.permissions.add(permissions)
    return None


async def edit_password(Authorization: str, password: str, new_password: str):
    id = verify_token(Authorization)["user_id"]
    user = await User.get(id=id)
    if verify_password(password, user.password) is False:
        raise HTTPException(status_code=400, detail="old password wrong")
    user.password = password_hash(new_password)
    await user.save()
    return None


async def role_list(name):
    data = {}
    if name:
        data["name__icontains"] = name
    roles = Role.filter(**data)
    return await paginate(roles)


async def permissions_list(description, code):
    data = {}
    if description:
        data["description__icontains"] = description
    if code:
        data["code"] = code
    permissions = Permissions.filter(**data)
    return paginate(permissions)


@atomic()
async def delete_permissions(id: int):
    permissions = await Permissions.get(id=id)
    await permissions.roles.clear()
    await permissions.delete()
    return None


@atomic()
async def creat_admin():
    admin_user = {
        "username": "admins",
        "password": password_hash("123456"),
        "is_frozen": False,
        "is_admin": True,
    }
    roles = {"name": "admin"}
    permissions = {"code": "1", "description": "访问全部接口"}
    try:
        user = await User.get(username="admins")
    except Exception as e:
        user = await User.create(**admin_user)
        role = await Role.create(**roles)
        permission = await Permissions.create(**permissions)
        await user.roles.add(role)
        await role.permissions.add(permission)
    return "创建成功"


async def redis_test_demo(redis: Redis):
    await redis.set(name="1", value=2)
    return None
