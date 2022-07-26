# coding = utf8

import os
import re
import subprocess
import traceback
from time import sleep

import pyautogui

pyautogui.FAILSAFE = True
from uiautomation import uiautomation as ui

os.path.abspath(".")

import uiautomation
import pandas as pd
import time
import logging

# 实时获取时间
cur_time = time.strftime("%Y%m%d_%H%M%S")

"""
    绝大多数Windows软件的自动化控件操作等可以用uiautomation库来实现：
    1、Python-UIAutomation-for-Windows-master + uiautomation
    2、 automation.py（搜索控件）
    3、 pyautogui模拟键盘操作，快捷键等，对于一些uiautomation搜索不到的UI控件
"""
"""
    @param:
    @description:logger构建器
        log_path:log生成路径
        logging_name:log名称
"""


def logger_config(log_path, logging_name):
    # 获取logger对象,取名
    logger = logging.getLogger(logging_name)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_path, encoding='UTF-8')
    # 生成并设置文件日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # 为logger对象添加句柄
    logger.addHandler(handler)

    return logger


# 打开Potplayer，传入potplayer启动exe路径
def openPotplayer(potplayer_path="D:\PotPlayer\PotPlayerMini64.exe"):
    global potplayer
    potplayer = subprocess.Popen(potplayer_path)
    sleep(2)
    if uiautomation.TextControl(searchDepth=3, Name="检查更新：").Exists():
        pyautogui.press("esc")


# 进入Potplayer设备连接设置页面
def enterDeviceSettings():
    global potplayer_frame
    global settings_frame
    potplayer_frame = uiautomation.WindowControl(searchDepth=1, Name="PotPlayer")
    pyautogui.hotkey("alt", "d")
    settings_frame = uiautomation.WindowControl(searchDepth=2, Name="设备设置")


# 获取当前摄像头支持的格式
def getFormatList():
    settings_frame.ComboBoxControl(AutomationId="3008").Click()
    sleep(1)
    format_list = settings_frame.ListControl(searchDepth=5, Name="格式：")
    all_format = format_list.GetChildren()
    formatList = []
    for format in all_format:
        # 筛选掉重复的分辨率格式
        if (str(format) != "开始播放时选择格式") | (str(format) != "默认格式(推荐)"):
            if "(P" in str(format):
                formatList.append(format.Name)
    return formatList


# 遍历格式切换所有分辨率
def switchResolution(resolution="YUY2 960×540P 30(P 16:9)"):
    settings_frame.ComboBoxControl(AutomationId="3008").Click()
    sleep(1)
    find = False
    count = 0
    while not find:
        if resolution:
            resolution_checked = settings_frame.ListItemControl(searchDepth=6, Name=resolution)
            findResolution = str(re.findall("Rect:(.*)(\[)", str(resolution_checked))[0][0]).strip()
            if findResolution != "(0,0,0,0)":
                find = True
                resolution_checked.Click()
                break
        else:
            print("Resolution error")
        if count < 10:
            pyautogui.scroll(500)
            sleep(0.5)
        else:
            pyautogui.scroll(-500)
            sleep(0.5)
        count += 1
        sleep(0.5)
    sleep(1)
    settings_frame.ButtonControl(searchDepth=3, Name="打开设备(O)").Click()
    # -- Need Modified, 等待时间
    sleep(5)  # sleep(3)
    pyautogui.hotkey("alt", "1")


# 获取当前分辨率下的摄像头的帧率和位率并返回一个list
def getPlayerInformation():
    pyautogui.hotkey("ctrl", "f1")
    # -- Need Modified, 等待时间
    sleep(8)  # sleep(3)
    player_information = uiautomation.WindowControl(searchDepth=1, Name="播放信息")
    current_frameRate = player_information.TextControl(AutomationId="3201").GetWindowText()
    current_bitRate = player_information.TextControl(AutomationId="3386").GetWindowText()
    framerate = re.findall("->(.*)", current_frameRate)[0]
    bitrate = re.findall("\/(.*)\skbps", current_bitRate)[0]
    print("帧率：{} fps".format(framerate), end=" -- ")
    print("位率：{} kbps".format(bitrate))
    print("")
    return framerate, bitrate


# 关闭Potplayer
def closePotplayer():
    potplayer.kill()


# 传入potplayer启动exe路径
def test_standard_test_data(potplayerPath, calculate_count):
    if not os.path.exists("./log/"):
        os.makedirs("./log/")
    logger = logger_config(log_path="./log/{}_{}_{}.log".format(cur_time, "resolutionSwitchStress", "mainLog"),
                           logging_name="resolutionSwitchStress")
    result_list = []
    for i in range(1):
        try:
            openPotplayer(potplayer_path=potplayerPath)
            enterDeviceSettings()
            formatList = []
            all_format = getFormatList()
            print("\n 当前存在{}种分辨率，即将对这些分辨率格式开始测试……".format(len(all_format)))
            logger.info("\n 当前存在{}种分辨率，即将对这些分辨率格式开始测试……".format(len(all_format)))
            print(all_format)
            closePotplayer()
            i = 0
            for format in all_format:
                i += 1
                logger.info("第{}次测试 -- 当前测试分辨率为：{}".format(str(i), format))
                print("第{}次测试 -- 当前测试分辨率为：{}".format(str(i), format))
                openPotplayer(potplayer_path=potplayerPath)
                enterDeviceSettings()
                switchResolution(format)
                testCount = calculate_count
                xlsxName = format
                getVIbus(xlsxName, testCount)
                closePotplayer()
        except Exception as ex:
            logger.error("Some error happened : {}".format(str(ex)))
            logging.error("\n" + traceback.format_exc())
            print("Some error happened : {}".format(str(ex)))
            closePotplayer()
            continue
        finally:
            closePotplayer()


def getVIbus(xlsxName="VIbusRecord.xlsx", testCount=0):
    xlsxName = xlsxName + ".xlsx"
    xlsxName = xlsxName.strip().replace(":", "_")
    print(xlsxName)
    data = [["number", "VBUS", "IBUS"]]
    for i in range(1, testCount + 1):
        sleep(1)
        childrenList = ui.GroupControl(searchDepth=5, Name="参数显示").GetChildren()
        vbus = childrenList[0].GetChildren()[1].Name
        ibus = childrenList[1].GetChildren()[1].Name
        print("catch time is 【{}】current vbus is [{}], ibus is [{}]".format(i, vbus, ibus))
        data.append([i, vbus, ibus])
        write_into_excel(xlsxName, data)


def write_into_excel(filename, data):
    if not os.path.exists("./result"):
        os.mkdir("./result")
        print("Create folder success!")
    file_path = "./result/{}".format(filename)
    df = pd.DataFrame(columns=data)
    df.to_excel(file_path, index=True)
    print("{} data fill success!".format(filename))


if __name__ == '__main__':
    sleep(3)
    """
        修改自身potplayer的打开目录，测试相机通过usb电流计连接（指定），并打开电流计上位机程序
    """
    potplayerPath = "D:\PotPlayer\PotPlayerMini64.exe"
    calculate_count = 60
    try:
        test_standard_test_data(potplayerPath, calculate_count)
    except Exception as ex:
        print("Main program has error please check: {}".format(str(ex)))
    finally:
        print("Test Finished!")
