# -*- coding: UTF-8 -*-
import hashlib
from services import BaseProducer


class AuthProducer(BaseProducer):

    @staticmethod
    def get_md5(pwd):
        return hashlib.md5(pwd.encode('utf-8')).hexdigest()

