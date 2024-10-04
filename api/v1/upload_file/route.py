from fastapi import APIRouter, UploadFile
from .services import upload_file
from .schemas import UploadFileVo

upload = APIRouter(tags=["upload_file"], prefix="/upload")


@upload.post("/file", summary="文件上传", response_model=UploadFileVo)
async def uploadFile(file: UploadFile):
    return await upload_file(file)
