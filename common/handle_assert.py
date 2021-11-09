"""
======================
Author: songs
Time: 2021-11-08
Project: handle_assert
Company: 软件自动化测试
======================
"""
from decimal import Decimal

from jsonpath import jsonpath

from common.handle_db import HandleDb
from common.handle_logger import logger


class HandleAssert:
    def __init__(self):
        # 存储sql语句查询之后的比较结果
        self.sql_comp_res = None
        # 存储响应结果比对之后的结果
        self.json_comp_res = {}

    # 连接数据库
    def init_sql_conn(self):
        self.db = HandleDb()

    # 判断断言结果
    def assert_result(self):
        sql_comp_res_flag = True
        json_comp_res_flag = True

        # 判断响应比对结果中，如果没有False，则全部通过，否则，表示比对失败
        if self.json_comp_res and False in self.json_comp_res.values():
            logger.info("响应断言失败，用例失败，请检查响应结果比对为False的条件！")
            sql_comp_res_flag = False

        # 判断sql断言结果
        if self.sql_comp_res:
            # 判断是否为列表，说明存在多条sql语句进行比对，则需要一个个确认是否有False
            if isinstance(self.sql_comp_res, list):
                for res in self.json_comp_res:
                    if False in res.values():
                        sql_comp_res_flag = False

            # 判断是否为字典，说明只有一条sql语句进行比较，则需要确认是否为False
            if isinstance(self.sql_comp_res, dict):
                if False in self.sql_comp_res.values():
                    sql_comp_res_flag = False

            if sql_comp_res_flag is False or json_comp_res_flag is False:
                logger.info("sql语句断言失败或者json响应结果断言失败！")
                logger.error(f"sql语句断言结果为：{sql_comp_res_flag}")
                logger.error(f"json响应结果断言结果为：{json_comp_res_flag}")
            else:
                logger.info("用例执行通过！")

    # 多条sql语句断言
    def get_multi_sql_comp_resp(self, check_sql_str):
        # 将期结果的sql表达式转成python对象
        check_sql_obj = eval(check_sql_str)
        # 判断是否是列表，多个sql语句比对，一条一条进行比对
        if isinstance(check_sql_obj, list):
            # 存储每条sql语句的比对结果
            self.sql_comp_res = []
            for check_sql_dict in check_sql_obj:
                one_sql_comp_res = self.__get_one_comp_resp(check_sql_dict)
                self.sql_comp_res.append(one_sql_comp_res)
        elif isinstance(check_sql_obj, dict):
            one_sql_comp_res = self.__get_one_comp_resp(check_sql_obj)
            self.sql_comp_res = one_sql_comp_res
        else:
            self.sql_comp_res = None

    # 单条sql语句断言
    def __get_one_comp_resp(self, check_sql_dict):
        one_sql_comp_res = {}
        logger.info("数据库开始校验！")

        # 判断查询结果类型为值
        if check_sql_dict["check_type"] == "value":
            logger.info("比较sql语句查询之后的值，sql查询结果为字典，将字典中的每一个都进行比较")
            sql_res = self.db.get_one_data(check_sql_dict["check_sql"])
            logger.info("执行sql语句：{}".format(check_sql_dict["check_sql"]))
            logger.info("查询结果为：{}".format(sql_res))
            logger.info("期望结果为：{}".format(check_sql_dict["expected"]))

            # 执行的结果进行比较
            for key, value in check_sql_dict["expected"].items():
                if key in sql_res.keys():
                    if isinstance(sql_res[key], Decimal):
                        sql_res[key] = float(sql_res[key])
                        logger.info("将Decimal类型转换成float，转换后的值为：{}".format(sql_res[key]))
                    if value == sql_res[key]:
                        one_sql_comp_res[key] = True    # 比较成功，存储到sql_comp_res中
                        logger.info("比对成功！")
                    else:
                        one_sql_comp_res[key] = False   # # 比较失败，存储到sql_comp_res中
                        logger.info("比对失败！")
                else:
                    logger.info("sql查询结果中没有对应的列名：{}， 请检查期望结果语句".format(key))
                    one_sql_comp_res[key] = False

        # 对比sql语句查询之后的条数
        elif check_sql_dict["check_type"] == "count":
            logger.info("比较sql语句查询之后的条数，sql查询结果为整数，只要比对数据即可")
            sql_res = self.db.get_count(check_sql_dict["check_sql"])
            logger.info("执行sql语句：{}".format(check_sql_dict["check_sql"]))
            logger.info("查询结果为：{}".format(sql_res))
            logger.info("期望结果为：{}".format(check_sql_dict["expected"]))

            # 比较执行的结果
            if sql_res == check_sql_dict["expected"]:
                one_sql_comp_res["count"] = True
            else:
                one_sql_comp_res["count"] = False
        return one_sql_comp_res

    # 响应结果断言
    def get_json_comp_res(self, expected_exprs_str, resp_dict):
        # 将预期结果转成字典
        expected_exprs_dict = eval(expected_exprs_str)
        # 遍历字典，通过jsonpath，从resp_dict中提取对应的数据，更新字典值
        for key, value in expected_exprs_dict.items():
            logger.info("提取表达式为：{}，期望结果为：{}".format(key, value))
            # 将jsonpath表达式中的key，通过jsonpath提取后，得到对应的值
            actual_value_list = jsonpath(resp_dict, key)
            logger.info("提取之后的结果为：{}".format(actual_value_list))

            # 将提取的表达式与期望的值做等值比较，没有提取到的值为false，提取到的是True
            if isinstance(actual_value_list, list):
                if actual_value_list[0] == value:
                    self.json_comp_res[f"jsonpath-{key}-actual-{value}-expected-{actual_value_list[0]}"] = True
                else:
                    self.json_comp_res[f"jsonpath-{key}-actual-{value}-expected-{actual_value_list[0]}"] = False
                logger.info("提取的值与期望的值比对结果为：{}".format(
                    self.json_comp_res[f"jsonpath-{key}-actual-{value}-expected-{actual_value_list[0]}"]
                ))

        logger.info("所有实际结果与期望结果的比对情况：")
        for key, value in self.json_comp_res.items():
            logger.info("{}:{}".format(key, value))
        print("----------------------------------")

    def close_sql_conn(self):
        self.db.close()


if __name__ == '__main__':
    check_sql_str = '{"check_type":"value",' \
                    '"check_sql":"select leave_amount,mobile_phone from member where id=17",' \
                    '"expected":{"leave_amount":float(0.00)+0,"mobile_phone":"13212072994"}}'

    ha = HandleAssert()
    ha.init_sql_conn()
    ha.get_multi_sql_comp_resp(check_sql_str)
    ha.close_sql_conn()














