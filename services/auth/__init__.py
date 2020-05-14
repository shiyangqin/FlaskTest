# -*- coding: UTF-8 -*-
from services import BaseProducer
from utils.permission import Permission


class AuthProducer(BaseProducer):
    """账户模块基类，不包括注册和登陆"""

    @Permission('auth')
    def do(self, **kwargs):
        return super().do(**kwargs)

