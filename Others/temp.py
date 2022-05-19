# coding = utf8
import os
import re
import subprocess
from time import sleep

import pyautogui

pyautogui.FAILSAFE = True
from uiautomation import uiautomation

os.path.abspath(".")


def openLocalCamera():
    uiautomation.TextControl(searchDepth=14, Name="设备管理").Click()
    uiautomation.TextControl(searchDepth=14, Name="摄像头").Click()


def closeLocalCamera():
    pass


if __name__ == "__main__":
    print("OK")
    openLocalCamera()