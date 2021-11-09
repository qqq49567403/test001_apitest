"""
======================
Author: songs
Time: 2021-11-07
Project: handle_phone
Company: 软件自动化测试
======================
"""
from random import randint
from common.handle_db import HandleDb
from common.handle_data import Data

prefix = [133, 153, 173, 177, 180, 181, 189, 199,
          130, 131, 132, 145, 155, 156, 171, 175, 176, 185, 186,
          134, 135, 136, 137, 138, 139, 147, 150, 151, 152, 157, 158, 159, 172, 178, 182, 183, 184, 187, 188]


# 生成随机手机号码
def _get_phone():
    index = randint(0, len(prefix))
    pre_three = prefix[index]

    after_eight = ''
    for _ in range(8):
        new_num = str(randint(0, 9))
        after_eight += new_num
    new_phone = str(pre_three) + after_eight
    return new_phone


def get_new_phone():
    while True:
        phone = _get_phone()
        hd = HandleDb()
        sql = f'select * from futureloan.member where mobile_phone={phone};'
        count = hd.get_count(sql)
        if count == 0:
            hd.close()
            setattr(Data, "phone", phone)
            return phone

print(get_new_phone())