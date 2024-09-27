from config import settings
from pydantic_settings import BaseSettings




class Data(BaseSettings):
    token: str


class UserVo(settings.HttpResponses):
    data:Data
