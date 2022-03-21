# coding = utf8
import csv
import multiprocessing
import re
import subprocess

from PyQt5.QtCore import QTimer
from airtest.core.api import *
from airtest.core.error import AdbError
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.exceptions import PocoNoSuchNodeException

cur_time = time.strftime("%Y%m%d_%H%M%S")

os.path.abspath("..")

"""
    设备初始化区域：
    1、获取设备序列号
    2、初始化设备，返回device（设备控制器）和poco（元素查找器）
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


def device_reboot(device_, poco, times):
    device_serialno = device_.serialno
    sleep(1)
    result_list = []
    for i in range(times):
        try:
            """
                实现区域：begin
            """
            print("第{}次重启测试".format(i + 1))
            device_.shell("reboot")
            device_start_reboot_time = time.strftime("%Y%m%d_%H%M%S")
            device_end_reboot_time = 0
            device_reboot_result = False
            count_time = 0
            while True:
                sleep(1)
                count_time += 1
                try:
                    device_ready_now = connect_device("Android:///{}".format(device_serialno))
                    device_ready_now.wake()
                    device_ready_now.unlock()
                    if "com.example.sampleleanbacklauncher" in device_ready_now.shell(
                            "dumpsys window | grep mCurrentFocus"):
                        device_reboot_result = True
                        device_end_reboot_time = time.strftime("%Y%m%d_%H%M%S")
                        break
                    elif count_time >= 600:
                        device_reboot_result = False
                        break
                except Exception as ex:
                    print("等待设备重启时间：{}s:_______:exception:{}".format(count_time, str(ex)))
                    continue
            """
                实现区域：end
            """
            result_list.append(
                [i + 1,
                 "第{}次重启测试开始时间:{}".format(i + 1, device_start_reboot_time) + " " +
                 "第{}次重启测试结束时间:{}".format(i + 1,
                                          device_end_reboot_time)
                    , "此次升级结果为{}".format(device_reboot_result)])
            print("第{}次重启测试_时间{}——————结果{}".format(i + 1, device_start_reboot_time, device_reboot_result))
        except PocoNoSuchNodeException as ex:
            result_list.append(
                [i + 1, time.strftime("%Y%m%d_%H%M%S"), "第{}次重启测试未找到元素，重试该次".format(i + 1)])
            print(time.strftime("%Y%m%d_%H%M%S") + "第{}次重启测试未找到元素，重试该次".format(i + 1))
            times += 1
            print(str(ex))
            device_.wake()
            device_.unlock()
            continue
        i += 1
    current_time = time.strftime("%Y%m%d_%H%M%S")
    result_calculate(result_list, "result_此次重启测试运行{}次结果_{}.csv".format(str(i), current_time))

    # 重启测试完成后进行Monkey测试
    test_poolMonkey = multiprocessing.Pool(1)
    test_poolMonkey.apply_async(func=monkeyTest)
    test_poolMonkey.close()
    test_poolMonkey.join()


"""
    结果生成区域：
    使用csv脚本统一记录：测试次数、测试时间、结果
"""


def result_calculate(data=[["1", "2", "3"], "1", "2", "3"], form_name="result.csv"):
    with open("./{}".format(form_name), "w", encoding="utf-8-sig") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["测试次数", "测试时间", "结果"])
        # 取出再写入
        for item in data:
            csv_writer.writerow(item)


"""
    Log获取区域：
        根据case名传入name，开启各自测试项的logcat
"""


def log_process():
    # subprocess.Popen("adb logcat -b all>./{}_camera_auto_test_stress1000.log".format(cur_time), shell=True).communicate()[0]
    # subprocess.Popen("adb logcat -b all>./{}_camera_auto_test_noGap2000.log".format(cur_time),
    #                  shell=True).communicate()[0]
    subprocess.Popen("adb logcat -b all>./{}_reboot_monkeyTestLogcat.log".format(cur_time),
                     shell=True).communicate()[0]


def monkeyTest():
    sleep(3)
    subprocess.Popen("adb shell monkey --ignore-crashes --ignore-timeouts --throttle 300 10000000",
                     shell=True).communicate()


"""
    测试自动化Case执行区域：
    1、多进程控制：logcat和测试同步开启
"""


def auto_case_test(device_, poco):
    test_pool = multiprocessing.Pool(2)
    test_pool.apply_async(func=log_process)
    # 这里func改成需要测试的case方法名即可
    # test_pool.apply_async(func=camera_operate(device_, poco, 1000))
    # test_pool.apply_async(func=camera_operate_capture_noGap(device_, poco, 2000))
    test_pool.apply_async(func=device_reboot(device_, poco, 2000))
    test_pool.close()
    test_pool.join()


if __name__ == '__main__':
    try:
        device_ready = init_device(get_serial_number())
        auto_case_test(device_ready[0], device_ready[1])
    except AdbError:
        pass
