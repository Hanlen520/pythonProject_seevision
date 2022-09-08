# coding = utf8
import os
import re
import subprocess
from time import sleep

import pandas as pd
import serial
from serial.tools.list_ports_windows import comports

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:powerSupplyControlTest.py
    @Author:十二点前要睡觉
    @Date:2022/8/23 11:28
"""
"""
    此脚本用于Android项目 - VS680的电源开关机压力测试
    原理：
    通过程控继电器，控制电源输入端的开关状态，来进行开关机压力测试，通过串口通信实时获取设备上电后的状态
"""
RELAY_CONTROL_COMPORT_1_OPEN = [0xFE, 0x05, 0x00, 0x00, 0xFF, 0x00, 0x98, 0x35]
RELAY_CONTROL_COMPORT_1_CLOSE = [0xFE, 0x05, 0x00, 0x00, 0x00, 0x00, 0xD9, 0xC5]


def getAllPorts():
    ports = []
    for port in list(comports()):
        if "Silicon Labs CP210x USB to UART Bridge" in str(port):
            current_port = re.findall("\((.*)\)", str(port))[0]
            ports.append(current_port)
    return ports


def openOUT1(s_obj):
    print("设备上电中……")
    s_obj.write(RELAY_CONTROL_COMPORT_1_OPEN)
    sleep(1)


def closeOUT1(s_obj):
    print("设备下电，下电完成，电源断开！")
    s_obj.write(RELAY_CONTROL_COMPORT_1_CLOSE)
    sleep(1)


def checkDeviceOnline():
    online = True
    while online:
        currentPage = subprocess.Popen("adb shell dumpsys window | grep mCurrentFocus", shell=True,
                                       stdout=subprocess.PIPE).communicate()[0]
        sleep(2)
        print("检测设备中……检测间隔为2s……")
        if "com.seevision.tv.launcher" in str(currentPage):
            print("电源上电，设备启动成功！")
            online = False
            return not online
    sleep(2)


def screenshotAndPullOut(screenshotName):
    if not os.path.exists("./screenshot/"):
        os.mkdir("./screenshot/")
    print("开始adb截图，截图当前所在页面图片……")
    subprocess.Popen("adb shell screencap -p /sdcard/{}.png".format(screenshotName), shell=True,
                     stdout=subprocess.PIPE).communicate()[0]
    sleep(1)
    print("截图完成，导出截图{}.png至PC文件夹中……".format(screenshotName))
    subprocess.Popen("adb pull /sdcard/{}.png ./screenshot/".format(screenshotName), shell=True,
                     stdout=subprocess.PIPE).communicate()[0]
    sleep(1)
    print("本次测试完成！开始下一轮测试……")
    return "{}.png".format(screenshotName)


def standard_test_DataGenerate(result_list=[]):
    alist = []
    blist = []
    clist = []
    for result in result_list:
        alist.append(result[0])
        blist.append(result[1])
        clist.append(result[2])
    df = pd.DataFrame({"测试次数": alist, "测试结果": blist, "截图名称": clist})
    df.to_excel("./电源开关机压力测试result.xlsx", engine="openpyxl")


if __name__ == '__main__':
    test_count = 1000
    print(getAllPorts())
    com_id = getAllPorts()[0]
    s_obj = serial.Serial(com_id, baudrate=9600)
    print(s_obj.port)
    result_list = []
    for i in range(test_count):
        openOUT1(s_obj)
        result_1 = checkDeviceOnline()
        result_2 = screenshotAndPullOut(i)
        result_list.append([i, result_1, result_2])
        standard_test_DataGenerate(result_list)
        closeOUT1(s_obj)
        sleep(1)
    # closeOUT1(s_obj)
