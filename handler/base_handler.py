#!/usr/bin/env python
# coding=utf-8

import os
import requests_html

from tools.config import *
from tools.log import *
from urllib.parse import urljoin
from kafka_util.kafka_producer import CrawlerProducer
from tools.config_parser import CrawlConfigParser
from tools.config import get_root_path
from tools.crawl_service import CrawlService

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
    def send_kafka_producer(self, send_data_li):
        kafka_conf_file = os.path.join(get_root_path(), "conf/application.conf")
        job_conf = CrawlConfigParser()
        job_conf.read(kafka_conf_file)
        topic = job_conf["kafka"]["event.topic"]
        crawler_producer = CrawlerProducer(job_conf, topic)
        crawler_producer.async_producer(send_data_li)

    def send_error_email(self, error_info, resp):
        msg = error_info
        if resp:
            msg = f"{error_info} \n {resp.html.html}"
        logger.error(msg)
        CrawlService.send_alert(crawl_pd=None, keyword=self.keywords, zh_type=self.zh_type, to_addrs=self.error_addrs,
                                error_msg=msg)


