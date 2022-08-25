# coding = utf8
import os
import re
from time import sleep

import pandas as pd
from airtest.core.api import connect_device
from airtest.core.error import DeviceConnectionError
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:outputStreamStressTest.py
    @Author:十二点前要睡觉
    @Date:2022/8/22 14:31
"""
"""
    此脚本用于Android项目 - VS680的显示输出流的切换压力测试
    原理：
    通过UI自动化进行控件定位，设备连接HDMI + MIPI两种屏幕，在之间进行切换测试
    因其每次切换成功后都会在对应屏幕上显示当前界面，由此来判断是否切换成功的标志
"""


def get_serial_number():
    devices_stream = os.popen("adb devices")
    devices = devices_stream.read()
    serial_no = re.findall("(.*)\tdevice", devices)
    devices_stream.close()
    return serial_no


def init_device(device_serial):
    device_ = connect_device("Android:///{}".format(device_serial))
    device_.wake()
    device_.unlock()
    poco = AndroidUiautomationPoco(device=device_, use_airtest_input=False, screenshot_each_action=False)
    return device_, poco


def startDisplayModeAppSwitchTest(device_test, poco_test, pattern):
    device_test.start_app_timing("com.synaptics.tv.settings", "com.synaptics.tv.settings.DisplayActivity")
    screen_width = int(device_test.display_info["width"])
    screen_height = int(device_test.display_info["height"])
    device_test.swipe((screen_width * 0.8, screen_height * 0.3), (screen_width * 0.8, screen_height * 0.05))
    multiDisplay = poco_test(text="Multi Display")
    multiDisplay.click()
    device_test.swipe((screen_width * 0.8, screen_height * 0.3), (screen_width * 0.8, screen_height * 0.05))
    poco_test(text=pattern).click()
    device_ready_now, poco_ready_now = rebootDeviceForOnline(device_test)
    print("{} switch test done!".format(pattern))
    return device_ready_now, poco_ready_now


def rebootDeviceForOnline(device_test):
    try:
        device_test.shell("reboot")
    except DeviceConnectionError:
        print("等待设备重启！")
    finally:
        while True:
            sleep(1)
            try:
                device_ready_now = connect_device("Android:///{}".format(device_serialno))
                device_ready_now.wake()
                device_ready_now.unlock()
                poco_ready_now = AndroidUiautomationPoco(device=device_ready_now, use_airtest_input=False,
                                                         screenshot_each_action=False)
                if "com.seevision.tv.launcher" in device_ready_now.shell("dumpsys window | grep mCurrentFocus"):
                    print("设备重启完成!!!!")
                    return device_ready_now, poco_ready_now
            except Exception as ex:
                print("等待设备重启")
                continue


global result_list


def standard_test_DataGenerate(result_list=[]):
    alist = []
    blist = []
    clist = []
    for result in result_list:
        alist.append(result[0])
        blist.append(result[1])
        clist.append(result[2])
    df = pd.DataFrame({"测试次数": alist, "测试Pattern": blist, "切换结果": clist})
    df.to_excel("./result.xlsx", engine="openpyxl")


if __name__ == '__main__':
    result_list = []
    device_serialno = get_serial_number()[0]
    device_ready = init_device(device_serialno)
    device_test = device_ready[0]
    poco_test = device_ready[1]
    test_display_pattern = ["HDMI", "MIPI", "HDMI MPG1 + MIPI G2", "HDMI MG1 + MIPI G2", "HDMI MG1 + MIPI P"]
    device_ready_now = ""
    poco_ready_now = ""
    test_count = 1000
    for i in range(test_count):
        for pattern in test_display_pattern:
            try:
                result = "FALSE"
                device_ready_now, poco_ready_now = startDisplayModeAppSwitchTest(device_test, poco_test, pattern)
                if (device_ready_now and poco_ready_now) is not None:
                    result = "PASS"
                else:
                    result = "FALSE"
                result_list.append([str(i), pattern, result])
            except Exception:
                print("开始下一个pattern测试")
            finally:
                device_test = device_ready_now
                poco_test = poco_ready_now
                standard_test_DataGenerate(result_list)
