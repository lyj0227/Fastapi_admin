from pydantic import BaseModel,Field
from datetime import datetime


class Permissions(BaseModel):
    code:int
    description:str

class Token(BaseModel):
    Authorization: str

class UserInfo(BaseModel):
    username:str
    is_frozen:bool
    is_admin:bool
    avatar:str|None
    role:list[str] = None
    permissions:list[Permissions] = None
    registration_time:datetime

class UserVo(BaseModel):
    userInfo: UserInfo
    authorization:str
    
class RegisterId(BaseModel):
    id:int

class PermissionsId(BaseModel):
    id:int

class Register(BaseModel):
    username:str
    is_frozen:bool
    is_admin:bool
    avatar:str|None
    password:str
    role:list[RegisterId]
    permissions:list[PermissionsId]


class CreateRole(BaseModel):
    name:str


class UserList(BaseModel):
    username:str
    is_frozen:bool
    is_admin:bool
    avatar:str|None
    registration_time:datetime


class UpdateUserInfo(Register):
    username:str = None
    is_admin:bool = None
    is_frozen:bool = None
    password:str = None
    role:list[RegisterId] = None


