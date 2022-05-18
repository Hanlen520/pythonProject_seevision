# coding = utf8
import os

import pandas as pd

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:VICurrentKeepReading.py
    @Author:十二点前要睡觉
    @Date:2022/5/17 8:47
"""
import pyautogui

pyautogui.FAILSAFE = True
from uiautomation import uiautomation as ui
from time import sleep


def getVIbus(xlsxName="VIbusRecord.xlsx", testCount=0):
    data = [["number", "VBUS", "IBUS"]]
    for i in range(1, testCount + 1):
        sleep(0.3)
        childrenList = ui.GroupControl(searchDepth=5, Name="参数显示").GetChildren()
        vbus = childrenList[0].GetChildren()[1].Name
        ibus = childrenList[1].GetChildren()[1].Name
        print("current vbus is [{}], ibus is [{}]".format(vbus, ibus))
        data.append([i, vbus, ibus])
        write_into_excel(xlsxName, data)


def write_into_excel(filename, data):
    if not os.path.exists("./result"):
        os.mkdir("./result")
        print("Create folder success!")
    file_path = "./result/{}".format(filename)
    df = pd.DataFrame(columns=data)
    df.to_excel(file_path, index=True)
    print("{} data fill success!".format(filename))


if __name__ == '__main__':
    """
        每切换一个分辨率后，录制1000组对应的V\IBus的数据
    """
    testCount = 1000
    xlsxName = "MJPEG1080P"
    getVIbus(xlsxName, testCount)
