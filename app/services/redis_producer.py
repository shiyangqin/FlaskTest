# -*- coding: UTF-8 -*-
import logging

import redis
from flask import current_app

logger = logging.getLogger(__name__)


class RedisProducer(object):
    """redis业务基类"""

    def __init__(self):
        self._redis = dict()

    def get_redis(self, db) -> redis.Redis:
        """获取redis连接
        :param db: db数
        :return:redis.Redis对象
        """
        if db not in self._redis:
            logger.debug(">>>>>>Redis get conn: " + "db=" + str(db))
            self._redis[db] = redis.Redis(connection_pool=current_app.pool.redis_pool, db=db)
        return self._redis[db]

    def __del__(self):
        if self._redis.values():
            logger.debug(">>>>>>Redis close")
            for r in self._redis.values():
                current_app.pool.redis_pool.release(r)
