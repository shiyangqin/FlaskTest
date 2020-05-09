+ [注册账号](#注册账号)

___
### 注册账号

url: /auth/register

methods：post

params：
```python
{
    "user_name": "",       # 账号
    "user_password": ""    # 密码
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
