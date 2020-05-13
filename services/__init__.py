# -*- coding: UTF-8 -*-
import hashlib
import json
import logging
from datetime import date
from datetime import datetime

import redis
from flask import current_app, request
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)


class DateEncoder(json.JSONEncoder):
    """解决json不能序列化时间问题"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


class PGProducer(object):
    """PG数据库业务基类"""
    def __init__(self):
        self._commit = False
        self._conn = None
        self._cursor = None
        self._dict_cursor = RealDictCursor

    def set_dict_cursor(self, dict_cursor=None):
        """设置cursor_factory类型，必须在第一次调用execute前设置"""
        self._dict_cursor = dict_cursor

    def execute(self, sql, sql_dict=(), show_sql=False):
        """执行sql语句，打印日志，设置提交标识，返回数据，数据库连接会在第一次使用时建立"""
        if not self._conn:
            logger.debug(">>>>>>PostgreSQL get conn ")
            self._conn = current_app.pool.pg_pool.getconn()
            if self._dict_cursor:
                self._cursor = self._conn.cursor(cursor_factory=self._dict_cursor)
            else:
                self._cursor = self._conn.cursor()
        self._cursor.execute(sql, sql_dict)
        if show_sql:
            logger.debug(">>>>>>sql>>>>>>: %s" % (self._cursor.mogrify(sql, sql_dict)))
        if ('update ' in sql) or ('insert ' in sql) or ('delete ' in sql):
            self._commit = True
        try:
            return self._cursor.fetchall()
        except Exception as e:
            pass

    def _pg_rollback(self):
        """数据库回滚"""
        if self._commit:
            logger.exception(">>>>>>PostgreSQL rollback")
            self._conn.rollback()
            self._commit = False

    def _pg_commit(self):
        """数据库提交"""
        if self._commit:
            logger.debug(">>>>>>PostgreSQL commit ")
            self._conn.commit()
            self._commit = False

    def __del__(self):
        if self._cursor:
            self._cursor.close()
            self._cursor = None
        if self._conn:
            logger.debug(">>>>>>PostgreSQL close")
            current_app.pool.pg_pool.putconn(self._conn)
            self._pg = None


class RedisProducer(object):
    """redis业务基类"""
    def __init__(self):
        self._redis = dict()

    def get_redis(self, db) -> redis.Redis:
        if db not in self._redis:
            logger.debug(">>>>>>Redis get conn: " + "db=" + str(db))
            self._redis[db] = redis.Redis(connection_pool=current_app.pool.redis_pool, db=db)
        return self._redis[db]

    def __del__(self):
        if self._redis.values():
            logger.debug(">>>>>>Redis close")
            for r in self._redis.values():
                current_app.pool.redis_pool.release(r)


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
