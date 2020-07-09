# -*- coding: UTF-8 -*-
from flask import Blueprint

from services.auth.auth import *

auth_app = Blueprint('auth', __name__, url_prefix='/auth')


@auth_app.route('/register', methods=['POST'])
def auth_register():
    """注册账号"""
    return AuthRegister().do()


@auth_app.route('/login', methods=['POST'])
def auth_login():
    """账号登陆"""
    return AuthLogin().do()


@auth_app.route('/logout', methods=['DELETE'])
def auth_logout():
    """账号登出"""
    return AuthLogout().do()


@auth_app.route('/info', methods=['GET'])
def auth_info():
    """获取账户信息"""
    return AuthInfo().do()
