# coding = utf8
import csv
import logging
import multiprocessing
import os
import random
import subprocess

from airtest.core.android.adb import ADB

os.path.abspath(".")

from airtest.core.api import *

auto_setup(__file__)
cur_time = time.strftime("%Y%m%d_%H%M%S")
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

# 过滤airtest log只打印ERROR的Log
logger_airtest = logging.getLogger("airtest")
logger_airtest.setLevel(logging.ERROR)

"""
    通过该函数，修改flashlight_seekbar为对应的同类型的拖动控件，可以实现随机点击进度条的效果
"""

TCL10SE_serialno_adb_wifi = "192.168.50.109:5555"

"""
    结果导出到csv表格中
"""


def result_calculate(data=[["1", "2", "3"], "1", "2", "3"], form_name="result_tap_seekbar.csv"):
    with open("./{}".format(form_name), "w", encoding="utf-8-sig") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["测试次数", "测试时间", "结果"])
        # 取出再写入
        for item in data:
            csv_writer.writerow(item)


"""
    logcat导出到本地
"""


def log_process(device):
    log = subprocess.call(
        "adb -s {} shell logcat -b all>./DEVICE[{}]seekbar_tap_stable_test_logcat.log".format(device, device),
        shell=True)


"""
    初始化设备并运行测试case，最后批量导出每台机器的logcat日志
"""


def initDevice_RunTest():
    devices = [tmp[0] for tmp in ADB().devices()]
    print(devices)
    test_pool = multiprocessing.Pool(len(devices))
    for device in devices:
        print(device)
        test_pool.apply_async(func=run_test(device))
        sleep(3)
    test_pool.close()
    test_pool.join()
    test_pool_log = multiprocessing.Pool(len(devices))
    for device in devices:
        test_pool_log.apply_async(func=log_process, args=(device,))
        sleep(3)
    test_pool_log.close()
    test_pool_log.join()


"""
    测试项：seekbar_tap_stable_test
"""


def seekbar_tap_stable_test(device_):
    csv_result = []
    device = ""
    apk_package = "com.webcamhostapp.app"
    try:
        device = connect_device("android:///{}?cap_method=javacap&touch_method=adb".format(device_))
        poco = AndroidUiautomationPoco(device, use_airtest_input=True, screenshot_each_action=False)
        if apk_package not in device.list_app():
            device.install_app("./apks/WebCamHostApp.apk")
            sleep(3)
        # device.start_app(package=apk_package)
        poco(text="WebCamHostApp").click()
        sleep(3)
        flashlight_seekbar = poco("com.webcamhostapp.app:id/seekbar_flashlight")
        print(flashlight_seekbar.attr("size"))
        print(flashlight_seekbar.attr("pos"))
        fwidth = round(flashlight_seekbar.attr("size")[0], 2)
        fheight = round(flashlight_seekbar.attr("size")[1], 2)
        flol_x = round(flashlight_seekbar.attr("pos")[0], 2)
        flol_y = round(flashlight_seekbar.attr("pos")[1], 2)
        flashlight_seekbar_point = [(flol_x, flol_y), (flol_x + fwidth, flol_y), (flol_x, flol_y + fheight),
                                    (flol_x + fwidth, flol_y + fheight)]
        print("flash light seekbar four point is 左上角：{}，右上角：{}，左下角：{}，右下角：{}".format(flashlight_seekbar_point[0],
                                                                                     flashlight_seekbar_point[1],
                                                                                     flashlight_seekbar_point[2],
                                                                                     flashlight_seekbar_point[3]))
        left_top_p = flashlight_seekbar_point[0]
        right_top_p = flashlight_seekbar_point[1]
        left_bottom_p = flashlight_seekbar_point[2]
        right_bottom_p = flashlight_seekbar_point[3]
        seekbar_middle_point_x = round(left_top_p[0] + fwidth / 2, 2)
        seekbar_middle_point_y = round(left_top_p[1] + fheight / 2, 2)
        print("Seekbar middle point is:{}, {}".format(seekbar_middle_point_x, seekbar_middle_point_y))
        seekbar_left_point_x = round(left_top_p[0], 2)
        seekbar_left_point_y = round(left_top_p[1] + fheight / 5, 2)
        seekbar_right_point_x = round(left_top_p[0] + fwidth, 2)
        seekbar_right_point_y = round(left_top_p[1] + fheight / 5, 2)

        print("Seekbar left to right range is {},{} to {},{}".format(seekbar_left_point_x, seekbar_left_point_y,
                                                                     seekbar_right_point_x, seekbar_right_point_y))
        screen_width = device.display_info["width"]
        screen_height = device.display_info["height"]
        for i in range(5000):
            print("This is {} times test!".format(i + 1))
            x = random.uniform(seekbar_left_point_x, seekbar_right_point_x) * (screen_width)
            y = random.uniform(seekbar_left_point_y, seekbar_right_point_y) * (screen_height)
            device.touch((x, y))
            print((x, y))
            sleep(3)
            csv_result.append([i + 1, cur_time, "Current tap location: ({},{})".format(x, y)])
    except Exception as ex:
        print("Current test is happened error, please check and error code is :{}".format(str(ex)))
    finally:
        result_calculate(data=csv_result, form_name="result_tap_seekbar.csv")
        device.keyevent("BACK")


"""
    执行测试项，多个即创建多个进程即可
"""


def run_test(device):
    test_pool = multiprocessing.Pool(1)
    test_pool.apply_async(func=seekbar_tap_stable_test, args=(device,))
    test_pool.close()
    test_pool.join()


if __name__ == '__main__':
    # 总入口
    # initDevice_RunTest()
    run_test("192.168.50.109:5555")
    # log_process("192.168.50.109:5555")