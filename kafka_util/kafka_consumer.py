
from kafka import KafkaConsumer
import json
from kafka_util.kafka_base import KafkaBase
from tools.log import *

cur_dirname = os.path.dirname(os.path.abspath(__file__))


class CrawlerConsumer(KafkaBase):

    def __init__(self, kafka_conf, topic):
        super(CrawlerConsumer, self).__init__(kafka_conf)
        self.topic = topic


    def consumer_event(self):
        consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id='test'
        )
        for message in consumer:
            res = json.loads(message.value.decode())
            print("receive,  value: {}".format(
                # 消息反序列化
                res
            ))


    def run(self):
        self.consumer_event()

if __name__ == "__main__":
    cur_dirname = os.path.dirname(os.path.abspath(__file__))
    conf_file = os.path.join(cur_dirname, "../conf/application.conf")
    from tools.config_parser import CrawlConfigParser

    jobconf = CrawlConfigParser()
    jobconf.read(conf_file)
    CrawlerConsumer(jobconf, "crawl_event_topic").run()
