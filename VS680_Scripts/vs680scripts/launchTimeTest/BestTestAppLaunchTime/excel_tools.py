# coding = utf8
import os

import pandas as pd

os.path.abspath(".")
"""
    @File:excel_tools.py
    @Author:Bruce
    @Date:2021/3/15
"""

"""
    @description:read_excel_for_page_element，通过excel表格形式对element控件的参数进行管理
    @param:
        form:表格路径
        sheet_name:指定sheet名称
        element_name:指定element元素名称
"""


# 从excel中读取数据并返回（element）
def read_excel_for_page_element(form="./Touch启动时间测试用例.xlsx", sheet_name="Touch启动时间测试"):
    df = pd.read_excel(form, sheet_name=sheet_name, index_col="case序号")
    rows = df.shape[0]
    test_data = []
    for row in range(1, rows + 1):
        app_text = df.loc[row, "测试应用名称"]
        packageName = df.loc[row, "测试应用包名"]
        activityName = df.loc[row, "待测应用Activity"]
        test_data.append([app_text, packageName, activityName])
    return test_data


def write_excel_with_specific_data(app_text, result, form="./Touch启动时间测试用例.xlsx",
                                   sheet_name="Touch启动时间测试"):
    df = pd.read_excel(form, sheet_name=sheet_name, index_col="case序号")
    rows = df.shape[0]
    for row in range(1, rows + 1):
        if app_text == df.loc[row, "测试应用名称"]:
            df.loc[row, "测试次数"] = result[0]
            df.loc[row, "测试结果_平均值"] = result[1]
    # df.loc[1, "测试次数"] = 10
    # df.loc[1, "测试结果_平均值"] = "[123, 982, 134]_435"
    df1 = pd.DataFrame(df)
    df1.to_excel(form, sheet_name)
    # print(df)


if __name__ == '__main__':
    # test_data = read_excel_for_page_element(form="./Touch启动时间测试用例.xlsx", sheet_name="Touch启动时间测试")
    # print(test_data)
    write_excel_with_specific_data("飞书", "", form="./Touch启动时间测试用例.xlsx", sheet_name="Touch启动时间测试")
