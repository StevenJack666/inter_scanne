#!/usr/bin/env python
# coding=utf-8


from tools.log import *
from mapper.model.task_model import MonitorTask

class MonitorTaskDao:

    '''
    获取任务列表
    '''
    @staticmethod
    @error_log()
    def list_monitor_task_info( send_status=False):

        logger.info(f"send_status is {send_status} ")
        crawl_infos = MonitorTask.select().where(
            MonitorTask.send_status == send_status
        )
        return list(crawl_infos.dicts())


    '''
    通过任务id获取任务详情
    '''
    @staticmethod
    @error_log()
    def monitor_task_detail_id(task_id):
        logger.info(f"task_id is {task_id} ")
        try:
            return MonitorTask.get(MonitorTask.id == task_id)
        except Exception as e:
            logger.info(f"query monitor_task_detail_id error {e} ")
            return None


