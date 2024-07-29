from pydantic import BaseModel


class UserModel(BaseModel):
    detail: str


class Token(UserModel):
    token: str

