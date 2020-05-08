# -*- coding: UTF-8 -*-
import logging

from . import main_app as app

logger = logging.getLogger(__name__)


@app.route('/test', methods=['GET'])
def test():
    """测试"""
    return "this is test"
