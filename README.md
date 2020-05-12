# OA
python个人练手OA后端服务

+ 部署

[安装docker](https://github.com/shiyangqin/doc/blob/master/Linux/docker.md#centos7%E5%AE%89%E8%A3%85docker)

将OA整个项目放在服务器的/opt目录下

执行部署命令（全部粘贴复制执行即可）：
```
tee ./deploy.sh <<-'EOF'
#!/bin/bash
docker volume create pg_data
docker network create oa_net
docker build -f /opt/OA/doc/deploy/pg.Dockerfile -t pg:oa /opt
docker run -itd --network=oa_net --network-alias pg_server -p 5432:5432 -v pg_data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=postgres --name pg pg:oa
sleep 3
docker exec -it pg sh /pg.start.sh
docker pull redis:6.0
docker run -itd --network=oa_net --network-alias redis_server --name redis  redis:6.0 --requirepass "redis"
docker build -f /opt/OA/doc/deploy/oa.Dockerfile -t oa:oa /opt
docker run -itd --network=oa_net --network-alias oa_server -p 80:80 --name oa oa:oa 
/bin/bash
EOF
sh ./deploy.sh
```

pg开放5432是为了外部连接，如果不需要，去掉 -p 5432:5432 参数即可

验证：打开浏览器输入服务器ip/test(例：10.255.175.224/test)，返回"{"status": "ok", "data": {"pg": true, "redis": true}}"则表示成功

+ [接口文档](doc/接口文档/home.md)
