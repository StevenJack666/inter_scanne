
__doc__ = """
清理telegram的消息框
"""


from tg_spiders.cli.telegram_base import *


cur_dirname = os.path.dirname(os.path.abspath(__file__))

class TelegramClearDialog(TelegramBase):
    def __init__(self, job_session, app_conf):
        super(TelegramClearDialog, self).__init__(job_session, app_conf)



    def telegram_clear_dialog(self, all):

        self.login_in()
        # 删除所有聊天对话框
        self.ta.delete_all_dialog(is_all=all)
        self.login_out()


    def run(self, *args, **kwargs):
        """
        CLI命令行入口
        """
        args = ''
        self.telegram_clear_dialog(args.config, args.all)



if __name__ == "__main__":
    protocal = "socks5"
    proxy_ip = "127.0.0.1"
    proxy_port = 7890
    clash_proxy = (protocal, proxy_ip, proxy_port)

