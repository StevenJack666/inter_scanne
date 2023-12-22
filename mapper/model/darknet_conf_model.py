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

class DarknetConf(BaseModel):
    Prim_Tbl_PK = BigIntegerField(primary_key=True, verbose_name="主键ID")
    TpCd = CharField(index=True, max_length=1, verbose_name="暗网类型(1暗网2TG)",  default="")
    Links_Adr = CharField(index=True, max_length=2048, verbose_name="链接地址",  default="")
    Nm = CharField(max_length=200, verbose_name="名称",  default="")
    str_name = CharField(max_length=512, verbose_name="子名称", default="")
    tenant_id = CharField(max_length=100,  verbose_name="租户ID")
    TXN_TPCD = CharField(max_length=10, verbose_name="子类型")


    access_path = CharField(max_length=512, verbose_name="机构权限" )
    record_by = CharField(max_length=64, verbose_name="填写人",  default="")
    record_by_org_code = CharField(max_length=64, verbose_name="填写人对应机构代码")
    remark = CharField(max_length=256, verbose_name="备注")
    memo1 = CharField(max_length=256, verbose_name="备用字段1")
    memo2 = CharField(max_length=256, verbose_name="备用字段2")
    memo3 = CharField(max_length=256, verbose_name="备用字段3")
    is_deleted = CharField(max_length=1, verbose_name="是否删除：0:为删除，1:已删除")
    insert_time = DateTimeField(verbose_name="创建时间")
    update_time = DateTimeField(verbose_name="更新时间")

    class Meta:
        table_name = "darknet_conf"
