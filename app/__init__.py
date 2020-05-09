# -*- coding: UTF-8 -*-
from flask import Blueprint
from services import Producer

main_app = Blueprint('main', __name__)


@main_app.route('/test', methods=['GET'])
def test():
    """测试"""
    return Producer().do()
