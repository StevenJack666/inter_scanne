#!/usr/bin/env python
# coding=utf-8

import time
import base64
import requests_html

from urllib.parse import urljoin
from kafka_util.kafka_producer import CrawlerProducer
from tools.config_parser import CrawlConfigParser
from tools.config import get_root_path
from service.task_model_service import *
from tools.tor_tool import connect_tor_with_retry

cur_dirname = os.path.dirname(os.path.abspath(__file__))


class BaseHandler(object):
    session = None

    def __init__(self, jobconf):
        self.jobconf = jobconf
        self.protocol = jobconf["url"]["url.protocol"]
        self.keywords = jobconf["parse"]["parse.match.keyword"].split(",")
        self.base_type = jobconf["base"]["type"]
        self.sub_type = jobconf["base"]["sub_type"]
        self.dtype = f"{self.base_type}_{self.sub_type}"
        self.alter_type = jobconf["alter"]["alter.type"]
        self.to_addrs = jobconf["alter"]["alter.mail.toaddrs"]
        self.error_addrs = jobconf["alter"]["alter.mail.error.addrs"]
        self.zh_type = ""
        self.crux_key = ''
        if "run_interval" in jobconf["others"] and jobconf["others"]["run_interval"]:
            self.run_interval = int(jobconf["others"]["run_interval"])
        else:
            self.run_interval = 1800

        if "proxies.http" in jobconf["proxy"] and jobconf["proxy"]["proxies.http"]:
            self.proxies = {
                'http': f'{jobconf["proxy"]["proxies.http"]}',
                'https': f'{jobconf["proxy"]["proxies.https"]}'
            }
        else:
            self.proxies = None

        self.tor_enable = False
        if "tor" in jobconf:
            self.tor_enable = jobconf["tor"]["enable"] == "True" or jobconf["tor"]["enable"] == "true"
            if self.tor_enable:
                self.firefox_binary = jobconf["tor"]["firefox.binary.path"]
                self.geckodriver_path = jobconf["tor"]["geckodriver.path"]
                self.headless = jobconf["tor"]["headless"] == "True" or jobconf["tor"]["headless"] == "true"

    def print_arguments(self):
        logger.info('\n'.join((f"{k}={v}" for k, v in self.__dict__.items())))

    def get_header(self):
        pass

    def new_session(self):
        session = requests_html.HTMLSession()
        session.headers = self.get_header()
        session.timeout = 30
        session.verify = False
        self.session = session

    def get(self, path: str, params: dict = None, cookies: str = "", auth_header: str = "", is_clear_cookies=False,
            is_abs_path=False, **kwargs):
        if cookies:
            self.session.headers['Cookie'] = cookies
        if is_clear_cookies:
            self.session.headers.pop('Cookie', None)

        if auth_header:
            self.session.headers['Authorization'] = auth_header

        if is_abs_path:
            req_path = path
        else:
            req_path = urljoin(self.index_url, path)

        logger.info(f"[GET METHOD] headers is : {self.session.headers}")
        logger.info(f"[GET METHOD] request url = {req_path}")
        logger.info(f"[GET METHOD] request proxy = {self.proxies}")
        logger.info(f"[GET METHOD] request params = {params}")
        resp = self.session.get(req_path, params=params, proxies=self.proxies, **kwargs)
        resp.encoding = "utf8"
        return resp


    def get_download(self, path: str, params: dict = None, cookies: str = "", auth_header: str = "", is_clear_cookies=False,
            is_abs_path=False, **kwargs):
        if cookies:
            self.session.headers['Cookie'] = cookies
        if is_clear_cookies:
            self.session.headers.pop('Cookie', None)

        if auth_header:
            self.session.headers['Authorization'] = auth_header

        if is_abs_path:
            req_path = path
        else:
            req_path = urljoin(self.index_url, path)

        logger.info(f"[GET METHOD] headers is : {self.session.headers}")
        logger.info(f"[GET METHOD] request url = {req_path}")
        logger.info(f"[GET METHOD] request proxy = {self.proxies}")
        logger.info(f"[GET METHOD] request params = {params}")
        resp = self.session.get(req_path, params=params, proxies=self.proxies)
        img_path_name = kwargs['img_name']
        with open(img_path_name, 'wb') as f:
            f.write(resp.content)
            f.flush()
            f.close()
        #resp.encoding = "utf8"
        #return resp

    def post(self, path, data: dict = None, json: dict = None, cookies: str = "", is_abs_path=False, **kwargs):
        if cookies:
            self.session.headers['Cookie'] = cookies

        if is_abs_path:
            req_path = path
        else:
            req_path = urljoin(self.index_url, path)

        logger.info(f"[POST METHOD] headers is : {self.session.headers}")
        logger.info(f"[POST METHOD] request url = {req_path}")
        logger.info(f"[POST METHOD] request proxy = {self.proxies}")
        logger.info(f"[POST METHOD] data is :{data}")
        resp = self.session.post(
            req_path,
            data=data,
            json=json,
            proxies=self.proxies,
            **kwargs,
        )
        resp.encoding = "utf8"
        return resp

    '''
    发送kafka消息
    '''

    def send_kafka_producer(self, send_data_li, dark_type):
        kafka_conf_file = os.path.join(get_root_path(), "conf/application.conf")
        job_conf = CrawlConfigParser()
        job_conf.read(kafka_conf_file)
        topic = job_conf["kafka"]["event.topic"]
        crawler_producer = CrawlerProducer(job_conf, topic)
        millis = int(round(time.time() * 1000))

        result_scan_mes_json = {"message_id": dark_type + "_" + str(millis), "type": dark_type,
                                "timestamp": str(millis), "data": send_data_li}
        crawler_producer.async_producer(result_scan_mes_json)

    def send_error_email(self, error_info, resp):
        msg = error_info
        if resp:
            msg = f"{error_info} \n {resp.html.html}"
        logger.error(msg)
        # CrawlService.send_alert(crawl_pd=None, keyword=self.keywords, zh_type=self.zh_type, to_addrs=self.error_addrs,
        #                         error_msg=msg)

    # 查询数据库获取关键字
    def query_db_for_curl(self, task_id):
        task_service = MonitorTaskService()
        task_detail = task_service.monitor_task_detail_id(task_id)
        if task_detail == None:
            return ''
        fileContent = task_detail.fileContent
        keywords = fileContent.split(",")
        self.crux_key = keywords

    def sample_datas_convert(self, id_millis, ocr_result):
        if ocr_result is None:
            return
        sample_datas = []
        for res in ocr_result:
            if res is None:
                break
            sample_datas.append({
                "original_event_id": id_millis,
                "tenant_id": "zhnormal",
                "phone_num": "",
                "bind_id": "",
                "user_name": "",
                "user_id": "",
                "identity_id": "",
                "home_addr": "",
                "original_data": res
            })
        return sample_datas


   # TODO 打开tor浏览器驱动,使用驱动截取图片
    def screenshot(self, href):
        logger.info("使用TOR浏览器登录")
        # 1、初始化driver
        try:
            self.driver = connect_tor_with_retry(self.firefox_binary, self.geckodriver_path, self.proxies,
                                                 self.headless)
            # 2、 请求主页
            # self.driver.get(self.index_url)

            # start
            self.driver.get(href)
            # 通过执行脚本，设置滚动条到最大宽度及最大高度
            width = self.driver.execute_script("return document.documentElement.scrollWidth")
            height = self.driver.execute_script("return document.documentElement.scrollHeight")
            self.driver.set_window_size(width, height)
            # 是否需要超时等待
            time.sleep(1000)
            # 保存的截图名字
            current_milli_time = int(round(time.time() * 1000))
            pic_name = str(current_milli_time) + '__screenshot.png'
            self.driver.save_screenshot(pic_name)
            return pic_name
            # end
        except Exception as e:
            logger.warning("screenshot failed,close driver", e)
            self.driver.quit()
            return None

        finally:
            if self.driver:
                self.driver.quit()

    def strToBase64(self, text):
        '''
        将字符串转换为base64字符串
        :param s:
        :return:
        '''
        strEncode = base64.b64encode(text.encode('utf8'))
        return str(strEncode, encoding='utf8')
