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


def init_device(device_serial):
    device_ = connect_device("Android:///{}".format(device_serial[0]))
    device_.wake()
    device_.unlock()
    poco = AndroidUiautomationPoco(device=device_, use_airtest_input=False, screenshot_each_action=False)
    return device_, poco


def reopenTest(device_, poco, i):
    # device_ready = connectDevice(get_serial_number())
    # global device, poco
    # device = device_ready[0]
    # poco = device_ready[1]
    if not os.path.exists("./snapshot/"):
        os.mkdir("./snapshot/")
    device_.home()
    position1 = poco(text="口算检查").wait(3).get_position()
    poco(text="口算检查").wait(3).click()
    position2 = poco("com.youdao.hardware.panda.countinginspect:id/ivBack").wait(3).get_position()
    poco("com.youdao.hardware.panda.countinginspect:id/ivBack").wait(3).click()
    try:
        for i in range(10000):
            poco.click(position1)
            device_.snapshot("./snapshot/Current{}_open.jpeg".format(i))
            poco.click(position2)
    except Exception:
        pass
    finally:
        logProcess()


def logProcess():
    if not os.path.exists("./log/"):
        os.mkdir("./log/")
    subprocess.Popen("adb logcat -b all>./log/{}_logcat.log".format(cur_time), shell=True).communicate()[0]


def auto_case_test(device_, poco):
    test_pool = multiprocessing.Pool(2)
    # test_pool.apply_async(func=logProcess)
    # 这里func改成需要测试的case方法名即可
    # test_pool.apply_async(func=camera_operate(device_, poco, 1000))
    test_pool.apply_async(func=reopenTest(device_, poco, 1))
    # test_pool.apply_async(func=device_reboot(device_, poco, 1000))
    test_pool.close()
    test_pool.join()


if __name__ == '__main__':
    device_ready = init_device(get_serial_number())
    auto_case_test(device_ready[0], device_ready[1])
