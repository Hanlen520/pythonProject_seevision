# coding = utf8

import os
import re
import subprocess
import time
import xml.etree.cElementTree as et

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


if __name__ == '__main__':
    # # 获取所有有launcher界面的app以及对应的activity
    # launchableApp_list = controlAppRange()
    # for package in launchableApp_list:
    #     getLaunchableActivity(package)
    # if appAndActivity:
    #     print("待测APP对应的Activity分别是：{}".format(appAndActivity))
    """
        通过mCurrentFocus去判断启动时间结束，通过冻结ui tree，再进行position点击，对点击前后的时间差即为模拟应用启动的时间
        现在需要传入的就是待测应用的：应用名称app_text和应用启动界面activityName以及清除应用数据的packageName
    """
    # clearAppDataBuffer(packageName="com.tencent.mobileqq")
    # x_pos, y_pos = getAppCenteralPosition(app_text="QQ")
    # print(touchApp(x_pos, y_pos, activityName="com.tencent.mobileqq.activity.SplashActivity"))

    clearAppDataBuffer(packageName="com.tencent.wemeet.app")
    x_pos, y_pos = getAppCenteralPosition(app_text="腾讯会议")
    print(touchApp(x_pos, y_pos, activityName="com.tencent.wemeet.app.StartupActivity"))
