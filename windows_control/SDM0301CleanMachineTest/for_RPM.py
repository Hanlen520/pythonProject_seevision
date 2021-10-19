# coding = utf8
import os

os.path.abspath(".")
import json

"""
    用于扫地机RPM.json文件分析，计算平均值，直接修改rpm_json：json文件存放路径即可计算
"""


def json_cal():
    rpm_json = r"C:\Users\CHENGUANGTAO\Desktop\SMD0301扫地机\扫地机测试用例 (1)\扫地机测试用例 (1)\temp\rpm_20211019142426.json"
    with open(rpm_json, "r") as file:
        file_dict = json.load(file)
        array = file_dict["rpm"]
        sum_num = 0
        for i in array:
            sum_num += i
        print("总共{}组数据，RPM总计得：{}，RPM平均值为：{}".format(len(array), str(sum_num), str(sum_num / len(array))))


if __name__ == "__main__":
    json_cal()
