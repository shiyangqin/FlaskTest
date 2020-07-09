# -*- coding: UTF-8 -*-

from services import BaseProducer
from services.permission import Permission


class XlsProducer(BaseProducer):

    @Permission('xls')
    def do(self, **kwargs):
        return super().do(**kwargs)
