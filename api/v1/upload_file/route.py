from fastapi import APIRouter,UploadFile,File
from .schemas import UploadFileVo
from .services import upload_file
upload= APIRouter(tags=["upload_file"], prefix="/upload")


@upload.post('/file', responses={200:{'description':'Successful Response','model':UploadFileVo}} )
async def uploadFile(file: UploadFile = File(...)):
    url =  await upload_file(file)
    return {'url':url}
    