# -*- coding: UTF-8 -*-
import logging

import redis
from psycopg2.pool import SimpleConnectionPool

from config import PG, REDIS

logger = logging.getLogger(__name__)


class DBPool(object):
    """pg数据库连接池"""

    def __init__(self):
        # pg数据库连接池
        logger.debug(">>>>>>pg_pool start create")
        self.pg_pool = SimpleConnectionPool(
            2,
            5,
            host=PG.host,
            port=PG.port,
            database=PG.name,
            user=PG.user,
            password=PG.pwd
        )
        logger.debug(">>>>>>pg_pool create success")

        # redis连接池
        logger.debug(">>>>>>redis_pool start create")
        self.redis_pool = redis.ConnectionPool(
            host=REDIS.host,
            port=REDIS.port,
            password=REDIS.pwd
        )
        logger.debug(">>>>>>redis_pool create success")

    def __del__(self):
        self.pg_pool.closeall()
        self.redis_pool.disconnect()
        del self.pg_pool
        del self.redis_pool
        self.pg_pool = None
        self.redis_pool = None
