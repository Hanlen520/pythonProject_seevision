# coding = utf8
import logging
import multiprocessing
import re
import subprocess

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:calendar_test.py
    @Author:十二点前要睡觉
    @Date:2022/2/14 10:22
    @Description:
    创建日程 - 批量创建
    1、使用脚本批量创建日程，根据脚本运行情况创建大数量日程
    2、创建完成后重启设备->观察创建的日程情况
    3、滑动日程列表
"""
cur_time = time.strftime("%Y%m%d_%H%M%S")


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


def log_process():
    if not os.path.exists("./log/"):
        os.mkdir("./log/")
    log_process = subprocess.Popen("adb logcat -b all>./log/{}_createScheduleLog.log".format(cur_time),
                                   shell=True).communicate()[0]


def logger_config(log_path, logging_name):
    # 获取logger对象,取名
    logger = logging.getLogger(logging_name)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_path, encoding='UTF-8')
    # 生成并设置文件日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # 为logger对象添加句柄
    logger.addHandler(handler)

    return logger


def calendar_test_area(test_count=5):
    testDevice, poco = init_device(get_serial_number())
    calendar = Calendar_Test(testDevice, poco)
    for i in range(test_count):
        calendar.launchCalendar()
        calendar.createSchedule("测试批量创建日程{}".format(str(i + 1)))
    print("Create Schedule Finished!")


class Calendar_Test:

    def __init__(self, testDevice, poco):
        self.testDevice = testDevice
        self.poco = poco
        self.logger = logger_config(log_path="./log/{}_{}_{}.log".format(cur_time, "createScheduleTest", "mainLog"),
                                    logging_name="createScheduleTest")

    def launchCalendar(self):
        print("Launch calendar！")
        self.logger.info("Launch calendar！")
        self.testDevice.start_app("com.android.calendar")
        sleep(1)

    def createSchedule(self, title):
        print("Let's create schedule its title is [{}]".format(title))
        self.logger.info("Let's create schedule its title is [{}]".format(title))
        print("Search com.android.calendar:id/action_create_events ")
        self.logger.info("Search com.android.calendar:id/action_create_events ")
        self.poco("com.android.calendar:id/action_create_events").wait(3).click()
        print("Search com.android.calendar:id/title")
        self.logger.info("Search com.android.calendar:id/title")
        self.poco("com.android.calendar:id/title").wait(3).set_text(title)

        if self.poco("com.sohu.inputmethod.sogou:id/doggyHead").exists():
            self.testDevice.keyevent("KEYCODE_BACK")
        self.poco("com.android.calendar:id/reminders_row").wait(3).click()
        self.poco(text="不提醒").wait().click()

        print("Search com.android.calendar:id/edit_event_save")
        self.logger.info("Search com.android.calendar:id/edit_event_save")
        save_button = self.poco("com.android.calendar:id/edit_event_save").wait(3)
        save_button.invalidate()
        if save_button.attr("enabled"):
            save_button.click()
            create_status = True
        else:
            print("Current Schedule {} is not saved!".format(title))
            self.logger.info("Current Schedule {} is not saved!")
            create_status = False
        print("Saved status is [{}]".format(create_status))
        self.logger.info("Saved status is [{}]".format(create_status))
        return title, create_status


if __name__ == '__main__':
    test_count = 500
    test_pool = multiprocessing.Pool(2)
    test_pool.apply_async(func=log_process, )
    test_pool.apply_async(func=calendar_test_area, args=(test_count,))
    test_pool.close()
    test_pool.join()
