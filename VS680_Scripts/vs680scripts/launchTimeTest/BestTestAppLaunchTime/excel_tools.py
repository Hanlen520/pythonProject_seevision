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
    @description:read_excel_for_case_parametrize，通过excel表格形式对case的参数进行管理
    @param:
        form:表格路径
        sheet_name:指定sheet名称
        case_name:指定case名称
"""


# 从excel中读取数据并返回（case）
def read_excel_for_case_parametrize(form="../test_case/before_fota_data.xlsx", sheet_name="before_fota",
                                    case_name="test_send_message"):
    df = pd.read_excel(form, sheet_name=sheet_name, index_col="case_name")
    original_data = df.loc[case_name, "case_data"]
    # 将数据获得后进行处理重新拼接为list
    final_data = []
    if "int" in str(type(original_data)):
        original_data = str(original_data)
        final_data.append(original_data)
    else:
        if "(" in original_data:
            dl = []
            d1 = original_data.split(",")[0].replace("(", "").strip()
            d2 = original_data.split(",")[1].replace(")", "").strip()
            dl.append(d1)
            dl.append(d2)
            final_data.append(tuple(dl))
        else:
            final_data.append(original_data)
    return final_data


"""
    @description:read_excel_for_page_element，通过excel表格形式对element控件的参数进行管理
    @param:
        form:表格路径
        sheet_name:指定sheet名称
        element_name:指定element元素名称
"""


# 从excel中读取数据并返回（element）
def read_excel_for_page_element(form="../page_android/page_sheet.xlsx", sheet_name="calendar_page",
                                element_name="guide_got_it"):
    df = pd.read_excel(form, sheet_name=sheet_name, index_col="element_name")
    original_data = df.loc[element_name, "element_data"]
    return original_data


if __name__ == '__main__':
    print(read_excel_for_page_element())
    # read_excel_for_case_parametrize()
    print(type(read_excel_for_page_element()))
