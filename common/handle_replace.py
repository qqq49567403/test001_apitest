"""
======================
Author: songs
Time: 2021-11-07
Project: handle_replace
Company: 软件自动化测试
======================
"""
import re

from common.handle_data import Data
from common.handle_logger import logger
from common.handle_yaml import HandleYmal
from common.handle_phone import get_new_phone


def data_replacement(cases_dict):
    # 读取yaml中的数据
    global_data = HandleYmal("data.yaml").data
    # 将用例数据转成字符串
    cases_str = str(cases_dict)
    # 正则提取
    data_mark_list = re.findall("#(\w+)#", cases_str)
    logger.info(f"正则提取的数据为：{data_mark_list}")

    if "phone" in data_mark_list:
        logger.info("有phone'字段，需要生成一个新的未注册收集号码，并设置到Data类中")
        get_new_phone()

    if data_mark_list:
        for mark in data_mark_list:
            # 数据读取yaml
            if mark in global_data.keys():
                cases_str = cases_str.replace(f"#{mark}#", str(global_data[mark]))
                logger.info(f"从data.yaml中进行替换的数据为：{mark}，替换后的数据为：{global_data[mark]}")
            else:
                cases_str = cases_str.replace(f"#{mark}#", getattr(Data, mark))
                logger.info(f"从Data类中进行替换的数据为：#{mark}#，替换后的数据为：{getattr(Data, mark)}")

    logger.info(f"替换之后的数据为：{cases_str}")
    return eval(cases_str)

