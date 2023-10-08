#!/usr/bin/env python
# coding=utf-8

import logging
import os
from termcolor import colored
from tools.config import Config
from logging import handlers

cur_dirname = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(cur_dirname, "../logs/info.log")
if not os.path.exists(filename):
    os.makedirs("logs")
fmt = "%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s"

logger = logging.getLogger("vcrawl")
format_str = logging.Formatter(fmt)#设置日志格式
logger.setLevel(logging.INFO)#设置日志级别
sh = logging.StreamHandler()#往屏幕上输出
sh.setFormatter(format_str) #设置屏幕上显示的格式
th = handlers.TimedRotatingFileHandler(filename=filename,when='D',backupCount=7,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
th.setFormatter(format_str)#设置文件里写入的格式
logger.addHandler(sh) #把对象加到logger里
logger.addHandler(th)

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S', filename='logs/info.log', filemode='a')
# Loger = logging.getLogger("vcrawl")

def info(txt):
    logger.info(f"{colored((txt), 'blue')}")
    return txt


def success(txt):
    logger.info(f"{colored((txt), 'green')}")
    return txt


def warning(txt):
    logger.info(f"{colored((txt), 'yellow')}")
    return txt


def error(txt):
    logger.info(f"{colored((txt), 'red')}")
    return txt


def debug(txt):
    if Config.debug:
        logger.info(f"{colored((txt),'cyan')}")
    return txt


def error_log(target="", default=None, raise_err=False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(e)
                if raise_err:
                    raise e
                return default

        return wrapper

    return decorator