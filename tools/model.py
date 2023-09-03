#!/usr/bin/env python
# coding=utf-8

from peewee import *
from peewee import __exception_wrapper__

from tools.config import Config

db_config = {
    "host": Config.mysql_host,
    "port": Config.mysql_port,
    "user": Config.mysql_usr,
    "password": Config.mysql_pass,
}

db = MySQLDatabase(Config.mysql_db, **db_config)

class BaseModel(Model):
    class Meta:
        database = db

class CrawlInfo(BaseModel):
    id = BigIntegerField(primary_key=True, verbose_name="主键ID")
    docid = CharField(unique=True, max_length=128, verbose_name="文档唯一标识编码")
    title = CharField(index=True, max_length=512, verbose_name="标题",  default="")
    dtype = CharField(index=True, max_length=512, verbose_name="文档类型",  default="")
    href = CharField(max_length=512, verbose_name="文档链接",  default="")
    publisher = CharField(max_length=64, verbose_name="发布者", default="")
    publish_time = CharField(max_length=128, index=True, verbose_name="发布时间")
    send_status = BooleanField(default = False, verbose_name="告警发送状态")
    doc_page_tag = CharField(max_length=32, verbose_name="文档页面标签:xx页xx行", default="")
    description = CharField(max_length=1024, verbose_name="文档描述",  default="")
    create_time = DateTimeField(verbose_name="记录插入时间")
    update_time = DateTimeField(verbose_name="记录更新时间")
    class Meta:
        table_name = "crawl_info"
