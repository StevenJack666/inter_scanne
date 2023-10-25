#!/usr/bin/env python
# coding=utf-8


from tools.log import *
from mapper.tg_channel_group_dao import TgChannelGroupDao
class TgGroupModelService:

    '''
    获取频道信息
    '''
    def channel_group_detail_id(self, user_name):
        tgGroup = TgChannelGroupDao()

        channelGroupDetail = tgGroup.channel_group_detail_id(user_name)
        if channelGroupDetail == None:
            logger.info(f"没有频道数据信息")
            return
        return channelGroupDetail


    '''
    插入/更新频道信息
    '''
    def insert_channel_group(self, item):
        tgGroup = TgChannelGroupDao()
        tgGroup.insert_channel_group_info(item)






if __name__ == "__main__":
    print()

