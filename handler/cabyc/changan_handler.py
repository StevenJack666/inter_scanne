#!/usr/bin/env python
# coding=utf-8
import logging
import os
import math
import gzip
import time
import json
import base64
from tools.captcha_code_tool import request_captcha_code
from urllib.parse import urljoin
from handler.base_handler import BaseHandler
from datetime import datetime
from tools.config import CrawlRuntimeException
from tools.config import Config
from tools.config import get_root_path
from requests import RequestException
from retry import retry
from tools.log import logger
from tools.tor_tool import connect_tor_with_retry
from http.client import RemoteDisconnected
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tools.type_enum import DarkType
import traceback


class ChangAn(BaseHandler):
    good_detail_suffix = '/#/detail?gid=%s'

    def __init__(self, jobconf):
        super(ChangAn, self).__init__(jobconf)
        self.auth_header = jobconf["url"]["url.auth.header"]
        self.max_pagenum = int(jobconf["parse"]["parse.max.pagenum"])
        self.query_path = jobconf["url"]["url.query.path"]
        self.domain = jobconf["url"]["url.domain"]
        self.index_url = f"{self.protocol}://{self.domain}"
        self.zh_type = "长安不夜城"
        self.username = jobconf["login"]["login.name"]
        self.passwd = jobconf["login"]["login.passwd"]
        self.query_cookies_str_format = jobconf["login"]["query.cookies.format"]
        self.detail_query_path = jobconf["url"]["detail.query.path"]
    """
    打开tor浏览器驱动
    使用驱动请求首页
    
    """

    def login_with_tor_headless(self):
        logger.info("使用TOR浏览器登录")
        # 1、初始化driver
        try:
            self.driver = connect_tor_with_retry(self.firefox_binary, self.geckodriver_path, self.proxies,
                                                 self.headless)
            # 2、 请求主页
            self.driver.get(self.index_url)
            # 3、登录校验并解析token
            return self.check_and_login()
        finally:
            if self.driver:
                self.driver.quit()

    def check_and_login(self):
        logger.info(f"step 1: login check")
        self.check()
        logger.info(f"step 2: login")
        self.login()
        logger.info(f"step 3: parse token")
        login_res_json = self.parse_token()
        parse_num = 5
        while login_res_json and parse_num > 0:
            logger.info(f"login request result is {login_res_json}")
            login_res_code = login_res_json.get("code")
            if login_res_code == 4002 or login_res_code == 4006:
                # 重新输入验证码和用户名登录
                parse_num = parse_num - 1
                logger.info(f"return code is {login_res_code}, login again")
                self.login()
                login_res_json = self.parse_token()
            elif login_res_code == 4087:
                # 错误次数过多,重新回到login check 步骤登录
                parse_num = parse_num - 1
                logger.info(f"return code is {login_res_code}, check and login again")
                self.check()
                self.login()
                login_res_json = self.parse_token()
            elif login_res_code == 2000:
                # 登录成功
                token = login_res_json.get("data").get("token")
                self.auth_header = self.query_cookies_str_format % token
                logger.info(f"login success, token is {self.auth_header}")
                return True

        logger.error("login failed, use backup token is {self.auth_header}")
        return False

    def login(self):
        # 等待不夜城的提示框出现并关闭它
        info_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".el-button--small")))
        info_button.click()
        # 加载验证码
        image_data = self.load_captcha_image(is_for_login=True)
        # 请求打码平台识别验证码
        captcha_code = request_captcha_code(image_data)
        # 输入账号密码验证码
        user_name_input = self.driver.find_element(By.CSS_SELECTOR,
                                                   'div.el-form-item:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)')
        # 清空输入框,防止重试时重复输入
        user_name_input.clear()
        # 循环输入字符,防止出现字符丢失的bug
        for onechar in self.username:
            user_name_input.send_keys(onechar)

        pass_word_input = self.driver.find_element(By.CSS_SELECTOR, '.m-input > input:nth-child(1)')
        pass_word_input.clear()
        for onechar in self.passwd:
            pass_word_input.send_keys(onechar)

        capture_input = self.driver.find_element(By.CSS_SELECTOR,
                                                 'div.el-form-item:nth-child(3) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)')
        capture_input.clear()
        for onechar in captcha_code:
            capture_input.send_keys(onechar)
        # 点击登录
        time.sleep(5)
        login_button = self.driver.find_element(By.CSS_SELECTOR, 'button.operate:nth-child(1)')
        login_button.click()

    @retry(CrawlRuntimeException, tries=5, delay=2, logger=logger)
    def parse_token(self):
        """
        解析登录请求的请求体，获取其返回值
        由于请求发送后有延迟，所以需要使用重试
        :return:
        """
        login_res_json = None
        for request in self.driver.requests:
            if request.response and "/api/account/login" in request.path:
                login_res_json = json.loads(gzip.decompress(request.response.body))
        if not login_res_json:
            # 如果没有解析出来请求结果，则等待2秒,重试的原因是：发送请求之后有延迟，导致driver没拦截到请求
            logger.warning("can not get login result, retry")
            raise CrawlRuntimeException("can not get login result, retry")
        return login_res_json

    """
    提取验证码，登陆验证
    """
    @retry(CrawlRuntimeException, tries=5, delay=20, logger=logger)
    def check(self):
        """
        处理登录校验页面,需要输入验证码,然后点击校验按钮发送校验请求
        :return:
        """
        # 加载验证码
        image_data = self.load_captcha_image(is_for_login=False)
        # 访问主页时可能会执行JS失败,因此需要重新访问
        retry_num = 5
        while (not image_data) and retry_num > 0:
            logger.warning(f"image load failed, retry={retry_num}")
            retry_num = retry_num - 1
            time.sleep(2)
            self.driver.get(self.index_url)
            image_data = self.load_captcha_image(is_for_login=False)

        if not image_data:
            logger.error("check error , can not get captcha image")
            now_time = int(time.time() * 1000)
            self.driver.save_screenshot(os.path.join(Config.img_dir, f"{now_time}.png"))
            raise Exception("check error , can not get captcha image")

        # 请求打码平台识别验证码
        captcha_code = request_captcha_code(image_data)
        # 请求登录验证页面,输入验证码点击进入到登录页面
        check_success = self.click_check_button(captcha_code)
        if not check_success:
            # 如果登录失败,则抛出异常后重试
            logger.warning("check failed, retry")
            raise CrawlRuntimeException("check failed, retry")

        return check_success

    def click_check_button(self, captcha_code):
        """
        输入验证码，点击校验按钮，发送校验请求
        :param captcha_code: 发送请求的验证码码
        :return:
        """
        logger.info(f"captcha code is {captcha_code}")
        # 等待输入框元素出现
        input_element = WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.el-input:nth-child(2) > input:nth-child(1)'))
        )
        # 填入值
        input_element.clear()
        # 循环输入字符,防止出现字符丢失的bug
        for onechar in captcha_code:
            input_element.send_keys(onechar);
        # 等待5s后提交
        time.sleep(5)
        # 等待提交按钮元素出现
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.el-button'))
        )
        # 点击提交按钮
        submit_button.click()
        # 等待5s后检测请求是否成功
        time.sleep(5)
        check_success = False
        for request in self.driver.requests:
            if request.response:
                if "/api/loginChecking" in request.path:
                    login_check_res_json = json.loads(gzip.decompress(request.response.body))
                    login_check_res_msg = login_check_res_json.get("data")
                    if "noLogin_" in login_check_res_msg:
                        check_success = True
        return check_success

    def load_captcha_image(self, is_for_login):
        """
        加载验证码
        :param is_for_login: 登录校验验证码和登录验证码,请求不一样
        :return:
        """
        image_data = None
        image_load = False
        retry_num = 5
        while (not image_load) and retry_num > 0:
            try:
                # 元素存在，执行某个动作
                element = self.driver.find_element(By.CSS_SELECTOR, '.el-image__inner')
                image_data = self.parse_captcha_image(is_for_login)
                image_load = True
            except NoSuchElementException:
                # 元素不存在，等待30后重试
                logger.info(f"captcha image not exists , retry")
                time.sleep(30)
                retry_num = retry_num - 1
        return image_data

    """
    解析验证码内容
    """

    def parse_captcha_image(self, is_for_login=False):
        """
        过滤获取验证码的请求，解析请求体获得图片信息
        :param is_for_login: 是否是登录验证码(登录校验验证码和登录验证码的请求不一样)
        :return:
        """
        image_res = None
        for request in self.driver.requests:
            if request.response:
                if "/api/public/captcha" in request.path:
                    if is_for_login and "Authorization" in request.headers:
                        logger.info(
                            f"is_for_login={is_for_login},request header url is {request.headers['Authorization']}")
                        image_res = request.response.body
                    elif (not is_for_login) and ("Authorization" not in request.headers):
                        logger.info(f"is_for_login={is_for_login}")
                        image_res = request.response.body

        image_data = None
        if image_res:
            decompressed_data = gzip.decompress(image_res)
            image_string = json.loads(decompressed_data).get("data").get("digits")
            # Base64编码的图片字符串
            base64_string = image_string.replace('data:image/png;base64,', '')
            # 解码Base64字符串为图像数据
            image_data = base64.b64decode(base64_string)
            logger.info(f"captcha image has decode success")

        return image_data

    '''
    设置session请求头
    '''

    def get_header(self):
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }

    def parse_max_pagenum(self, resp_json):
        if 'data' in resp_json:
            total_num = resp_json['data']['total']
            page_size = resp_json['data']['page_size']
            self.max_pagenum = math.ceil(total_num / page_size)
        logger.info(f"parse max page is {self.max_pagenum}")

    def get_all_types(self):
        self.get_single_type(query_path=self.query_path, page=1)
        for page_num in range(2, self.max_pagenum):
            self.get_single_type(query_path=self.query_path, page=page_num)

    """
    1.爬取数据
    2.爬取失败，匹配是否由命中关键字的数据，命中发送邮件
    3.爬取成功：数据标准化，插入数据库
    """

    @retry((RequestException, RemoteDisconnected), tries=5, delay=20, logger=logger)
    def get_single_type(self, query_path: str = "", page: int = 1):
        req_params = {
            "page_num": page,
            "page_size": 10,
            "order": "ctime",
            "order_by": "ascending"
        }
        resp = self.get(query_path, params=req_params, auth_header=self.auth_header)
        resp_json = json.loads(resp.text)
        if resp_json['code'] != 2000:
            logger.error(f"{resp_json}")
            # CrawlService.match_crawl_info(self.keywords, self.dtype, self.to_addrs, self.zh_type)
            err_msg = f"request code is {resp.status_code},please reset cookies,response={resp.html.html}"
            logger.error(err_msg)
            raise Exception(err_msg)

        if page == 1:
            self.parse_max_pagenum(resp_json)

        logger.info(f"parse page = {page} data")
        self.parse_summary(resp_json, page=page)
        # for s_data in self.parse_summary(resp_json, page=page):
        #     CrawlService.insert_crawl_info(s_data)

    """
    爬取数据标准化，准备入库
    """

    def parse_summary(self, resp_json, page: int = 0):
        crux_key_tmp = ''
        result = []
        dark_type = DarkType.chang_an.value
        if 'data' in resp_json:
            goods = resp_json['data']['goods']
            for idx, good in enumerate(goods):
                try:
                    good_id = good['id']
                    title = good['name']
                    publisher = good['owner']['name']
                    ctime = good['ctime']
                    description = good['intro']
                    time_local = time.gmtime(ctime)
                    publish_time_tmp = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                    time_tuple = time.strptime(publish_time_tmp, '%Y-%m-%d %H:%M:%S')
                    publish_time_timestamp = int(time.mktime(time_tuple)*1000)
                    href = urljoin(self.index_url, self.good_detail_suffix % good_id)
                    self.query_db_for_curl(self.task_id)
                    for value in self.crux_key:
                        if value in title:
                            crux_key_tmp = value
                            break
                    detail_data = self.get(self.detail_query_path + good_id, auth_header=self.auth_header)
                    resp_json_detail = json.loads(detail_data.content)
                    pic_list = resp_json_detail['data']['pics']
                    paths = ''
                    for pic_res in pic_list:
                        pic = pic_res.get('pic')
                        if pic is not None and len(pic) != 0:
                            last_slash_index = pic.rfind('/')
                            filename = pic[last_slash_index+1:]
                            image_path = f'{get_root_path()}data/image/changan/{filename}'
                            self.get_download(pic, auth_header=self.auth_header, img_name=image_path)
                            paths = f'{image_path},{paths}'
                    tmp_ori = resp_json_detail['data']['intro']
                    for value in self.crux_key:
                        if value in tmp_ori:
                            crux_key_tmp = value
                            break
                    id_millis = str(int(round(time.time() * 1000)))
                    result.append({
                        "id": id_millis,
                        "tenant_id": "zhnormal",
                        "doc_id": good_id,
                        "content_title": title,
                        "publish_time": publish_time_timestamp,
                        "data_link": href,
                        "publisher": publisher,
                        "publisher_id": "",
                        "crux_key": crux_key_tmp,
                        "origin_data": tmp_ori,
                        "image_path": paths,
                        "doc_desc": description,
                        "crawl_dark_type": self.dtype,
                        "href_name": f"{page}页{idx}行"
                    })
                    self.send_kafka_producer(result, dark_type)
                except Exception as e:
                    trace_msg = traceback.format_exc()
                    logger.exception(e)
                    logger.error(f"error page={page},error idx={idx}, trace_msg={trace_msg}")
        if len(result) == 0:
            logger.error(f"parse error, page={page}")

        return result

    def time_convert(self, publish_time):
        # 将字符串转换为 datetime 对象
        time_obj = datetime.strptime(publish_time, "%Y-%m-%d")
        # 将 datetime 对象转换为时间戳
        publish_time_stamp = int(time_obj.timestamp() * 1000)
        return publish_time_stamp

    def run(self, *args, **kwargs):
        self.task_id = kwargs['id']
        self.print_arguments()
        if self.tor_enable:
            if not self.login_with_tor_headless():
                self.send_error_email(f"长安不夜城登录失败,异常信息:", None)
        self.new_session()
        try:
            self.get_all_types()
        except Exception as e:
            self.send_error_email(f"长安不夜城爬虫错误,异常信息:{e}", None)
            return
        # CrawlService.match_crawl_info(self.keywords, self.dtype, self.to_addrs, self.zh_type)

    def run_forever(self):
        pass


if __name__ == "__main__":
    cur_dirname = os.path.dirname(os.path.abspath(__file__))
    conf_file = os.path.join(cur_dirname, "../../changan.conf")
    from tools.config_parser import CrawlConfigParser

    jobconf = CrawlConfigParser()
    jobconf.read(conf_file)
    ChangAn(jobconf).run()
