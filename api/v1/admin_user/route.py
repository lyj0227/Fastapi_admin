from auth.authorization import auth
from .schemas import UserVo,Register,CreateRole
from utils.password import password_hash
from utils.scopes import set_scopes,Scopes
from auth.authorization import verify_token
from .models import User, Role , Permissions
from fastapi import APIRouter, Form, Depends,Security
from .services import user_check, create_user, edit_password,create_role


user = APIRouter(tags=["admin-user"], prefix="/admin")


@user.post('/login', summary='用户登录', response_model=UserVo)
async def admin_user_login(username: str = Form(min_length=6, max_length=12),
                           password: str = Form(min_length=6, max_length=12)):
    return await user_check(username, password)


@user.post('/register', summary='用户注册',dependencies=[Security(auth,scopes=set_scopes(Scopes(roles=['admin'],permissions=['1'])))])
async def admin_user_register(register:Register):
    return await create_user(register)


@user.post('/create_role',summary='创建角色', dependencies=[Security(auth,scopes=set_scopes(Scopes(roles=['admin'],permissions=['1'])))])
async def create_roles(createRole:CreateRole):
    return await create_role(createRole)


@user.post('/edit-password', summary='修改密码')
async def admin_user_edit_password(token: str = Depends(verify_token),
                                   password: str = Form(min_length=6, max_length=12,
                                                        regex='^[a-zA-Z0-9_]+$'),
                                   new_password: str = Form(min_length=6, max_length=12,
                                                            regex='^[a-zA-Z0-9_]+$')
                                   ):
    await edit_password(token['userid'], password, new_password)
    return None


@user.get('/creatadmin')
async def creatadmin():
    admin_user = {
        'username':'admins',
        'password':password_hash('123456'),
        "is_frozen":False,
        "is_admin":True
    }
    roles = {
        "name":'admin'
    }
    permissions = {
        "code":'1',
        "description":"访问全部接口"
    }
    user = await User.create(**admin_user)
    role = await Role.create(**roles)
    permission = await Permissions.create(**permissions)
    await user.roles.add(role)
    await role.permissions.add(permission)
    return '创建成功'



@user.get('/demo',dependencies=[Security(auth,scopes=set_scopes(Scopes(roles=['admin','user'],permissions=['1','2'])))])
async def demo():
    return 