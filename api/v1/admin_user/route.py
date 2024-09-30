from .schemas import UserVo
from .services import user_check, create_user, edit_password
from fastapi import APIRouter, Form, Depends,Security,Header
from auth.authorization import verify_token
from tortoise.transactions import atomic
from .models import User, Role , Permissions
from utils.password import password_hash
from utils.scopes import set_scopes
from auth.authorization import auth

user = APIRouter(tags=["admin-user"], prefix="/admin")


@user.post('/login', summary='用户登录', response_model=UserVo)
async def admin_user_login(username: str = Form(min_length=6, max_length=12),
                           password: str = Form(min_length=6, max_length=12)):
    return await user_check(username, password)


@user.post('/register', summary='用户注册')
async def admin_user_register(username: str = Form(min_length=6, max_length=12),
                              password: str = Form(min_length=6, max_length=12,
                                                   regex='^[a-zA-Z0-9_]+$')):
    await create_user(username, password)
    return None


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
@atomic()
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


@user.get('/demo',dependencies=[Security(auth,scopes=set_scopes({'roles':['user'],'permissions':['1','2','3']}))])
async def demo():
    return 