# coding = utf8
import multiprocessing
import os
import re
import subprocess

from airtest.core.api import *
from airtest.core.error import DeviceConnectionError
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.exceptions import PocoNoSuchNodeException

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:OralCheckTest.py
    @Author:十二点前要睡觉
    @Date:2022/5/26 15:56
"""


def get_serial_number():
    devices_stream = os.popen("adb devices")
    devices = devices_stream.read()
    serial_no = re.findall("(.*)\tdevice", devices)
    devices_stream.close()
    return serial_no


def connectDevice(device_serial):
    device_ = connect_device("Android:///{}".format(device_serial[0]))
    device_.wake()
    device_.unlock()
    poco = AndroidUiautomationPoco(device=device_, use_airtest_input=False, screenshot_each_action=False)
    return device_, poco


def reopenTest():
    device_ready = connectDevice(get_serial_number())
    global device, poco
    device = device_ready[0]
    poco = device_ready[1]
    if not os.path.exists("./snapshot/"):
        os.mkdir("./snapshot/")
    device.home()
    position1 = poco(text="口算检查").wait(3).get_position()
    poco(text="口算检查").wait(3).click()
    position2 = poco("com.youdao.hardware.panda.countinginspect:id/ivBack").wait(3).get_position()
    poco("com.youdao.hardware.panda.countinginspect:id/ivBack").wait(3).click()
    for i in range(10000):
        poco.click(position1)
        device.snapshot("./snapshot/Current{}_open.jpeg".format(i))
        poco.click(position2)



if __name__ == '__main__':
    reopenTest()
