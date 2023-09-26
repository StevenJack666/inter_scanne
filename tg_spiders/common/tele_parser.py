
from telethon.utils import get_display_name
class TeleParser():


    def __init__(self, path):
        self.app_id = '24251370'
        self.app_hash = 'd2fabea38cdb06ebe6aa58c1970ced0c'
        self.app_user = 't'
        self.channel_id = '1691273405'
        self.image_path =path

    def login(self):
        from telethon import TelegramClient
        self.client = TelegramClient('test_session.session', self.app_id, self.app_hash, proxy=("http", '127.0.0.1', 7890))

    async def load_history_to_save(self):
        latest_id = 10
        entity = await self.client.get_entity(self.channel_id)
        async for message in self.client.iter_messages(entity, reverse=True, offset_id=latest_id, limit=None):
            print(message.text)

    from telethon.utils import get_display_name
    async def format_message(self, message, chat_id):
        if not message.text or message.media:
            return None

        chat = await message.get_chat()

        chat_display_name = get_display_name(chat)
        sender_user = await message.get_sender()
        doc_data = {
            "timestamp": message.date,
            "sender": {
                "username": getattr(sender_user, 'username', ''),
                "firstName": getattr(sender_user, 'first_name', ''),
                "lastName": getattr(sender_user, 'last_name', '')
            },
            "channel": chat_display_name,
            "channel_id": chat_id,
            "text": self.converter.convert(message.text),
            "message_id": message.id
        }
        return doc_data


    async def load_history_to_save(self):

        # key：channel_id, value：已保持到es的最新的id
        self.channel_dict = {
            -1001094615131: 0,  # archlinux-cn-offtopic
        }


        """从api拉取数据并保存到es"""
        for channel_id, latest_id in self.channel_dict.items():
            entity = await self.client.get_entity(channel_id)
            async for message in self.client.iter_messages(entity,
                                                           reverse=True, offset_id=latest_id, limit=None):
                doc_data = await self.format_message(message, channel_id)
                print(doc_data)
                '''
                数据存储
                '''
                # await self.save_to_es(doc_data, message.id, channel_id)

    def start(self):
        with self.client:
            self.client.loop.run_until_complete(self.load_history_to_save())


if __name__ == "__main__":
    protocal = "socks5"
    proxy_ip = "127.0.0.1"
    proxy_port = 7890
    clash_proxy = (protocal, proxy_ip, proxy_port)
    cli = TeleParser('./')
    cli.login()
    cli.start()
