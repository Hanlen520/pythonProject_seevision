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
    3、判断升级成功与否
    new_version = [ro.fota.version]: [EM_TK1032_20210924_v1.1.0_20210924-1222]
    old_version = [ro.fota.version]: [EM_TK1032_20210924_v1.1.0_20210924-0524]
    判断当前是否在new version，升级从old to new
    
    压力测试需要UserDebug版本才能进行测试，User版本无法disable-verity
"""


def check_adb_online():
    device_on = False
    while not device_on:
        print("Check device online?")
        sleep(3)
        adb_connnect = len(str(subprocess.Popen("adb devices", stdout=subprocess.PIPE).communicate()[0]))
        if adb_connnect > 35:
            if get_current_page():
                print("Yes, device online……")
                sleep(5)
                return True


def root():
    if check_adb_online():
        sleep(3)
        print("Begin adb root……")
        root_step_1 = subprocess.Popen("adb root", shell=True,
                                       stdout=subprocess.PIPE).communicate()[0]
        sleep(3)
        print("Begin adb disable-verity……")
        root_step_2 = subprocess.Popen("adb disable-verity", shell=True,
                                       stdout=subprocess.PIPE).communicate()[0]
        sleep(3)
        print("Begin adb reboot……")
        root_step_3 = subprocess.Popen("adb reboot", shell=True,
                                       stdout=subprocess.PIPE).communicate()[0]
        sleep(3)
        if wait_for_device_reboot():
            print("Begin adb root……")
            root_step_4 = subprocess.Popen("adb root", shell=True,
                                           stdout=subprocess.PIPE).communicate()[0]
            sleep(3)
            print("Begin adb remount……")
            root_step_5 = subprocess.Popen("adb remount", shell=True,
                                           stdout=subprocess.PIPE).communicate()[0]


def get_current_page():
    current_page = subprocess.Popen("adb shell dumpsys window | grep mCurrentFocus", shell=True,
                                    stdout=subprocess.PIPE).communicate()[0]
    if "StatusBar" in str(current_page) or "launcher3" in str(current_page):
        return True


def wait_for_device_reboot():
    if check_adb_online():
        i = 0
        while i < 36000:
            sleep(3)
            i += 1
            print("Wait for device boot!")
            if get_current_page():
                print("Device online!")
            return True


def push_updateZip_to():
    if check_adb_online():
        print("Begin push:adb push update.zip /data/ota_package/")
        push_into_device = \
            subprocess.Popen("adb push update.zip /data/ota_package/", stdout=subprocess.PIPE).communicate()[
                0]


def update_to_new_version(old_version, new_version):
    if check_adb_online():
        print("Analysis update.zip package……")
        update_command_write = subprocess.Popen("python ota.py update.zip", stdout=subprocess.PIPE).communicate()[0]
        with open("update.txt", "w") as update_command_file:
            print("Get update code and write in update.txt……")
            update_command_file.write(update_command_write.decode())
        update_command = "update.txt"
        print("Execute update process……")
        update_command_execute = \
            subprocess.Popen("adb shell < {}".format(update_command), shell=True, stdout=subprocess.PIPE).communicate()[
                0]
        sleep(10)
        print("After update ,reboot deivce……")
        reboot_device = subprocess.Popen("adb reboot", shell=True, stdout=subprocess.PIPE).communicate()[
            0]
        if check_current_version(old_version, new_version):
            print("First version upgrade success ,Begin new version cycle flash test!")
        else:
            print("Please check, new version upgrade fail, cannot continue test,please check……")


def check_current_version(old_version, new_version):
    if wait_for_device_reboot():
        print("Check current version……")
        current_version = (
            subprocess.Popen("adb shell getprop ro.fota.version", shell=True, stdout=subprocess.PIPE).communicate()[
                0]).decode().strip()
        print("Current Version is {}".format(current_version))
        if current_version == new_version:
            print("New version update success!")
            return True
        elif current_version == old_version:
            print("New version update fail!")
            return False


if __name__ == "__main__":
    for i in range(5):
        old_version = "EM_TK1032_20210924_v1.1.0_20210924-1315"
        new_version = "EM_TK1032_20210924_v1.1.0_20210924-1315"
        print(
            "Start {} test and wait for device……\n We will update from\n: old - 【{}】 to new -  【{}】".format(str(i + 1),
                                                                                                            old_version,
                                                                                                            new_version))
        # device = connect_device("android:///{}?cap_method=javacap&touch_method=adb".format("c59a06bf"))
        # poco = AndroidUiautomationPoco(device, use_airtest_input=True, screenshot_each_action=False)
        root()
        push_updateZip_to()
        update_to_new_version(old_version, new_version)
        print("End {} test……".format(str(i + 1)))
        sleep(5)
