#!/usr/bin/env python
# coding=utf-8

from peewee import *

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

class TgGroupModel(BaseModel):
    id = BigIntegerField(primary_key=True, verbose_name="主键ID")
    channel_id = CharField(index=True, max_length=20, verbose_name="频道ID",  default="")
    tenant_id = CharField(index=True, max_length=20, verbose_name="租户ID",  default="")
    title = CharField(max_length=64, verbose_name="频道标题", default="")
    username = CharField(max_length=20, verbose_name="频道名称", default="")
    hex_url = CharField(max_length=20, verbose_name="频道地址", default="")
    offset_date = BigIntegerField(verbose_name="爬虫起始时间", default="")

    megagroup = CharField(max_length=20, verbose_name="", default="")
    member_count = IntegerField(verbose_name="群组成员数", default="")
    channel_description = CharField(max_length=64, verbose_name="频道描述", default="")
    last_message_id = IntegerField( verbose_name="最新消息条数", default="")
    is_public = IntegerField(verbose_name="是否公开", default="")
    join_date = DateTimeField(verbose_name="加入时间")

    create_time = DateTimeField(verbose_name="创建时间")
    update_time = DateTimeField(verbose_name="更新时间")

    class Meta:
        table_name = "tg_channel_group"
