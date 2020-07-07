# -*- coding: UTF-8 -*-
from flask import Blueprint

from services.file.file import *

file_app = Blueprint('file', __name__, url_prefix='/file')


@file_app.route('/upload', methods=['POST'])
def file_upload():
    """文件上传"""
    return FileUpload().do()


@file_app.route('/download/<file_md5>', methods=['GET'])
def file_download(file_md5):
    """文件下载"""
    return FileDownload().do(file_md5=file_md5)
