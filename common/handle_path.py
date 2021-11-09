"""
======================
Author: songs
Time: 2021-10-20
Project: handle_path
Company: 软件自动化测试
======================
"""

import os

root_dir = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))

conf_dir = os.path.join(root_dir, "conf")
log_dir = os.path.join(root_dir, "output", "log")
report_dir = os.path.join(root_dir, 'output', 'report')
testcases_dir = os.path.join(root_dir, "testcases")
testdatas_dir = os.path.join(root_dir, "testdatas")

