from .schemas import Token, UserModel
from .services import user_check, create_user, edit_password
from auth.token import creat_token
from fastapi import APIRouter, Form, Depends
from auth.token import verify_token

user = APIRouter(tags=["admin-user"], prefix="/admin")


@user.post('/login', summary='用户登录')
async def admin_user_login(username: str = Form(min_length=6, max_length=12),
                           password: str = Form(min_length=6, max_length=12,
                                                regex='^[a-zA-Z0-9_]+$')):
    state = await user_check(username, password)
    token = creat_token({"userid": state.id})
    return {'token':token}


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

