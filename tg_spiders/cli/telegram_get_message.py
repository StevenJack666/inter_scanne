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
from service.tg_group_model_service import *
from tg_spiders.cli.telegram_base import *
from tools.type_enum import *
from service.task_model_service import *
cur_dirname = os.path.dirname(os.path.abspath(__file__))

class TelegramGetMessage(TelegramBase):


    def __init__(self, jobconf, app_conf):
        super(TelegramGetMessage, self).__init__(jobconf, app_conf)
        self.publish_time = None
        self.task_id = None
        self.crux_key = None

    def telegram_get_message(self, **kwargs):
        # 获取群组聊天消息
        global last_message_id_tmp
        self.login_in()
        self.query_db_for_curl()
        dialog_list = self.ta.get_dialog_list()
        for item in dialog_list['data']:
            if item['username'] is None:
                continue
            chat_dialog = self.ta.get_dialog_chat(item['username'])
            tg_group_detail = self.query_db_for_channelGroup(item['username'])
            # 获取未读的消息，确定本次遍历的条数

            last_message_id = -1
            if tg_group_detail == None:
                offset_date_tmp = self.offset_date
            else:
                # last_message_id = tg_group_detail.last_message_id
                offset_date_tmp = tg_group_detail.offset_date
            # 遍历读取消息
            now_tmp = int(round(time.time() * 1000))
            self.publish_time = offset_date_tmp
            while (now_tmp > self.publish_time):
                param = {
                    "limit": 10,
                    "offset_date": offset_date_tmp,
                    "last_message_id": last_message_id,  # -1表示从第一条开始
                }
                # TODO 循环遍历所有的消息，并记录最新的消息ID
                # 爬取群组消息
                message_res = self.ta.scan_message(chat_dialog, **param)
                if message_res['result'] == 'success':
                    # 对爬取的群组消息输出
                    last_message_id_tmp = self.print_res(message_res, item['username'])
                    last_message_id = last_message_id_tmp
                else:
                    break
            item['last_message_id'] = -1
            item['offset_date'] = self.publish_time
            self.insert_update_channel_group(item)
        #     TODO 存储爬到的消息id，下次从这里爬取消息
        self.ta.close_client()

    def print_res(self, json_res, group_name):
        if json_res['result'] == 'success':
            data = json_res['data']

            last_message_id = -1
            for item in data:
                if data is None:
                    print("获取群数据失败")
                    continue
                message_id = item.get("message_id", "")
                message = item.get("content_title", "")
                time_tmp = item.get("publish_time", "")
                # timeArray = datetime.datetime.strptime(str(time_tmp), "%Y-%m-%d %H:%M:%S+00:00").strftime("%Y-%m-%d %H:%M:%S")
                item["publish_time"] = self.convert_time(time_tmp)
                item["group_name"] = group_name
                item["tenant_id"] = "zhnormal"

                # TODO  比对关键字，并给数据打标
                for value in self.crux_key:
                    if value in message:
                        item['crux_key'] = value
                    break
                if item.get('crux_key') is None or item.get('crux_key') == '':
                    item['crux_key'] = ''
                last_message_id = message_id
            tg_type = TgType.group_message_type.value
            self.send_kafka_producer(data, tg_type)
            return last_message_id

    def convert_time(self, dt):
        # date_time_obj = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S.%f%z')
        # 转换成时间数组
        if '+' in dt:
            timeArray = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S+00:00").strftime("%Y-%m-%d %H:%M:%S")
        else:
            timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")

        # 转换成时间戳
        timestamp = time.mktime(timeArray)
        return int(timestamp*1000)

    # TODO 查询数据库频道信息
    def query_db_for_channelGroup(self, user_name):
        tgService = TgGroupModelService()
        detail = tgService.channel_group_detail_id(user_name)
        return detail


    # TODO 更新用户频道信息
    def insert_update_channel_group(self, item):
        tgService = TgGroupModelService()
        tgService.insert_channel_group(item)


    # TODO 查询数据库获取关键字
    def query_db_for_curl(self):
        task_service = MonitorTaskService()
        task_detail = task_service.monitor_task_detail_id(self.task_id)
        if task_detail == None:
            self.crux_key = ''
            return ''
        fileContent = task_detail.fileContent
        keywords = fileContent.split(",")
        self.crux_key = keywords



    def run(self, *args, **kwargs):

        """
        CLI命令行入口
        """
        self.task_id = kwargs['id']
        self.telegram_get_message()


if __name__ == "__main__":
    t = '2023-06-05 05:25:48+00:00'
    # t = "2020-10-16T17:36:00+08:00"

    new_t = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S+00:00").strftime("%Y-%m-%d %H:%M:%S")
    print(new_t)
    # te = TelegramGetMessage('../../conf/tg_config.json')
    # te.run()
