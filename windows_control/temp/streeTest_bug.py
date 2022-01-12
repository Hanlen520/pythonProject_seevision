# coding = utf8
import os
import re
import subprocess

os.path.abspath(".")
"""
    @Project:PycharmProjects
    @File:streeTest_bug.py
    @Author:十二点前要睡觉
    @Date:2022/1/12 17:32
"""

import pyautogui
import uiautomation
from time import sleep

if __name__ == '__main__':
    for i in range(10000):
        print(
            "=====================================第{}次Amcap MJPEG 1080P->H264 4K分辨率切换压测=====================================".format(
                str(i)))
        amcap = uiautomation.ButtonControl(searchDepth=5, Name="Capture Application (Sample)")
        amcap.Click()
        sleep(3)
        option = uiautomation.MenuItemControl(searchDepth=3, Name="Options")
        option.Click()
        sleep(1)
        video_capture_pin = uiautomation.MenuItemControl(searchDepth=3, Name="Video Capture Pin...")
        video_capture_pin.Click()
        sleep(1)
        format_list = uiautomation.ComboBoxControl(AutomationId="1058", Depth=5)
        format_list.Click()
        sleep(1)
        h264 = uiautomation.ListItemControl(Depth=7, Name="H264")
        h264.Click()
        sleep(1)
        resolution_list = uiautomation.ComboBoxControl(AutomationId="1059", Depth=5)
        resolution_list.Click()
        sleep(1)
        pyautogui.scroll(1000)
        sleep(0.5)
        four_k = uiautomation.ListItemControl(Depth=7, Name="3840 x 2160  (default)")
        four_k.Click()
        open_button = uiautomation.ButtonControl(Depth=3, Name="确定")
        open_button.Click()
        sleep(5)
        pyautogui.screenshot("./bugVerified/{}.jpg".format(i))
        sleep(1)
        pid_get = subprocess.Popen("tasklist | grep amcap", shell=True, stdout=subprocess.PIPE).communicate()[0]
        pid = re.findall("amcap v3.0.9.exe(.*)Console", str(pid_get))[0].strip(" ")
        os.system("taskkill /pid {}".format(pid))
