# coding = utf8
import os
from time import sleep

os.path.abspath(".")
"""
    @Project:PycharmProjects
    @File:getBatteryHealthd.py
    @Author:十二点前要睡觉
    @Date:2021/12/20 17:36s
"""

if __name__ == '__main__':
    i = 0
    while True:
        i += 1
        print("第{}次dump电池充电数据情况：\n".format(str(i)))
        result = os.system("adb shell dmesg | grep healthd")
        sleep(3)
