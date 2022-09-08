# coding = utf8
import multiprocessing
import re

import pandas as pd
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.exceptions import PocoNoSuchNodeException

cur_time = time.strftime("%Y%m%d_%H%M%S")

os.path.abspath("..")
"""
    此脚本用于Android项目 - VS680重启压力测试
    原理：
    通过UI自动化控制设备重启，并获取重启后的状态，反复压测
"""
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


global i
result_list = []

# Case 1:使用自动化脚本测试reboot 1000次
"""
    测试步骤：手机重启1000次
    测试期望结果：可以重启成功，不会死机
    case自动化拆解：
    一、device_reboot:
        1、使用shell命令配合adb命令将手机进行重启
        2、等待重启完成，通过判断当前界面是否在launcher界面来进行确认是否重启成功
        循环1000次重启
        3、每次重启的开始和结束时间+次数写入excel文档记录
    二、result_calculate:
        4、测试完成后查看机器状态+excel表格结果情况，是否有重启失败的时间点
    四、同步Log抓取:
        log_process:测试启动时，启动logcat同步抓取，防止机器log丢失
"""

global current_time
global i


def device_reboot(device_, poco, times):
    # try:
    device_serialno = device_.serialno
    sleep(1)
    except_stop = False
    for i in range(times):
        try:
            """
                实现区域：begin
            """
            if not os.path.exists("./screenshot"):
                os.mkdir("./screenshot")
                print("Create folder success!")
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
                    if "com.seevision.tv.launcher" in device_ready_now.shell("dumpsys window | grep mCurrentFocus"):
                        device_reboot_result = True
                        device_end_reboot_time = time.strftime("%Y%m%d_%H%M%S")
                        except_stop = False
                        current_time = time.strftime("%Y%m%d_%H%M%S")
                        device_ready_now.snapshot("./screenshot/第{}次测试截图{}.jpg".format(str(i), current_time))
                        break
                    elif count_time >= 600:
                        device_reboot_result = False
                        except_stop = True
                        current_time = time.strftime("%Y%m%d_%H%M%S")
                        device_ready_now.snapshot("./screenshot/第{}次测试截图{}.jpg".format(str(i), current_time))
                        break
                except Exception as ex:
                    print("等待设备重启时间：{}s:_______:exception:{}".format(count_time, str(ex)))
                    continue
                except KeyboardInterrupt:
                    except_stop = True
                    break
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
            current_time = time.strftime("%Y%m%d_%H%M%S")
            standard_test_DataGenerate(result_list)
            if except_stop:
                break
        except PocoNoSuchNodeException as ex:
            result_list.append(
                [i + 1, time.strftime("%Y%m%d_%H%M%S"), "第{}次重启测试未找到元素，重试该次".format(i + 1)])
            print(time.strftime("%Y%m%d_%H%M%S") + "第{}次重启测试未找到元素，重试该次".format(i + 1))
            times += 1
            print(str(ex))
            device_.wake()
            device_.unlock()
            print("异常中断，result保存！")
            continue
        i += 1


"""
    结果生成区域：
    使用excel脚本统一记录：测试次数、测试时间、结果
"""


def standard_test_DataGenerate(result_list=[]):
    alist = []
    blist = []
    clist = []
    for result in result_list:
        alist.append(result[0])
        blist.append(result[1])
        clist.append(result[2])
    df = pd.DataFrame({"测试次数": alist, "测试时间": blist, "结果": clist})
    df.to_excel("./重启压力测试result.xlsx", engine="openpyxl")


"""
    测试自动化Case执行区域：
    1、多进程控制：logcat和测试同步开启
"""


def auto_case_test(device_, poco):
    test_pool = multiprocessing.Pool(1)
    # 这里func改成需要测试的case方法名即可
    test_pool.apply_async(func=device_reboot(device_, poco, 1000))
    test_pool.close()
    test_pool.join()


if __name__ == '__main__':
    device_ready = init_device(get_serial_number())
    auto_case_test(device_ready[0], device_ready[1])
