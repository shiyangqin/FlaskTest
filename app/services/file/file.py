# -*- coding: UTF-8 -*-
import os
from urllib.parse import quote

from flask import make_response, send_from_directory

from . import FileProducer

try:
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'file')
    os.makedirs(file_path)
except:
    pass


class FileDownload(FileProducer):
    def process(self, **kwargs):
        sql = "select file_name from file_info where file_md5=%(file_md5)s"
        file_info = self.get_pg().execute(sql, {"file_md5": kwargs['file_md5']})
        if not file_info:
            raise Exception("文件不存在")
        response = make_response(send_from_directory(file_path, kwargs['file_md5']))
        response.headers["Content-Disposition"] = \
            "attachment; filename={0}; filename*=utf-8''{0}".format(quote(file_info[0]['file_name']))
        self.set_process_type()
        return response


class FileUpload(FileProducer):
    def process(self, **kwargs):
        f = kwargs['request'].files['file']
        sql_dict = {
            "file_name": f.filename,
            "file_md5": self.get_file_md5(f)
        }
        sql_dict['file_path'] = os.path.join(file_path, sql_dict['file_md5'])
        sql = """
            insert into file_info(
                file_md5,
                file_name,
                file_path
            ) values(
                %(file_md5)s,
                %(file_name)s,
                %(file_path)s
            ) on conflict(file_md5) do nothing
            returning xmax
        """
        flag = self.get_pg().execute(sql, sql_dict)
        if flag and flag[0]['xmax'] == "0":
            f.seek(0)
            f.save(sql_dict['file_path'])
        else:
            raise Exception("文件已存在")
        return sql_dict

