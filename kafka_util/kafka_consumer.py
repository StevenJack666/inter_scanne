
from kafka import KafkaConsumer
import json
from kafka_util.kafka_base import KafkaBase
from tools.log import *

cur_dirname = os.path.dirname(os.path.abspath(__file__))


class Consumer(KafkaBase):

    def __init__(self, kafkaconf, topic):
        super(Consumer, self).__init__(kafkaconf)
        self.topic = topic


    def consumer_event(self):
        consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id='test'
        )
        for message in consumer:
            print("receive, key: {}, value: {}".format(
                json.loads(message.key.decode()),
                json.loads(message.value.decode())
            ))


    def run(self):
        self.producer_event()

if __name__ == "__main__":
    cur_dirname = os.path.dirname(os.path.abspath(__file__))
    conf_file = os.path.join(cur_dirname, "../../application.conf")
    from tools.config_parser import CrawlConfigParser

    jobconf = CrawlConfigParser()
    jobconf.read(conf_file)
    Consumer(jobconf, "test").run()
