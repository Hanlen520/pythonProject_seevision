# coding = utf8
import os
import re
import subprocess
from time import sleep

import pyautogui
from uiautomation import uiautomation

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:windowsControl.py
    @Author:十二点前要睡觉
    @Date:2022/3/23 10:35
"""


def openPotplayer(potplayer_path="D:\PotPlayer\PotPlayerMini64.exe"):
    global potplayer
    potplayer = subprocess.Popen(potplayer_path)
    sleep(2)
    if uiautomation.TextControl(searchDepth=3, Name="检查更新：").Exists():
        pyautogui.press("esc")


def enterDeviceSettings():
    global potplayer_frame
    global settings_frame
    potplayer_frame = uiautomation.WindowControl(searchDepth=1, Name="PotPlayer")
    pyautogui.hotkey("alt", "d")
    settings_frame = uiautomation.WindowControl(searchDepth=2, Name="设备设置")


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
    sleep(5)


def openHidTool(hidtool_path="D:\HIDTools_2.5\HIDTool_2_5.exe"):
    global hidtool
    hidtool = subprocess.Popen(hidtool_path)
    sleep(2)


def closeHidTool():
    if hidtool:
        hidtool.kill()


# 关闭Potplayer
def closePotplayer():
    if potplayer:
        potplayer.kill()


# 放大
def hidZoomIn(step):
    step_edit = uiautomation.EditControl(AutomationId="eptz_size_textbox_length")
    step_edit.GetValuePattern().SetValue("")
    step_edit.SendKeys(str(step))
    uiautomation.ButtonControl(AutomationId="button2").Click()
    sleep(1)


# 缩小
def hidZoomOut(step):
    step_edit = uiautomation.EditControl(AutomationId="eptz_size_textbox_length")
    step_edit.GetValuePattern().SetValue("")
    step_edit.SendKeys(str(step))
    uiautomation.ButtonControl(AutomationId="button3").Click()
    sleep(1)


# 复位
def hidReset():
    uiautomation.ButtonControl(AutomationId="button4").Click()
    sleep(1)


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


if __name__ == '__main__':
    potplayer_path = r"D:\PotPlayer\PotPlayerMini64.exe"
    openPotplayer(potplayer_path)
    enterDeviceSettings()
    resolution = "YUY2 960×540P 30(P 16:9)"
    switchResolution(resolution)
    hidtool_path = r"D:\HIDTools_2.5\HIDTool_2_5.exe"
    openHidTool(hidtool_path)
    hidZoomIn(5)
    hidZoomOut(1)
    hidReset()
