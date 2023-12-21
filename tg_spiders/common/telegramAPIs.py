# -*- coding: utf-8 -*-
# @Time    :   2021/09/10 16:37:22
# @Author  :   ddvv
# @公众号   :   NextB
# @File    :   telegramAPIs.py
# @Software:   Visual Studio Code
# @Desc    :   None

import json
import os
import time
import datetime
import logging
import asyncio
import re
from ocr_handler.cnocr.ocr_base import *
import socks
import telethon.tl.types
from telethon.tl.types import InputMessagesFilterPhotos

from random import randint
from telethon import TelegramClient, sync
from telethon.tl.functions.channels import (
    GetFullChannelRequest,
    JoinChannelRequest,
    GetParticipantsRequest,
)
from telethon.tl.functions.messages import (
    ImportChatInviteRequest,
    CheckChatInviteRequest,
    GetFullChatRequest,
)
from telethon.tl.functions.contacts import DeleteContactsRequest, GetContactsRequest
from telethon.tl.types import (
    ChatInviteAlready,
    ChatInvite,
    Message,
    Channel,
    Chat,
    ChannelForbidden,
    ChannelParticipantsSearch, InputChannel,
)

from telethon.tl.types import PeerUser, PeerChat, PeerChannel, UpdateNewChannelMessage

logging.basicConfig(level=logging.INFO)
logging.getLogger("telethon").setLevel(level=logging.INFO)
logging.getLogger("scrapy").setLevel(level=logging.INFO)


# TODO: make the hardcode code (e.g. BASE_PATH) as configurable in settings files
# TODO: use Sqlacademy ORM instead operation such data in low-level

# 接受监视的媒体格式(tg里面直接发送gif最后是mp4格式！)，如果需要下载mp4内容可以添加"image/mp4"
accept_file_format = ["image/jpeg", "image/gif", "image/png","image/webp"]


