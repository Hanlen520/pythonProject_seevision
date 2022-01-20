# coding = utf8
import os

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:pandas_excel_operate.py
    @Author:十二点前要睡觉
    @Date:2022/1/20 15:39
"""
import pandas as pd


class Pandas_Excel_Operate:

    def __init__(self):
        pass

    def one(self):
        df1 = pd.DataFrame({"col1": ["A", "B"], "col2": ["C", "D"]})
        df1.to_excel(r".\excel1.xlsx", "TEST")


if __name__ == '__main__':
    peo = Pandas_Excel_Operate()
    peo.one()
