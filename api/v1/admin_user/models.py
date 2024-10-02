from tortoise import Model, fields

# 定义用户表
class User(Model):
    id = fields.IntField(pk=True,description='用户id')
    registration_time = fields.DatetimeField(auto_now_add=True,description='创建时间')
    username = fields.CharField(max_length=14, unique=True,db_index=True,description='用户名')
    password = fields.CharField(max_length=255,description='用户密码')
    is_frozen = fields.BooleanField(default=False,description='是否被冻结')
    is_admin = fields.BooleanField(default=False,description='是否为管理员')
    avatar = fields.CharField(null=True,max_length=255,description='头像')
    update_time = fields.DatetimeField(auto_now=True,description='更新时间')
    roles = fields.ManyToManyField("models.Role",db_constraint=False)

# 定义角色表
class Role(Model):
    id = fields.IntField(pk=True,description='角色id')
    name=fields.CharField(max_length=50,description='角色名',unique=True,db_index=True)
    permissions = fields.ManyToManyField("models.Permissions",db_constraint=False)


# 定义权限表
class Permissions(Model):
    id = fields.IntField(pk=True,description='权限id')
    code=fields.IntField(description='权限码',unique=True,db_index=True)
    description=fields.CharField(max_length=255,description='权限描述')
