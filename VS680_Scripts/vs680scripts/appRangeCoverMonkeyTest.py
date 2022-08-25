# coding = utf8
import os
import re
import subprocess

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:appRangeCoverMonkeyTest.py
    @Author:十二点前要睡觉
    @Date:2022/8/24 14:51
"""

"""
    adb push ./Fastbot_Android-main/Fastbot_Android-main/fastbot-thirdpart.jar ./Fastbot_Android-main/Fastbot_Android-main/framework.jar ./Fastbot_Android-main/Fastbot_Android-main/monkeyq.jar /sdcard
    adb push ./Fastbot_Android-main/Fastbot_Android-main/libs/arm64-v8a ./Fastbot_Android-main/Fastbot_Android-main/libs/armeabi-v7a ./Fastbot_Android-main/Fastbot_Android-main/libs/x86 ./Fastbot_Android-main/Fastbot_Android-main/libs/x86_64 /data/local/tmp/
    adb push ./abl.strings  /sdcard
    adb shell CLASSPATH=/sdcard/monkeyq.jar:/sdcard/framework.jar:/sdcard/fastbot-thirdpart.jar exec app_process /system/bin com.android.commands.monkey.Monkey  --agent reuseq  --act-blacklist-file /sdcard/abl.strings --bugreport --output-directory /sdcard/monkeyCrashLog/crash --ignore-crashes --ignore-timeouts --kill-process-after-error --ignore-security-exceptions  --running-minutes 1 --throttle 500 -v -v
"""


def fastbot_monkey_cover_test(package):
    print("当前测试的APP为【{}】".format(package))
    os.system(
        "adb push ./Fastbot_Android-main/Fastbot_Android-main/fastbot-thirdpart.jar ./Fastbot_Android-main/Fastbot_Android-main/framework.jar ./Fastbot_Android-main/Fastbot_Android-main/monkeyq.jar /sdcard")
    os.system(
        "adb push ./Fastbot_Android-main/Fastbot_Android-main/libs/arm64-v8a ./Fastbot_Android-main/Fastbot_Android-main/libs/armeabi-v7a ./Fastbot_Android-main/Fastbot_Android-main/libs/x86 ./Fastbot_Android-main/Fastbot_Android-main/libs/x86_64 /data/local/tmp/")
    os.system("adb push ./abl.strings  /sdcard")
    os.system(
        "adb shell CLASSPATH=/sdcard/monkeyq.jar:/sdcard/framework.jar:/sdcard/fastbot-thirdpart.jar exec app_process /system/bin com.android.commands.monkey.Monkey -p {}  --agent reuseq  --act-blacklist-file /sdcard/abl.strings --bugreport --output-directory /sdcard/monkeyCrashLog/crash --ignore-crashes --ignore-timeouts --kill-process-after-error --ignore-security-exceptions  --running-minutes 30 --throttle 500 -v -v".format(
            package))


def controlAppRange():
    wholeApp = subprocess.Popen("adb shell pm list packages", shell=True, stdout=subprocess.PIPE).communicate()[0]
    app_list = re.findall("package:(.*)", str(wholeApp).replace("\\r\\n", "\n"))
    launchableApp_list = []
    for package in app_list:
        haveLauncher = str(
            subprocess.Popen("adb shell dumpsys package {} | grep category.LAUNCHER".format(package), shell=True,
                             stdout=subprocess.PIPE).communicate()[0]).replace(" ", "").replace("b''", "")
        if haveLauncher:
            print("APP 【{}】 have launcher page to view!".format(package))
            # print(haveLauncher)
            launchableApp_list.append(package)
    print("筛选前，当前系统版本存在APP：{}个".format(len(app_list)))
    print("筛选后，当前系统版本存在APP：{}个".format(len(launchableApp_list)))
    print("当前即将进行测试的APP列表为：\n{}".format(launchableApp_list))
    return launchableApp_list


if __name__ == '__main__':
    print("现在开始对系统各模块APP进行遍历压测……，通过FastBot_Android进行完全遍历，每个APP遍历60分钟……请耐心等待其跑完……")
    for package in controlAppRange():
        fastbot_monkey_cover_test(package)
