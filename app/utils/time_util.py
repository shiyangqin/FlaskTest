# -*- coding: UTF-8 -*-
import time
import datetime


class TimeUtil(object):
    """时间相关操作工具类"""

    @staticmethod
    def get_time(t_type=0):
        """
        获取时间戳
        :param t_type:
            0：保留小数位
            1：不保留小数位
        :return:
            0：float,例：1589445857.0671408
            1：int,例：1589445870
        """
        res = time.time()
        if t_type == 0:
            return res
        elif t_type == 1:
            return int(res)
        else:
            return None

    @staticmethod
    def get_date(d_type=0):
        """
        获取当前时间
        :param d_type:
            0:原生格式
            1:转字符串，格式：yyyy-mm-dd hh:mm:ss
        :return:
            0：datatime,例：2020-05-14 16:46:50.111089
            1：str,例：2020-05-14 16:47:59
        """
        res = datetime.datetime.now()
        if d_type == 0:
            return res
        elif d_type == 1:
            return '%04d-%02d-%02d %02d:%02d:%02d' % (res.year, res.month, res.day, res.hour, res.minute, res.second)
        else:
            return None
