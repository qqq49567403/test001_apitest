"""
======================
Author: songs
Time: 2021-10-26
Project: handle_excel
Company: 软件自动化测试
======================
"""

from openpyxl import load_workbook


class HandleExcel:
    def __init__(self, filename, sheet):
        # read file
        self.wb = load_workbook(filename)
        # read sheet
        self.sh = self.wb[sheet]

    # get all data
    def __get_all(self):
        self.all_rows = list(self.sh.rows)

    # get the first data, set the title
    def __get_one_to_title(self):
        # get all data
        self.__get_all()
        # get the first data,set the key
        title = []
        for item in self.all_rows[0]:
            title.append(item.value)
        return title

    # 获取所有行数据，与title进行拼接，以key-value的形式
    def get_all_data(self):
        # 获取title
        title = self.__get_one_to_title()
        # 测试数据集
        testcases = []
        # 遍历测试数据，与title进行拼接
        for item in self.all_rows[1:]:
            value = []
            for cell in item:
                value.append(cell.value)
            case = dict(zip(title, value))
            testcases.append(case)
        return testcases

    # add data to excel
    def write_data(self, row, cel, value):
        self.sh.rows(row, cel).value = value

    # save data
    def save(self, filename):
        self.wb.save(filename)


if __name__ == '__main__':
    import os
    from common.handle_path import testcases_dir

    excel_path = os.path.join(testcases_dir, "api_cases.xlsx")
    he = HandleExcel(excel_path, "注册")
    cases = he.get_all_data()
    print(cases)
