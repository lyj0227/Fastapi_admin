from .schemas import Token, UserModel
from .services import user_check, create_user, edit_password
from auth.token import creat_token
from fastapi import APIRouter, Form, Depends
from auth.token import verify_token

user = APIRouter(tags=["admin"], prefix="/admin")


@user.post('/login', summary='用户登录', response_model=Token)
async def admin_user_login(username: str = Form(min_length=6, max_length=12, default='admins'),
                           password: str = Form(min_length=6, max_length=12, default='qwer1234',
                                                regex='^[a-zA-Z0-9_]+$')):
    state = await user_check(username, password)
    token = creat_token({"userid": state.id}, 3)
    message = {"token": token, "detail": 'success'}
    return message


@user.post('/register', summary='用户注册', response_model=UserModel)
async def admin_user_register(username: str = Form(min_length=6, max_length=12),
                              password: str = Form(min_length=6, max_length=12, default='123456',
                                                   regex='^[a-zA-Z0-9_]+$')):
    state = await create_user(username, password)
    if state is True:
        return {"detail": 'success'}


@user.post('/edit-password', summary='修改密码', response_model=UserModel)
async def admin_user_edit_password(token: str = Depends(verify_token),
                                   password: str = Form(min_length=6, max_length=12,
                                                        regex='^[a-zA-Z0-9_]+$'),
                                   new_password: str = Form(min_length=6, max_length=12,
                                                            regex='^[a-zA-Z0-9_]+$')
                                   ):
    state = await edit_password(token['userid'], password, new_password)
    if state is True:
        return {"detail": 'success'}

