# -*- coding: UTF-8 -*-
import logging

from flask import current_app
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)


class PGProducer(object):
    """PG数据库业务基类
    commit: 提交标识，默认为false，当执行的sql包含更新数据操作时置为true，提交和回滚时使用，避免多余的提交回滚操作
    conn: pg数据库连接对象
    cursor: cursor对象
    """

    def __init__(self, cursor_factory=RealDictCursor):
        logger.debug(">>>>>>PostgreSQL get conn ")
        self._commit = False
        self._conn = current_app.pool.pg_pool.getconn()
        if cursor_factory:
            self._cursor = self._conn.cursor(cursor_factory=RealDictCursor)
        else:
            self._cursor = self._conn.cursor()

    def execute(self, sql, sql_dict=(), show_sql=False):
        """执行sql语句
        :param sql:sql语句
        :param sql_dict:sql参数,格式：dict
        :param show_sql:是否打印sql日志
        :return:sql返回值
        """
        self._cursor.execute(sql, sql_dict)
        if show_sql:
            logger.debug(">>>>>>sql>>>>>>: %s" % (self._cursor.mogrify(sql, sql_dict)))
        if ('update ' in sql) or ('insert ' in sql) or ('delete ' in sql):
            self._commit = True
        try:
            return self._cursor.fetchall()
        except Exception as e:
            pass

    def commit(self):
        """pg数据库提交"""
        if self._commit:
            logger.debug(">>>>>>PostgreSQL commit ")
            self._conn.commit()
            self._commit = False

    def rollback(self):
        """pg数据库回滚"""
        if self._commit:
            logger.debug(">>>>>>PostgreSQL rollback")
            self._conn.rollback()
            self._commit = False

    def __del__(self):
        if self._cursor:
            self._cursor.close()
            self._cursor = None
        if self._conn:
            logger.debug(">>>>>>PostgreSQL close")
            self._conn.close()
            self._conn = None
