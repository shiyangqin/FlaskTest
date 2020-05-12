# -*- coding: UTF-8 -*-
from utils.permission import Permission
from services import BaseProducer


class AuthProducer(BaseProducer):

    @Permission('auth')
    def do(self, **kwargs):
        return super().do(**kwargs)

