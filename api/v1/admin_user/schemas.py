from pydantic import BaseModel


# 相应类
class UserModel(BaseModel):
    message: str


class Token(UserModel):
    token: str

