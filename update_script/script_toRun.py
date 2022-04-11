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
        print("-------------------------------------------Check device online?")
        toTxt("-------------------------------------------Check device online?")
        sleep(5)
        adb_connnect = len(str(subprocess.Popen("adb devices", stdout=subprocess.PIPE).communicate()[0]))
        if adb_connnect > 35:
            if get_current_page():
                print("-------------------------------------------Yes, device online……")
                toTxt("-------------------------------------------Yes, device online……")
                sleep(5)
                return True


def root():
    if check_adb_online():
        sleep(3)
        print("-------------------------------------------Begin adb root……")
        toTxt("-------------------------------------------Begin adb root……")
        root_step_1 = subprocess.Popen("adb root", shell=True,
                                       stdout=subprocess.PIPE).communicate()[0]


def get_current_page():
    current_page = subprocess.Popen("adb shell dumpsys window | grep mCurrentFocus", shell=True,
                                    stdout=subprocess.PIPE).communicate()[0]
    if "StatusBar" in str(current_page) or "launcher3" in str(current_page) or "com.youdao.hardware.panda" in str(
            current_page):
        return True


def wait_for_device_reboot():
    if check_adb_online():
        i = 0
        while i < 36000:
            sleep(5)
            i += 1
            print("-------------------------------------------Wait for device boot!")
            toTxt("-------------------------------------------Wait for device boot!")
            if get_current_page():
                print("-------------------------------------------Device online!")
                toTxt("-------------------------------------------Device online!")
            return True


def push_updateZip_to(version_path):
    if check_adb_online():
        print("-------------------------------------------Begin push:adb push {}update.zip /data/ota_package/".format(
            version_path))
        toTxt("-------------------------------------------Begin push:adb push {}update.zip /data/ota_package/".format(
            version_path))
        push_into_device = \
            subprocess.Popen("adb push {}update.zip /data/ota_package/".format(version_path),
                             stdout=subprocess.PIPE).communicate()[
                0]


def check_current_version(old_version, new_version):
    if wait_for_device_reboot():
        print("-------------------------------------------Check current version……")
        toTxt("-------------------------------------------Check current version……")
        current_version = (
            subprocess.Popen("adb shell getprop ro.fota.version", shell=True, stdout=subprocess.PIPE).communicate()[
                0]).decode().strip()
        print("-------------------------------------------Current Version is {}".format(current_version))
        toTxt("-------------------------------------------Current Version is {}".format(current_version))
        if current_version == old_version:
            print("-------------------------------------------New version update success!")
            toTxt("-------------------------------------------New version update success!")
            return True
        else:
            print("-------------------------------------------New version update fail!")
            toTxt("-------------------------------------------New version update fail!")
            return False


# 开始循环升级测试 --reset_status
def begin_upgrade_test(old_version, new_version, version_path):
    if check_adb_online():
        if get_current_page():
            print("-------------------------------------------Analysis update.zip package……")
            toTxt("-------------------------------------------Analysis update.zip package……")
            update_command = "{}ota_command.txt".format(version_path)
            print("-------------------------------------------Execute upgrade cycle update process……")
            toTxt("-------------------------------------------Execute upgrade cycle update process……")
            update_command_execute = \
                subprocess.Popen("adb shell < {}".format(update_command), shell=True,
                                 stdout=subprocess.PIPE).communicate()[0]
            sleep(10)
            print("-------------------------------------------After update ,reboot device……")
            toTxt("-------------------------------------------After update ,reboot device……")
            reboot_device = subprocess.Popen("adb reboot", shell=True, stdout=subprocess.PIPE).communicate()[
                0]
            if check_current_version(old_version, new_version):
                print(
                    "【结果检查点：当前升级结果为：PASS】")
                toTxt("【结果检查点：当前升级结果为：PASS】")
            else:
                print(
                    "【结果检查点：当前升级结果为：FAIL】")
                toTxt("【结果检查点：当前升级结果为：FAIL】")


def toTxt(result):
    """
    结果写入函数：将每次的结果追加写入各自串口的结果文本中
    :param result:每次刷机后版本判断结果
    :return:None
    """
    try:
        with open("./【{}】Result.txt".format("RunningLog"), "a+") as f:
            f.write(result + "\n")
    except (AttributeError, TypeError) as ex:
        print("【Error need check, maybe not important】 : \r\n{}\r\n".format(str(ex)))
        f.write("【Error need check, maybe not important】 : \r\n{}\r\n".format(str(ex)))


if __name__ == "__main__":

    # 测试前，Pycharm设置log输出方式：Run->Edit Configurations……->Logs->Save console output to file:设置自己保存的输出的文件log信息，每次测试测完更新log文件即可

    # sys.stdout = Logger("running.log")
    """ test area: 方式1，通过reset status进行重复当前版本升降级"""

    old_version = "YDC015_0.0.2_20220407_20220407-1543"
    new_version = "YDC015_0.2.2_20220410_20220410-0055"
    oldVersionPath = "./20220407_144459/firmware/"
    # newVersionPath = "./20220409_234335/firmware/"
    newVersionPath = "./20220407_144459/firmware/"

    print(
        "Start test and wait for device……\n We will update from\n: old - 【{}】 to new -  【{}】".format(
            old_version,
            new_version))
    toTxt("Start test and wait for device……\n We will update from\n: old - 【{}】 to new -  【{}】".format(
        old_version,
        new_version))
    # 修改测试次数
    for i in range(3):
        test_number = str(i + 1)
        print("-------------------------------------------Begin {} times reset cycle version upgrade test……".format(
            test_number))
        toTxt("-------------------------------------------Begin {} times reset cycle version upgrade test……".format(
            test_number))
        root()
        # version_path = ""
        version_path = oldVersionPath
        # if check_current_version(old_version, new_version):
        #     # new version->old
        #     print("Downgrade version test begin")
        #     version_path = oldVersionPath
        # else:
        #     # old version->new
        #     print("Upgrade version test begin")
        #     version_path = newVersionPath
        push_updateZip_to(version_path)
        begin_upgrade_test(old_version, new_version, version_path)
        print("-------------------------------------------The {} times reset cycle version upgrade test done!".format(
            test_number))
        toTxt("-------------------------------------------The {} times reset cycle version upgrade test done!".format(
            test_number))
        reboot_device = subprocess.Popen("adb reboot", shell=True, stdout=subprocess.PIPE).communicate()[
            0]
    print("-------------------------------------------End test……")
    toTxt("-------------------------------------------End test……")
