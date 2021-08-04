# coding = utf8

import os
import subprocess
import time

os.path.abspath(".")

import uiautomation

"""
    绝大多数Windows软件的自动化控件操作等可以用uiautomation库来实现：
    1、Python-UIAutomation-for-Windows-master + uiautomation
    2、 automation.py（搜索控件）
    3、 pyautogui模拟键盘操作，快捷键等，对于一些uiautomation搜索不到的UI控件
"""

subprocess.Popen("D:\EVCapture\EVCapture.exe")
time.sleep(2)
ev_frame = uiautomation.WindowControl(searchDepth=1, Name="EV录屏")
# ev_frame.SetTopmost(True)
# ev_frame.TextControl(Name="场景编辑").Click()
ev_frame.TextControl(searchDepth=9, Name="图片水印").Click()
