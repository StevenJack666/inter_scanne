#!/usr/bin/env python
# coding=utf-8


from tools.log import *
from mapper.darknet_conf_dao import DarknetConfDao

class DarkconfService:

    '''
    获取配置信息，对任务结果排序输出
    '''
    def darkconf_list(self, type):
        return DarknetConfDao.list_darknet_conf(type)




