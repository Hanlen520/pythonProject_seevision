# coding = utf8
import os
from time import sleep

import pyautogui

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5
os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:ocr_script.py
    @Author:十二点前要睡觉
    @Date:2022/4/12 11:41
"""


# bin:D:\PycharmProjects\pythonProject_seevision\HW_Scripts\OCR_PADS\Mentor PADS VX2.5\PADS_2.5\PADSVX.2.5\SDD_HOME\common\win32\bin\powerpcb.exe
# pcb_file:D:\PycharmProjects\pythonProject_seevision\HW_Scripts\OCR_PADS\pcb_file

# 打开Potplayer，传入potplayer启动exe路径
# 先在C盘创建文件夹：flexlm->将LICENSE.DAT放入文件夹中，后续脚本打开授权检测用
# def openPADSLayout(
#         padsLayout_path=r"D:\PycharmProjects\pythonProject_seevision\HW_Scripts\OCR_PADS\Mentor PADS VX2.5\PADS_2.5\PADSVX.2.5\SDD_HOME\common\win32\bin\powerpcb.exe"):
#     global padsLayout
#     padsLayout = subprocess.Popen(padsLayout_path)
#     sleep(5)
#
#
# def openPcbFile(
#         pcb_path=r"D:\PycharmProjects\pythonProject_seevision\HW_Scripts\OCR_PADS\pcb_file\S00703_V01_20220409.pcb"):
#     pyautogui.hotkey("ctrl", "o")
#     ui.ButtonControl(searchDepth=8, Name="上一个位置").Click()
#     pyautogui.press("delete")
#     ui.PaneControl(AutomationId="41477").SendKeys(pcb_path)
#     ui.ButtonControl(searchDepth=3, Name="打开(O)").Click()
#     ui.ButtonControl(searchDepth=3, Name="最大化").Click()
#     pyautogui.press("HOME")


def openSearchBox(name="D15"):
    pyautogui.press("s")
    pyautogui.press("s")
    pyautogui.typewrite(" {}".format(name))
    pyautogui.press("enter")
    pyautogui.hotkey("ctrl", "w")
    for i in range(6):
        pyautogui.doubleClick()
    pyautogui.hotkey("ctrl", "w")


def resize_home():
    pyautogui.press("HOME")


def catchFramePicture(name):
    if not os.path.exists("./screenshot/"):
        os.mkdir("./screenshot/")
    x, y = pyautogui.position()
    pyautogui.screenshot("./screenshot/{}.jpeg".format(name), region=(x - 325, y - 175, 650, 350))


if __name__ == '__main__':
    # openPADSLayout()
    # openPcbFile()
    sleep(3)
    demo_list = ["D15", "D16", "CM12", "CM23", "CM21", "C93"]
    # for demo in demo_list:
    #     openSearchBox(demo)
    #     sleep(1)
    #     resize_home()
    name = "D15"
    openSearchBox(name)
    catchFramePicture(name)
