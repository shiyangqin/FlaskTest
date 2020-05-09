# -*- coding: UTF-8 -*-
from flask import Blueprint

from services.auth.auth import *

auth_app = Blueprint('auth', __name__, url_prefix='/auth')


@auth_app.route('/register', methods=['POST'])
def auth_register():
    """注册账号"""
    return AuthRegister().do()
