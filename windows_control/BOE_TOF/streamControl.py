# coding = utf8
import os
import subprocess
import time
from time import sleep

os.path.abspath(".")
import pyautogui

import uiautomation as ui
import pandas as pd

"""
    控制BOE_TOF上位机开关
    1、连接固件，检查端口和更新驱动程序，SecureCRTPortable连接端口
    2、运行脚本进行测试，打开相机，关闭相机
    3、第一场景，关闭相机5秒后打开相机
    4、第二场景，关闭相机20秒后打开相机
    5、持续运行两小时，查看下位机开关流是否正常：SecureCRTPortable查看是否存在ldxldx sig"	"1、不同场景下，打开或关闭相机，下位机运行正常
    2、下位机开关流正常，每一个场景的log中不存在ldxldx sig"
"""


def open_BOE_TOF(boe_tof_path):
    """
    打开Boe_tof上位机程序
    :param boe_tof_path:上位机程序所在路径
    :return: None
    """
    global boe_tof
    boe_tof = subprocess.Popen(boe_tof_path)


def scene_test(close_time, cycle_times):
    """
    第一场景：关闭相机5s后打开相机
    第二场景：关闭相机20s后打开相机
    :return:None
    """

    data = [["number", "time", "fps"]]
    filename = "test_stream_control_{}s.xlsx".format(str(close_time))

    for i in range(cycle_times):
        open_BOE_TOF(boe_tof_path)
        ui.TabItemControl(searchDepth=5, Name="相机控制").Click()
        middle_x = get_data()[0]
        middle_y = get_data()[1]
        number = str(i + 1)
        open_camera()
        sleep(2)
        close_camera()

        open_camera()
        pyautogui.click(middle_x, middle_y)
        sleep(3)
        fps_open = ui.TextControl(AutomationId="MainWindow.centralwidget.fps_disp").Name
        print("Camera opened and FPS is : {}".format(fps_open))
        sleep(close_time)
        close_camera()
        pyautogui.click(middle_x, middle_y)
        cur_time = time.strftime("%Y%m%d_%H%M%S")
        data.append([number, cur_time, "相机开启时FPS:{}".format(fps_open)])
        write_into_excel(filename, data)

        boe_tof.kill()


def open_camera():
    ui.ButtonControl(searchDepth=6, Name="刷新相机列表").Click()
    ui.ListItemControl(searchDepth=7, Name="UVC DEPTH").Click()
    open_camera = ui.ButtonControl(searchDepth=6, Name="打开相机")
    open_camera.Click()


def close_camera():
    close_camera = ui.ButtonControl(searchDepth=6, Name="关闭相机")
    close_camera.Click()


def get_data():
    rect = ui.CustomControl(AutomationId="MainWindow.centralwidget.rgbCameraWidget").BoundingRectangle
    position = str(rect).split(")")[0].replace("(", "")
    position = position.split(",")
    frame_rect = str(rect).split(")")[1].replace("[", "").replace("]", "").split("x")
    frame_x = int(frame_rect[0])
    frame_y = int(frame_rect[1])
    print(frame_x, frame_y)
    middle_x = int(position[0]) + frame_x / 2
    middle_y = int(position[1]) + frame_y / 2
    return middle_x, middle_y


def write_into_excel(filename, data):
    if not os.path.exists("./result"):
        os.mkdir("./result")
        print("Create folder success!")
    file_path = "./result/{}".format(filename)
    df = pd.DataFrame(columns=data)
    df.to_excel(file_path, index=True)
    print("{} generate success!".format(filename))


if __name__ == '__main__':
    global boe_tof_path
    boe_tof_path = r"C:\Users\Liuwe\Desktop\BOE_TOF\BOE_TOF\SeeVision3DCameraViewer_V1.8.7_20211105190051_win_x64_2\SeeVision3DCameraViewer.exe"
    # test wait 5s close_time = 5, cycle_time = 720
    # test wait 20s close_time = 20, cycle_time = 288
    # connect to SecurtCRT in background to check the log whether exists ldxldx sig
    close_time = 5
    cycle_time = 720
    # test wait 20s close_time = 20, cycle_time = 288
    # connect to SecurtCRT in background to check the log whether exists ldxldx sig
    # close_time = 20
    # cycle_time = 288
    # scene_test(close_time, cycle_time)
    inf = os.popen("adb devices").read()
    print(inf)
