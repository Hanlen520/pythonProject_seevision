# coding = utf8
import os
from time import sleep

os.path.abspath(".")
import uiautomation as ui
import pandas as pd

"""
    @Project:pythonProject_seevision
    @File:getFPSdata.py
    @Author:十二点前要睡觉
    @Date:2022/5/27 17:47
"""


def getFPSdata():
    sleep(0.5)
    fps = ui.TextControl(AutomationId="MainWindow.centralwidget.fps_disp").Name
    print(fps)
    return fps


def writeIntoExcel(fps_list):
    df = pd.DataFrame({"FPS记录": fps_list})
    df.to_excel("./fps_list.xlsx")


if __name__ == '__main__':
    sleep(5)
    fps_list = []
    try:
        while True:
        # for i in range(100):
            fps_list.append(getFPSdata())
            writeIntoExcel(fps_list)
    except Exception:
        print("Manual Operation Done!")
    finally:
        print("Write into excel……")
        writeIntoExcel(fps_list)
