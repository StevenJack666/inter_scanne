#!/usr/bin/env python
# coding=utf-8
import os
import parse
import re
import time
import ddddocr

from ocr_handler.cnocr.ocr_base import *
from http.client import RemoteDisconnected
from urllib.parse import urljoin
from urllib.parse import urlparse
from requests import RequestException
from retry import retry
from tools.tor_tool import make_new_tor_id
from handler.base_handler import BaseHandler
import traceback
from tools.type_enum import DarkType
from service.task_model_service import *
from datetime import datetime
from tools.config import  *

class DarkNetTradingNet(BaseHandler):
    is_login: bool = False
    session_id: str = ""
    session_key = "PHPSESSID"
    page_link_dict: dict = dict()

    def __init__(self, jobconf):
        super(DarkNetTradingNet, self).__init__(jobconf)
        self.tor_port = int(jobconf["proxy"]["tor.port"])
        self.username = jobconf["login"]["login.name"]
        self.passwd = jobconf["login"]["login.passwd"]
        self.login_cookies_str_format = jobconf["login"]["login.cookies.format"]
        self.query_cookies_str_format = jobconf["login"]["query.cookies.format"]
        self.max_pagenum = int(jobconf["parse"]["parse.max.pagenum"])
        self.domains = jobconf["url"]["url.domain"].split(",")
        self.zh_type = "暗网中文网"

    '''
    设置session请求头
    '''

    def get_header(self):
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Host": self.domain,
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }

    def download_image(self, img_resp_content, img_file_path):
        with open(img_file_path, "wb") as f:
            f.write(img_resp_content)

    def parse_captcha(self, img_file_path):
        with open(img_file_path, 'rb') as f:
            img_bytes = f.read()

        ocr = ddddocr.DdddOcr()
        captcha = ocr.classification(img_bytes)
        captcha = "".join(re.findall("[0-9a-zA-Z]", captcha)).upper()
        return captcha

    def get_captcha_and_session(self):
        session_resp = self.get(self.login_path, is_get_session=True)
        logger.info(f"capthca session cookies is {session_resp.cookies}")
        self.session_id = session_resp.cookies[self.session_key]

        captcha_cookies = self.login_cookies_str_format % self.session_id
        captcha_resp = self.get(self.captcha_path, cookies=captcha_cookies)

        img_dir = Config.img_dir
        if not os.path.exists(img_dir):
            os.mkdir(img_dir)
        img_file_path = os.path.join(img_dir, self.session_id + ".png")

        self.download_image(captcha_resp.content, img_file_path)
        self.captcha = self.parse_captcha(img_file_path)
        self.print_arguments()

    def check_is_login(self, resp):
        return '退出' == resp.html.find("div.div_navigate_welcome a")[-1].text

    def enter_request(self):
        logger.info("step1: request enter url")
        resp = self.get("", is_clear_cookies=True)
        if not resp.cookies:
            logger.error("step1 response cookies is empty")
            raise ValueError("response cookies is empty")
        logger.info(f"resp cookies is {resp.cookies}")
        self.session_id = resp.cookies[self.session_key]

        for a_link in resp.html.find("a"):
            if a_link.text == '账户登录':
                return a_link.attrs['href']

    '''
    获取登陆链接
    '''

    @retry((RequestException, RemoteDisconnected), tries=5, delay=20, logger=logger)
    def login_request(self, url, login_cookies):
        logger.info("step2: request login url")
        resp = self.get(url, cookies=login_cookies)
        for a_link in resp.html.find("a"):
            if "entranceLogin.php" in a_link.attrs['href']:
                return a_link.attrs['href']

    """
    获取账户登陆地址
    """

    @retry((RequestException, RemoteDisconnected), tries=5, delay=20, logger=logger)
    def account_login_url_request(self, url, login_cookies):
        logger.info("step3: request account_login_url")
        resp = self.get(url, cookies=login_cookies)
        return resp.html.find("form", first=True).attrs['action']

    @retry((RequestException, RemoteDisconnected), tries=5, delay=20, logger=logger)
    def account_post_request(self, url, login_cookies):
        logger.info("step4: request account_input_url")
        post_data = dict()
        post_data['submit_login_id'] = self.username
        post_data['login_id_submit'] = '下一步'
        resp = self.post(url, data=post_data, cookies=login_cookies)
        return resp.html.find("form", first=True).attrs['action']

    """
    发送post请求
    """

    @retry((RequestException, RemoteDisconnected), tries=5, delay=20, logger=logger)
    def passwd_post_request(self, url, login_cookies):
        logger.info("step5: request passwd_input_url")
        post_data = dict()
        post_data['login_password'] = self.passwd
        post_data['login_password_submit'] = '下一步'
        resp = self.post(url, data=post_data, cookies=login_cookies)
        url_content = resp.html.find("meta", first=True).attrs['content']
        return url_content[url_content.index("URL=") + len("URL="):]

    def update_domain_info(self, url):
        logger.info("step6: update domain info")
        url_parse_ans = urlparse(url)
        self.domain = url_parse_ans.netloc
        self.index_url = f"{url_parse_ans.scheme}://{self.domain}"
        self.session.headers['Host'] = self.domain
        logger.info(f"new index is {self.index_url}")
        logger.info(f"new headers is {self.session.headers}")

    @retry((RequestException, RemoteDisconnected), tries=5, delay=20, logger=logger)
    def redirect_passwd_request(self, url):
        logger.info("step7: request redirect_passwd_request url:{}", url)
        resp = self.get(url, is_clear_cookies=True, is_abs_path=True)
        self.session_id = resp.cookies['PHPSESSID']
        return resp.html.find("form", first=True).attrs['action']

    @retry((RequestException, RemoteDisconnected), tries=5, delay=20, logger=logger)
    def passwd_again_post_request(self, url, login_cookies):
        logger.info("step8: request double_passwd_input_url")
        post_data = dict()
        post_data['login_password'] = self.passwd
        post_data['login_password_submit'] = '下一步'
        resp = self.post(url, data=post_data, cookies=login_cookies)
        return resp

    """
    暗网中文网登陆
    获取爬取的第一页链接
    """

    @retry(exceptions=ValueError, tries=5, delay=20, logger=logger)
    def login(self):
        if self.is_login:
            return
        self.new_session()
        login_url = self.enter_request()
        login_cookies = self.login_cookies_str_format % self.session_id
        logger.info(f"login cookies is {login_cookies}")
        account_login_url = self.login_request(login_url, login_cookies)
        account_input_url = self.account_login_url_request(account_login_url, login_cookies)
        passwd_input_url = self.account_post_request(account_input_url, login_cookies)
        login_check_url = self.passwd_post_request(passwd_input_url, login_cookies)
        self.update_domain_info(login_check_url)
        double_passwd_input_url = self.redirect_passwd_request(login_check_url)
        query_cookies = self.query_cookies_str_format % (self.session_id, self.username)
        logger.info(f"query cookies is {query_cookies}")
        resp = self.passwd_again_post_request(double_passwd_input_url, query_cookies)
        if '退出' != resp.html.find("div.div_navigate_welcome a")[-1].text:
            logger.error(f"登录失败")
            raise ValueError("登录失败")
        # 获取数据与信息页面链接,作为第一页的链接
        query_target_url = resp.html.find("table.table_ad_b td")[0].links.pop()
        self.page_link_dict["1"] = query_target_url
        logger.info(f"page link dict 1 page num is {self.page_link_dict}")
        self.is_login = True
        logger.info("登录成功")

    """
    解析获取每页URL
    """

    def parse_page_url(self, resp):
        page_button_links = resp.html.find("table.table_goods_area a.href_button_page")
        for page_link in page_button_links:
            self.page_link_dict[page_link.text] = page_link.links.pop()
        logger.info(f"page link dict is {self.page_link_dict}")

    """
    初始化会话信息：使用Tor网站，解决网站IP封禁问题
    """

    def get_all_types(self):
        if not self.is_login:
            return
        if not self.session:
            self.new_session()

        # 解析多页数据
        for page_num in range(1, self.max_pagenum):
            page_link = self.page_link_dict.get(str(page_num))
            if page_link:
                self.get_single_type(page_link, page=str(page_num))

    @retry((RequestException, RemoteDisconnected), tries=5, delay=20, logger=logger)
    def parse_order_first_page(self, page_link: str = ""):
        logger.info(f"parse order page,url={page_link}")
        query_cookies = self.query_cookies_str_format % (self.session_id, self.username)
        resp = self.get(page_link, cookies=query_cookies)
        publish_order_url = resp.html.find("table.table_goods_area > tr")[0].find("a", first=True).links.pop()
        resp_order = self.get(publish_order_url, cookies=query_cookies)
        self.parse_page_url(resp_order)

    """
    获取列表页和详情页对应属性信息
    并插入数据
    """
    def get_single_type(self, page_link: str = "", page: str = ""):
        crux_key_tmp = ''
        logger.info(f"parse page={page},url={page_link}")
        send_data_li = []
        dark_type = DarkType.darknet.value
        for idx, datas in enumerate(self.parse_list(page_link)):
            href = datas.get("href")
            parse_tag = f"{page}_{idx}"
            try:
                detail = self.parse_detail(href, parse_tag)
                self.query_db_for_curl(self.task_id)
                for value in self.crux_key:
                    if value in datas.get("title"):
                        crux_key_tmp = value
                    break
                # 生成主键id
                id_millis = str(int(round(time.time() * 1000)))
                sample_datas, paths = self.ocr_scan(id_millis, detail['image_list'])
                # todo 字段补齐
                send_data_li.append({
                    "id": id_millis,
                    "tenant_id": "zhnormal",
                    "doc_id": detail.get("docid"),
                    "content_title": datas.get("title"),
                    "publish_time": self.time_convert(detail.get("publish_time")),
                    "data_link": urljoin(self.index_url, href),
                    "publisher": datas.get("user"),
                    "publisher_id": "",
                    "crux_key": crux_key_tmp,
                    "doc_desc": "",
                    "origin_data": "",
                    "image_path": paths,
                    "crawl_dark_type": self.dtype,
                    "href_name": f"{page}页{idx}行",
                    "sample_datas": sample_datas
                })
                self.send_kafka_producer(send_data_li, dark_type)
            except Exception as e:
                trace_msg = traceback.format_exc()
                logger.error(f"[parse error {href},{datas}, {e} ; trace {trace_msg}")


    def ocr_scan(self, id_millis, image_paths):
        sample_datas = []
        paths = ''
        ocr_image = OcrImage()
        for image in image_paths:
            path = image['img_name']
            ocr_result = ocr_image.ocr_for_single_lines(path)
            sample_datas_tmp = self.sample_datas_convert(id_millis, ocr_result)
            paths = f'{path},{paths}'
            sample_datas.extend(sample_datas_tmp)
        return sample_datas, paths
    '''
    时间转化毫秒时间戳
    '''

    def time_convert(self, publish_time):
        # 将字符串转换为 datetime 对象
        time_obj = datetime.strptime(publish_time, "%Y-%m-%d")
        # 将 datetime 对象转换为时间戳
        publish_time_stamp = int(time_obj.timestamp() * 1000)
        return publish_time_stamp

    '''
    解析列表信息，并获取对应字段值    
    '''

    @retry((RequestException, RemoteDisconnected), tries=5, delay=20, logger=logger)
    def parse_list(self, list_url):
        query_cookies = self.query_cookies_str_format % (self.session_id, self.username)
        resp_origin = self.get(list_url, cookies=query_cookies)
        # 首先请求按照发布时间排序页面
        publish_order_url = resp_origin.html.find("table.table_goods_area > tr")[0].find("a", first=True).links.pop()
        resp = self.get(publish_order_url, cookies=query_cookies)
        self.parse_page_url(resp)
        try:
            trs = resp.html.find("table.table_goods_area > tr")[3:-1][::2]
            result = []
            for tr in trs:
                href = tr.pq("td:nth-child(3) a").attr["href"]
                result.append(
                    {
                        "href": href,
                        "user": tr.pq("td:nth-child(2)").text(),
                        "title": tr.pq("td:nth-child(3)").text(),
                        "priceBTC": tr.pq("td:nth-child(5)").text(),
                        "doc_desc": tr.pq("td:nth-child(5)").text(),
                    },
                )
            return result
        except Exception as e:
            logger.error(f"parse list info error:{e}")
            return []

    """
    解析详情页信息
    """

    @retry((RequestException, RemoteDisconnected), tries=5, delay=20, logger=logger)
    def parse_detail(self, detail_url, parse_tag):
        logger.info(f"parse parse_tag={parse_tag}, url={detail_url}")
        query_cookies = self.query_cookies_str_format % (self.session_id, self.username)
        resp = self.get(detail_url, cookies=query_cookies)
        try:
            detail_tds = resp.html.find("table.table_view_goods td")
            image_path = resp.html.find("div.div_view_goods_reply div img")
            ans = dict()
            ans["docid"] = self.find_match_value("交易编号", detail_tds)
            ans["publish_time"] = self.find_match_value("上架日期", detail_tds)
            ans["image_list"] = self.find_match_image(image_path)
            return ans
        except Exception as e:
            logger.error(f"parse detail info error:{e}")
            return dict()

    @staticmethod
    def find_match_value(value, items):
        for i, item in enumerate(items):
            if value in item.text:
                index = i + 1
                if index < len(items):
                    return items[index].text
        return ""



    #下载图片
    def find_match_image(self, items):
        image_list = []
        for i, item in enumerate(items):
            img_path = item.attrs.get('src')
            img_name = item.attrs.get('alt')
            image_all_path = f'{get_root_path()}data/image/darknet/{img_name}'
            image = {"img_path": img_path,
                     "img_name": image_all_path
                     }
            query_cookies = self.query_cookies_str_format % (self.session_id, self.username)
            self.get_download(img_path, query_cookies, is_abs_path=True, img_name=image_all_path)
            image_list.append(image.copy())
        return image_list


    def run(self, *args, **kwargs):
        self.task_id = kwargs['id']
        self.print_arguments()
        make_new_tor_id(self.tor_port)
        domain_available = False
        error_domain_exceptions = []
        for domain in self.domains:
            if not domain_available:
                self.domain = domain
                self.index_url = f"{self.protocol}://{self.domain}"
                logger.info(f"parse domain is {self.domain}, index_url is {self.index_url}")
                try:
                    self.login()
                    domain_available = True
                except Exception as e:
                    error_domain_exceptions.append(f"暗网中文网使用域名{self.domain}错误,异常信息:{e}")
                    domain_available = False
        if domain_available:
            self.get_all_types()
            '''
            关键字匹配，发送告警邮件
         
            CrawlService.match_crawl_info(self.keywords, self.dtype, self.to_addrs, self.zh_type, send_dict= {
                "title": "标题",
                "publish_time": "发布时间",
                "publisher": "发布人",
                "docid": "交易编号",
            })
            '''
        else:
            self.send_error_email(f"暗网中文网爬虫错误,异常信息:{error_domain_exceptions}", None)

    def run_forever(self):
        self.print_arguments()
        logger.error("暗网中文网不支持forever模式")
        raise ValueError("暗网中文网不支持forever模式")

    # 测试专用方法
    def set_is_login(self):
        self.is_login = True
        self.session_id = "699n41p2s5ejc586c5kcjovmpk"


if __name__ == "__main__":
    id_millis = int(round(time.time() * 1000))
    print(id_millis)
    cur_dirname = os.path.dirname(os.path.abspath(__file__))
    conf_file = os.path.join(cur_dirname, "../../darknet.conf")
    from tools.config_parser import CrawlConfigParser

    jobconf = CrawlConfigParser()
    jobconf.read(conf_file)
    DarkNetTradingNet(jobconf).run()
