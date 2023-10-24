#!/usr/bin/env python
# coding=utf-8

import os
import time
import hashlib
from urllib.parse import urljoin
from handler.base_handler import BaseHandler
from tools.crawl_service import CrawlService
from requests import RequestException
from retry import retry
from tools.log import logger
from bs4 import BeautifulSoup
from datetime import datetime

cur_dirname = os.path.dirname(os.path.abspath(__file__))

class BreachedTo(BaseHandler):
    def __init__(self, jobconf):
        super(BreachedTo, self).__init__(jobconf)
        self.cookies_key = jobconf["url"]["url.cookies.key"]
        self.max_pagenum = int(jobconf["parse"]["parse.max.pagenum"])
        self.query_params = jobconf["url"]["url.query.params"].split(",")
        self.zh_type = "breached中文论坛"

    def get_header(self):
        now_time_sec = str(int(time.time()))
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,nb;q=0.7",
            # "cookie":"mybb[announcements]=0; mybb[forumread]=a%3A1%3A%7Bi%3A3%3Bi%3A1665744559%3B%7D; mybb[threadread]=a%3A3%3A%7Bi%3A16284%3Bi%3A1665303055%3Bi%3A33093%3Bi%3A1665546210%3Bi%3A19928%3Bi%3A1665744877%3B%7D; sid=7d746dd9674b10e17aa610378e232991; mybb[lastvisit]=1665885861; cf_clearance=TpNdU.NpBtRfQ9kUcQCFbs_wTyaiyhYXQ6YZ4vjGRj0-1665903528-0-150; mybb[lastactive]=1665903662",
            "cookie": f"{self.cookies_key} mybb[lastactive]={now_time_sec}",
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        }

    
    def parse_max_pagenum(self, resp):
        html = BeautifulSoup(resp.content,'html.parser')
        pages = html.find_all("a", class_="pagination_page")
        parse_max_pagenum = int(pages[-1].string)
        if parse_max_pagenum > self.max_pagenum:
            self.max_pagenum = parse_max_pagenum
        logger.info(f"parse max page is {self.max_pagenum}")


    @retry((RequestException), delay=1)
    def get_all_types(self):
        for query_param in self.query_params:
            self.get_singel_type(query_param=query_param)
            for pagenum in range(2, self.max_pagenum):
                time.sleep(30)
                self.get_singel_type(query_param=query_param, page=pagenum)


    @retry((RequestException), delay=1)
    def get_singel_type(self, query_param: str="", page: int = 1):
        if page == 1:
            path = f"{query_param}?sortby=started"
        else:
            path = f"{query_param}?page={page}&sortby=started"

        resp = self.get(path, verify=False)
        if resp.status_code != 200:
            # check_resp = self.parse_check(resp)
            # if check_resp.status_code != 200:
            logger.error(f"{resp.status_code}")
            CrawlService.match_crawl_info(self.keywords, self.dtype, self.to_addrs, self.zh_type)
            self.send_error_email(f"request code is {resp.status_code},please reset cookies",resp)
            raise Exception("request error, reset cookies")

        if page == 1:
            self.parse_max_pagenum(resp)

        for s_data in self.parse_summary(resp, page=page):
            logger.info(f"parse page = {page} data")
            CrawlService.insert_crawl_info(s_data)
    

    def parse_summary(self, resp, page:int = 0):
        html = BeautifulSoup(resp.content,'html.parser')
        tds = html.find_all("td", class_="forumdisplay_regular")
        result = []
        for idx, td in enumerate(tds):
            try:
                if td.find("span", class_="subject_new"):
                    title = td.find("span", class_="subject_new").string
                    if td.find("span", class_="author smalltext").find("span"):
                        user = td.find("span", class_="author smalltext").find("span").string
                    else:
                        user = td.find("span", class_="author smalltext").string
                    create_time = td.find("span", class_="forum-display__thread-date").get_text()
                    href = td.find("span", class_="subject_new").find("a")['href']
                    docid = hashlib.md5(href.encode('utf-8')).hexdigest()
                    result.append({
                        "docid":docid,
                        "title":title,
                        "publisher" :user,
                        "publish_time":create_time,
                        "href": urljoin(self.index_url, href),
                        "dtype":self.dtype,
                    })
            except Exception as e:
                logger.exception(e)
                logger.error(f"error page={page},error idx={idx}")
        if len(result) == 0:
            logger.error(f"parse error, page={page}")
            self.send_error_email("parse error,  page={page}",resp)
        return result

    def parse_check(self, resp):
        check_html = BeautifulSoup(resp.content,'html.parser')
        check_path = check_html.find("form")["action"]
        check_data = {}
        for input in check_html.find("form").find_all("input"):
            check_data[input["name"]] = input["value"]
        resp = self.post(
            check_path,
            data=check_data
        )
        logger.info(resp.status_code)
        logger.info(resp.html.html)
        return resp


    def run(self):
        self.print_arguments()
        self.new_session()
        while True:
            self.get_all_types()
            CrawlService.match_crawl_info(self.keywords, self.dtype, self.to_addrs, self.zh_type)


if __name__ == "__main__":
    args = {
        "domain":"123"
    }
    try:
        BreachedTo(args).run()
    except Exception as e:
        raise e
