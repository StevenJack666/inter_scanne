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


if __name__ == "__main__":
    from pprint import pprint

    pprint(Config.__dict__)
