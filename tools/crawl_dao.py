#!/usr/bin/env python
# coding=utf-8


import datetime
from tools.log import *
from tools.model import CrawlInfo


class CrawlDao:
    @staticmethod
    @error_log()
    def insert_crawl_info(crawl_info):
        crawl_info_cnt = CrawlInfo.select(CrawlInfo.docid).where(CrawlInfo.docid == crawl_info.get("docid")).count()
        logger.debug(f"doc has insert")
        if crawl_info_cnt == 0:
            now = datetime.datetime.now()
            crawl_info["create_time"] = now
            crawl_info["update_time"] = now
            return CrawlInfo.create(**crawl_info)

    @staticmethod
    @error_log()
    def get_crawl_info_by_docid(docid):
        logger.info(f"docid is {docid}")
        return CrawlInfo.get(CrawlInfo.docid == docid)

    @staticmethod
    @error_log()
    def list_crawl_info_by_keyword(keyword, dtype, send_status = False):
        """
        按照关键字匹配文档-V1版本,根据title匹配
        :param keyword:
        :param dtype:
        :param send_status:
        :return:
        """
        logger.info(f"keyword is {keyword}, dtype is {dtype}")
        crawl_infos = CrawlInfo.select().where(
            CrawlInfo.title.contains(keyword),
            CrawlInfo.dtype == dtype,
            CrawlInfo.send_status == send_status
        )
        return list(crawl_infos.dicts())

    @staticmethod
    @error_log()
    def list_crawl_info_by_keyword_v2(keyword, dtype, send_status = False):
        """
        按照关键字匹配文档-V2版本,根据title和description匹配
        :param keyword:
        :param dtype:
        :param send_status:
        :return:
        """
        logger.info(f"keyword is {keyword}, dtype is {dtype}")
        crawl_infos = CrawlInfo.select().where(
            ((CrawlInfo.title.contains(keyword)) | (CrawlInfo.description.contains(keyword)))
            & (CrawlInfo.dtype == dtype) & (CrawlInfo.send_status == send_status)
        )
        return list(crawl_infos.dicts())

    @staticmethod
    @error_log()
    def batch_update_send_status(crawl_infos, send_status = True):
        ids = [crawl_info["id"] for crawl_info in crawl_infos]
        now = datetime.datetime.now()
        q = CrawlInfo.update(send_status = send_status, update_time = now).where(CrawlInfo.id.in_(ids))
        q.execute()
