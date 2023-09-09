
from kafka import KafkaProducer
from kafka.errors import kafka_errors
import traceback
import json
from kafka_util.kafka_base import KafkaBase
from tools.log import *

cur_dirname = os.path.dirname(os.path.abspath(__file__))


class Producer(KafkaBase):

    def __init__(self, kafkaconf, topic):

        super(Producer, self).__init__(kafkaconf)
        self.topic = topic
        """
        kafka 生产者
        :param bootstrap_servers: 地址
        :param topic:  topic
        """
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda m: json.dumps(m).encode('ascii'), )  # json 格式化发送的内容
        self.topic = topic


    def sync_producer(self, data_li: list):
        """
        同步发送 数据
        :param data_li:  发送数据
        :return:
        """
        for data in data_li:
            future = self.producer.send(self.topic, data)
            record_metadata = future.get(timeout=10)  # 同步确认消费
            partition = record_metadata.partition  # 数据所在的分区
            offset = record_metadata.offset  # 数据所在分区的位置
            print('save success, partition: {}, offset: {}'.format(partition, offset))

    def asyn_producer(self, data_li: list):
        """
        异步发送数据
        :param data_li:发送数据
        :return:
        """
        for data in data_li:
            self.producer.send(self.topic, data)
        self.producer.flush()  # 批量提交

    def asyn_producer_callback(self, data_li: list):
        """
        异步发送数据 + 发送状态处理
        :param data_li:发送数据
        :return:
        """
        for data in data_li:
            self.producer.send(self.topic, data).add_callback(self.send_success).add_errback(self.send_error)
        self.producer.flush()  # 批量提交

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
            self.producer.close()
        except:
            pass












if __name__ == "__main__":
    cur_dirname = os.path.dirname(os.path.abspath(__file__))
    conf_file = os.path.join(cur_dirname, "../application.conf")
    from tools.config_parser import CrawlConfigParser

    jobconf = CrawlConfigParser()
    jobconf.read(conf_file)

    send_data_li = [{"test": 1}, {"test": 2}]


    prod = Producer(jobconf, "test")

    prod.sync_producer(send_data_li)
    prod.close_producer()
