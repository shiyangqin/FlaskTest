# -*- coding: UTF-8 -*-
from flask import session
from . import AuthProducer


class AuthRegister(AuthProducer):
    def process(self, **kwargs):
        param = kwargs['request'].get_json()

        # 查询账号是否已存在
        sql = "select * from sys_login where user_name=%(user_name)s and state='1'"
        if self.get_pg().execute(sql, param):
            return {
                "flag": False,
                "msg": "账户已存在"
            }

        # 添加账号信息
        sql = """
            insert into sys_login(
                user_name,
                user_password,
                repeat,
                state
            ) values(
                %(user_name)s,
                %(user_password)s,
                0,
                '1'
            ) returning login_id
        """
        login_id = self.get_pg().execute(sql, param)[0]['login_id']
        sql = "insert into sys_login_role(login_id, role_id) values(%(login_id)s, '3')"
        self.get_pg().execute(sql, {"login_id": login_id})

        return {
            "flag": True,
            "msg": "注册成功"
        }


class AuthLogin(AuthProducer):
    def process(self, **kwargs):
        param = kwargs['request'].get_json()
        token = session.sid
