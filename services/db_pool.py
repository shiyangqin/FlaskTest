# -*- coding: UTF-8 -*-
import logging
import threading

import redis
from psycopg2.pool import ThreadedConnectionPool

from config import PG, REDIS

logger = logging.getLogger(__name__)


class DBPool(object):
    """pg数据库连接池"""

    _instance_lock = threading.Lock()

    def __init__(self):
        # pg数据库连接池
        logger.debug(">>>>>>pg_pool start create")
        self.pg_pool = ThreadedConnectionPool(
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

    def __new__(cls):
        if not hasattr(DBPool, "_instance"):
            with DBPool._instance_lock:
                if not hasattr(DBPool, "_instance"):
                    DBPool._instance = object.__new__(cls)
        return DBPool._instance

    def __del__(self):
        if hasattr(self, "pg_pool") and self.pg_pool:
            self.pg_pool.closeall()
            del self.pg_pool
            self.pg_pool = None
        if hasattr(self, "redis_pool") and self.redis_pool:
            self.redis_pool.disconnect()
            del self.redis_pool
            self.redis_pool = None
