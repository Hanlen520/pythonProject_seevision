# coding = utf8
import os
import subprocess
from time import sleep

import imagehash
import pyautogui
import uiautomation as ui
from PIL import Image
from serial import SerialException

from ralayControl.BOE_STRESS_TEST import serialComportList
from ralayControl.BOE_STRESS_TEST.serialControl import SerialSwitch

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:stress_test_outflow.py
    @Author:十二点前要睡觉
    @Date:2022/2/17 14:10
"""


def open_BOE_TOF(boe_tof_path):
    """
    打开Boe_tof上位机程序
    :param boe_tof_path:上位机程序所在路径
    :return: None
    """
    sleep(1)
    global boe_tof
    boe_tof = subprocess.Popen(boe_tof_path)
    print("打开BOE上位机")
    # os.startfile(boe_tof_path)
    sleep(3)
    # pyautogui.scroll(-500)
    # boe_tof = ui.ListItemControl(searchDepth=8, Name="SeeVision3DCameraViewer.exe")
    # boe_tof.DoubleClick()


def open_camera(circle_times):
    print("打开相机")
    sleep(0.5)
    ui.TabItemControl(searchDepth=5, Name="相机控制").Click()
    sleep(0.5)
    ui.ButtonControl(searchDepth=6, Name="刷新相机列表").Click()
    sleep(0.5)
    # ui.ListItemControl(searchDepth=7, Name="UVC DEPTH").Click()
    ui.ListItemControl(searchDepth=7, Name="UVC DEPTH").Click()
    sleep(0.5)
    open_camera = ui.ButtonControl(searchDepth=6, Name="打开相机")
    open_camera.Click()
    sleep(3)
    print("进行截图")
    if not os.path.exists("./screenshot/"):
        os.mkdir("./screenshot/")
    pyautogui.screenshot("./screenshot/{}.jpg".format(circle_times))


def kill_BOE_TOF():
    print("关闭BOE上位机")
    sleep(0.5)
    boe_tof.kill()
    sleep(0.5)


def close_camera():
    print("关闭相机")
    close_camera = ui.ButtonControl(searchDepth=6, Name="关闭相机")
    close_camera.Click()


def voltage_5V_on(serialControl):
    try:
        print("打开5V USB供电")
        serialControl.switch_on(serialComportList.RELAY_CONTROL_COMPORT_2_OPEN)
        sleep(0.5)
    except SerialException:
        print("Not find Serial or somthing went wrong please check connection.")
        os.system("pause")


def voltage_5V_off(serialControl):
    try:
        print("关闭5V USB供电")
        serialControl.switch_off(serialComportList.RELAY_CONTROL_COMPORT_2_CLOSE)
        sleep(0.5)
    except SerialException:
        print("Not find Serial or somthing went wrong please check connection.")
        os.system("pause")


def voltage_12V_on(serialControl):
    try:
        print("打开12V USB供电")
        serialControl.switch_on(serialComportList.RELAY_CONTROL_COMPORT_1_OPEN)
        sleep(0.5)
    except SerialException:
        print("Not find Serial or somthing went wrong please check connection.")
        os.system("pause")


def voltage_12V_off(serialControl):
    try:
        print("关闭12V USB供电")
        serialControl.switch_off(serialComportList.RELAY_CONTROL_COMPORT_1_CLOSE)
        sleep(0.5)
    except SerialException:
        print("Not find Serial or somthing went wrong please check connection.")
        os.system("pause")


def picture_compare(original_image, compare_image):
    print("进行图片比对{} compare with {}".format(original_image, compare_image))
    original = imagehash.average_hash(Image.open(original_image))
    compare = imagehash.average_hash(Image.open(compare_image))
    if compare == original:
        result = "{} is PASS".format(compare_image)
    else:
        result = "{} is FAIL".format(compare_image)
    toTxt(result)


def toTxt(result):
    print("结果写入txt中》》》》》》[{}]".format(result))
    with open("./Result.txt", "a+") as f:
        f.write(result + "\n")


if __name__ == '__main__':
    global boe_tof_path
    boe_tof_path = r"D:\BOE_TOF\最新机器2022\SeeVision3DCameraViewer_V1.9.2_20220209140941_win_x64\SeeVision3DCameraViewer.exe"
    serialControl = SerialSwitch("COM3")
    original_image = "./originalImage.jpg"

    open_BOE_TOF(boe_tof_path)
    for i in range(3000):
        # for i in range(5):
        i += 1
        voltage_12V_on(serialControl)
        voltage_5V_on(serialControl)
        sleep(10)
        open_camera(i)
        close_camera()
        if i % 2 == 0:
            kill_BOE_TOF()
            open_BOE_TOF(boe_tof_path)
        picture_compare(original_image, "./screenshot/{}.jpg".format(i))
        voltage_12V_off(serialControl)
        voltage_5V_off(serialControl)
        sleep(3)
