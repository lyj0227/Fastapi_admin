from config import settings
from pydantic_settings import BaseSettings

class UploadFile(BaseSettings):
    url: str


class UploadFileVo(settings.HttpResponses):
    data:UploadFile