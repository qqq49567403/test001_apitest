"""
======================
Author: songs
Time: 2021-10-26
Project: handle_logger
Company: 软件自动化测试
======================
"""

import os
import logging

from common.handle_path import log_dir
from common.handle_conf import conf


class HandleLogger(logging.Logger):
    def __init__(self):
        # set log name, read conf file
        super().__init__(conf.get("log", "name"))
        # set log level, read conf file
        self.setLevel(conf.get("log", "level"))

        # set log formatter
        fmt = "%(asctime)s %(name)s %(levelname)s %(filename)s [第%(lineno)d行] %(message)s"
        formatter = logging.Formatter(fmt)

        # set StreamHandle
        handle1 = logging.StreamHandler()
        handle1.setFormatter(formatter)

        # set FileHandle
        log_path = os.path.join(log_dir, conf.get("log", "file"))
        handle2 = logging.FileHandler(log_path, encoding="utf-8")
        handle2.setFormatter(formatter)

        # addHandler
        self.addHandler(handle1)
        self.addHandler(handle2)

logger = HandleLogger()
logger.info("Hello World")
