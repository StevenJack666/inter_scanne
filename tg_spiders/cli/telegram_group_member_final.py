# -*- coding: utf-8 -*-
# @Time     : 2022/11/16 15:24:41
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : telegram_run_spider.py
# @Software : Visual Studio Code
# @WeChat   : NextB


__doc__ = """
获取联系人信息
"""

from tg_spiders.common.telegramAPIs import *

scrapy_cfg = """# Automatically created by: scrapy startproject
#
# For more information about the [deploy] section see:
# https://scrapyd.readthedocs.io/en/latest/deploy.html

[settings]
default = NextBSpiders.settings
"""
from tg_spiders.cli.telegram_base import *


class TelegramGroupMemberFinal(TelegramBase):

    def __init__(self, jobconf, app_conf):
        super(TelegramGroupMemberFinal, self).__init__(jobconf, app_conf)

    def telegram_group_member_final(self):
        self.login_in()

        dialog_list = self.ta.get_dialog_list()
        # 遍历当前用户的群组，并爬取每个群组的消息
        for item in dialog_list['data']:
            try:
                members = self.ta.query_chat_member(item['id'], 100)
                self.print_res(members)
            except:
                pass
        # 获取当前用户的所有群组，并进行遍历
        self.ta.close_client()

    def print_res(self, json_res):
        if json_res['result'] == 'success':
            data = json_res['data']
            for item in data:
                if data is None:
                    print("获取群组用户数据失败")
                    continue
                user_id = item.get("user_id", "")
                user_first_name = item.get("user_first_name", "")
                user_last_name = item.get("user_last_name", "")
                user_name = item.get("user_name", "")
                user_phone = item.get("user_phone", "")

                print(
                    "{},{},{},{},{}".format(
                        user_id,
                        user_first_name,
                        user_last_name,
                        user_name,
                        user_phone
                    )
                )

    def run(self, *args, **kwargs):
        """
        CLI命令行入口
        """
        self.telegram_group_member_final()


if __name__ == "__main__":
    te = TelegramGroupMemberFinal('../../conf/tg_config.json')
    te.run()
