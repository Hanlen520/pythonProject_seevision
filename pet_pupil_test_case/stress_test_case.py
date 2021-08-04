# coding = utf8
import csv
import logging
import multiprocessing
import os
import subprocess
import sys

os.path.abspath(".")
__author__ = "CHENGUANGTAO"

from airtest.core.api import *

auto_setup(__file__)
cur_time = time.strftime("%Y%m%d_%H%M%S")
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

# 过滤airtest log只打印ERROR的Log
logger_airtest = logging.getLogger("airtest")
logger_airtest.setLevel(logging.ERROR)

"""
    考虑到adb连接问题，当前测试使用adb wifi模式连接，框架中有关adb调用，如device.stop_app()\device.start_app()均不能使用，需要使用其他方法兼容
"""


def init_Device(serialno="7c2440fd"):
    device = connect_device("android:///{}?cap_method=javacap&touch_method=adb".format(serialno))
    poco = AndroidUiautomationPoco(device, use_airtest_input=True, screenshot_each_action=False)
    return poco, device


def stress_test(device, poco, test_times=1000):
    cur_test_app = "com.tawuyun.storecenter"
    i = 1
    csv_result = []
    try:
        for i in range(i, test_times):
            # device.start_app(cur_test_app)
            sleep(3)
            poco(text="它物云门店").wait().click()
            sleep(1)
            poco(text=">>模拟采集").wait().click()
            sleep(1)
            poco(text="激活").wait().click()
            sleep(3)

            poco(text="开始采集").wait().click()
            sleep(10)
            if poco(text="OK").wait().exists():
                poco(text="OK").wait().click()
                sleep(3)
            if poco(text="OK").wait().exists():
                poco(text="OK").wait().click()
                sleep(3)
            sleep(5)
            test_result = exists(Template(
                r"tpl1626862299337.png",
                record_pos=(
                    -0.385, -0.989),
                resolution=(720, 1640)))
            print("Test times is：{} -- Check whether picture exists and result is {}".format(str(i), test_result))
            csv_result.append([i, cur_time, test_result])
            sleep(1)
            device.keyevent("BACK")
    except Exception as ex:
        print("Current test is happened error, please check and error code is :{}".format(str(ex)))
    finally:
        result_calculate(data=csv_result)
        sys.exit(0)


def stress_webcam_test(device, poco, test_times=1000):
    cur_test_app = "com.webcamhostapp.app"
    i = 1
    csv_result = []
    try:
        for i in range(i, test_times):
            sleep(3)
            poco(text="WebCamHostApp").click()
            sleep(3)
            if poco(text="OK").wait().exists():
                poco(text="OK").wait().click()
                sleep(3)
            if poco(text="OK").wait().exists():
                poco(text="OK").wait().click()
                sleep(3)
            sleep(5)
            test_result = exists(Template(
                r"tpl1626862299337.png",
                record_pos=(
                    -0.385, -0.989),
                resolution=(720, 1640)))
            print("Test times is：{} -- Check whether picture exists and result is {}".format(str(i), test_result))
            csv_result.append([i, cur_time, test_result])
            sleep(1)
            device.keyevent("BACK")

    except Exception as ex:
        print("Current test is happened error, please check and error code is :{}".format(str(ex)))
    finally:
        result_calculate(data=csv_result)
        sys.exit(0)


def log_process():
    subprocess.Popen("adb -s 192.168.50.109:5555 shell logcat -b all>./stress_test.log", shell=True).communicate()[0]


def result_calculate(data=[["1", "2", "3"], "1", "2", "3"], form_name="result.csv"):
    with open("./{}".format(form_name), "w", encoding="utf-8-sig") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["测试次数", "测试时间", "结果"])
        # 取出再写入
        for item in data:
            csv_writer.writerow(item)


if __name__ == '__main__':
    init_item = init_Device(serialno="192.168.50.109:5555")
    device = init_item[1]
    poco = init_item[0]

    test_pool = multiprocessing.Pool(2)
    test_pool.apply_async(func=stress_webcam_test(device, poco, 5))
    # test_pool.apply_async(func=log_process)
    test_pool.close()
    test_pool.join()
