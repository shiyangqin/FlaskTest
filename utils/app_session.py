# -*- encoding:utf-8 -*-
import pickle
import random
import uuid

import redis
from flask.sessions import SessionMixin, SessionInterface
from werkzeug.datastructures import CallbackDict

from config import REDIS, session_save_time


def _get_new_sid():
    return uuid.uuid5(uuid.uuid4(), str(random.random)).hex


class SessionObj(CallbackDict, SessionMixin):
    def __init__(self, initial=None, sid=None):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.modified = False


class RedisSessionInterface(SessionInterface):
    serializer = pickle
    session_class = SessionObj

    def __init__(self, connection_pool):
        self.conn = redis.Redis(connection_pool=connection_pool, db=REDIS.session)

    def open_session(self, app, request):
        """获取Session"""
        session_id = request.cookies.get(app.session_cookie_name)
        if not session_id:
            return self.session_class(sid=_get_new_sid())
        session_data = self.conn.get(session_id)
        if session_data is None:
            return self.session_class(sid=_get_new_sid())
        session_data = self.serializer.loads(session_data)
        return self.session_class(session_data, sid=session_id)

    def save_session(self, app, session, response):
        """保存Session"""
        if not session:
            self.conn.delete(session.sid)
            if session.modified:
                response.delete_cookie(app.session_cookie_name)
            return
        session_data = self.serializer.dumps(dict(session))
        self.conn.setex(session.sid, session_save_time, session_data)
        response.set_cookie(
            app.session_cookie_name,
            session.sid,
            # expires=self.get_expiration_time(app, session),     # session过期时间
            # path=self.get_cookie_path(app),                     # 路径
            # domain=self.get_cookie_domain(app),                 # 域名
            # secure=self.get_cookie_secure(app)                  # secure属性
            # httponly=self.get_cookie_httponly(app),             # httponly属性
        )
