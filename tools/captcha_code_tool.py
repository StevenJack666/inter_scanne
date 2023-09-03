#!/usr/bin/env python
# coding=utf-8

import json
import os.path

from tools.log import *
from tools.config import Config
import requests
import base64
import time
from io import BytesIO
from PIL import Image

"""
提取图片中的验证码
"""

def request_captcha_code(image_data):
    begin_time = int(time.time() * 1000)
    # 创建BytesIO对象
    image_stream = BytesIO(image_data)
    # 打开图像
    image = Image.open(image_stream)
    # 保存图像到文件
    image.save(os.path.join(Config.img_dir, f"{begin_time}.png"))
    cap_verify = YdmVerify()
    cap_code = cap_verify.common_verify(image_data)
    end_time = int(time.time() * 1000)
    logger.info(f"request {begin_time}.png captcha code is {cap_code}, cost time is{end_time - begin_time}")
    return str(cap_code)


class YdmVerify(object):
    _custom_url = "http://api.jfbym.com/api/YmServer/customApi"
    _token = "nMBGHKC594pihTR3PGcURGYvfPrNEJn_ryNk7ps5M2M"
    _headers = {
        'Content-Type': 'application/json'
    }

    def common_verify(self, image, verify_type="50103"):
        # 数英汉字类型
        # 通用数英1-4位 10110
        # 通用数英5-8位 10111
        # 通用数英9~11位 10112
        # 通用数英12位及以上 10113
        # 通用数英1~6位plus 10103
        # 定制-数英5位~qcs 9001
        # 定制-纯数字4位 193
        # 中文类型
        # 通用中文字符1~2位 10114
        # 通用中文字符 3~5位 10115
        # 通用中文字符6~8位 10116
        # 通用中文字符9位及以上 10117
        # 中文字符 1~4位 plus 10118
        # 定制-XX西游苦行中文字符 10107
        # 计算类型
        # 通用数字计算题 50100
        # 通用中文计算题 50101
        # 定制-计算题 cni 452
        payload = {
            "image": base64.b64encode(image).decode(),
            "token": self._token,
            "type": verify_type
        }
        resp = requests.post(self._custom_url, headers=self._headers, data=json.dumps(payload))
        logger.info(f"request captcha platform ans is: {resp.text}")
        return resp.json()['data']['data']