class TelegramAPIs(object):
    def __init__(self, session_name, app_id, app_hash, proxy=None, image_path=None):
        self.client = None
        self.session_name = session_name
        self.app_id = app_id
        self.app_hash = app_hash
        self.proxy = proxy
        self.phone_number = '13849016535'
        self.image_path = image_path


    def init_client(self):
        """
        初始化client
        :param session_name: session文件名
        :param api_id: api id
        :param api_hash: api hash
        :param proxy: socks代理，默认为空
        """
        if self.proxy is None:
            self.client = TelegramClient(self.session_name, self.app_id, self.app_hash)
        else:
            self.client = TelegramClient(self.session_name, self.app_id, self.app_hash, proxy=self.proxy)

        # self.check()
        self.client.start(phone=self.phone_number, password='Qzhang450000')

    def close_client(self):
        """
        关闭client
        """
        if self.client.is_connected():
            self.client.disconnect()

    # 加入频道或群组
    def join_conversation(self, invite):
        """
        加入方式主要分为
            1. 加入公开群组/频道：invite为username
            2. 加入私有群组/频道：invite为hash

        注意：需要测试如下两个逻辑，
            1. 换了群组的username之后，使用新username加入时的返回值(会显示无效，已测)
            2. 是否能直接通过ID加入(不能，通过id只能获取已经加入的频道/群组信息，并通过get_entity方法获取该频道的信息)
        :param invite: channel/group username/hash
        :return: 返回json, {'data': {'id':, 'chat':}, 'result': 'success/failed', 'reason':''}
        data: chat_id
        """
        # 每个加组的操作都休眠10秒先，降低速率
        time.sleep(10)
        chat_id = 0
        result = "Failed"
        result_json = {
            "data": {"id": chat_id, "group_name": invite},
            "result": result,
            "reason": "",
        }
        try:
            # Checking a link without joining
            # 检测私有频道或群组时，由于传入的是hash，可能会失败(已测试，除非是被禁止的，否则也会成功)
            updates = self.client(CheckChatInviteRequest(invite))
            if isinstance(updates, ChatInviteAlready):
                chat_id = updates.chat.id
                # chat = updates.chat
                result = "Done"
            elif isinstance(updates, ChatInvite):
                # Joining a private chat or channel
                updates = self.client(ImportChatInviteRequest(invite))
                # updates = self.client(CheckChatInviteRequest(invite))
                chat_id = updates.chats[0].id
                # chat = updates.chats[0]
                result = "Done"
        except Exception as e:
            try:
                # Joining a public chat or channel
                updates = self.client(JoinChannelRequest(invite))
                result = "Done"
            except Exception as ee:
                result_json["reason"] = str(ee)
                return result_json
            chat_id = updates.chats[0].id
            # chat = updates.chats[0]
        result_json["data"]["id"] = chat_id
        result_json["result"] = result

        return result_json

    def delete_all_dialog(self, is_all=0):
        """
        删除对话框
        """
        for dialog in self.client.get_dialogs():
            # like "4721 4720"、"5909 5908"
            name = dialog.name
            is_new_user = False
            if " " in name and ("1" in name or "3" in name or "6" in name):
                is_new_user = True
            # 退出频道或群组
            if is_all and hasattr(dialog.entity, "title"):
                chat = dialog.entity
                self.client.delete_dialog(chat)
                print("已离开<{}>群组".format(dialog.entity.title))
            # 删除delete account
            elif dialog.name == "":
                chat = dialog.entity
                self.client.delete_dialog(chat)
                print("已删除Deleted Account用户对话框")
            elif is_new_user:
                chat = dialog.entity
                self.client.delete_dialog(chat)
                print("已删除{}用户对话框".format(dialog.name))
            elif is_all:
                chat = dialog.entity
                self.client.delete_dialog(chat)
                print("已删除{}用户对话框".format(dialog.name))
            else:
                pass

    def get_me(self):
        """
        获取当前账户信息
        """
        myself = self.client.get_me()
        return myself

    async def send_message_to_myself(self):
        while 1:
            talkTime = randint(200, 250)
            self.client.send_message("me", str(talkTime))
            print("发送成功")
            await asyncio.sleep(talkTime)

    '''
    查询群组成员
    '''

    def query_chat_member(self, channel_id, group_num):
        channel = self.client.get_entity(PeerChannel(int('{channel_id}'.format(channel_id=channel_id))))  # 根据群组id获取群组对
        # 两种channel都可以,人数少于1w的时候正常请求，多余1w 主动探测请求
        result_dialog_json = {"result": "success", "reason": "ok", "data": []}
        result = []  # 用于储存json文件
        try:
            if (int(group_num) <= 10000):
                member_res = self.client.iter_participants(channel)  # 获取群组所有用户信息
            else:
                member_res = self.client.iter_participants(channel, aggressive=True)
        except Exception as e:
            print(e)
            pass
        if member_res is not None:
            for resp in member_res:
                try:
                    # print('用户id：',resp.id,'用户first_name',resp.first_name,'用户last_name',resp.last_name,'用户名 username',resp.username,'用户 phone',resp.phone)
                    temp_dict = {}
                    temp_dict['user_id：'] = resp.id
                    temp_dict['user_first_name'] = resp.first_name
                    temp_dict['user_last_name'] = resp.last_name
                    temp_dict['user_name'] = resp.username
                    temp_dict['user_phone'] = resp.phone
                    result.append(temp_dict.copy())
                except Exception as e:
                    print(e.args)
                    pass
        print('==== 获取群成员结束 ==== %s', result)
        result_dialog_json["data"] = result
        return result_dialog_json

    def get_contacts(self):
        """
        获取联系人
        """
        contacts = self.client(GetContactsRequest(0))
        return contacts

    def delete_contact(self, ids):
        """
        删除联系人
        """
        self.client(DeleteContactsRequest(ids))

    def get_dialog_list(self):
        """
        获取已经加入的频道/群组列表
        :return: 返回json, {'data': [], 'result': 'success/failed', 'reason':''}
        data: list类型，
        """
        list_dialog = []
        for dialog in self.client.get_dialogs():
            # 确保每次数据的准确性
            result_dialog_json = {"result": "success", "reason": "ok", "data": []}

            # 只爬取频道或群组，排除个人
            if hasattr(dialog.entity, "title"):
                chat = dialog.entity
                if isinstance(chat, Channel):
                    channel_full = self.client(GetFullChannelRequest(chat))
                    member_count = channel_full.full_chat.participants_count
                    channel_description = channel_full.full_chat.about
                    username = channel_full.chats[0].username
                    megagroup = channel_full.chats[0].megagroup

                    reg = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
                    # reg = 'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
                    url_temp = re.findall(reg, channel_full.full_chat.about)

                    if len(username):
                        hex_url = 'https://t.me/' + username
                    elif len(url_temp):
                        hex_url = url_temp[0]

                elif isinstance(chat, Chat):
                    channel_full = self.client(GetFullChatRequest(chat.id))
                    member_count = channel_full.chats[0].participants_count
                    # channel_description = channel_full.full_chat.about
                    channel_description = ""
                    hex_url = None
                    username = None
                    megagroup = ""
                else:
                    # yield result_json
                    continue
                # megagroup: true表示超级群组(官方说法)
                # 实际测试发现(TaiwanNumberOne该群组)，megagroup表示频道或群组，true表示群，false表示频道
                # democracy: 暂时不清楚什么意思
                out = {
                    "channel_id": chat.id,
                    "title": chat.title,
                    "username": username,
                    "hex_url": hex_url,
                    # 'democracy': channel_full.chats[0].democracy,
                    "megagroup": "channel" if megagroup else "group",
                    "member_count": member_count,
                    "channel_description": channel_description,
                    "is_public": 1 if username else 0,
                    "join_date": chat.date.strftime("%Y-%m-%d %H:%M:%S+%Z"),
                    "unread_count": dialog.unread_count,
                }
                list_dialog.append(out.copy())

                # yield result_json
        result_dialog_json["data"] = list_dialog
        return result_dialog_json

    def get_dialog_chat(self, chat_id, is_more=False):
        """
        方法一：通过遍历的方式获取chat对象，当chat_id相等时，返回
        方法二：对于已经加入的频道/群组，可以直接使用get_entity方法
        :param chat_id: 群组/频道 ID
        :param is_more: 默认为False，不使用遍历的方式
        :return: chat对象，用于后续操作
        """
        # 方法一
        if is_more:
            chat = None
            for dialog in self.client.get_dialogs():
                if dialog.entity.id == chat_id:
                    chat = dialog.entity
                    break
        # 方法二
        else:
            chat = self.client.get_entity(chat_id)

        return chat

    def scan_message(self, chat, **kwargs):
        """
        遍历消息
        :param chat:
        :param kwargs:
        """
        tick = 0
        waterline = randint(5, 20)
        limit = kwargs["limit"]
        min_id = kwargs["last_message_id"]
        # 默认只能从最远开始爬取
        offset_date = None
        if 0 and kwargs["offset_date"]:
            offset_date = datetime.datetime.strptime(
                kwargs["offset_date"], "%Y-%m-%d %H:%M:%S"
            )
        count = 0
        result_scan_mes_json = {"result": "success", "reason": "ok"}
        list_message = []
        for message in self.client.iter_messages(
                chat,
                limit=limit,
                offset_date=offset_date,
                offset_id=min_id,
                wait_time=1,
                reverse=True,
        ):

            if isinstance(message, Message):

                content = ""
                try:
                    content = message.message
                except Exception as e:
                    print(e)
                if content == "":
                    continue
                m = dict()
                m["message_id"] = message.id
                m["publisher_id"] = 0
                m["publisher"] = ""
                m["nick_name"] = ""
                m["reply_to_msg_id"] = 0
                m["from_name"] = ""
                m["image_path"] = ""
                # m["from_time"] = datetime.datetime.fromtimestamp(657224281)
                if message.sender:
                    m["publisher_id"] = message.sender.id
                    if isinstance(message.sender, ChannelForbidden):
                        username = ""
                    else:
                        username = message.sender.username
                        username = username if username else ""
                    m["publisher"] = username
                    if isinstance(message.sender, Channel) or isinstance(
                            message.sender, ChannelForbidden
                    ):
                        first_name = message.sender.title
                        last_name = ""
                    else:
                        first_name = message.sender.first_name
                        last_name = message.sender.last_name
                        first_name = first_name if first_name else ""
                        last_name = " " + last_name if last_name else ""
                    m["nick_name"] = "{0}{1}".format(first_name, last_name)
                if message.is_reply:
                    m["reply_to_msg_id"] = message.reply_to_msg_id
                if message.forward:
                    m["from_name"] = message.forward.from_name
                    # m["from_time"] = message.forward.date
                m["chat_id"] = chat.id
                # m['postal_time'] = message.date.strftime('%Y-%m-%d %H:%M:%S')
                m["publish_time"] = datetime.datetime.strptime(str(message.date), "%Y-%m-%d %H:%M:%S+00:00").strftime("%Y-%m-%d %H:%M:%S")
                m["content_title"] = content
                file_name = self.download_image(message)
                id_millis = str(int(round(time.time() * 1000)))
                if file_name is not None:
                    ocr_image = OcrImage()
                    ocr_result = ocr_image.ocr_for_single_lines(file_name)
                    m["sample_datas"] = self.sample_datas_convert(id_millis, ocr_result)
                    m["image_path"] = file_name
                m["id"] = id_millis
                tick += 1
                if tick >= waterline:
                    tick = 0
                    waterline = randint(5, 10)
                    time.sleep(waterline)
                count += 1

                list_message.append(m.copy())
        print("total: %d" % count)
        if len(list_message) == 0:
            result_scan_mes_json["result"] = "failed"
        else:
            result_scan_mes_json["data"] = list_message
        return result_scan_mes_json




    # 下载媒体的具体方法
    def download_image(self, message):
        picture_storage_path = "/"
        # message_tmp = self.client.get_messages('https://t.me/xliluo', None, max_id=100000, min_id=0, filter=InputMessagesFilterPhotos)
        # total = len(photos)
        # index = 0
        # for photo in photos:
        #     #    filename = picture_storage_path + "/" +str(photo.text)+"_"+str(photo.id) + ".jpg" #名字_id
        #     filename = "/Users/zhangmingming/" + str(photo.id) + ".jpg"
        #     index = index + 1
        #     print("downloading:", index, "/", total, " : ", filename)
        #     if os.path.exists(filename) == False:
        #         self.client.download_media(photo, filename)
        #         print('done!')
        #     else:
        #         print('exist!')




        # for message in message_tmp:
            # 获取媒体类型
        is_webpage = isinstance(message.media, telethon.tl.types.MessageMediaWebPage)
        is_photo = isinstance(message.media, telethon.tl.types.MessageMediaPhoto)
        is_doc = isinstance(message.media, telethon.tl.types.MessageMediaDocument)

            # 判断媒体是否是受支持的
        if not (is_photo or is_webpage):  # 不是照片也不是网页
            if is_doc:  # 如果是文件
                is_accept_media = message.media.document.mime_type in accept_file_format  # 检查文件类型是否属于支持的文件类型
                if not is_accept_media:  # 判断文件类型是否是需要的类型
                    # print("不接受的媒体类型")
                    return
                # 如果不是文件就放弃（可能是音频啥的）
            else:
                return
            # download_media()可以自动命名，下载成功后会返回文件的保存名
        filename = self.client.download_media(message, self.image_path)


        # print(f"媒体下载完成:{filename}")
        return filename
            # 下面注释的代码不知道什么原因无法在文件不存在的情况下新建文件
            # async with async_open(save_path + "1.txt", "a") as f:
            #     await f.write(filename + "\n")
            # 原消息内容输出显示
        # print(message.sender.id, message.raw_text)

            # 通知mirai机器人干活（没有这个需求的可以把这句注释掉）


    def download_user_photo(self, chat_id, nick_names, download_path="./", compress=0):
        """
        通过用户昵称下载用户头像
        :param chat: 频道/群组对象
        :param nick_names: 用户昵称列表
        download_path: 头像保存路径
        compress: 是否压缩头像至 64 * 64大小
        """
        use_pil_image = True
        if compress:
            try:
                from PIL import Image
            except Exception as e:
                print(
                    "检测到未安装PIL库，无法对头像进行缩放处理，保存原始头像。若要保存缩放后的头像，请安装PIL，安装命令：pip install Pillow")
                use_pil_image = False
        # chat = self.get_dialog(chat_id, is_more=True)
        chat = self.get_dialog(chat_id, is_more=False)

        for nick_name in nick_names:
            try:
                participants = self.client(
                    GetParticipantsRequest(
                        chat,
                        filter=ChannelParticipantsSearch(nick_name),
                        offset=0,
                        limit=randint(5, 10),
                        hash=0,
                    )
                )
            except Exception as e:
                print("查找《{}》用户失败，失败原因：{}".format(nick_name, str(e)))
                continue

            if not participants.users:
                print("未找到《{}》用户。".format(nick_name))
                continue

            for entity in participants.users:
                member_id = entity.id
                if entity.photo:
                    photo_down = os.path.join(download_path, "{}.jpg".format(member_id))
                    self.client.download_profile_photo(
                        entity, file=photo_down, download_big=False
                    )
                    if compress and use_pil_image:
                        picture = Image.open(photo_down)
                        picture = picture.resize((64, 64))
                        picture.save(photo_down)
                        print("《{}》用户压缩头像（64 * 64）保存至：{}".format(nick_name, photo_down))
                    else:
                        print("《{}》用户原始头像保存至：{}".format(nick_name, photo_down))
                else:
                    print("《{}》用户没有使用自定义头像。".format(nick_name))

            print(
                "在《{}》群中找到{}个昵称为《{}》的用户，休眠5-10秒".format(
                    chat.title, len(participants.users), nick_name
                )
            )
            time.sleep(randint(5, 10))

    '''
    遍历数据，从latest_id开始
    '''

    def load_tg_history(self, channel_id, latest_id):
        result_scan_mes_json = {"result": "success", "reason": "ok"}
        entity = self.client.get_entity(channel_id)
        list_message = []
        count = 0
        for message in self.client.iter_messages(entity, reverse=True, offset_id=latest_id, limit=None):
            m = dict()
            m["message_id"] = message.id
            m["user_id"] = 0
            m["user_name"] = ""
            m["nick_name"] = ""
            m["reply_to_msg_id"] = 0
            m["from_name"] = ""
            #m["from_time"] = datetime.datetime.fromtimestamp(657224281)
            if message.sender:
                m["user_id"] = message.sender.id
                if isinstance(message.sender, ChannelForbidden):
                    username = ""
                else:
                    username = message.sender.username
                    username = username if username else ""
                m["user_name"] = username
                if isinstance(message.sender, Channel) or isinstance(
                        message.sender, ChannelForbidden
                ):
                    first_name = message.sender.title
                    last_name = ""
                else:
                    first_name = message.sender.first_name
                    last_name = message.sender.last_name
                    first_name = first_name if first_name else ""
                    last_name = " " + last_name if last_name else ""
                m["nick_name"] = "{0}{1}".format(first_name, last_name)
            if message.is_reply:
                m["reply_to_msg_id"] = message.reply_to_msg_id
            if message.forward:
                m["from_name"] = message.forward.from_name
                m["from_time"] = message.forward.date
            # m['postal_time'] = message.date.strftime('%Y-%m-%d %H:%M:%S')
            m["postal_time"] = message.date
            m["message"] = message.message
            m["channel_id"] = channel_id

            list_message.append(m.copy())
            if (len(list_message) > 100):
                break
        result_scan_mes_json["data"] = list_message
        return result_scan_mes_json


    def sample_datas_convert(self, id_millis, ocr_result):
        if ocr_result is None:
            return
        sample_datas = []
        for res in ocr_result:
            sample_datas.append({
                "original_event_id": id_millis,
                "tenant_id": "zhnormal",
                "phone_num": "",
                "bind_id": "",
                "user_name": "",
                "user_id": "",
                "identity_id": "",
                "home_addr": "",
                "data_type": "2",
                "original_data": res
            })
        return sample_datas

