#!/usr/bin/env python
# coding=utf-8


from tools.log import *
from mapper.model.darknet_conf_model import DarknetConf

class DarknetConfDao:

    '''
    获取爬取任务列表列表
    '''
    @staticmethod
    @error_log()
    def list_darknet_conf(type):

        logger.info(f"send_status is {type} ")
        crawl_infos = DarknetConf.select().where(
            DarknetConf.TpCd == type
        )
        return list(crawl_infos.dicts())




