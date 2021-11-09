"""
======================
Author: songs
Time: 2021-10-25
Project: handle_db
Company: 软件自动化测试
======================
"""

import pymysql
from handle_conf import conf


class HandleDb:
    def __init__(self):
        try:
            # 建立连接
            self.conn = pymysql.connect(
                host=conf.get("mysql", "host"),
                user=conf.get("mysql", "user"),
                password=conf.get("mysql", "password"),
                database=conf.get("mysql", "db"),
                port=conf.getint("mysql", "port"),
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor
            )

            # 建立游标
            self.cur = self.conn.cursor()
        except:
            print("数据库连接失败！")
            raise

    # 查看统计数量
    def get_count(self, sql, args=None):
        # 提交数据
        self.conn.commit()
        # 执行sql语句
        return self.cur.execute(sql, args)

    # 查看一条数据
    def get_one_data(self, sql, args=None):
        self.conn.commit()
        self.cur.execute(sql, args)
        return self.cur.fetchone()

    # 查看所有数据
    def get_all_data(self, sql, args=None):
        self.conn.commit()
        self.cur.execute(sql, args)
        return self.cur.fetchall()

    # 关闭数据库连接
    def close(self):
        self.cur.close()
        self.conn.close()

if __name__ == '__main__':
    hd = HandleDb()
    sql = "select leave_amount from member where id=17"
    res = hd.get_one_data(sql)
    print(res)
    for key,value in res.items():
        print(value)
    hd.close()