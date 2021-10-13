# coding = utf8
import os
import subprocess
import time
from time import sleep

import pyautogui
import uiautomation

os.path.abspath(".")
os.path.join(
    r"C:\Users\CHENGUANGTAO\Desktop\SMD0301扫地机\上位机\视熙\激光雷达数据采集程序v1.0.4.2_20211012_MSVC2019_64bit-Release\build-seevision-smd0301-gui-Desktop_Qt_5_15_2_MSVC2019_64bit-Release\resource\model.json")

from serial.tools.list_ports import *

cur_time = time.strftime("%Y%m%d_%H%M%S")


def checkDeviceConnect():
    isConnect = False
    cycle_count = 0
    current_port = ""
    while not isConnect:
        sleep(1)
        cycle_count += 1
        if cycle_count >= 301:
            return False
        plist = list(comports())
        for port in plist:
            print("Current test number is : {} - {}".format(str(cycle_count), str(list(port))))
            for port_number in list(port):
                if "Silicon Labs CP210x USB to UART Bridge" in port_number:
                    isConnect = True
                    current_port = re.findall("\((.*)\)", port_number)
    return current_port[0]


def openSeevisionVisualizer(
        seevisionVisualizer_path=r"C:\Users\CHENGUANGTAO\Desktop\SMD0301扫地机\上位机\视熙\激光雷达数据采集程序v1.0.4.2_20211012_MSVC2019_64bit-Release\build-seevision-smd0301-gui-Desktop_Qt_5_15_2_MSVC2019_64bit-Release\SeeVisionSerialVisualizer.exe"):
    global seevisionVisualizer
    seevisionVisualizer = subprocess.Popen(seevisionVisualizer_path)
    sleep(2)


def closeSeevisionVisualizer():
    seevisionVisualizer.kill()
    sleep(2)


# 1、启动SeeVisionSerialVisualizer.exe - openSeevisionVisualizer
# 2、获取当前的port - checkDeviceConnect
# 3、有port则进行连接：->点击设备控制tab->点击刷新设备->点击当前port->点击连接设备 - connect_device
# 4、获取基础数据 - get_basic_data
# 5、点击关闭设备 - disconnect_device
# 6、关闭SeeVisionSerialVisualizer.exe - closeSeevisionVisualizer
# step1 ~ 6重复1000次
# python stableTest.py >./run.log
def connect_device(current_port):
    device_control = uiautomation.TabItemControl(searchDepth=5, Name="设备控制")
    device_control.Click()
    sleep(1)
    refresh_button = uiautomation.ButtonControl(searchDepth=6, Name="刷新设备")
    refresh_button.Click()
    sleep(1)
    cur_port = uiautomation.ListItemControl(searchDepth=7, Name=current_port)
    cur_port.Click()
    sleep(1)

    # 增加一个选择波特率115200，通过键盘输入+回车进行对ComboBox的item进行选择
    baud_rate = uiautomation.ComboBoxControl(
        AutomationId="MainWindow.centralwidget.wRootCtrlTab.qt_tabwidget_stackedwidget.wCtrlTab.wSetBaudCombo")
    baud_rate.Click()
    sleep(1)
    pyautogui.typewrite("115200")
    sleep(0.5)
    pyautogui.press("enter")
    sleep(0.5)

    connect_button = uiautomation.ButtonControl(searchDepth=6, Name="连接设备")
    connect_button.Click()
    sleep(1)


def disconnect_device():
    disconnect_button = uiautomation.ButtonControl(searchDepth=6, Name="关闭设备")
    disconnect_button.Click()


# 获取测量频率，断开时为0，连接时不为0进行判断结果
def get_basic_data():
    measure_frequence = uiautomation.TextControl(
        AutomationId="MainWindow.centralwidget.wPrevStackView.wPrevPolarRoot.wSamplingFreqCounterLabel")
    return measure_frequence.Name


def connect_disconnectTest():
    result_list = []
    # 1000次4H，测2000次，8H，当前120次30分钟
    for i in range(10):
        result = False
        current_port = checkDeviceConnect()
        test_number = str(i + 1)
        print("第{}次测试：".format(test_number))
        if current_port:
            openSeevisionVisualizer()
            connect_device(current_port)
            sleep(3)
            print("OK,connect success!")
            measure_frequence = get_basic_data()
            if measure_frequence:
                print("当前测量频率为：{}".format(measure_frequence))
                sleep(3)
                result = True
                disconnect_device()
            closeSeevisionVisualizer()
        else:
            result = False
        result_list.append([test_number, cur_time, result])
    print("{}:Current test result is {}".format(cur_time, str(result)))
    return result_list


if __name__ == '__main__':
    seevisionVisualizerRootPath = r"C:\Users\CHENGUANGTAO\Desktop\SMD0301扫地机\上位机\视熙\激光雷达数据采集程序v1.0.4.2_20211012_MSVC2019_64bit-Release\build-seevision-smd0301-gui-Desktop_Qt_5_15_2_MSVC2019_64bit-Release"
    os.chdir(seevisionVisualizerRootPath)
    for result in connect_disconnectTest():
        print(result)
