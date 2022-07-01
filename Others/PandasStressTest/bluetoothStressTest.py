# coding = utf8
import multiprocessing
import re
import subprocess

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

cur_time = time.strftime("%Y%m%d_%H%M%S")
os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:bluetoothStressTest.py
    @Author:十二点前要睡觉
    @Date:2022/6/6 10:50
"""


def get_serial_number():
    devices_stream = os.popen("adb devices")
    devices = devices_stream.read()
    serial_no = re.findall("(.*)\tdevice", devices)
    devices_stream.close()
    return serial_no


def init_device(device_serial):
    device_ = connect_device("Android:///{}".format(device_serial[0]))
    device_.wake()
    device_.unlock()
    poco = AndroidUiautomationPoco(device=device_, use_airtest_input=False, screenshot_each_action=False)
    return device_, poco


def logProcess():
    if not os.path.exists("./log/"):
        os.mkdir("./log/")
    subprocess.Popen("adb logcat -b all>./log/bluetooth_{}_logcat.log".format(cur_time), shell=True).communicate()[0]


def reopenTest(device_, poco, i):
    if not os.path.exists("./snapshot/"):
        os.mkdir("./snapshot/")
    device_.home()
    try:
        for i in range(10000):
            pass
    except Exception:
        pass
    finally:
        logProcess()


def auto_case_test(device_, poco):
    test_pool = multiprocessing.Pool(2)
    # 这里func改成需要测试的case方法名即可
    test_pool.apply_async(func=reopenTest(device_, poco, 1))
    test_pool.close()
    test_pool.join()


if __name__ == '__main__':
    device_ready = init_device(get_serial_number())
    auto_case_test(device_ready[0], device_ready[1])
