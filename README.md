# OA
python个人练手OA后端服务

+ 部署

将OA整个项目放在服务器的/opt目录下，且以下命令在/opt目录下执行

[安装docker](https://github.com/shiyangqin/doc/blob/master/Linux/docker.md#centos7%E5%AE%89%E8%A3%85docker)

创建pg数据卷：
```
docker volume create pg_data
```

创建oa网络:
```
docker network create -d bridge oa-net
```

构建pg镜像：
```
docker build -f /opt/OA/doc/deploy/pg.Dockerfile -t pg:test .
```

构建oa镜像：
```
docker build -f /opt/OA/doc/deploy/oa.Dockerfile -t oa:test .
```

启动pg容器：
```
docker run -itd --network=oa-net --network-alias pg_server -p 5432:5432 -v pg_data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=postgres --name pg pg:test
```

初始化pg数据库：
```
docker exec -it pg sh /pg.start.sh
```

这里先启动容器再初始化pg数据库是因为使用dockerfile构建容器时，使用psql命令失败，使用启动容器时初始化会覆盖原有的启动服务命令，我个人尝试失败了，所以做了妥协，理想状态应该是使用dockerfile构建镜像，启动后自动初始化

启动oa容器：
```
docker run -itd --network=oa-net --network-alias oa_server -p 80:80 --name oa oa:test /oa.start.sh
```
