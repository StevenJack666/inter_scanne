# -*- coding: utf-8 -*-
# @Time     : 2022/11/19 20:01:59
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : telegram_get_user_photo.py
# @Software : Visual Studio Code
# @WeChat   : NextB


__doc__ = """
获取telegram用户的头像
"""

import json
import argparse
from tg_spiders.common.telegramAPIs import *
cur_dirname = os.path.dirname(os.path.abspath(__file__))
from tg_spiders.cli.telegram_base import *

class TelegramGetUserPhoto(TelegramBase):



    def __init__(self, jobconf, app_conf):
        super(TelegramGetUserPhoto, self).__init__(jobconf, app_conf)

    def telegram_get_user_photo(self):

        # 获取群组聊天消息
        self.login_in()
        # 获取当前用户的所有群组，并进行遍历
        # list_dialog = self.ta.get_dialog_list()
        for item_g in self.group:
            group_id = item_g['group_id']
            limit = item_g['limit']
            last_message_id = item_g['last_message_id']
            offset_date = item_g['offset_date']

            param = {
                "limit": limit,
                "offset_date": offset_date,
                "last_message_id": last_message_id,  # -1表示从第一条开始
            }
            # 爬取群组消息
            chat_dialog = self.ta.get_dialog_chat(group_id)
            message_res = self.ta.scan_message(chat_dialog, **param)
            # 根据昵称，获取群组所有用户的头像
            nicknames = []
            for item_data in message_res['data']:
                nicknames.append(item_data['nick_name'])
            nicknames_tmp = list(set(nicknames))
            # 根据群组ID和用户昵称 ，下载所有用户的头像,输出到指定目录
            self.ta.download_user_photo(group_id, nicknames_tmp, './')
        self.ta.close_client()


    def run(self, *args, **kwargs):
        """
        CLI命令行入口
        """
        self.telegram_get_user_photo()


if __name__ == "__main__":
    te = TelegramGetUserPhoto('../../conf/tg_config.json')
    te.run()
