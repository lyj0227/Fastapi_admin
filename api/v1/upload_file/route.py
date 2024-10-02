from fastapi import APIRouter,UploadFile,File
from .schemas import UploadFile
from .services import upload_file
upload= APIRouter(tags=["upload_file"], prefix="/upload")


@upload.post('/file', response_model=UploadFile )
async def uploadFile(file: UploadFile = File(...)):
    url =  await upload_file(file)
    return {'url':url}
    