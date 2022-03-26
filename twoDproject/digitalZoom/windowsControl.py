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
    pass


# 缩小
def hidZoomOut(step):
    pass


# 复位
def hidReset():
    pass


if __name__ == '__main__':
    potplayer_path = r"D:\PotPlayer\PotPlayerMini64.exe"
    openPotplayer(potplayer_path)
    enterDeviceSettings()
    resolution = "YUY2 960×540P 30(P 16:9)"
    switchResolution(resolution)
    closePotplayer()
    hidtool_path = r"D:\HIDTools_2.5\HIDTool_2_5.exe"
    openHidTool(hidtool_path)
    closeHidTool()
