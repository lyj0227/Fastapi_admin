import json


class Permissions:
    code:str|int


class Scopes:
    roles:list[str]
    permissions:list[Permissions]
    def __init__(self,roles,permissions) -> None:
        self.roles = roles
        self.permissions = permissions

def set_scopes(scopes:Scopes) ->list[str]:
    if type(scopes) != Scopes:
        raise Exception('类型不为Scopes')
    scopes = scopes.__dict__
    data = json.dumps(scopes)
    return [data]