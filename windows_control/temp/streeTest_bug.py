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
    for i in range(100):
        print(
            "=====================================第{}次Amcap MJPEG 1080P->H264 4K分辨率切换压测=====================================".format(
                str(i)))
        amcap = uiautomation.ButtonControl(searchDepth=5, Name="Capture Application (Sample)")
        amcap.Click()
        sleep(3)
        option = uiautomation.MenuItemControl(searchDepth=3, Name="Options")
        option.Click()
        sleep(0.5)
        video_capture_pin = uiautomation.MenuItemControl(searchDepth=3, Name="Video Capture Pin...")
        video_capture_pin.Click()
        sleep(0.5)
        format_list = uiautomation.ComboBoxControl(AutomationId="1058", Depth=5)
        format_list.Click()
        sleep(0.5)
        h264 = uiautomation.ListItemControl(Depth=7, Name="H264")
        h264.Click()
        sleep(0.5)
        resolution_list = uiautomation.ComboBoxControl(AutomationId="1059", Depth=5)
        resolution_list.Click()
        sleep(0.5)
        pyautogui.scroll(3000)
        sleep(1)
        four_k = uiautomation.ListItemControl(Depth=7, Name="3840 x 2160  (default)")
        four_k.Click()
        sleep(0.5)
        open_button = uiautomation.ButtonControl(Depth=3, Name="确定")
        open_button.Click()
        sleep(3)
        pyautogui.screenshot("./bugVerified/{}.jpg".format(i))
        sleep(0.5)
        pid_get = subprocess.Popen("tasklist | grep amcap", shell=True, stdout=subprocess.PIPE).communicate()[0]
        pid = re.findall("amcap v3.0.9.exe(.*)Console", str(pid_get))[0].strip(" ")
        os.system("taskkill /pid {}".format(pid))
        sleep(0.5)
