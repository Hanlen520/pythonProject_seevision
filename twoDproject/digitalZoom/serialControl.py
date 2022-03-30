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
    @Description:通用控制串口通信文件，可复用
"""


def getConnectCOMs():
    """
    获取当前电脑已连接的COM端口，并返回端口号，列表形式
    :return:coms，返回所有已连接的端口号（Silicon Labs CP210x USB to UART Bridge）
    """
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
    """
    初始化串口对象，并连接上
    :param com_id:串口id
    :param baud_rate:串口波特率
    :return:返回初始化的串口对象
    """
    com_obj = serial.Serial(com_id, baudrate=baud_rate)
    print("[{}]串口初始化完成".format(com_id))
    return com_obj


def enterPSD(com_obj):
    """
    串口输入账号密码以获得超管权限
    :param com_obj:串口对象
    :return:None
    """
    print("输入账号密码……")
    com_obj.write("\r\n".encode("UTF-8"))
    com_obj.write("root\r\n".encode("UTF-8"))
    sleep(1)
    com_obj.write("bunengshuo\r\n".encode("UTF-8"))
    print("账号密码输入完成！")


def dmesg_n5(com_obj):
    """
    串口打开级别5的log输出
    :param com_obj:串口对象
    :return:None
    """
    print("打开关键Log输出……")
    com_obj.write("dmesg -n5\r\n".encode("UTF-8"))
    sleep(1)
    print("关键Log输出已打开！")


def getWaitingData(com_obj):
    """
    获取串口input数据，用于每次执行操作后对串口回传的数据进行获取
    :param com_obj:串口对象
    :return:返回接收到的数据
    """
    print("获取本次接收数据……")
    while True:
        count = com_obj.inWaiting()
        sleep(2)
        if count > 0:
            data = str(com_obj.read(count))
            # print("本次获取数据内容：[{}]".format(data))
            return data


def exitRootMode(com_obj):
    """
    串口退出超管权限模式
    :param com_obj:串口对象
    :return:None
    """
    print("退出root模式……")
    com_obj.write("exit\r\n".encode("UTF-8"))
    sleep(1)
    print("已退出root模式")


if __name__ == '__main__':
    """
        用于调试
    """
    com_obj = initCom(getConnectCOMs()[0], baud_rate=115200)
    enterPSD(com_obj)
    # print(getWaitingData(com_obj))
    # exitRootMode(com_obj)
    # getWaitingData(com_obj)
    while True:
        getWaitingData(com_obj)
