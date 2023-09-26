# -*- coding: utf-8 -*-
# @Time     : 2022/11/16 15:38:06
# @Author   : ddvv
# @Site     : https://ddvvmmzz.github.io
# @File     : telegram_get_message.py
# @Software : Visual Studio Code
# @WeChat   : NextB


__doc__ = """
获取telegram的消息
"""

from tg_spiders.common.telegramAPIs import *
cur_dirname = os.path.dirname(os.path.abspath(__file__))

from tg_spiders.cli.telegram_base import *


class TelegramIterMessages(TelegramBase):
    def __init__(self, jobconf, app_conf):
        super(TelegramIterMessages, self).__init__(jobconf, app_conf)


    def telegram_get_message(self):
        # 加载配置文件
        self.login_in()
        for group in self.group:
            last_message_id = group.get("last_message_id")
            tg_history = self.ta.load_tg_history(group.get("group_id"), last_message_id)
            #  todo 记录最后一条爬取的消息id
            self.print_res(tg_history)

        # 获取当前用户的所有群组，并进行遍历
        list_dialog = self.ta.get_dialog_list()
        for item_group in list_dialog['data']:
            last_message_id = item_group.get("last_message_id")
            tg_history = self.ta.load_tg_history(item_group['username'], last_message_id)
            self.print_res(tg_history)
        self.ta.close_client()



    def print_res(self, json_res):
        if json_res['result'] == 'success':
            data = json_res['data']
            for item in data:
                if data is None:
                    print("获取群数据失败")
                    continue
                message_id = item.get("message_id", "")
                user_id = item.get("user_id", "")
                user_name = item.get("user_name", "")
                nick_name = item.get("nick_name", "")
                reply_to_msg_id = item.get("reply_to_msg_id", "")
                from_name = item.get("from_name", "")
                from_time = item.get("from_time", "")
                chat_id = item.get("chat_id", "")
                postal_time = item.get("postal_time", "")
                message = item.get("message", "")
                channel_id = item.get("channel_id", "")
                print(
                    "{},{},{},{},{},{},{},{},{},{},{}".format(
                        message_id,
                        user_id,
                        user_name,
                        nick_name,
                        reply_to_msg_id,
                        from_name,
                        from_time,
                        chat_id,
                        postal_time,
                        message,
                        channel_id
                    )
                )


    def run(self, *args, **kwargs):
        """
        CLI命令行入口
        """
        self.telegram_get_message()



if __name__ == "__main__":
    te = TelegramIterMessages('../../conf/tg_config.json')
    te.run()