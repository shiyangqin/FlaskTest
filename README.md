# OA
python个人练手OA后端服务

+ 部署

[安装docker](https://github.com/shiyangqin/doc/blob/master/Linux/docker.md#centos7%E5%AE%89%E8%A3%85docker)

将OA整个项目放在服务器的/opt目录下

执行部署命令：
```
sh /opt/OA/doc/deploy/deploy.sh
```

验证：打开浏览器输入服务器ip/test(例：10.255.175.224/test)，返回"{"status": "ok", "data": {"pg": true, "redis": true}}"则表示成功

+ [接口文档](doc/接口文档/home.md)
