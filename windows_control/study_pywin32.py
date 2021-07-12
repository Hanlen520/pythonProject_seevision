# coding = utf8

import os
from time import sleep

import win32com.client
import win32gui

os.path.abspath(".")

# 基于pywin32库

import win32api
import win32con
import win32file


def SimpleFileDemo():
    # 基于pywin32库简单演示demo
    testName = os.path.join(win32api.GetTempPath(), "win32temp_demo_file.txt")
    if os.path.exists(testName):
        os.unlink(testName)

    # open for writing
    handle = win32file.CreateFile(testName, win32file.GENERIC_WRITE, 0, None, win32con.CREATE_NEW, 0, None)
    test_data = "Hello there".encode("ascii")
    win32file.WriteFile(handle, test_data)
    handle.Close()

    # open for reading
    handle = win32file.CreateFile(testName, win32file.GENERIC_READ, 0, None, win32con.OPEN_EXISTING, 0, None)
    rc, data = win32file.ReadFile(handle, 1024)
    handle.Close()
    if data == test_data:
        print("Successfully wrote and read a file")
    else:
        raise Exception("Got different data back???")
    # os.unlink(testName)


def open_program():
    # open chrome：打开windows程序
    win32api.ShellExecute(1, "open", r"C:\Users\CHENGUANGTAO\AppData\Local\Google\Chrome\Application\chrome.exe", "",
                          "", 1)


def find_handle():
    # 查找窗口句柄
    para_hld = win32gui.FindWindow(None, "Foxmail")
    print("handle:{}".format(para_hld))
    handle_title = win32gui.GetWindowText(para_hld)
    print("handle_title:{}".format(handle_title))
    handle_classname = win32gui.GetClassName(para_hld)
    print("handle_classname:{}".format(handle_classname))
    return para_hld


def show_all_handle():
    # 展示当前所有运行在上层界面的窗口
    handle_list = []
    win32gui.EnumWindows(lambda handle_i, param: param.append(handle_i), handle_list)
    for handle_ in handle_list:
        if win32gui.IsWindow(handle_) and win32gui.IsWindowVisible(handle_) and win32gui.IsWindowEnabled(handle_):
            title = win32gui.GetWindowText(handle_)
            if title:
                print("{} : {}".format(handle_, title))


def put_handle_on_top(handle_item):
    # 将handle句柄的窗口放到窗口顶部并最大化
    win32gui.ShowWindow(handle_item, win32con.SW_MAXIMIZE)
    win32gui.SetForegroundWindow(handle_item)


def monitor_keyboard_input():
    # 模拟键盘输入
    win32api.keybd_event(13, 0, 1, 0)  # 第三位0，按下，1释放
    # win32api.keybd_event(13, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)


def monitor_mouse_keyboard_input():
    # 模拟鼠标键盘输入
    print("当前鼠标位置坐标：{}".format(win32api.GetCursorPos()))
    print("当前显示器长{}, 宽{}".format(win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)))
    monitor_length = win32api.GetSystemMetrics(0)
    monitor_width = win32api.GetSystemMetrics(1)
    center_point = (int(monitor_length / 2), int(monitor_width / 2))
    win32api.SetCursorPos((center_point[0], center_point[1]))
    print("当前鼠标位置坐标：{}".format(win32api.GetCursorPos()))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, center_point[0], center_point[1], 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, center_point[0], center_point[1], 0, 0)


if __name__ == '__main__':
    # win32api.MessageBox(None, "Hello pywin32!", "PyWin32", win32con.MB_OK)
    # SimpleFileDemo()
    # open_program()
    # find_handle()
    # show_all_handle()
    # put_handle_on_top(find_handle())
    # sleep(2)
    # monitor_keyboard_input()
    # while True:
    #     sleep(1)
    #     monitor_mouse_input()
    monitor_mouse_keyboard_input()
