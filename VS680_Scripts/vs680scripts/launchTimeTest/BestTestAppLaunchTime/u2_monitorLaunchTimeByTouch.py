# coding = utf8

import os
import re
import subprocess
import time
import xml.etree.cElementTree as et

import numpy as np
import uiautomator2 as u2

from excel_tools import read_excel_for_page_element, write_excel_with_specific_data
from grantPermission import grant_permission

os.path.abspath(".")

""" 
    该版本使用uiautomator2去实现点击功能看看效果如何
"""


def getMSTime():
    t = time.time()
    return int(round(t * 1000))


def touchApp(x_pos, y_pos, activityName="com.tencent.wemeet.app.StartupActivity"):
    time1 = getMSTime()
    print(time1)
    os.popen("adb shell input tap {} {}".format(x_pos, y_pos))
    return keepWaitingActivity(time1=time1, activityName=activityName)


def keepWaitingActivity(activityName="com.tencent.wemeet.sdk.meeting.premeeting.home.GuestGuideActivity", time1=0):
    while True:
        returnLine = str(
            subprocess.Popen('adb shell "dumpsys window | grep mCurrentFocus"', shell=True,
                             stdout=subprocess.PIPE).communicate()[0]).replace("b'", "").replace("\\n'", "")
        print(returnLine)
        # 特殊情况3：微信多次kill会触发安全模式，需要兼容下再Kill掉
        if "com.tencent.mm.recovery.ui.RecoveryUI" in returnLine:
            killApp("com.tencent.mm")
            return 0
        if activityName in returnLine:
            print("APP启动完成")
            time2 = getMSTime()
            print("time1 = {} and time2 = {}".format(time1, time2))
            return time2 - time1


def controlAppRange():
    wholeApp = subprocess.Popen("adb shell pm list packages", shell=True, stdout=subprocess.PIPE).communicate()[0]
    app_list = re.findall("package:(.*)", str(wholeApp).replace("\\r\\n", "\n"))
    launchableApp_list = []
    for package in app_list:
        haveLauncher = str(
            subprocess.Popen('adb shell "dumpsys package {} | grep category.LAUNCHER"'.format(package), shell=True,
                             stdout=subprocess.PIPE).communicate()[0]).replace(" ", "").replace("b''", "")
        if haveLauncher:
            print("APP 【{}】 have launcher page to view!".format(package))
            launchableApp_list.append(package)
    return launchableApp_list


appAndActivity = {}


def killApp(package):
    command = "adb shell am force-stop {}".format(package)
    str(subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()[0])


def clearAppDataBuffer(packageName="com.tencent.wemeet.app"):
    os.system("adb shell pm clear {}".format(packageName))
    print("APP {} 数据清除完成".format(packageName))


def TouchAppTest(device, packageName, app_text, activityName):
    print(app_text)
    time1 = 0
    if device().scroll.to(text=app_text):
        app = device(text=app_text)
        app.click()
        time1 = getMSTime()
        print(time1)
    else:
        print("未找到app：【{}】".format(app_text))
        return "当前系统未安装此app：【{}】，请检查！".format(app_text)
    launch_time = keepWaitingActivity(time1=time1, activityName=activityName)
    print("此次启动时间为：【{}】".format(launch_time))
    return launch_time


def specialToHomeOperate():
    os.system("adb shell input keyevent 20")
    time.sleep(1)
    os.system("adb shell input keyevent 20")
    time.sleep(1)
    os.system("adb shell input keyevent 20")


if __name__ == '__main__':
    """
        目前需要保证待测的应用程序需要有app的text显示在桌面上，是依靠text进行点击的
        通过mCurrentFocus去判断启动时间结束，通过冻结ui tree，再进行position点击，对点击前后的时间差即为模拟应用启动的时间
        现在需要传入的就是待测应用的：应用名称app_text和应用启动界面activityName以及清除应用数据的packageName
        测试前，会先将所有APP都进行授权，保证第一个Activity是应用程序的
        USB无线投屏应用需要手动先授权，点击一次立即激活即可
    """
    test_times = 10
    test_result = {}
    applist_range = controlAppRange()
    for app in applist_range:
        clearAppDataBuffer(app)
    grant_permission(applist_range)
    test_data = read_excel_for_page_element(form="./Touch启动时间测试用例.xlsx", sheet_name="Touch启动时间测试")
    for app_info in test_data:
        app_text = app_info[0]
        packageName = app_info[1]
        activityName = app_info[2]
        test_timess = []
        for i in range(test_times):
            device = u2.connect()
            # 特殊情况1，当是switchhdmi的时候，需要将焦点放到最底部才会显示应用名称
            if app_text == "switchhdmi":
                specialToHomeOperate()

            # packageName = "com.seevision.screencastingassistant"
            # activityName = "com.seevision.screencastingassistant.ScreencastingMainActivity"
            # app_text = "Screencasting Guide"

            test_time = TouchAppTest(device, packageName, app_text, activityName)
            test_timess.append(test_time)
            if app_text == "USB无线投屏":
                os.system("adb shell input keyevent 4")
                time.sleep(1)
                killApp("com.bozee.usbdisplay")
            """
                兼容VS680桌面设计，每次测完kill launcher再点击，就不会出现点击失败的问题了
            """
            killApp(packageName)
            # 特殊情况2，当是screencasting guide的时候，需要返回键回到Home界面
            if packageName == "com.seevision.screencastingassistant":
                os.system("adb shell input keyevent 4")
            killApp("com.seevision.tv.launcher")
            time.sleep(1)
            if type(test_time) == type(""):
                break
        """
            增加容错，如果没有app，则结果打上记号跳过该app
        """
        test_temp = ""
        test_result[app_text] = test_timess
        if type(test_timess[0]) == type(""):
            if test_result[app_text]:
                average = "Skip"
                test_temp = [test_times, str(test_timess) + "_" + str(average)]
        else:
            average = round(float(np.mean(test_timess)), 3)
            test_temp = [test_times, str(test_timess) + "_" + str(average)]
        write_excel_with_specific_data(app_text, test_temp, form="./Touch启动时间测试用例.xlsx",
                                       sheet_name="Touch启动时间测试")
    print("测试结束，当前测试次数，每个APP测试【{}】次，总测试结果为：\n{}".format(test_times, test_result))
