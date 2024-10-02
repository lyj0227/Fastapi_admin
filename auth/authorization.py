import jwt
import json
from config import settings
from fastapi import Header,HTTPException
from datetime import datetime, timedelta
from fastapi.security import SecurityScopes

ALGORITHM = "HS256"



# 生成签名
def creat_token(data: dict) -> str:
    jwt_data = data.copy()
    exp = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    jwt_data.update({'exp': exp})
    return jwt.encode(jwt_data, settings.SECRET_KEY, algorithm=ALGORITHM)


# 签名解密
def verify_token(Authorization: str):
    Authorization = Authorization.split()[1]
    return jwt.decode(Authorization, settings.SECRET_KEY, ALGORITHM)


# 权限控制
def auth(securityScopes:SecurityScopes,Authorization:str = Header()):
    scopes = securityScopes.scopes[0]
    scopes = json.loads(scopes)
    # 判断登录状态
    if Authorization == None:
        raise HTTPException(status_code=401,detail='Not Log In')
    Authorization = verify_token(Authorization)
    if Authorization['is_frozen'] is True:
       raise HTTPException(status_code=404,detail='NOT FOUND')
    # 判断角色身份
    roles = json.loads(Authorization['roles'])
    for k in roles:
        if k not in scopes['roles']:
            raise HTTPException(status_code=404,detail='NOT FOUND')
    # 判断角色权限
    permissions = json.loads(Authorization['permissions'])
    for k in permissions:
         if str(k['code']) not in  scopes['permissions']:
              raise HTTPException(status_code=404,detail='NOT FOUND')
            
         
    

