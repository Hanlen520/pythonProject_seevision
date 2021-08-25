# coding = utf8

import os
import re
import subprocess
from time import sleep

import pyautogui

os.path.abspath(".")

import uiautomation
import pandas as pd

"""
    绝大多数Windows软件的自动化控件操作等可以用uiautomation库来实现：
    1、Python-UIAutomation-for-Windows-master + uiautomation
    2、 automation.py（搜索控件）
    3、 pyautogui模拟键盘操作，快捷键等，对于一些uiautomation搜索不到的UI控件
"""


def openPotplayer(potplayer_path="D:\PotPlayer\PotPlayerMini64.exe"):
    global potplayer
    potplayer = subprocess.Popen(potplayer_path)
    sleep(2)


def enterDeviceSettings():
    global potplayer_frame
    global settings_frame
    potplayer_frame = uiautomation.WindowControl(searchDepth=1, Name="PotPlayer")
    pyautogui.hotkey("alt", "d")
    settings_frame = uiautomation.WindowControl(searchDepth=2, Name="设备设置")


formatList = []


def getFormatList():
    settings_frame.ComboBoxControl(AutomationId="3008").Click()
    sleep(1)
    format_list = settings_frame.ListControl(searchDepth=5, Name="格式：")
    all_format = format_list.GetChildren()
    for format in all_format:
        # print(format.Name)
        formatList.append(format.Name)
    return formatList


def switchResolution(resolution="YUY2 960×540P 30(P 16:9)"):
    settings_frame.ComboBoxControl(AutomationId="3008").Click()
    sleep(1)
    find = False
    count = 0
    while not find:
        if count < 5:
            pyautogui.scroll(500)
        else:
            pyautogui.scroll(-500)
        count += 1
        resolution_checked = settings_frame.ListItemControl(searchDepth=6, Name=resolution)
        findResolution = str(re.findall("Rect:(.*)(\[)", str(resolution_checked))[0][0]).strip()
        if findResolution != "(0,0,0,0)":
            find = True
            resolution_checked.Click()
            break
    sleep(1)
    settings_frame.ButtonControl(searchDepth=3, Name="打开设备(O)").Click()
    sleep(1)


def getPlayerInformation():
    pyautogui.hotkey("ctrl", "f1")
    sleep(5)
    player_information = uiautomation.WindowControl(searchDepth=1, Name="播放信息")
    current_frameRate = player_information.TextControl(AutomationId="3201").GetWindowText()
    current_bitRate = player_information.TextControl(AutomationId="3386").GetWindowText()
    print("帧率：{}".format(current_frameRate), end=" -- ")
    print("位率：{}".format(current_bitRate))
    print("")
    framerate = re.findall("->(.*)", current_frameRate)[0]
    bitrate = re.findall("\/(.*)\skbps", current_bitRate)[0]
    return framerate, bitrate


# 帧率：30.039 -> 29.95 -- 位率：-1.64076e+06/107628 kbps

def closePotplayer():
    potplayer.kill()


def firstResultAnalysis(test_number="", result_list=[]):
    resolution_list = []
    frame_rate_list = []
    bit_rate_list = []
    for result in result_list:
        resolution_list.append(result[0])
        frame_rate_list.append(result[1])
        bit_rate_list.append(result[2])
    df = pd.DataFrame({"分辨率": resolution_list, "帧率": frame_rate_list, "位率": bit_rate_list})
    df.to_excel("./第{}次测试_resolutionTest.xlsx".format(test_number))


def getFirstStandardData(potplayerPath):
    result_list = []
    for i in range(50):
        try:
            openPotplayer(potplayer_path=potplayerPath)
            enterDeviceSettings()
            all_format = getFormatList()
            closePotplayer()
            for j in range(2, len(all_format)):
                resolution_now = all_format[j]
                print("第{}轮{}次测试 -- 当前测试分辨率为：{}".format(str(i + 1), str(j - 1), resolution_now))
                openPotplayer(potplayer_path=potplayerPath)
                enterDeviceSettings()
                switchResolution(resolution_now)
                list_cur = getPlayerInformation()
                closePotplayer()
                result_list.append([resolution_now, list_cur[0], list_cur[1]])
        except Exception as ex:
            print("Some error happened : {}".format(str(ex)))
            continue
        finally:
            firstResultAnalysis(test_number=str(i + 1), result_list=result_list)
            result_list = []
            closePotplayer()


def compare2StandardDataTest():
    # 进行第二次测试，完善与第一次测试的数据比较并得出结果
    # 完善好后，学习PyQt5，将其转换成单独的工具：
    # 1、功能分开
    # 2、接口独立
    # 第二次测试和第一次测试数据进行读取后比较，再生成一个测试结果的Excel表格 -- ongoing
    pass


def readExcel():
    read = pd.read_excel(io="./第1次测试_resolutionTest.xlsx", header=0, names=["分辨率", "帧率", "位率"], sheet_name="Sheet1")
    # print(read.values)
    for i in read.values:
        # 分辨率
        print(i[0])
        # 帧率
        print(i[1])
        # 位率
        print(i[2])


if __name__ == '__main__':
    potplayerPath = "D:\PotPlayer\PotPlayerMini64.exe"
    getFirstStandardData(potplayerPath)
    # compare2StandardDataTest()
    # readExcel()
