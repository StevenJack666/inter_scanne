# -*- coding: utf-8 -*-
# @Time     : 2022/11/16 15:24:31
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : telegram_get_dialog.py
# @Software : Visual Studio Code
# @WeChat   : NextB


__doc__ = """
获取telegram的消息框
"""

from tg_spiders.cli.telegram_base import *

cur_dirname = os.path.dirname(os.path.abspath(__file__))


class TelegramGetDialog(TelegramBase):

    def __init__(self, jobconf, app_conf):
        super(TelegramGetDialog, self).__init__(jobconf, app_conf)

    def telegram_get_dialog(self):


        self.login_in()
        json_res = self.ta.get_dialog_list()


        if json_res['result'] == 'success':
            data = json_res['data']
            for item in data:
                if data is None:
                    print("获取对话框数据失败")
                    continue
                group_id = item.get("id", "")
                group_title = item.get("title", "")
                group_username = item.get("username", "")
                group_megagroup = item.get("megagroup", "")
                group_member_count = item.get("member_count", "")
                group_unread_count = item.get("unread_count", "")
                group_channel_description = item.get("channel_description", "")
                group_is_public = item.get("is_public", "")
                group_join_date = item.get("join_date", "")

                print(
                    "{},{},{},{},{},{}".format(
                        group_id,
                        group_title,
                        group_username,
                        group_megagroup,
                        group_member_count,
                        group_unread_count,
                        group_join_date,
                        group_channel_description,
                        group_is_public
                    )
                )


        self.ta.close_client()


    def run(self, *args, **kwargs):
        """
        CLI命令行入口
        """
        # args = parse_cmd()
        self.telegram_get_dialog()



if __name__ == "__main__":
    te = TelegramGetDialog('../../conf/tg_config.json')
    te.run()
