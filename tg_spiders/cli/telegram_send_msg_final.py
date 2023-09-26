
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

class TelegramSenfMsgFinal(TelegramBase):

    def __init__(self, jobconf, app_conf):
        super(TelegramSenfMsgFinal, self).__init__(jobconf, app_conf)


    def telegram_senf_msg_final(self):
        # 加载配置文件
        self.login_in()

        # 获取当前用户的所有群组，并进行遍历
        list_contact = self.ta.send_message_to_myself()
        self.ta.close_client()


    def print_res(json_res):
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
        self.telegram_senf_msg_final()

if __name__ == "__main__":
    te = TelegramSenfMsgFinal('../../conf/tg_config.json')
    te.run()
