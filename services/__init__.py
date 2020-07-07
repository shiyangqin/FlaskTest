# -*- coding: UTF-8 -*-
import hashlib
import json
import logging

import redis
from flask import request

from services.date_encoder import DateEncoder
from services.pg_producer import PGProducer
from services.redis_producer import RedisProducer

logger = logging.getLogger(__name__)


class BaseProducer(object):
    """
    逻辑处理基类

    子类继承并重写process函数实现业务开发
    权限验证通过在子类中使用Permission装饰器设置

    process_type: 0-默认值，将process返回的msg作为json处理，用于大部分业务
                  1-将process返回的msg直接返回给前端，用于下载等业务
    """

    def __init__(self):
        self._process_type = 0
        self._pg = None
        self._redis = None

    def get_pg(self) -> PGProducer:
        if not self._pg:
            self._pg = PGProducer()
        return self._pg

    def get_redis(self, db) -> redis.Redis:
        if not self._redis:
            self._redis = RedisProducer()
        return self._redis.get_redis(db)

    def set_process_type(self, process_type=1):
        """设置返回值类型"""
        self._process_type = process_type

    def do(self, **kwargs):
        """业务代码公共部分"""
        result_msg = {}
        try:
            logger.debug("==================  " + self.__class__.__name__ + "  ==================")
            # 业务处理逻辑
            kwargs['request'] = request
            msg = self.process(**kwargs)

            # 处理返回值
            if self._process_type == 0:
                result_msg['status'] = 'ok'
                result_msg['data'] = msg
                result_msg = json.dumps(result_msg, cls=DateEncoder).replace(': null', ': \"\"')
            if self._process_type == 1:
                result_msg = msg
            if self._pg:
                self._pg.commit()
            return result_msg
        except Exception as e:
            # 异常处理逻辑
            if self._pg:
                self._pg.rollback()
            logger.exception(e)
            result_msg['status'] = "数据异常！"
            result_msg['error'] = str(e)
            return json.dumps(result_msg)
        finally:
            if self._pg:
                del self._pg
                self._pg = None
            if self._redis:
                del self._redis
                self._redis = None

    def process(self, **kwargs):
        """业务代码逻辑部分,在子类中重写process来处理业务"""
        res = {
            "pg": False,
            "redis": False
        }
        try:
            self.get_pg().execute("select * from sys_user")
            res['pg'] = True
        except Exception as e:
            pass

        try:
            self.get_redis(0).append('test', '0')
            self.get_redis(0).delete('test')
            res['redis'] = True
        except Exception as e:
            pass

        return res

    @staticmethod
    def get_new_id(pwd):
        return hashlib.md5(pwd.encode('utf-8')).hexdigest()

    @staticmethod
    def get_file_md5(file):
        """获取文件md5"""
        my_hash = hashlib.md5()
        while True:
            b = file.read(4096)
            if not b:
                break
            my_hash.update(b)
        return my_hash.hexdigest()
