# coding = utf8
import os
import subprocess
from time import sleep

import pandas as pd
import uiautomation

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:flash_stress.py
    @Author:十二点前要睡觉
    @Date:2022/8/2 14:07
"""


def openHidTool(hidTool):
    print("打开HidTool")
    global hidTool_exe
    hidTool_exe = subprocess.Popen(hidTool)
    sleep(2)


def closeHidTool():
    sleep(1)
    print("关闭HidTool")
    hidTool_exe.kill()


def enterBootloader():
    uiautomation.ButtonControl(searchDepth=3, Name="启动Bootloader模式").Click()
    uiautomation.ButtonControl(searchDepth=3, Name="确定").Click()


def getVersion():
    uiautomation.ButtonControl(searchDepth=3, Name="获取音频版本号").Click()
    audio_version = uiautomation.TextControl(AutomationId="65535").GetWindowText()
    uiautomation.ButtonControl(searchDepth=3, Name="确定").Click()
    return audio_version


def toExcel(data):
    number_iList = data[0]
    number_jList = data[1]
    result_zList = data[2]
    df = pd.DataFrame(
        {"old_version": number_iList, "new_version": number_jList, "test_result": result_zList})
    df.to_excel("./result.xlsx")


def flashIntoVersion(version):
    print(version)
    if version == old:
        path_ = old_Version
    elif version == new:
        path_ = new_Version
    os.chdir("{}release_images/".format(path_))
    os.system("sh ./flash.sh")
    sleep(1)
    os.chdir(os.path.dirname(os.path.realpath(__file__)))


if __name__ == '__main__':
    old = "2.3.1"
    new = "2.3.4"
    test_count = 4000
    hidTool = r"C:\Users\CHENGUANGTAO\Desktop\视熙测试部脚本以及测试工具\测试工具\HIDTool2.8\HIDTool.exe"
    old_Version = r"./2_3_1/"
    new_Version = r"./2_3_4/"
    version = old
    data_list_i = []
    data_list_j = []
    data_list_r = []
    for i in range(test_count):
        openHidTool(hidTool)
        audio_version = getVersion()
        closeHidTool()
        audio_version = str(audio_version).split(":")[1].replace(" ", "").strip()
        print(audio_version)
        if audio_version == old:
            version = new
        if audio_version == new:
            version = old
        data_list_i.append(audio_version)
        openHidTool(hidTool)
        enterBootloader()
        closeHidTool()
        flashIntoVersion(version)
        sleep(90)
        openHidTool(hidTool)
        audio_version_2 = getVersion()
        audio_version_2 = str(audio_version_2).split(":")[1].replace(" ", "").strip()
        closeHidTool()
        data_list_j.append(audio_version_2)
        if (version == new) & (audio_version_2 == new) | (version == old) & (audio_version_2 == old):
            data_list_r.append("PASS")
        else:
            data_list_r.append("FAIL")
        toExcel([data_list_i, data_list_j, data_list_r])
