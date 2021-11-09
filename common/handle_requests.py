"""
======================
Author: songs
Time: 2021-10-18
Project: requests
Company: 软件自动化测试
======================
"""

import requests
import json

from common.handle_logger import logger
from common.handle_conf import conf


class HandleRequests:
    def __init__(self):
        self.headers = {"X-Lemonban-Media-Type": "lemonban.v2"}

    # 处理请求头数据
    def __deal_token(self, token=None):
        # 判断token是否为空
        if token is not None:
            self.headers["Authorization"] = "Bearer {}".format(token)

    # 处理请求数据
    def __deal_data(self, data):
        # 判断data是不是str类型
        if isinstance(data, str):
            # 将json转换成字典
            self.data = json.loads(data)
        else:
            self.data = data
        logger.info(f"请求数据为: {self.data}")

    # 处理请求dul
    def __deal_url(self, url):
        base_url = conf.get("server", "baseurl")
        url = base_url + url
        return url

    # 发送请求
    def send_requests(self, method, url, data=None, token=None):
        logger.info("=====  发送一次http请求  =====")
        logger.info(f"请求的method为：{method}")
        logger.info(f"请求的url为：{url}")
        url = self.__deal_url(url)
        self.__deal_data(data)
        self.__deal_token(token)
        if method.upper() == "GET":
            response = requests.get(url, params=self.data, headers=self.headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=self.data, headers=self.headers)
        else:
            response = requests.patch(url, json=self.data, headers=self.headers)
        logger.info(f"响应code为：{response.status_code}")
        logger.info(f"响应的msg为：{response.json()}")
        return response


if __name__ == '__main__':
    ss = HandleRequests()
    url = "http://api.lemonban.com/futureloan/member/login"
    data = {"mobile_phone": "18557519118", "pwd": "123456789"}
    response = ss.send_requests('post', url, data)
