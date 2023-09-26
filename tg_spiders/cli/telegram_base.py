import json

from tg_spiders.common.telegramAPIs import *
from kafka_util.kafka_producer import CrawlerProducer
from tools.config_parser import CrawlConfigParser
from tools.type_enum import *

cur_dirname = os.path.dirname(os.path.abspath(__file__))

class TelegramBase(object):
    session = None


    def __init__(self, job_conf, app_conf):
        self.ta = None
        # 加载配置文件
        with open(job_conf, "r", encoding="utf-8") as f:
            data = f.read()
        config_js = json.loads(data)
        # tg配置
        self.root_path = self.get_root_path()
        self.session_name = self.root_path + config_js.get("session_name")
        self.app_id = config_js.get("api_id")
        self.app_hash = config_js.get("api_hash")
        self.offset_date = config_js.get("offset_date")

        self.proxy = config_js.get("proxy", {})
        clash_proxy = None
        # 如果配置代理
        if self.proxy:
            self.protocal = self.proxy.get("protocal", "socks5")
            self.proxy_ip = self.proxy.get("ip", "127.0.0.1")
            self.proxy_port = self.proxy.get("port", 7890)
            self.clash_proxy = (self.protocal, self.proxy_ip, self.proxy_port)
        self.group = config_js.get("group", [])
        # kafka配置
        self.app_conf = app_conf
        kafka_conf_file = os.path.join(cur_dirname, app_conf)
        job_conf = CrawlConfigParser()
        job_conf.read(kafka_conf_file)
        self.topic = job_conf["kafka"]["event.topic"]

    def login_in(self):
        self.ta = TelegramAPIs(self.session_name, self.app_id, self.app_hash, self.clash_proxy)
        self.ta.init_client()

    def login_out(self):
        self.ta.close_client()



    '''
    发送kafka消息
    '''
    def send_kafka_producer(self, data: list, tg_type):

        crawler_producer = CrawlerProducer(self.app_conf, self.topic)
        # 生成消息id和时间戳
        millis = int(round(time.time() * 1000))
        result_scan_mes_json = {"message_id": tg_type+"_"+str(millis), "type": tg_type, "timestamp": str(millis)}
        result_scan_mes_json["data"] = data
        crawler_producer.async_producer(result_scan_mes_json)

    # 获得根路径
    def get_root_path(self):
        # 获取文件目录
        curPath = os.path.abspath(os.path.dirname(__file__))
        # 获取项目根路径，内容为当前项目的名字
        rootPath = curPath[:curPath.find("vcrawl/") + len("vcrawl/")]
        return rootPath