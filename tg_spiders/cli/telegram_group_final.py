# -*- coding: utf-8 -*-
# @Time     : 2022/11/16 15:24:41
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : telegram_run_spider.py
# @Software : Visual Studio Code
# @WeChat   : NextB


__doc__ = """
获取群组信息
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


class TelegramGroupFinal(TelegramBase):
    def __init__(self, jobconf, app_conf):
        super(TelegramGroupFinal, self).__init__(jobconf, app_conf)


    def telegram_group_final(self):
        # 加载配置文件
        self.login_in()
        # 获取当前用户的所有群组，并进行遍历
        list_dialog = self.ta.get_dialog_list()
        self.print_res(list_dialog)
        self.ta.close_client()



    def print_res(self, json_res):
        if json_res['result'] == 'success':
            data = json_res['data']
            for item in data:
                if data is None:
                    print("获取群组数据失败")
                    continue
                id = item.get("id", "")
                title = item.get("title", "")
                username = item.get("username", "")
                hex_url = item.get("hex_url", "")
                megagroup = item.get("megagroup", "")
                member_count = item.get("member_count", "")
                channel_description = item.get("channel_description", "")
                is_public = item.get("is_public", "")
                join_date = item.get("join_date", "")
                unread_count = item.get("unread_count", "")

                print(
                    "{},{},{},{},{},{},{},{},{},{}".format(
                        id,
                        title,
                        username,
                        hex_url,
                        megagroup,
                        member_count,
                        channel_description,
                        is_public,
                        join_date,
                        unread_count
                    )
                )


    def run(self, *args, **kwargs):
        """
        CLI命令行入口
        """
        self.telegram_group_final()

if __name__ == "__main__":
    te = TelegramGroupFinal('../../conf/tg_config.json', '../../conf/application.yml')

    te.telegram_group_final()

    time.sleep(2000)

