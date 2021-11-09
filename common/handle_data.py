"""
======================
Author: songs
Time: 2021-11-07
Project: handle_data
Company: 软件自动化测试
======================
"""
from jsonpath import jsonpath


class Data:
    pass


def data_extraction(resp, extract):
    # 将读取的数据转成字典
    extract_dict = eval(extract)

    for key, value in extract_dict.items():
        real_value = jsonpath(resp, value)
        if real_value:
            setattr(Data, key, str(real_value[0]))
