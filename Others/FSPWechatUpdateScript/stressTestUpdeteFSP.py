# coding = utf8
import os
import random
import subprocess

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:stressTestUpdeteFSP.py
    @Author:十二点前要睡觉
    @Date:2022/5/16 17:03
"""

import serial
from time import sleep

RELAY_CONTROL_COMPORT_1_OPEN = [0xFE, 0x05, 0x00, 0x00, 0xFF, 0x00, 0x98, 0x35]
RELAY_CONTROL_COMPORT_1_CLOSE = [0xFE, 0x05, 0x00, 0x00, 0x00, 0x00, 0xD9, 0xC5]


def flashImageIntoDevice(imagePath=r".\table_nand_ASR7205_EVB_16BIT.cfg",
                         aimgtool_winPath=r".\aimgtool_win\aimgtool.exe"):
    print("当前第{}次刷机测试 -- 开始固件刷写".format(i))
    toTxt("当前第{}次刷机测试 -- 开始固件刷写".format(i))
    flash_command = "{} download -t {}".format(aimgtool_winPath, imagePath)
    print(flash_command)
    print("当前第{}次刷机测试 -- 刷写指令为：\n{}".format(i, flash_command))
    toTxt("当前第{}次刷机测试 -- 刷写指令为：\n{}".format(i, flash_command))
    os.system(flash_command)


def flashImageWithPowerOff(imagePath, aimgtool_winPath):
    print("当前第{}次异常刷机测试 -- 开始固件刷写".format(i))
    toTxt("当前第{}次异常刷机测试 -- 开始固件刷写".format(i))
    flash_command = "{} download -t {}".format(aimgtool_winPath, imagePath)
    print(flash_command)
    print("当前第{}次异常刷机测试 -- 刷写指令为：\n{}".format(i, flash_command))
    toTxt("当前第{}次异常刷机测试 -- 刷写指令为：\n{}".format(i, flash_command))
    subprocess.Popen(flash_command)
    randomSleepTime = 3 * random.random()
    print("当前测试随机中断刷机间隔时间为：{}".format(randomSleepTime))
    toTxt("当前测试随机中断刷机间隔时间为：{}".format(randomSleepTime))
    sleep(randomSleepTime)
    electricOff()
    sleep(1)
    electricOn()
    deviceSendEnter()
    flashImageIntoDevice(imagePath, aimgtool_winPath)
    electricOff()


def initDevicePort(comId="COM44"):
    global devicePort
    devicePort = serial.Serial(comId, baudrate=115200)


def initRalayPort(comId="COM35"):
    global ralayPort
    ralayPort = serial.Serial(comId, baudrate=9600)


def electricOn():
    print("当前第{}次刷机测试 -- 电源打开，设备上电".format(i))
    toTxt("当前第{}次刷机测试 -- 电源打开，设备上电".format(i))
    ralayPort.write(RELAY_CONTROL_COMPORT_1_OPEN)
    sleep(1)


def electricOff():
    print("当前第{}次刷机测试 -- 电源关闭，设备下电".format(i))
    toTxt("当前第{}次刷机测试 -- 电源关闭，设备下电".format(i))
    ralayPort.write(RELAY_CONTROL_COMPORT_1_CLOSE)
    sleep(1)


def deviceSendEnter():
    for j in range(10):
        devicePort.write("\r\n".encode("UTF-8"))
    print("当前第{}次刷机测试 -- 回车并进入download_mode".format(i))
    toTxt("当前第{}次刷机测试 -- 回车并进入download_mode".format(i))
    devicePort.write("download_mode\r\n".encode("UTF-8"))
    sleep(1)


def toTxt(result):
    try:
        with open("./Result.txt", "a+") as f:
            f.write(result + "\n")
    except (AttributeError, TypeError) as ex:
        print("【Error need check, maybe not important】 : \r\n{}\r\n".format(str(ex)))
        f.write("【Error need check, maybe not important】 : \r\n{}\r\n".format(str(ex)))


def fiveThousandTest(test_count=5000):
    global i
    for i in range(test_count + 1):
        i += 1
        print("当前第{}次刷机测试".format(i))
        toTxt("当前第{}次刷机测试".format(i))
        electricOn()
        deviceSendEnter()
        flashImageIntoDevice(imagePath, aimgtool_winPath)
        electricOff()
        print("当前第{}次刷机测试 -- 结束\n".format(i))
        toTxt("当前第{}次刷机测试 -- 结束\n".format(i))


def twoThousandTest(test_count=2000):
    global i
    for i in range(test_count + 1):
        i += 1
        print("当前第{}次异常刷机测试".format(i))
        toTxt("当前第{}次异常刷机测试".format(i))
        electricOn()
        deviceSendEnter()
        flashImageWithPowerOff(imagePath, aimgtool_winPath)
        print("当前第{}次异常刷机测试 -- 结束\n".format(i))
        toTxt("当前第{}次异常刷机测试 -- 结束\n".format(i))


if __name__ == '__main__':
    deviceComId = "COM44"
    ralayComId = "COM35"
    imagePath = r".\table_nand_ASR7205_EVB_16BIT.cfg"
    aimgtool_winPath = r".\aimgtool_win\aimgtool.exe"
    initDevicePort(deviceComId)
    initRalayPort(ralayComId)
    # test_count = 5000
    # Case 1:5000次刷机正常测试
    # fiveThousandTest(test_count)
    twoThousandTest(5)
