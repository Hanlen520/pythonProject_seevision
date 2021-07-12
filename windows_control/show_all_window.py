# coding = utf8

import os

os.path.abspath(".")
import win32gui

handle_title = {}

"""
    打印出当前Windows已启动的所有窗体的句柄和名称
"""


def get_all_running_handle(handle_, mouse):
    if win32gui.IsWindow(handle_) and win32gui.IsWindowEnabled(handle_) and win32gui.IsWindowVisible(handle_):
        handle_title.update({handle_: win32gui.GetWindowText(handle_)})


if __name__ == '__main__':
    win32gui.EnumWindows(get_all_running_handle, 0)
    for handle, title in handle_title.items():
        if title:
            print(handle, title)
