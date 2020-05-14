#!/bin/bash
docker volume create oa_pg_data
docker volume create oa_redis_data
docker network create oa_net
docker build -f /opt/OA/doc/deploy/pg.Dockerfile -t pg:oa /opt
docker run -itd --network=oa_net --network-alias oa_pg_server -p 5432:5432 -v oa_pg_data:/var/lib/postgresql/data --name oa_pg pg:oa
docker pull redis:6.0
docker run -itd --network=oa_net --network-alias oa_redis_server -p 6379:6379 -v oa_redis_data:/data --name oa_redis  redis:6.0 --requirepass "redis"
docker build -f /opt/OA/doc/deploy/oa.Dockerfile -t oa:oa /opt
docker run -itd --network=oa_net --network-alias oa_server -p 80:80 --name oa oa:oa