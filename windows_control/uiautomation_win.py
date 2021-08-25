# coding = utf8

import os
import re
import subprocess
from time import sleep

import pyautogui

os.path.abspath(".")

import uiautomation

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
    sleep(3)
    player_information = uiautomation.WindowControl(searchDepth=1, Name="播放信息")
    current_frameRate = player_information.TextControl(AutomationId="3201").GetWindowText()
    current_bitRate = player_information.TextControl(AutomationId="3386").GetWindowText()
    print("当前分辨率帧率为：{}".format(current_frameRate))
    print("当前分辨率位率为：{}".format(current_bitRate))


def closePotplayer():
    potplayer.kill()


if __name__ == '__main__':
    for i in range(3):
        openPotplayer(potplayer_path="D:\PotPlayer\PotPlayerMini64.exe")
        enterDeviceSettings()
        switchResolution("YUY2 960×540P 30(P 16:9)")
        getPlayerInformation()
        closePotplayer()
