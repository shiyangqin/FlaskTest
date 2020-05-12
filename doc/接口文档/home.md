# 接口文档

json返回值统一格式为：
```python
{
    "status": "",
    "error": "",
    "data": {}
}
```

+ status： 状态信息
    + "time out": session过期
    + "not allow": 权限验证失败
    + "数据异常！"：出现了意料之外的异常
    + "ok": 成功
    
+ error： 异常信息，当status为"数据异常！"时才返回

+ data: 返回数据，当status为"ok"时才返回

+ [账户模块](auth.md)
