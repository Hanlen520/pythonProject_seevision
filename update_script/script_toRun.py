# encoding = utf8

import os
import subprocess
from time import sleep

os.path.abspath(".")

"""
    1、先Root
    将需要测试的update.zip、ota.py包放到脚本目录下
    先用升级到新版本，然后再push进去update.zip包，再执行如下的循环刷入当前版本的测试即可
    2、再Root（每次刷入版本后都需要Root）
    手机自带的/system/bin/update_engine_client 驱动，adb shell /system/bin/update_engine_client  --reset_status
"""


def root():
    print("Begin adb root……")
    root_step_1 = subprocess.Popen("adb root", shell=True,
                                   stdout=subprocess.PIPE).communicate()[0]
    print("Begin adb disable-verity……")
    root_step_2 = subprocess.Popen("adb disable-verity", shell=True,
                                   stdout=subprocess.PIPE).communicate()[0]
    print("Begin adb reboot……")
    root_step_3 = subprocess.Popen("adb reboot", shell=True,
                                   stdout=subprocess.PIPE).communicate()[0]
    if wait_for_device_reboot():
        print("Begin adb root……")
        root_step_4 = subprocess.Popen("adb root", shell=True,
                                       stdout=subprocess.PIPE).communicate()[0]
        print("Begin adb remount……")
        root_step_5 = subprocess.Popen("adb remount", shell=True,
                                       stdout=subprocess.PIPE).communicate()[0]


def wait_for_device_reboot():
    i = 0
    while i < 36000:
        sleep(3)
        i += 1
        print("Wait for device boot!")
        if "StatusBar" in str(subprocess.Popen("adb shell dumpsys window | grep mCurrentFocus", shell=True,
                                               stdout=subprocess.PIPE).communicate()[0]):
            print("Device online!")
            return True


def update_to_new_version():
    update_command_write = subprocess.Popen("python ota.py update.zip", stdout=subprocess.PIPE).communicate()[0]
    with open("update.txt", "w") as update_command_file:
        update_command_file.write(update_command_write.decode())
    update_command = "update.txt"
    update_command_execute = \
        subprocess.Popen("adb shell < {}".format(update_command), shell=True, stdout=subprocess.PIPE).communicate()[0]


if __name__ == "__main__":
    print("Start test……")
    # device = connect_device("android:///{}?cap_method=javacap&touch_method=adb".format("c59a06bf"))
    # poco = AndroidUiautomationPoco(device, use_airtest_input=True, screenshot_each_action=False)
    # root()
    update_to_new_version()
    print("End test……")
