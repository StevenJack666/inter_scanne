#!/usr/bin/env python
# coding=utf-8


from tools.log import *
from mapper.model.tg_group_model import TgGroupModel
import datetime

class TgChannelGroupDao:



    '''
    插入频道信息
    '''

    @error_log()
    def insert_channel_group_info(self, item):
        channel_group_tmp = TgGroupModel.select(TgGroupModel.channel_id).where(
            TgGroupModel.channel_id == item.get("channel_id")).count()

        if channel_group_tmp == 0:
            now = datetime.datetime.now()
            item["create_time"] = now
            item["update_time"] = now
            item["tenant_id"] = 'zhnormal'
            return TgGroupModel.create(**item)
        else:
            self.update_channel_group(item)




    # 根据频道id，更新数据
    @error_log()
    def update_channel_group(self, channel_group):
        now = datetime.datetime.now()
        q = TgGroupModel.update(offset_date=channel_group.get("offset_date"), last_message_id=channel_group.get("last_message_id"),
                                update_time=now).where(TgGroupModel.channel_id == channel_group.get("channel_id"))
        q.execute()





    '''
    通过频道id获取频道详情
    '''

    @error_log()
    def channel_group_detail_id(self, user_name):
        logger.info(f"channel_id is {user_name} ")

        try:
            return TgGroupModel.get(TgGroupModel.username == user_name)
        except Exception as e:
            logger.info(f"query channel_group_detail error {e} ")
            return None




