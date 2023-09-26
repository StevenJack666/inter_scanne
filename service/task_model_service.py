#!/usr/bin/env python
# coding=utf-8


import pandas as pd
from tools.send_email import send_mail
from tools.log import *
from mapper.monitor_task_dao import MonitorTaskDao

class MonitorTaskService:

    '''
    获取任务列表，对任务结果排序输出
    '''
    def match_monitor_task_info(self):
        match_all_infos = MonitorTaskDao.list_monitor_task_info()
        if len(match_all_infos) == 0:
            logger.error(f"没有监控任务信息")
            return

        for bean in match_all_infos:
            id = bean['id']
            task_id = bean['task_id']
            tenant_id = bean['tenant_id']
            Mon_Tp_Nm = bean['Mon_Tp_Nm']
            T_FIELD = bean['T_FIELD']
            Acq_Tsk_StTm = bean['Acq_Tsk_StTm']
            Tsk_EdTm_Pnt = bean['Tsk_EdTm_Pnt']
            Exec_Frq = bean['Exec_Frq']
            CRONTAB_EXP_INF = bean['CRONTAB_EXP_INF']
            Upload_File_Rte = bean['Upload_File_Rte']
            fileContent = bean['fileContent']
            Ctg_Rule_DSC = bean['Ctg_Rule_DSC']
            DEL_ST = bean['DEL_ST']
            CREATE_TIME = bean['CREATE_TIME']
            UPDATE_TIME = bean['UPDATE_TIME']
            print('')


    '''
    获取任务
    '''
    def monitor_task_detail_id(self, task_id):
        task_detail = MonitorTaskDao.monitor_task_detail_id(task_id)
        if task_detail == None:
            logger.error(f"没有监控任务信息")
            return
        return task_detail








if __name__ == "__main__":
    match_all_infos = MonitorTaskDao.list_monitor_task_info()
    logger.error(match_all_infos)

