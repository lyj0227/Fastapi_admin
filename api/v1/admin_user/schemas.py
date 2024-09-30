from pydantic import BaseModel
from datetime import datetime

class Permissions(BaseModel):
    id:int 
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
    

