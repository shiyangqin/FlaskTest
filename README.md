# FlaskTest

python个人练手后端服务

## 部署

+ [安装docker](https://github.com/shiyangqin/Doc/blob/master/Docker/centos7%E5%AE%89%E8%A3%85docker.md)

+ [安装docker-compose](https://github.com/shiyangqin/Doc/blob/master/Docker/centos7%E5%AE%89%E8%A3%85docker-compose.md)

+ 将整个项目上传至服务器，在项目目录下执行部署命令：

```shell
docker-compose up -d
```

+ 验证：打开浏览器输入服务器ip/test(例：10.255.175.224/test)，返回"{"status": "ok", "data": {"pg": true, "redis": true}}"则表示成功

## [接口文档](doc/home.md)
