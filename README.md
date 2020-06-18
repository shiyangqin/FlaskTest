# OA

python个人练手OA后端服务

## 部署

+ [安装docker](https://github.com/shiyangqin/Doc/blob/master/%E5%AD%A6%E4%B9%A0%E6%96%87%E6%A1%A3/Docker/centos7%E5%AE%89%E8%A3%85docker.md)

+ [安装docker-compose](https://github.com/shiyangqin/Doc/blob/master/%E5%AD%A6%E4%B9%A0%E6%96%87%E6%A1%A3/Docker/centos7%E5%AE%89%E8%A3%85docker-compose.md)

+ 将OA整个项目上传至服务器，在OA目录下执行部署命令：

```shell
docker-compose up -d
```

+ 验证：打开浏览器输入服务器ip/test(例：10.255.175.224/test)，返回"{"status": "ok", "data": {"pg": true, "redis": true}}"则表示成功

## [接口文档](doc/接口文档/home.md)
