#!/usr/bin/env python
# coding=utf-8

import os

cur_dirname = os.path.dirname(os.path.abspath(__file__))


class CrawlRuntimeException(Exception):
    pass


class Config:
    """
    Default configuration , Can be effetively changed by env variables.
    DEMO:
        export DEBUG=FALSE
        export MYSQL_HOST=192.168.1.1
    """
    debug = True

    # mysql配置
    mysql_host = "127.0.0.1"
    mysql_port = 3306
    mysql_usr = "root"
    mysql_pass = "Qzhang450000"
    mysql_db = "vcrawl"

    # email配置
    mail_user = "superchaosos@163.com"
    mail_password = "FGTLHOGZHCDGNHTU"
    mail_host = "smtp.163.com"
    mail_port = 465

    data_dir = os.path.join(cur_dirname, "../data")
    log_dir = os.path.join(cur_dirname, "../logs")
    img_dir = os.path.join(data_dir, "image")


def get_root_path():
        # 获取文件目录
   curPath = os.path.abspath(os.path.dirname(__file__))
   # 获取项目根路径，内容为当前项目的名字
   rootPath = curPath[:curPath.find("vcrawl/") + len("vcrawl/")]
   # logger.info("crawler root path: "+rootPath)
   return rootPath


scanner_headers = {
        'Content-Type': 'application/json',
        'scantoken': 'MTY5NjA1NjI0MjUzODExMDk3N3wwMjA0ZTc3MjZlODY0ZWY5YjI5MzVjYjc1NTNkOGFhNXxlZDliZmFjMGQzNGVjNWY3MWM5NmIzYzFhZGY1MDY4YWQ5ZGFlMzc4ZmNhOWU5MzY3OGFhZDQ5Mzk5MjUyMzVl',
        'tenantid':'zhnormal'
}


scanner_image_headers = {

        'scantoken': 'MTY5NjA1NjI0MjUzODExMDk3N3wwMjA0ZTc3MjZlODY0ZWY5YjI5MzVjYjc1NTNkOGFhNXxlZDliZmFjMGQzNGVjNWY3MWM5NmIzYzFhZGY1MDY4YWQ5ZGFlMzc4ZmNhOWU5MzY3OGFhZDQ5Mzk5MjUyMzVl',
        'tenantid':'zhnormal'
}
scanner_tg_image_url = 'http://116.63.10.153:9001/prod-api/openapi/common/file/upload'

scanner_tg_mes_url = 'http://116.63.10.153:9001/prod-api/openapi/leak/sendKafka/tg'


if __name__ == "__main__":
    from pprint import pprint

    get_root_path()
    pprint(Config.__dict__)
