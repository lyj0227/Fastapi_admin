from tortoise import Model, fields


# 定义用户表
class User(Model):
    id = fields.IntField(pk=True)
    registrationTime = fields.DatetimeField(auto_now_add=True)
    userName = fields.CharField(max_length=14, unique=True)
    passWord = fields.CharField(max_length=100)
