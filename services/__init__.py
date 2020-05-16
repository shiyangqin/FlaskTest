# -*- coding: UTF-8 -*-
import hashlib
import json
import logging

from flask import request

from services.date_encoder import DateEncoder
from services.pg_producer import PGProducer
from services.redis_producer import RedisProducer

logger = logging.getLogger(__name__)


class BaseProducer(PGProducer, RedisProducer):
    """
    逻辑处理基类：
        do：统一进行异常处理和数据库的连接、提交、异常回滚、关闭等操作，调用process逻辑处理函数
        process：只负责逻辑处理，创建子类重写，数据库通过self.get_pg()获取
        _process_type：process函数返回值类别
                        0-默认值，将process返回的msg作为json处理，用于大部分业务
                        1-将process返回的msg直接返回给前端，用于下载等业务
    """

    def __init__(self):
        PGProducer.__init__(self)
        RedisProducer.__init__(self)
        self._process_type = 0

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
            self._pg_commit()
            return result_msg
        except Exception as e:
            # 异常处理逻辑
            self._pg_rollback()
            logger.exception(e)
            result_msg['status'] = "数据异常！"
            result_msg['error'] = str(e)
            return json.dumps(result_msg)

    def __del__(self):
        PGProducer.__del__(self)
        RedisProducer.__del__(self)

    def process(self, **kwargs):
        """业务代码逻辑部分,在子类中重写process来处理业务"""
        res = {
            "pg": False,
            "redis": False
        }
        try:
            self.execute("select * from sys_login")
            res['pg'] = True
        except Exception as e:
            pass

        try:
            redis_coon = self.get_redis(0)
            redis_coon.append('test', '0')
            redis_coon.delete('test')
            res['redis'] = True
        except Exception as e:
            pass

        return res

    @staticmethod
    def get_md5(pwd):
        return hashlib.md5(pwd.encode('utf-8')).hexdigest()
