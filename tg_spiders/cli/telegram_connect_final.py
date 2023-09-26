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
from tg_spiders.cli.telegram_base import *

scrapy_cfg = """# Automatically created by: scrapy startproject
#
# For more information about the [deploy] section see:
# https://scrapyd.readthedocs.io/en/latest/deploy.html

[settings]
default = NextBSpiders.settings
"""

class TelegramConnectFinal(TelegramBase):


    def __init__(self, jobconf, app_conf):
        super(TelegramConnectFinal, self).__init__(jobconf, app_conf)

    def telegram_contact_final(self):
        ta = TelegramAPIs(self.session_name, self.app_id, self.app_hash, self.clash_proxy)
        ta.init_client()
        # 获取当前用户的所有联系人，并进行遍历
        list_contact = ta.get_contacts()
        self.print_res(list_contact)
        ta.close_client()



    def print_res(self, json_res):
        contacts = json_res.contacts
        if contacts is None:
            return None
        for item in contacts:
            if item is None:
                print("获取联系人数据失败")
                continue
            user_id = item.user_id
            print("{}".format(user_id))

    def run(self, *args, **kwargs):
        """
        CLI命令行入口
        """
        self.telegram_contact_final()

if __name__ == "__main__":

    tg = TelegramConnectFinal('../../conf/tg_config.json')
    tg.run()
