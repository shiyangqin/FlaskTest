# -*- coding: utf-8 -*-

import logging

from logging.handlers import RotatingFileHandler

import os

LEVELS = {
    'NOSET': logging.NOTSET,
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}


def logging_config(file_name="log.log", log_level="NOSET"):
    """日志配置
    :param file_name:日志文件名，默认在同级目录logs下
    :param log_level:日志等级
    :return:None
    """
    # 创建文件夹
    logs_dir = os.path.join(os.path.dirname(__file__), "logs")
    if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
        pass
    else:
        os.makedirs(logs_dir)
    file_name = os.path.join(logs_dir, file_name)

    logging.getLogger("").handlers = []

    # 设置RotatingFileHandler
    rotating_file_handler = RotatingFileHandler(filename=file_name, maxBytes=1024 * 1024 * 50, backupCount=3)
    formatter = logging.Formatter("%(asctime)s %(name)s %(process)d %(levelname)s %(lineno)s %(message)s")
    rotating_file_handler.setFormatter(formatter)
    logging.getLogger("").addHandler(rotating_file_handler)

    # 设置StreamHandler
    console = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(name)s %(process)d %(levelname)s %(lineno)s %(message)s")
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)

    # 设置日志打印级别
    logger = logging.getLogger("")
    level = LEVELS[log_level.upper()]
    logger.setLevel(level)
