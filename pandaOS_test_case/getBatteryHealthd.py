# coding = utf8
import os
from time import sleep

os.path.abspath(".")
"""
    @Project:PycharmProjects
    @File:getBatteryHealthd.py
    @Author:十二点前要睡觉
    @Date:2021/12/20 17:36
"""

if __name__ == '__main__':
    i = 0
    while True:
        i += 1
        result = os.system("adb shell dmesg | grep healthd")
        print("第{}次dump电池充电数据情况：\n".format(result))
        sleep(3)
