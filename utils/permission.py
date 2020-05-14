# -*- encoding:utf-8 -*-
import copy
import functools

from flask import session


class Permission(object):
    """类函数权限验证装饰器"""

    def __init__(self, function, fail_msg='{"status": "not allow"}', invalid_msg='{"status": "time out"}'):
        self.function = function
        self.failMsg = fail_msg
        self.invalid_msg = invalid_msg

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if 'user_info' not in session:
                return self.invalid_msg
            if self.function in session['user_info']['function']:
                try:
                    kwargs['user_info'] = copy.copy(session['user_info'])
                    return func(*args, **kwargs)
                except TypeError as te:
                    raise te
            else:
                return self.failMsg
        return wrapper
