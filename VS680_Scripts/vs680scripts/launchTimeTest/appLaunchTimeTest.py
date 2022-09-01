# coding = utf8
import os
import re
import subprocess
from time import sleep

import pandas as pd

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:appLaunchTimeTest.py
    @Author:十二点前要睡觉
    @Date:2022/8/30 9:58
"""


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
            # print(haveLauncher)
            launchableApp_list.append(package)
    # print("筛选前，当前系统版本存在APP：{}个".format(len(app_list)))
    # print("筛选后，当前系统版本存在APP：{}个".format(len(launchableApp_list)))
    # print("当前即将进行测试的APP列表为：\n{}".format(launchableApp_list))
    return launchableApp_list


appAndActivity = {}


def getLaunchableActivity(packageName):
    backResponse = str(subprocess.Popen("adb shell monkey -p {} -vvv 1".format(packageName), shell=True,
                                        stdout=subprocess.PIPE).communicate()[0]).replace(" ", "").replace("b''", "")
    # print(backResponse)
    launchActivity = re.findall("component=(.*);end", backResponse)[0]
    appAndActivity[packageName] = launchActivity
    sleep(0.3)
    killApp(packageName)


def killApp(package):
    command = "adb shell am force-stop {}".format(package)
    str(subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()[0])


"""
    adb shell am start -S -R 10 -W com.seevision.android.documentsui/com.filemanager.FilesCategoryActivity
"""

runResult = {}


def runTest(app, launchActivity):
    runResponse = str(subprocess.Popen("adb shell am start -S -R 10 -W {}".format(launchActivity), shell=True,
                                       stdout=subprocess.PIPE).communicate()[0]).replace(" ", "").replace("b''", "")
    print(runResponse)
    # if len(runResponse) != 20:
    #     runResult[app] = ["No result", "No result", "No result", "No result", "No result", "No result", "No result",
    #                       "No result", "No result", "No result", "No result"]
    runResult[app] = re.findall("TotalTime:(\d*)", runResponse)
    sleep(0.3)
    killApp(app)


"""
     {'com.seevision.screencastingassistant': ['0', '177', '323', '332', '342', '331', '333', '341', '337', '334', '338'], 'com.seevision.android.documentsui': ['382', '349', '352', '372', '338', '362', '343', '374', '338', '367', '349'], 'com.seevision.usermanual': ['428', '392', '405', '433', '406', '434', '433', '430', '407', '429', '409'], 'com.android.quicksearchbox': ['265', '232', '259', '260', '264', '239', '245', '241', '278', '282', '243'], 'com.tencent.mm': ['601', '588', '647', '622', '579', '692', '558', '559', '603', '617'], 'com.android.contacts': ['412', '429', '410', '368', '406', '412', '401', '439', '423', '424', '414'], 'com.android.camera2': [], 'com.android.calendar': [], 'com.mn2square.videolistingmvp': ['363', '340', '453', '340', '369', '540', '548', '331', '357', '423', '540'], 'com.seevision.meetingassistant': ['303', '281', '307', '310', '318', '284', '286', '277', '268', '276', '320'], 'com.android.gallery3d': ['233', '250', '270', '218', '279', '233', '253', '255', '231', '259', '259'], 'com.ss.android.lark': ['890', '875', '883', '916', '896', '872', '912', '917', '875', '959', '919'], 'org.chromium.webview_shell': ['512', '504', '501', '500', '506', '474', '474', '493', '467', '491', '477'], 'com.bozee.usbdisplay': ['361', '428', '380', '413', '279', '360', '345', '258', '348', '388', '398'], 'com.synaptics.aisample': ['293', '431', '271', '252', '255', '276', '240', '283', '270', '284', '323'], 'com.tencent.wemeet.app': ['478', '473', '472', '519', '449', '462', '455', '484', '429', '469', '459'], 'com.marvell.tvsample': ['263', '259', '268', '274', '264', '267', '274', '261', '260', '267', '229'], 'com.seevision.painter': [], 'cn.wps.moffice_eng': ['714', '646', '639', '684', '632', '641', '622', '642', '630', '683', '647']} 
"""


def toExcel(runResult):
    writer = pd.ExcelWriter(r"./APP启动时间.xlsx")
    dfList = []
    sheet_name_list = []
    for app, run_result in runResult.items():
        df = pd.DataFrame(data=run_result, columns=["启动时间(TotalTime)"])
        dfList.append(df)
        # sheet_name_list.append(str(app[-31:]).split(".")[-1])

        sheet_name_list.append(str(app[-31:]))
    for i in range(len(dfList)):
        dfList[i] = dfList[i].style.set_properties(**{'text-align': 'center'})
        dfList[i].to_excel(writer, sheet_name=sheet_name_list[i])
        worksheet = writer.sheets[sheet_name_list[i]]
        worksheet.set_column('A:B', 16)
    writer.close()


"""
    接入相机后测试，每个app20组测试数据
    pip3 install xlsxwriter
    pip3 install pandas                                               
"""
if __name__ == '__main__':
    for package in controlAppRange():
        getLaunchableActivity(package)
    if appAndActivity:
        print("待测APP对应的Activity分别是：{}".format(appAndActivity))
    sleep(1)
    # appAndActivity = {
    #     'com.seevision.screencastingassistant': 'com.seevision.scr    eencastingassistant/.ScreencastingMainActivity',
    #     'com.seevision.android.documentsui': 'com.seevision.android.documentsui/com.filemanager.FilesCategoryActivity'}
    for app, activity in appAndActivity.items():
        print(app + " : ----- : " + activity)
        runTest(app, activity)
    if runResult:
        print("最终所有的APP对应的启动测试30次后的结果为：\n {} ".format(runResult))
        toExcel(runResult)
