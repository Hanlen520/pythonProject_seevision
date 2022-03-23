# coding = utf8
import os
import re
from time import sleep

import serial
from serial.tools.list_ports_windows import comports

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:serialControl.py
    @Author:十二点前要睡觉
    @Date:2022/3/23 10:34
"""


def getConnectCOMs():
    coms = []
    for com in list(comports()):
        if "Silicon Labs CP210x USB to UART Bridge" in str(com):
            current_com = re.findall("\((.*)\)", str(com))[0]
            coms.append(current_com)
    if coms:
        print("Current connect coms have:[{}]".format(coms))
    else:
        print("No com connect ,please check!")
    return coms


def initCom(com_id, baud_rate):
    com_obj = serial.Serial(com_id, baudrate=baud_rate)
    return com_obj


def enterPSD(com_obj):
    print("输入账号密码……")
    com_obj.write("\r\n".encode("UTF-8"))
    com_obj.write("root\r\n".encode("UTF-8"))
    sleep(1)
    com_obj.write("bunengshuo\r\n".encode("UTF-8"))


def getWaitingData(com_obj):
    print("获取本次接收数据……")
    while True:
        if com_obj.inWaiting() > 0:
            data = str(com_obj.read_all())
            print("本次获取数据内容：[{}]".format(data))
            return data


if __name__ == '__main__':
    com_obj = initCom(getConnectCOMs(),)
