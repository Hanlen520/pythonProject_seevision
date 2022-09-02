# coding = utf8

import os
import re
import subprocess
import time
import xml.etree.cElementTree as et

from excel_tools import read_excel_for_page_element
from grantPermission import grant_permission

os.path.abspath(".")


def getMSTime():
    t = time.time()
    return int(round(t * 1000))


def touchApp(x_pos, y_pos, activityName="com.tencent.wemeet.app.StartupActivity"):
    time1 = getMSTime()
    print(time1)
    os.popen("adb shell input tap {} {}".format(x_pos, y_pos))
    return keepWaitingActivity(time1=time1, activityName=activityName)


def dumpXml():
    os.system(f'adb shell uiautomator dump --compressed /{"/sdcard/ui.xml"}')
    os.system(f'adb pull {"/sdcard/ui.xml"} {"./"}')
    source = et.parse("./ui.xml")
    return source.getroot()


def getAppCenteralPosition(app_text):
    root = dumpXml()
    for node in root.iter("node"):
        if node.attrib["text"] == app_text:
            bounds = node.attrib["bounds"]
            pattern = re.compile(r"\d+")
            coord = pattern.findall(bounds)
            x_pos = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
            y_pos = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
            return x_pos, y_pos


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


def getLaunchableActivity(packageName):
    backResponse = str(subprocess.Popen("adb shell monkey -p {} -vvv 1".format(packageName), shell=True,
                                        stdout=subprocess.PIPE).communicate()[0]).replace(" ", "").replace("b''", "")
    launchActivity = re.findall("component=(.*);end", backResponse)[0]
    appAndActivity[packageName] = launchActivity
    time.sleep(0.3)
    killApp(packageName)


def killApp(package):
    command = "adb shell am force-stop {}".format(package)
    str(subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()[0])


def clearAppDataBuffer(packageName="com.tencent.wemeet.app"):
    os.system("adb shell pm clear {}".format(packageName))
    print("APP {} 数据清除完成".format(packageName))


def TouchAppTest(packageName, app_text, activityName):
    # clearAppDataBuffer(packageName=packageName)
    x_pos, y_pos = getAppCenteralPosition(app_text=app_text)
    test_time = touchApp(x_pos, y_pos, activityName=activityName)
    print("当前测试的启动时间：【{}】".format(test_time))
    return test_time


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
    test_times = 1
    test_result = {}
    # applist_range = controlAppRange()
    # for app in applist_range:
    #     clearAppDataBuffer(app)
    # grant_permission(applist_range)
    test_data = read_excel_for_page_element(form="./Touch启动时间测试用例.xlsx", sheet_name="Touch启动时间测试")
    for app_info in test_data:
        app_text = app_info[0]
        packageName = app_info[1]
        activityName = app_info[2]
        # 特殊情况1，当是switchhdmi的时候，需要将焦点放到最底部才会显示应用名称
        test_timess = []
        for i in range(test_times):
            if app_text == "switchhdmi":
                specialToHomeOperate()
            test_time = TouchAppTest(packageName, app_text, activityName)
            test_timess.append(test_time)
            time.sleep(1)
            if app_text == "USB无线投屏":
                os.popen("adb shell input keyevent 4")
                time.sleep(1)
                killApp("com.bozee.usbdisplay")
            else:
                killApp(packageName)
            # 特殊情况2，当是screencasting guide的时候，需要返回键回到Home界面
            if packageName == "com.seevision.screencastingassistant":
                os.popen("adb shell input keyevent 4")
        test_result[app_text] = test_timess
    print("测试结束，当前测试次数，每个APP测试【{}】次，总测试结果为：\n{}".format(test_times, test_result))
