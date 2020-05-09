# -*- coding: UTF-8 -*-
import time
import datetime


class TimeUtil(object):
    """时间相关操作工具类"""

    @staticmethod
    def get_time():
        """获取时间戳，不保留小数点位"""
        return str(int(time.time()))

    @staticmethod
    def get_date():
        """获取当前时间，格式：yyyy-mm-dd hh:mm:ss"""
        now = datetime.datetime.now()
        res = '%04d-%02d-%02d %02d:%02d:%02d' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
        return res
