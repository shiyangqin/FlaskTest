# -*- encoding:utf-8 -*-
import copy
import functools

from flask import session


class Permission(object):
    """类函数权限验证装饰器"""

    def __init__(self, function='', fail_msg='{"status": "not allow"}', invalid_msg='{"status": "time out"}'):
        self.function = function
        self.failMsg = fail_msg
        self.invalid_msg = invalid_msg

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not self.function:
                # 当权限为空时，无需验证，直接返回
                if 'user_info' in session:
                    kwargs['user_info'] = copy.copy(session['user_info'])
                return func(*args, **kwargs)
            else:
                # 当权限不为空时
                if 'user_info' not in session:
                    # 没有账号信息则代表未登录或session已过期，返回time out
                    return self.invalid_msg
                if self.function in session['user_info']['function']:
                    try:
                        kwargs['user_info'] = copy.copy(session['user_info'])
                        return func(*args, **kwargs)
                    except Exception as e:
                        raise e
                else:
                    # 权限验证失败，返回not allow
                    return self.failMsg
        return wrapper
