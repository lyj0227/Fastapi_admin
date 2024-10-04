from pydantic_settings import BaseSettings


class UploadFileVo(BaseSettings):
    url: str
