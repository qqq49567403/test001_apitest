"""
======================
Author: songs
Time: 2021-11-07
Project: main
Company: 软件自动化测试
======================
"""

import unittest
from datetime import datetime
from httprunner import HttpRunner
from unittestreport import TestRunner

from common.handle_path import testcases_dir
from common.handle_path import report_dir

ss = unittest.TestLoader().discover(testcases_dir)

now_time = datetime.now().strftime("%y-%m-%d %H-%M-%S %p")
report_name = "test_report_ss_{}.html".format(now_time)

hruns = HttpRunner()
runner = TestRunner(ss,
                    filename=report_name,
                    report_dir=report_dir,
                    title="金融类测试报告样板",
                    tester="ss",
                    desc="测试项目测试生成的报告"
                    )
runner.run()
runner.send_email(host="smtp.163.com",
                  port=465,
                  user="songsheng920101@163.com",
                  password="ss920101",
                  to_addrs="1129126506@qq.com"
                  )