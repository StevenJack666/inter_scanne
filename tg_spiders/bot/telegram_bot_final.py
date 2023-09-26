import telegram
# from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext.filters import MessageFilter

import requests

TOKEN = '6060781778:AAFqJNBvoqxYwTI1RoRtby6XMNEHk47h_ic'
CHANNEL_USERNAME = 'thor_zhang'
GROUP_USERNAME = '+WpAo0CJoG781YTdl'

def test():
    # 填入Telegram Bot Token

    # 填入需要获取新消息的频道用户名（不带'@'）


    # 创建Bot实例
    bot = telegram.Bot(token=TOKEN)

    # 获取频道的Chat ID
    chat_id = bot.get_chat('@{}'.format(CHANNEL_USERNAME)).id

    # 处理每条新消息
    def handle_new_message(update, context):
        message = update.message
        print('New message from {}: {}'.format(message.chat.title, message.text))

    # 创建Updater和MessageHandler实例，并启动Bot
    # updater = Updater(token=TOKEN, use_context=True)
    # updater.dispatcher.add_handler(MessageHandler(Filters.chat(chat_id), handle_new_message))
    # updater.start_polling()

# https://t.me/

class Telegram:

    def __init__(self, app=None):
        self.app = app
        self._session = requests.session()
        self.token = TOKEN
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.token = TOKEN

    def send_message_to_channel(self, text, chat_id):
        response = self._session.get(
            f"https://api.telegram.org/bot{self.token}/sendMessage?text={text}&chat_id=@{CHANNEL_USERNAME}")

        print(response)

    def send_message_to_group(self, text, chat_id):
        response = self._session.get(
            f"https://api.telegram.org/bot{self.token}/sendMessage?text={text}&chat_id=@{chat_id}")

        print(response)


if __name__ == "__main__":
    protocal = "socks5"
    proxy_ip = "127.0.0.1"
    proxy_port = 7890
    clash_proxy = (protocal, proxy_ip, proxy_port)
    telegram_test = Telegram()
    telegram_test.send_message_to_channel("last_channel", CHANNEL_USERNAME)
    telegram_test.send_message_to_group("last_group", 'xliluo')

    # test()

