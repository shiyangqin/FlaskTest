+ [注册账号](#注册账号)
+ [账号登陆](#账号登陆)
+ [获取用户信息](#获取用户信息)

___
前端传输密码时需加密，后端对前端加密后的密码再次处理后存储，前端只需保证在注册和登陆时，传输的密文一致即可
___
### 注册账号

url: /auth/register

methods：post

params：
```python
{
    "user_name": "",        # 账号
    "user_password": "",    # 密码
    "person_name": "",      # 姓名
    "sex": "",              # 性别 0-女 1-男
    "birthday": "",         # 出生日期
    "email": "",            # 邮件地址
    "phone": "",            # 手机号
    "remark": ""            # 备注
}
```

return：
```python
{
    "status": "ok",
    "data": {
        "flag": True,      # true/false
        "msg": "注册成功"   # "注册成功"/"失败信息，例：账号已存在"
    }
}
```

___
### 账号登陆

url: /auth/register

methods：post

params：
```python
{
    "user_name": "",        # 账号
    "user_password": ""     # 密码
}
```

return：
```python
{
    "status": "ok",
    "data": {
        "login_id": 5,
        "user_name": "test",
        "login_time": "2020-05-11 12:53:42",
        "person_name": "",
        "sex": "1",
        "birthday": "",
        "email": "",
        "phone": "",
        "remark": "",
        "role_name": "超级管理员/管理员/普通用户",
        "function": [
            "auth"
        ],
        "session": "dabb17217aa050e2a7ab8ac3a64fd1a3"
    }
}
```


___
### 获取用户信息

url: /auth/info

methods：get

params：无

return：
```python
{
    "status": "ok",
    "data": {
        "login_id": 5,
        "user_name": "test",
        "login_time": "2020-05-11 12:53:42",
        "person_name": "",
        "sex": "1",
        "birthday": "",
        "email": "",
        "phone": "",
        "remark": "",
        "role_name": "超级管理员/管理员/普通用户",
        "function": [
            "auth"
        ],
        "session": "dabb17217aa050e2a7ab8ac3a64fd1a3"
    }
}
```
