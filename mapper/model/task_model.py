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

class MonitorTask(BaseModel):
    id = BigIntegerField(primary_key=True, verbose_name="主键ID")
    task_id = CharField(index=True, max_length=200, verbose_name="任务名称",  default="")
    tenant_id = CharField(index=True, max_length=20, verbose_name="租户ID",  default="")
    Mon_Tp_Nm = CharField(max_length=1, verbose_name="监控类型：1:暗网，2:开源社区，3:在线文档，4:网盘",  default="")
    T_FIELD = CharField(max_length=100, verbose_name="监控目标", default="")
    Acq_Tsk_StTm = DateTimeField( verbose_name="监控周期开始时间")
    Tsk_EdTm_Pnt = DateTimeField(  verbose_name="监控周期结束时间")
    Exec_Frq = BigIntegerField( verbose_name="监控频率：1:每小时，2:每天，3:每月" )
    CRONTAB_EXP_INF = CharField(max_length=80, verbose_name="CRON表达式",  default="")
    Upload_File_Rte = CharField(max_length=80, verbose_name="爬虫关键字文件ID")
    fileContent = CharField(max_length=10000, verbose_name="文件内容")
    Ctg_Rule_DSC = CharField(max_length=2000, verbose_name="规则描述")
    DEL_ST = CharField(max_length=8, verbose_name="是否删除：0:为删除，1:已删除")
    CREATE_TIME = DateTimeField(verbose_name="创建时间")
    UPDATE_TIME = DateTimeField(verbose_name="更新时间")

    class Meta:
        table_name = "tb_monitor_task"
