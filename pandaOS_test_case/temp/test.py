# coding = utf8
import os

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:test.py
    @Author:十二点前要睡觉
    @Date:2022/1/20 17:19
"""
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco


def init_device(device_serial):
    device_ = connect_device("Android:///{}".format(device_serial))
    poco = AndroidUiautomationPoco(device=device_, use_airtest_input=False, screenshot_each_action=False)
    return device_, poco


if __name__ == '__main__':
    GET = init_device(device_serial="127.0.0.1:7555")
    device_i = GET[0]
    poco_i = GET[1]
    machine_radio = poco_i(text="机动车损失险").parent().children()[0].children()[0]
    print(machine_radio.get_text())
    machine_radio.click()
    machine_radio.invalidate()
    print(machine_radio.get_text())
