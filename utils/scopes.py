from pydantic import BaseModel
import json


class Permissions(BaseModel):
    code:str|int


class Scopes(BaseModel):
    roles:list[str]
    permissions:list[Permissions]

def set_scopes(scopes:Scopes):
    data = json.dumps(scopes)
    return [data]