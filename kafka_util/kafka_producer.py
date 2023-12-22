
from kafka import KafkaProducer
import json
from kafka_util.kafka_base import KafkaBase
from tools.log import *
from tools.config_parser import CrawlConfigParser
from tools.complex_encoder import *
cur_dirname = os.path.dirname(os.path.abspath(__file__))

import tools
import functools



class CrawlerProducer(KafkaBase):
    __producer = None
    __first_init = True

    def __new__(cls, *args, **kwargs):
        if cls.__producer == None:
            cls.__producer = object.__new__(cls)
        return cls.__producer

    def __init__(self,  kafka_conf, topic):
        print("-----init----")
        if self.__first_init:

            self.__class__.__first_init = False
            super(CrawlerProducer, self).__init__(kafka_conf)

            """
            kafka 生产者
            :param bootstrap_servers: 地址
            :param topic:  topic
            """
            self.__producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers, batch_size=10485760, max_block_ms=10000,
                value_serializer=lambda m: json.dumps(m, ensure_ascii=False, cls=DateEncoder).replace("'", "\"")[1:-1].encode('utf-8'), request_timeout_ms=60000,
                api_version=(3, 5, 1))  # json 格式化发送的内容
            self.topic = topic


    def sync_producer(self, data_li: list):
        """
        同步发送 数据
        :param data_li:  发送数据
        :return:
        """
        for data in data_li:
            future = self.__producer.send(self.topic, data)
            record_metadata = future.get(timeout=10)  # 同步确认消费
            partition = record_metadata.partition  # 数据所在的分区
            offset = record_metadata.offset  # 数据所在分区的位置
            print('save success, partition: {}, offset: {}'.format(partition, offset))

    def async_producer(self, data):
        # 对消息序列化
        data_json = json.dumps(data, ensure_ascii=False, cls=DateEncoder)
        # dic_str = json.loads(str(data), cls=DateEncoder)
        python_object = json.loads(data_json)
        json_data_without_slash = json.dumps(python_object)

        # data_json = json.loads(data)

        #logger.debug('send success, value')
        #print(repr(data_json))
        """
        异步发送数据
        :param data_li:发送数据
        :return:
        """
        self.__producer.send(self.topic, value=str(data))
        self.__producer.flush()  # 批量提交
        logger.debug('send success, value')

    def async_producer_callback(self, data_li: list):
        """
        异步发送数据 + 发送状态处理
        :param data_li:发送数据
        :return:
        """
        for data in data_li:
            self.__producer.send(self.topic, data).add_callback(self.send_success).add_errback(self.send_error)
        self.__producer.flush()  # 批量提交

    def send_success(self, *args, **kwargs):
        """异步发送成功回调函数"""
        print('save success')
        return

    def send_error(self, *args, **kwargs):
        """异步发送错误回调函数"""
        print('save error')
        return

    def close_producer(self):
        try:
            self.__producer.close()
        except:
            pass












if __name__ == "__main__":
    CrawlerProducer
    cur_dirname = os.path.dirname(os.path.abspath(__file__))
    conf_file = os.path.join("../conf/application.conf")
    from tools.config_parser import CrawlConfigParser

    jobconf = CrawlConfigParser()
    jobconf.read(conf_file)



    prod = CrawlerProducer(jobconf, "test")
    prod2 = CrawlerProducer(jobconf, "test")
    prod3 = CrawlerProducer(jobconf, "test")

    print(id(prod2) == id(prod))
    print(id(prod3) == id(prod))

    send_data_li = [{"test": 1}, {"test": 2}, {"test": 3}]
    prod.sync_producer(send_data_li)
    prod.async_producer(send_data_li)

    prod.close_producer()
