from pydantic import BaseModel


class UserModel(BaseModel):
    message: str


class Token(UserModel):
    token: str

