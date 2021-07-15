# coding = utf8
import csv
import multiprocessing
import os
import re
import subprocess

from airtest.core.api import *
from airtest.core.error import DeviceConnectionError
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
    device_.shell("settings put system screen_brightness_mode 0")
    device_.shell("settings put system screen_brightness 999999")
    device_.shell("settings put system screen_off_timeout 1")
    poco = AndroidUiautomationPoco(device=device_, use_airtest_input=False, screenshot_each_action=False)
    return device_, poco


"""
    Case区域：
"""
global i
result_list = []

# Case1：拍摄1000张图片
"""
    测试步骤：启动相机，点击拍照按钮进行拍照1000次
    测试期望结果：拍照成功，相机进入相册的入口更新照片及时，照片成功保存
    case自动化拆解：
    一、camera_operate:
        1、启动相机
        2、点击拍照按钮
        3、点击图库->重命名（根据当前时间+次数）
        4、返回相机
        5、每次拍照的时间+次数写入excel文档记录
    二、继续step2->5循环直到拍照1000次完成
    三、result_calculate:
        6、最后1000次测试完成后->统计excel文档中是否有次数缺失进而判断1000次测试PASS或FAIL
            比对：测试完成后统计是否有1000张照片，如果没有通过比对脚本的时间和实际相片的拍摄时间判断哪一次拍照出现FAIL
    四、同步Log抓取:
        log_process:测试启动时，启动logcat同步抓取，防止机器log丢失
"""


def camera_operate(device_, poco, times):
    try:
        for i in range(times):
            try:
                sleep(1)
                device_.start_app("com.android.camera2")
                sleep(2)
                poco("com.android.camera2:id/front_back_switcher").wait().parent().children()[3].click()
                sleep(3)
                poco("com.android.camera2:id/preview_thumb").wait().click()
                sleep(3)
                poco("com.android.gallery:id/action_bar").wait().children()[1].click()
                sleep(2)
                poco(text="重命名").wait().click()
                sleep(2)
                current_time = time.strftime("%Y%m%d_%H%M%S")
                poco("com.android.gallery:id/InputText").wait().set_text(
                    "第{}次_{}".format(i + 1, current_time))
                result_list.append(
                    [i + 1, current_time,
                     "第{}次_{}.JPG".format(i + 1, current_time)])
                print("第{}次测试_{}.JPG".format(i + 1, current_time))
                sleep(2)
                poco(text="确定").wait().click()
                sleep(1)
            except PocoNoSuchNodeException as ex:
                result_list.append(
                    [i + 1, time.strftime("%Y%m%d_%H%M%S"), "第{}次未找到元素，重试该次".format(i + 1)])
                print(time.strftime("%Y%m%d_%H%M%S") + "第{}次未找到元素，重试该次".format(i + 1))
                device_.stop_app("com.android.camera2")
                times += 1

                print(str(ex))

                device_.wake()
                device_.unlock()
                continue
            i += 1
    except DeviceConnectionError as ex:
        print(str(ex) + "测试中断，当前测试次数：{}".format(times))
    finally:
        current_time = time.strftime("%Y%m%d_%H%M%S")
        if i < times:
            a = times - i
            print("count test number less than {} so continue!".format(times))
            result_calculate(result_list, "result_此次运行{}次结果_{}.csv".format(str(i), current_time))
            camera_operate(device_, poco, a)
        else:
            result_calculate(result_list, "result_此次运行{}次结果_{}.csv".format(str(i), current_time))


# Case2：不间断拍摄2000张图片,间隔1s
"""
    测试步骤：启动相机，点击拍照按钮进行拍照2000次
    测试期望结果：可以正常拍照，图片显示正常，相机\相册不会卡死退出
    case自动化拆解：
    一、camera_operate_capture_noGap:
        1、启动相机
        2、点击拍照按钮
        循环2000次拍照按钮点击
        3、每次拍照的时间+次数写入excel文档记录
    二、result_calculate:
        4、测试完成后到相册查看2000张图片与excel表格对应时间一致且图片是否可以正常显示
    四、同步Log抓取:
        log_process:测试启动时，启动logcat同步抓取，防止机器log丢失
"""


def camera_operate_capture_noGap(device_, poco, times):
    try:
        sleep(1)
        device_.start_app("com.android.camera2")
        sleep(1)
        for i in range(times):
            try:
                poco("com.android.camera2:id/front_back_switcher").wait().parent().children()[3].click()
                current_time = time.strftime("%Y%m%d_%H%M%S")
                sleep(1)
                result_list.append(
                    [i + 1, current_time,
                     "第{}次不间断拍照测试_{}".format(i + 1, current_time)])
                print("第{}次不间断拍照测试_{}.JPG".format(i + 1, current_time))
            except PocoNoSuchNodeException as ex:
                result_list.append(
                    [i + 1, time.strftime("%Y%m%d_%H%M%S"), "第{}次不间断拍照测试未找到元素，重试该次".format(i + 1)])
                print(time.strftime("%Y%m%d_%H%M%S") + "第{}次不间断拍照测试未找到元素，重试该次".format(i + 1))
                device_.stop_app("com.android.camera2")
                times += 1
                print(str(ex))
                device_.wake()
                device_.unlock()
                continue
            i += 1
    except DeviceConnectionError as ex:
        print(str(ex) + "测试中断，当前测试次数：{}".format(times))
    finally:
        current_time = time.strftime("%Y%m%d_%H%M%S")
        if i < times:
            a = times - i
            print("count test number less than {} so continue!".format(times))
            result_calculate(result_list, "result_此次不间断拍照测试运行{}次结果_{}.csv".format(str(i), current_time))
            camera_operate_capture_noGap(device_, poco, a)
        else:
            result_calculate(result_list, "result_此次不间断拍照测试运行{}次结果_{}.csv".format(str(i), current_time))


# Case 3:使用自动化脚本测试reboot 1000次
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


def device_reboot(device_, poco, times):
    # try:
    device_serialno = device_.serialno
    sleep(1)
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
                    if "com.android.launcher3" in device_ready_now.shell("dumpsys window | grep mCurrentFocus"):
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


# except DeviceConnectionError as ex:
#     print(str(ex) + "测试中断，当前测试次数：{}".format(times))
# finally:
#     current_time = time.strftime("%Y%m%d_%H%M%S")
#     if i < times:
#         a = times - i
#         print("count test number less than {} so continue!".format(times))
#         result_calculate(result_list, "result_此次重启测试运行{}次结果_{}.csv".format(str(i), current_time))
#         device_reboot(device_, poco, a)
#     else:
#         result_calculate(result_list, "result_此次重启测试运行{}次结果_{}.csv".format(str(i), current_time))


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
    subprocess.Popen("adb logcat -b all>./{}_device_auto_test_reboot1000.log".format(cur_time),
                     shell=True).communicate()[0]


"""
    测试自动化Case执行区域：
    1、多进程控制：logcat和测试同步开启
"""


def auto_case_test(device_, poco):
    test_pool = multiprocessing.Pool(2)
    test_pool.apply_async(func=log_process)
    # 这里func改成需要测试的case方法名即可
    # test_pool.apply_async(func=camera_operate(device_, poco, 1000))
    test_pool.apply_async(func=camera_operate_capture_noGap(device_, poco, 2000))
    # test_pool.apply_async(func=device_reboot(device_, poco, 100))
    test_pool.close()
    test_pool.join()


if __name__ == '__main__':
    device_ready = init_device(get_serial_number())
    auto_case_test(device_ready[0], device_ready[1])
