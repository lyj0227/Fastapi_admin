# FastAPI-Admin

#### 简介

Fastapi-admin是一款开源的后端项目模板,项目基于python3.11，fastapi 0.111.1,uvicorn 0.30.1,oss2 2.18.3, tortoise-orm 0.21.5 ,PyJWT 2.8.0 等技术

Gitee仓库 [gitee](https://gitee.com/liuyuanjie2234/fast-api-admin.git)
GitHub仓库 [GitHub](https://github.com/lyj0227/Fastapi_admin.git)

### 特性

- python3.11
- fastapi 0.111.1
- uvicorn 0.30.1
- 阿里云oss上传:oss2 2.18.3
- 路由级的权限控制:scopes
- 集成JWT令牌验证:PyJWT 2.8.0
- 便捷的分页模式:fastapi-pagination 0.12.29
- 异步的orm类库:tortoise-orm 0.21.5
- 增加了异常拦截以及响应体拦截
- 集成了docker,无需担心环境问题
- 对整体路由进行了请求速率的限制
- 集成了pytest
- 异步的redis连接池

#### 目录结构

```
|——admin
    ├─api
       ├─v1                         #接口版本
          │─admin_user              #admin-user模块
             │─models               #数据库模型
             │─route                #路由模块
             │─schemas              #响应模块
             │─services             #业务模块
          │─ main                   #初始化路由
    ├─auth                          #权限模块
        ├─authorization
    |——interceptors                 #拦截器
        |——http_intercept           #http异常拦截器
    |——middleware                   #中间件
        |——linkdb_middleware        #数据库中间件        
        |——logger_middleware        #日志中间件
        |——response_intercept       #响应体异常拦截中间件
    ├─sql_app                       #sql配置模块
        ├─mysqlServe                #mysql
        ├─redisServe                #redis
    ├─static                        #静态目录
    ├─tests                         #测试模块
    ├─utils                         #工具函数
        ├─scopes                    #权限实例化工具
        ├─password                  #密码加密函数
        ├─toolkit                   #时间格式化函数
    ├─venv                          #虚拟环境
    ├─config.py                     #环境配置文件
    ├─.env                          #环境文件
    ├─main                          #入口文件
    ├─requirements                  #模块包文件
    ├─test_main.http                #测试文件
```

#### 安装教程

- 1、git clone 本仓库
- 2、确保本地没有mysql:3306以及redis:6379服务，本地端口3000无占用
- 3、配置.env文件
- 4、docker compost up --build

#### 功能

- 权限控制：基于路由级别的权限控制
- 环境：集成了docker 无需担心多环境问题
- 异常处理：内部进行了异常拦截处理，无需担心无法处理未知的异常问题
- 统一的响应体结构
- 日志集成：集成了日志功能， 自动记录异常
- 基本的测试demo
- redis连接池测试demo
