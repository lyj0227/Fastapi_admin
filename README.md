# FastAPI-Admin

#### 介绍
该项目是由FastAPI开发的一款后端项目模板，配置了简单的环境变量，并且有简单的demo请求可以作为参考使用

#### 目录结构
```
├─api
│  ├─v1                         #接口版本
│  │  │─admin_user              #admin-user模块
│  │  │  │─models               #数据库模型
│  │  │  │─route                #路由模块
│  │  │  │─schemas              #响应模块
│  │  │  │─services             #业务模块
├─auth                          #权限模块
│ ├─token                       #token
├─sql_app                       #sql配置模块
│ ├─database                    #数据库配置模块
├─utils                         #工具函数
│  ├─api_response               #响应函数
│  ├─password                   #密码加密函数
├─venv                          #虚拟环境
├─main                          #入口文件
├─requirements                  #模块包文件
├─test_main.http                #测试文件
```



#### 安装教程
1、git clone 本仓库
2、pip install -r requirements.txt 安装模块包
3、配置database文件
4、通过python main.py --env (dev/pro) 运行项目
#### 使用说明
1、该项目基于python3.11开发,请检查当前python运行版本
#### 特性
```
·采用python3.11版本
·Tortoise ORM——————Tortoise ORM是一个受Django启发的易于使用的ORM(对象关系映射器)。
·FastAPI——————FastAPI 是一个用于构建 API 的现代、快速（高性能）的 web 框架，使用 Python 并基于标准的 Python 类型提示。
·pyjwt——————是一个Python库，它允许你编码和解码JSON Web 令牌(JWT)
·Uvicorn——————高性能 ASGI 服务器
```
