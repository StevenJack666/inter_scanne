import json

from tg_spiders.common.telegramAPIs import *
from kafka_util.kafka_producer import CrawlerProducer
from tools.config_parser import CrawlConfigParser
from tools.config import *
import requests
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
            self.username = self.proxy.get("username", 'test')
            self.password = self.proxy.get("password", 'TeSt1024')

            # self.clash_proxy = (self.protocal, self.proxy_ip, self.proxy_port)

            self.clash_proxy = {
                'proxy_type': self.protocal,  # (mandatory) protocol to use (see above)
                'addr': self.proxy_ip,  # (mandatory) proxy IP address
                'port': self.proxy_port,  # (mandatory) proxy port number
                'username': self.username,  # (optional) username if the proxy requires auth
                'password': self.password,  # (optional) password if the proxy requires auth
                'rdns': True  # (optional) whether to use remote or local resolve, default remote
            }
        self.group = config_js.get("group", [])
        # kafka配置
        self.app_conf = app_conf
        kafka_conf_file = os.path.join(cur_dirname, app_conf)
        self.job_conf = CrawlConfigParser()
        self.job_conf.read(kafka_conf_file)
        self.topic = self.job_conf["kafka"]["event.topic"]
        self.image_path = config_js.get("image_path")

    def login_in(self):
        self.ta = TelegramAPIs(self.session_name, self.app_id, self.app_hash, self.clash_proxy, self.image_path)
        self.ta.init_client()

    def login_out(self):
        self.ta.close_client()



    '''
    发送kafka消息
    '''
    def send_kafka_producer(self, data: list, tg_type):
        # 生成消息id和时间戳
        millis = int(round(time.time() * 1000))
        result_scan_mes_json = {"message_id": tg_type+"_"+str(millis), "type": tg_type, "timestamp": str(millis)}
        result_scan_mes_json["data"] = data
        if tg_type != '2':
            crawler_producer = CrawlerProducer(self.job_conf, self.topic)
            crawler_producer.async_producer(result_scan_mes_json)
        else:
            time.sleep(1)
            self.upload_files(data)
            resp = requests.post(scanner_tg_mes_url, headers=scanner_headers, data=json.dumps(result_scan_mes_json))
            print(resp)

    def upload_files(self, data):

        for item in data:
            if data is None:
                continue
            file_path = item.get("image_path", "")
            # 指定上传的文件路径
            if file_path is None or file_path == '':
                return
            # 构建HTTP请求
            files = {'file': open(file_path, 'rb')}

            # 发送POST请求
            response = requests.post(scanner_tg_image_url, headers=scanner_image_headers, files=files)
            decoded_string = response.content.decode('utf-8')
            tmp = json.loads(decoded_string)
            code = tmp['code']
            data = tmp['data']
            if code == 200:
                filePath = data['filePath']
                item["image_path"] = filePath


    # 获得根路径
    def get_root_path(self):
        # 获取文件目录
        curPath = os.path.abspath(os.path.dirname(__file__))
        # 获取项目根路径，内容为当前项目的名字
        rootPath = curPath[:curPath.find("vcrawl/") + len("vcrawl/")]
        return rootPath


if __name__ == "__main__":
    base = TelegramBase('../../conf/tg_config.json', '../../conf/application.conf')
    base.upload_files('/Users/zhangmingming/Desktop/test.png')

