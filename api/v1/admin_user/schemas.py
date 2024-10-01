from pydantic import BaseModel,Field
from datetime import datetime
from typing import ClassVar


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
    role:list[str]
    permissions:list[Permissions]
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
    registration_time:ClassVar


class CreateRole(BaseModel):
    name:str