if __name__ == "__main__":

    protocal = "socks5"
    aa = socks.SOCKS5
    proxy_ip = "45.32.223.200"
    proxy_port = 65534

    my_proxy = {
        'proxy_type': protocal,  # (mandatory) protocol to use (see above)
        'addr': '45.32.223.200',  # (mandatory) proxy IP address
        'port': 65534,  # (mandatory) proxy port number
        'username': 'test',  # (optional) username if the proxy requires auth
        'password': 'TeSt1024',  # (optional) password if the proxy requires auth
        'rdns': True  # (optional) whether to use remote or local resolve, default remote
    }

    # proxy = (aa, proxy_ip, proxy_port, 'TeSt1024', 'test')

    proxy = (socks.SOCKS5, proxy_ip, proxy_port, 'test', 'TeSt1024')

    cli = TelegramAPIs('test_session.session',
                       '24251370', 'd2fabea38cdb06ebe6aa58c1970ced0c',
                       proxy=my_proxy)


    cli.init_client()
    me = cli.get_me()
    contacts = cli.get_contacts()
    cli.send_message_to_myself()

    dialog_list = cli.get_dialog_list()
    # 遍历当前用户的群组，并爬取每个群组的消息
    for item in dialog_list['data']:
        print(item)
        if item['username'] is None:
            continue
        chat_dialog = cli.get_dialog_chat('caisheen88888')
        # members = cli.query_chat_member(item['id'])
        param = {
            "limit": 1000,
            "offset_date": '2020-01-01 00:00:00',
            "last_message_id": -1,  # -1表示从第一条开始
        }
        # 爬取群组消息
        message_res = cli.scan_message(chat_dialog, **param)
        # print(message_res)
        # print()
        #
        # # 获取群组所有用户的头像
        # nicknames = []
        # for item_data in message_res['data']:
        #     nicknames.append(item_data['nick_name'])
        # nicknames_tmp = list(set(nicknames))
        # # 根据群组ID和用户昵称 ，下载所有用户的头像
        # cli.download_user_photo(item['username'], nicknames_tmp)

    # 加入群组
    join_test = cli.join_conversation('xliluo')

    cli.load_history_to_save('xliluo')
    cli.client.bot
    print(me)
    print(contacts)
    print(join_test)
    print(dialog_list['data'])
    print(dialog_list)

    # print(chat_dialog)
    # print(message_res)
    cli.close_client()
