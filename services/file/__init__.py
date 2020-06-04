# -*- coding: UTF-8 -*-

from services import BaseProducer
from services.permission import Permission


class FileProducer(BaseProducer):

    @Permission('file')
    def do(self, **kwargs):
        return super().do(**kwargs)
