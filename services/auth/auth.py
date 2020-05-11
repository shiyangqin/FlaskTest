# -*- coding: UTF-8 -*-
from flask import session

from utils.time_util import TimeUtil
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

        param['user_password'] = self.get_md5(param['user_password'])
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
        param['login_id'] = self.get_pg().execute(sql, param)[0]['login_id']

        # 添加用户角色
        sql = "insert into sys_login_role(login_id, role_id) values(%(login_id)s, '3')"
        self.get_pg().execute(sql, param)

        # 添加用户信息
        param['birthday'] = None if not param['birthday'] else param['birthday']
        param['phone'] = None if not param['phone'] else param['phone']
        sql = """
            insert into sys_person(
                login_id,
                person_name,
                sex,
                birthday,
                email,
                phone,
                remark
            ) values(
                %(login_id)s,
                %(person_name)s,
                %(sex)s,
                %(birthday)s,
                %(email)s,
                %(phone)s,
                %(remark)s
            )
        """
        self.get_pg().execute(sql, param)
        return {
            "flag": True,
            "msg": "注册成功"
        }


class AuthLogin(AuthProducer):
    def process(self, **kwargs):
        param = kwargs['request'].get_json()

        # 查询账号是否已存在
        sql = "select * from sys_login where user_name=%(user_name)s and state='1'"
        if not self.get_pg().execute(sql, param):
            return {
                "flag": False,
                "msg": "账户不存在"
            }

        # 验证账号密码
        param['user_password'] = self.get_md5(param['user_password'])
        sql = """
            select 
                login_id 
            from 
                sys_login 
            where 
                user_name=%(user_name)s 
            and user_password=%(user_password)s 
            and state='1'
        """
        login_id = self.get_pg().execute(sql, param)
        if not login_id:
            sql = """
                update sys_login set
                    repeat=(select repeat from sys_login where user_name=%(user_name)s and state='1') + 1	
                where 
                    user_name=%(user_name)s
                and state='1'
                returning repeat
            """
            repeat = self.get_pg().execute(sql, param)[0]['repeat']
            return {
                "flag": False,
                "msg": "密码错误，这是第" + str(repeat) + "次失败！"
            }
        login_id = login_id[0]['login_id']
        sql = "update sys_login set repeat='0',login_time=%(time)s where login_id=%(login_id)s"
        self.get_pg().execute(sql, {"login_id": login_id, "time": TimeUtil.get_date()})

        # 获取用户信息
        sql = """
            select 
                a.login_id,
                a.user_name,
                a.login_time,
                b.person_name,
                b.sex,
                b.birthday,
                b.email,
                b.phone,
                b.remark,
                c.role_id
            from 
                sys_login as a
                inner join sys_person as b on a.login_id=b.login_id and a.login_id=%(login_id)s
                inner join sys_login_role as c on a.login_id=c.login_id
        """
        user_info = self.get_pg().execute(sql, {"login_id": login_id})[0]
        sql = """
            select 
                c.function_name 
            from 
                sys_login_role as a 
                inner join sys_role_function as b on a.role_id=b.role_id and a.login_id=%(login_id)s
                inner join sys_function as c on b.function_id=c.function_id
        """
        user_info['function'] = [f['function_name'] for f in self.get_pg().execute(sql, {"login_id": login_id})]

        # 存储token与用户信息
        user_info['session'] = session.sid
        session['user_info'] = user_info
        return user_info


class AuthInfo(AuthProducer):
    def process(self, **kwargs):

        user_info = session['user_info']