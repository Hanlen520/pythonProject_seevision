# coding = utf8
import os
import re

import pyautogui

os.path.abspath(".")

os.path.abspath(".")

import time
from time import sleep
import uiautomation

# 实时获取时间
cur_time = time.strftime("%Y%m%d_%H%M%S")

import subprocess
import json


def getDeviceUSBPort():
    print("获取Windows USB端口信息")
    out = subprocess.getoutput(
        "PowerShell -Command \"& {Get-PnpDevice | Select-Object Status,Class,FriendlyName,InstanceId | ConvertTo-Json}\"")
    j = json.loads(out)
    o = []
    for dev in j:
        o.append(str(dev['Status']) + " " + str(dev['Class']) + " " + str(dev['FriendlyName']) + " " + str(
            dev['InstanceId']))
    return o


def openHidTool(hidTool):
    print("打开HidTool")
    global hidTool_exe
    hidTool_exe = subprocess.Popen(hidTool)
    sleep(2)


def openFlashToolByClick(flashFolder):
    print("打开FlashTool")
    os.startfile(flashFolder)
    sleep(1)
    flashtool_exe = uiautomation.ListItemControl(searchDepth=8, Name="FlashTool.exe")
    flashtool_exe.DoubleClick()
    pyautogui.hotkey("alt", "tab")
    pyautogui.hotkey("ctrl", "w")
    sleep(1)
    pyautogui.hotkey("alt", "tab")
    pyautogui.hotkey("alt", "tab")
    sleep(1)


def closeHidTool():
    sleep(1)
    print("关闭HidTool")
    hidTool_exe.kill()


def closeFlashTool():
    sleep(1)
    print("关闭FlashTool")
    pid_get = subprocess.Popen("tasklist | grep FlashTool.exe", shell=True, stdout=subprocess.PIPE).communicate()[0]
    pid = re.findall("FlashTool.exe(.*)Console", str(pid_get))[0].strip(" ")
    os.system("taskkill /pid {}".format(pid))


def getSerialPort(comport_i):
    print("获取序列端口信息")
    while True:
        print("Get Serial Port now!")
        for port in getDeviceUSBPort():
            if "OK Ports Silicon Labs CP210x USB to UART Bridge ({}) USB".format(comport_i) in port:
                return port


def getPortablePort():
    print("获取便携设备端口信息")
    while True:
        print("Get Portable Port now!")
        for port in getDeviceUSBPort():
            if "OK WPD E:\\" in port:
                return port


def getSmartCamera():
    print("获取相机端口信息")
    while True:
        print("Get Smart Camera Port now!")
        for port in getDeviceUSBPort():
            if "OK Camera Smart Camera USB" in port:
                return port


def enterBootLoaderMode():
    print("进入BootLoader模式")
    if getSmartCamera():
        print("Smart camera port存在，可以进入Bootloader")
        uiautomation.ButtonControl(searchDepth=2, Name="启动Bootloader模式").Click()
    sleep(5)


def fastbootCommand(comport_i):
    print("进入Fastboot模式")
    if getSerialPort(comport_i):
        print("Serial port存在，可以执行fastboot")
        erase = subprocess.Popen("fastboot erase all")
        sleep(1)
        reboot = subprocess.Popen("fastboot reboot")
        sleep(1)


def flashImageIntoDevice(flashFolder, softwareName, type):
    print("开始将固件刷入设备")
    if getPortablePort():
        print("Portable port存在，可以执行刷机操作")
        openFlashToolByClick(flashFolder)
        uiautomation.ButtonControl(searchDepth=2, Name="选择固件路径").Click()
        uiautomation.TreeItemControl(searchDepth=6, Name=softwareName).Click()
        pyautogui.scroll(-300)
        uiautomation.TreeItemControl(searchDepth=8, Name=type).Click()
        uiautomation.TreeItemControl(searchDepth=9, Name="images").Click()
        uiautomation.ButtonControl(searchDepth=3, Name="确定").Click()
        uiautomation.ButtonControl(searchDepth=2, Name="开始下载").Click()
        while True:
            try:
                sleep(1)
                print("正在刷机中……")
                if uiautomation.ButtonControl(searchDepth=2, Name="下载完成").Exists(maxSearchSeconds=3):
                    print("下载完成")
                    return True
            except LookupError:
                continue


if __name__ == '__main__':
    """
        测试准备：
        开启SecureCRT在后台持续录制串口信息
        1、安装pyautogui、uiautomation：pip3 install uiautomation, pip3 install 安装pyautogui
        2、需要刷机的固件放在桌面以文件夹形式
        3、将flashFolder、hidTool、flashTool、flash_software、softwareName都替换成正确的路径和名称
        4、定义testCount测试次数
        5、测试类型：type->nand或nor
        6、以管理员模式启动cmd：python flashTool_Stable.py >> log_record.log，运行时的log会记录在该文件中，或者不记录直接执行python flashTool_Stable.py
    """
    flashFolder = r"D:\PycharmProjects\pythonProject_seevision\windows_control\SY0102\FlashTool"
    hidTool = r"D:\PycharmProjects\pythonProject_seevision\windows_control\SY0102\HIDTool\HIDTool\HIDTool.exe"
    flashTool = r"D:\PycharmProjects\pythonProject_seevision\windows_control\SY0102\FlashTool\FlashTool.exe"
    flash_software = r"D:\PycharmProjects\pythonProject_seevision\windows_control\SY0102\20211101_201937_V112-20211101-201937\nor\images"
    softwareName = "20211112_012300"
    testCount = 10
    type = "nand"
    comport_i = "COM22"
    for i in range(testCount):
        print("\n\n当前是第{}次测试".format(str(i + 1)))
        openHidTool(hidTool)
        enterBootLoaderMode()
        closeHidTool()
        fastbootCommand(comport_i)
        flashImageIntoDevice(flashFolder, softwareName, type)
        closeFlashTool()
        sleep(8)
