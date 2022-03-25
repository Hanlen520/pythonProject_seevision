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
        print("当前存在的串口为:[{}]".format(coms))
    else:
        print("未检测到有串口，请检查!")
    return coms


def initCom(com_id, baud_rate):
    com_obj = serial.Serial(com_id, baudrate=baud_rate)
    print("[{}]串口初始化完成".format(com_id))
    return com_obj


def enterPSD(com_obj):
    print("输入账号密码……")
    com_obj.write("\r\n".encode("UTF-8"))
    com_obj.write("root\r\n".encode("UTF-8"))
    sleep(1)
    com_obj.write("bunengshuo\r\n".encode("UTF-8"))
    print("账号密码输入完成！")


def dmesg_n5(com_obj):
    print("打开关键Log输出……")
    com_obj.write("dmesg -n5\r\n".encode("UTF-8"))
    sleep(1)
    print("关键Log输出已打开！")


def getWaitingData(com_obj):
    print("获取本次接收数据……")
    while True:
        if com_obj.inWaiting() > 0:
            sleep(1)
            data = str(com_obj.read_all())
            print("本次获取数据内容：[{}]".format(data))
            return data


def exitRootMode(com_obj):
    print("退出root模式……")
    com_obj.write("exit\r\n".encode("UTF-8"))
    sleep(1)
    print("已退出root模式")


if __name__ == '__main__':
    com_obj = initCom(getConnectCOMs()[0], baud_rate=115200)
    enterPSD(com_obj)
    # print(getWaitingData(com_obj))
    # exitRootMode(com_obj)
    # getWaitingData(com_obj)
    while True:
        getWaitingData(com_obj)
