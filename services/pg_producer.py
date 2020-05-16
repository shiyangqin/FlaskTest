# -*- coding: UTF-8 -*-
import logging

from flask import current_app
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)


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
        """
        执行sql语句，数据库连接会在第一次使用时建立
        :param sql:sql语句
        :param sql_dict:sql参数,格式：dict
        :param show_sql:是否打印sql日志
        :return:sql查询结果
        """
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

    def _pg_commit(self):
        """pg数据库提交"""
        if self._commit:
            logger.debug(">>>>>>PostgreSQL commit ")
            self._conn.commit()
            self._commit = False

    def _pg_rollback(self):
        """pg数据库回滚"""
        if self._commit:
            logger.exception(">>>>>>PostgreSQL rollback")
            self._conn.rollback()
            self._commit = False

    def __del__(self):
        if self._cursor:
            self._cursor.close()
            self._cursor = None
        if self._conn:
            logger.debug(">>>>>>PostgreSQL close")
            current_app.pool.pg_pool.putconn(self._conn)
            self._pg = None
