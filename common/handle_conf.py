"""
======================
Author: songs
Time: 2021-10-20
Project: handle_conf
Company: 软件自动化测试
======================
"""

import os
from configparser import ConfigParser
from handle_path import conf_dir


class HandleConf(ConfigParser):
    def __init__(self, filename):
        super().__init__()
        # 读取文件，设置类型为utf-8
        self.read(filename, encoding='utf-8')

conf = HandleConf(os.path.join(conf_dir, 'conf.ini'))

if __name__ == '__main__':
    print(conf.get("log", "name"))