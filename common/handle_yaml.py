"""
======================
Author: songs
Time: 2021-11-07
Project: handle_yaml
Company: 软件自动化测试
======================
"""

import yaml
import os

from common.handle_path import conf_dir


class HandleYmal:
    def __init__(self, filename):
        # 继承父类的方法，传入文件参数
        path = os.path.join(conf_dir, filename)
        # 上下文读取yaml文件，中文设置utf-8
        with open(path, encoding="utf-8") as fs:
            self.data = yaml.load(fs, yaml.FullLoader)

if __name__ == '__main__':
    i = HandleYmal("data.yaml").data
    print(i)