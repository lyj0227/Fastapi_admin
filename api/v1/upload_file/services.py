import os
import oss2
import secrets
import string
from config import settings
from fastapi import UploadFile, HTTPException


async def upload_file(file: UploadFile):
    _, extension = os.path.splitext(file.filename)
    content = await file.read()
    file_name = (
        "".join(secrets.choice(string.ascii_letters + string.digits) for i in range(16))
        + extension
    )
    auth = oss2.AuthV4(settings.ACCESS_KEY_ID, settings.ACCESSKEY_SECRET)
    bucket = oss2.Bucket(
        auth,
        "https://oss-cn-beijing.aliyuncs.com",
        "fastapi-admin1",
        region="cn-beijing",
    )
    try:
        result = bucket.put_object(f"static/{file_name}", content)
        if result.status != 200:
            raise HTTPException(status_code=400, detail="文件上传失败")
        else:
            url = (
                "your_aliyun_url"
                + f"static/{file_name}"
            )
            return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=400, detail="文件上传失败")
