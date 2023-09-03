#!/usr/bin/env python
# coding=utf-8

from tools.crawl_dao import CrawlDao

import pandas as pd
import datetime
import os
from tools.config import Config
from tools.send_email import send_mail
from tools.log import *


class CrawlService:

    @staticmethod
    def match_crawl_info(keywords, dtype, to_addrs, zh_type, send_dict=None):
        now = datetime.datetime.now()
        match_all_infos = []
        for keyword in keywords:
            crawl_infos = CrawlDao.list_crawl_info_by_keyword_v2(keyword, dtype)
            match_all_infos.extend(crawl_infos)

        match_infos = CrawlService.remove_dup(match_all_infos)
        if len(match_infos) == 0:
            logger.error(f"未找到没发送的{dtype}类型的匹配{keywords}的告警信息")
            return

        excel_dir = os.path.join(Config.data_dir, "excel")
        if not os.path.exists(excel_dir):
            os.mkdir(excel_dir)
        file_name = f"{dtype}_{now}.xlsx"
        file_path = os.path.join(excel_dir, file_name)

        crawl_pd = pd.DataFrame(match_infos)
        rename_columns = send_dict
        if not rename_columns:
            rename_columns = {
                "title": "标题",
                "publish_time": "发布时间",
                "publisher": "发布人",
                "href": "链接",
                "description": "简介",
            }
        drop_columns = []
        for col_name in crawl_pd.columns:
            if col_name not in rename_columns:
                drop_columns.append(col_name)
        crawl_pd = crawl_pd.drop(columns=drop_columns)
        crawl_pd = crawl_pd.rename(columns=rename_columns)
        CrawlService.gen_excel(crawl_pd, file_path)
        CrawlService.send_alert(crawl_pd, keywords, zh_type, file_path, to_addrs)
        CrawlDao.batch_update_send_status(match_infos)

    @staticmethod
    def gen_excel(crawl_pd, file_path):
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
            crawl_pd.to_excel(writer)

    @staticmethod
    def send_alert(crawl_pd, keyword=None, zh_type: str = "", file_path="", to_addrs: str = "", error_msg=""):
        if keyword is None:
            keyword = []
        if crawl_pd is not None:
            subject = f"信息泄露监测报告-[{zh_type}]类型匹配结果"
            content = crawl_pd.to_html()
            message = f"""[{zh_type}]类型的匹配{keyword}的告警信息如下:
            
            {content}
            """
        else:
            subject = f"信息泄露监测异常-[{zh_type}]任务执行异常"
            message = error_msg

        sender_show = "信息泄露监测组"
        recipient_show = to_addrs
        to_addrs_str = to_addrs
        send_mail(message, subject, sender_show, recipient_show, to_addrs_str, attack_file=file_path)

    @staticmethod
    def insert_crawl_info(crawl_info):
        return CrawlDao.insert_crawl_info(crawl_info)

    @staticmethod
    def remove_dup(match_docs):
        match_dict = {doc["docid"]: doc for doc in match_docs}
        return match_dict.values()


if __name__ == "__main__":
    CrawlService.match_crawl_info(["数"], "darknet_trading_net", "zhangchaoss122@163.com", "测试不夜城", send_dict= {
        "title": "标题",
        "publish_time": "发布时间",
        "publisher": "发布人",
        "docid": "交易编号",
    })