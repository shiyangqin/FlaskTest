# -*- coding: UTF-8 -*-
from flask import request, session

from services import BaseProducer
from utils.time_util import TimeUtil
from . import AuthProducer


class AuthRegister(BaseProducer):
    def process(self, **kwargs):
        param = request.get_json()

        # 查询账号是否已存在
        sql = "select * from sys_user where user_name=%(user_name)s and state='1'"
        if self.get_pg().execute(sql, param):
            return {
                "flag": False,
                "msg": "账户已存在"
            }

        param['user_password'] = self.get_new_id(param['user_password'])

        # 添加账号信息
        sql = """
            insert into sys_user(
                user_name,
                user_password,
                repeat,
                state
            ) values(
                %(user_name)s,
                %(user_password)s,
                0,
                '1'
            ) returning user_id
        """
        param['user_id'] = self.get_pg().execute(sql, param)[0]['user_id']

        # 添加用户角色,第一个用户为超级管理员
        if param['user_id'] == 1:
            sql = "insert into sys_user_role(user_id, role_id) values(%(user_id)s, '1')"
        else:
            sql = "insert into sys_user_role(user_id, role_id) values(%(user_id)s, '3')"
        self.get_pg().execute(sql, param)

        # 添加用户信息
        param['birthday'] = param['birthday'] or None
        param['phone'] = param['phone'] or None
        sql = """
            insert into sys_person(
                user_id,
                name,
                sex,
                birthday,
                email,
                phone,
                remark
            ) values(
                %(user_id)s,
                %(name)s,
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


class AuthLogin(BaseProducer):
    def process(self, **kwargs):
        param = request.get_json()

        # 查询账号是否已存在
        sql = "select * from sys_user where user_name=%(user_name)s and state='1'"
        if not self.get_pg().execute(sql, param):
            return {
                "flag": False,
                "msg": "账户不存在"
            }

        # 验证账号密码
        param['user_password'] = self.get_new_id(param['user_password'])
        sql = """
            select 
                user_id 
            from 
                sys_user 
            where 
                user_name=%(user_name)s 
            and user_password=%(user_password)s 
            and state='1'
        """
        user_id = self.get_pg().execute(sql, param)
        if not user_id:
            sql = """
                update sys_user set
                    repeat=(select repeat from sys_user where user_name=%(user_name)s and state='1') + 1	
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
        user_id = user_id[0]['user_id']
        sql = "update sys_user set repeat='0',login_time=%(time)s where user_id=%(user_id)s"
        self.get_pg().execute(sql, {"user_id": user_id, "time": TimeUtil.get_date()})

        # 获取用户信息
        sql = """
            select 
                a.user_id,
                a.user_name,
                a.login_time,
                b.name,
                b.sex,
                b.birthday,
                b.email,
                b.phone,
                b.remark,
                d.role_name
            from 
                sys_user as a
                inner join sys_person as b on a.user_id=b.user_id and a.user_id=%(user_id)s
                inner join sys_user_role as c on a.user_id=c.user_id
                inner join sys_role as d on c.role_id=d.role_id
        """
        user_info = self.get_pg().execute(sql, {"user_id": user_id})[0]
        sql = """
            select 
                c.function_name 
            from 
                sys_user_role as a 
                inner join sys_role_function as b on a.role_id=b.role_id and a.user_id=%(user_id)s
                inner join sys_function as c on b.function_id=c.function_id
        """
        user_info['function'] = [f['function_name'] for f in self.get_pg().execute(sql, {"user_id": user_id})]

        # 设置session
        user_info['session'] = session.sid
        session['user_info'] = user_info
        return user_info


class AuthLogout(AuthProducer):
    def process(self, **kwargs):
        del session['user_info']
        self.set_process_type(1)
        return '{"status": "time out"}'


class AuthInfo(AuthProducer):
    def process(self, **kwargs):
        user_info = kwargs['user_info']
        del user_info['function'], user_info['session']
        return user_info
