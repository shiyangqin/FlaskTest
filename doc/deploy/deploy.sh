#!/bin/bash
docker volume create pg_data
docker volume create redis_data
docker network create oa_net
docker build -f /opt/OA/doc/deploy/pg.Dockerfile -t pg:oa /opt
docker run -itd --network=oa_net --network-alias pg_server -p 5432:5432 -v pg_data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=postgres --name pg pg:oa
sleep 3
docker exec -it pg sh /pg.start.sh
docker pull redis:6.0
docker run -itd --network=oa_net --network-alias redis_server -p 6379:6379 -v redis_data:/data --name redis  redis:6.0 --requirepass "redis"
docker build -f /opt/OA/doc/deploy/oa.Dockerfile -t oa:oa /opt
docker run -itd --network=oa_net --network-alias oa_server -p 80:80 --name oa oa:oa