# -*- coding: UTF-8 -*-
import platform
import configparser
import os


def load_config(path):
    """
    加载配置文件
    :param path: 指定配置文件路径
    :return: dict, 详细配置
    """
    cf = configparser.ConfigParser()
    # if "Linux" == platform.system(): # 这里可以指定从linux下的指定文件读取配置，可以实现配置文件与项目分离
    #     path = 'opt/sap.ini'
    cf.read(path)
    sets = cf.sections()
    config = {}
    for key in sets:
        config[key] = {}
        for val in cf.items(key):
            config[key][val[0]] = val[1]
    return config


# 获取sap.ini所在路径（当前文件所在路径）
filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sap.ini')
conf = load_config(filepath)

session_save_time = 60 * 60


class LOG(object):
    """日志配置"""
    file_name = conf.get('LOG').get('file_name')
    level = conf.get('LOG').get('level')


class PG(object):
    """PG数据库配置"""
    host = conf.get('PG').get('host')
    port = conf.get('PG').get('port')
    user = conf.get('PG').get('user')
    pwd = conf.get('PG').get('pwd')
    name = conf.get('PG').get('name')


class REDIS(object):
    """REDIS配置"""
    host = conf.get('REDIS').get('host')
    port = conf.get('REDIS').get('port')
    pwd = conf.get('REDIS').get('pwd')
    session = 0  # 存session

