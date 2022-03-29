# coding = utf8
import os
import re

import openpyxl
import pandas as pd
import uiautomation

from twoDproject.digitalZoom.serialControl import initCom, getConnectCOMs, enterPSD, getWaitingData, dmesg_n5
from twoDproject.digitalZoom.windowsControl import openHidTool, openPotplayer, enterDeviceSettings, switchResolution, \
    hidZoomIn, closeHidTool, closePotplayer, hidZoomOut, rightNarrow

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:digitalZoomTestCase.py
    @Author:十二点前要睡觉
    @Date:2022/3/23 10:33
    @Description:自动化测试点分解：（每次测试操作 + 一次串口log获取操作 = 完整的操作）
        1、6个分辨率：
            MJPG 3840*2160
            MJPG 1920*1080
            MJPG 1280*720
            H264 3840*2160
            H264 1920*1080
            H264 1280*720
        2、测试点：
            a、错误值：
                无缩放状态->缩小1step  
                    [1、弹框操作失败，2、zoom: 1, step 1]
                无缩放状态->过度放大53step   
                    [1、弹框操作失败，2、zoom: 0, step 53]
                放大40step状态->过度缩小53step
                    [1、zoom: 0, step 40，2、x: 1280, y: 720, w: 1280, h: 720]
            b、有效值：
                放大->右移动画面1step：
                    放大5step
                        [1、zoom: 0, step 5，2、x: 160, y: 90, w: 3520, h: 1980，3、direction: 3, step 1，4、x: 192, y: 90]
                        规律： -- important
                            (通过w、h、x、y来判断放大、缩小、移动的值是否正确)
                            所有分辨率的放大缩小移动都是以4K的进行的
                            1、放大的公式：w=w1-step*64，h=h1-step*36
                            2、缩小的公式：w=w1+step*64，h=h1+step*36
                            3、右移动的公式：x=x1+step*32, y=y1
                放大40step->缩小->右移动画面1step：
                    缩小1step
                        [1、zoom: 0, step 40，2、x: 1280, y: 720, w: 1280, h: 720，3、zoom: 1, step 1，4、x: 1248, y: 702, w: 1344, h: 756，5、direction: 3, step 1，6、x: 1280, y: 702]
        3、Case执行方式：
        0 - 错误值测试case - [1, '0,MJPG 3840×2160P 30(P 16:9),-1'] -- 弹框“操作失败”关键字
        1 - 放大测试case - [2, '1,MJPG 3840×2160P 30(P 16:9),5']
        2 - 缩小测试case - [22, '2,MJPG 3840×2160P 30(P 16:9),40,-1']
"""


# Case 错误值 无变焦缩小1 无变焦放大53
def case_1or53_errorValue(row, resolution, step):
    print("【case{}】测试类型【{}】测试分辨率【{}】测试步长【{}】".format(row, "错误值测试", resolution, step))
    log_toTxt("【case{}】测试类型【{}】测试分辨率【{}】测试步长【{}】".format(row, "错误值测试", resolution, step))
    # operate area
    openPotplayer(potplayer_path)
    enterDeviceSettings()
    switchResolution(resolution)
    openHidTool(hidtool_path)
    if step == 1:
        hidZoomOut(abs(step))
    elif step == 53:
        hidZoomIn(step)

    test_result = checkErrorMessage()
    print("本次case测试结果为【{}】".format(test_result))
    log_toTxt("本次case测试结果为【{}】".format(test_result))

    # case结束后关闭应用程序
    closeHidTool()
    closePotplayer()
    write_into_excel(form=form, sheet_name=sheet_name, row=row, column=7, value=test_result)


# Case 错误值 先放大40再缩小53
def case_40_53_errorValue(row, resolution, step1, step2):
    print("【case{}】测试类型【{}】测试分辨率【{}】测试步长1【{}】测试步长2【{}】".format(row, "错误值测试", resolution, step1, step2))
    log_toTxt("【case{}】测试类型【{}】测试分辨率【{}】测试步长1【{}】测试步长2【{}】".format(row, "错误值测试", resolution, step1, step2))
    # operate area
    openPotplayer(potplayer_path)
    enterDeviceSettings()
    switchResolution(resolution)
    openHidTool(hidtool_path)

    hidZoomIn(step1)
    hidZoomOut(step2)

    test_result = checkErrorMessage()
    print("本次case测试结果为【{}】".format(test_result))
    log_toTxt("本次case测试结果为【{}】".format(test_result))

    # case结束后关闭应用程序
    closeHidTool()
    closePotplayer()
    write_into_excel(form=form, sheet_name=sheet_name, row=row, column=7, value=test_result)


# case 放大 step
def caseZoomIn(type, row, resolution, step):
    print("【case{}】测试类型【{}】测试分辨率【{}】测试步长【{}】".format(row, "放大测试", resolution, step))
    log_toTxt("【case{}】测试类型【{}】测试分辨率【{}】测试步长【{}】".format(row, "放大测试", resolution, step))
    # operate area
    openPotplayer(potplayer_path)
    enterDeviceSettings()
    switchResolution(resolution)
    openHidTool(hidtool_path)
    hidZoomIn(step)

    # check area
    # 所有分辨率都是以4K进行step缩放的 - 缩放结果
    data1 = checkZoomCorrectLog(type, 3840, 2160, step)
    zoom_check_result = data1[0]
    print("本次放大【{}】step测试比对结果为：【{}】".format(step, zoom_check_result))
    log_toTxt("本次放大【{}】step测试比对结果为：【{}】".format(step, zoom_check_result))

    if zoom_check_result == "PASS":
        test_result = "PASS"
        # 移动结果
        rightNarrow(1)
        move_check_result = checkRightMoveCorrectLog(int(data1[1]), int(data1[2]), 1)
        print("本次移动【{}】step测试比对结果为：【{}】".format(1, move_check_result))
        log_toTxt("本次移动【{}】step测试比对结果为：【{}】".format(1, move_check_result))
        if test_result == move_check_result:
            test_result = "PASS"
        else:
            test_result = "FAIL"
            print("当前case移动1step失败，FAIL")
            log_toTxt("当前case移动1step失败，FAIL")
    else:
        test_result = "FAIL"
    print("本次case测试结果为【{}】".format(test_result))
    log_toTxt("本次case测试结果为【{}】".format(test_result))

    # case结束后关闭应用程序
    closeHidTool()
    closePotplayer()
    write_into_excel(form=form, sheet_name=sheet_name, row=row, column=7, value=test_result)


# case 缩小 step
def caseZoomOut(type, row, resolution, step1, step2):
    print("【case{}】测试类型【{}】测试分辨率【{}】测试步长1【{}】测试步长2【{}】".format(row, "缩小测试", resolution, step1, step2))
    log_toTxt("【case{}】测试类型【{}】测试分辨率【{}】测试步长1【{}】测试步长2【{}】".format(row, "缩小测试", resolution, step1, step2))
    # operate area
    openPotplayer(potplayer_path)
    enterDeviceSettings()
    switchResolution(resolution)
    openHidTool(hidtool_path)
    hidZoomIn(step1)
    first_data = getZoomLogData(com_obj)
    w1 = first_data[2]
    h1 = first_data[3]
    print("缩小测试：第一次放大返回w为【{}】，h为【{}】".format(w1, h1))
    log_toTxt("缩小测试：第一次放大返回w为【{}】，h为【{}】".format(w1, h1))
    hidZoomOut(step2)

    # check area
    data1 = ""
    if step1 == abs(step2):
        zoom_check_result = checkBorderOver()
    else:
        data1 = checkZoomCorrectLog(type, int(w1), int(h1), step2)
        zoom_check_result = data1[0]
    print("本次先放大【{}】后缩小【{}】step测试比对结果为：【{}】".format(step1, step2, zoom_check_result))
    log_toTxt("本次先放大【{}】后缩小【{}】step测试比对结果为：【{}】".format(step1, step2, zoom_check_result))
    if zoom_check_result == "PASS":
        test_result = "PASS"
        if step1 != abs(step2):
            # 移动结果
            rightNarrow(1)
            move_check_result = checkRightMoveCorrectLog(int(data1[1]), int(data1[2]), 1)
            print("本次移动【{}】step测试比对结果为：【{}】".format(1, move_check_result))
            log_toTxt("本次移动【{}】step测试比对结果为：【{}】".format(1, move_check_result))
            if test_result == move_check_result:
                test_result = "PASS"
            else:
                test_result = "FAIL"
                print("当前case移动1step失败，FAIL")
    else:
        test_result = "FAIL"
    print("本次case测试结果为【{}】".format(test_result))
    log_toTxt("本次case测试结果为【{}】".format(test_result))
    # case结束后关闭应用程序
    closeHidTool()
    closePotplayer()
    write_into_excel(form=form, sheet_name=sheet_name, row=row, column=7, value=test_result)


# 错误值弹框检测
def checkErrorMessage():
    value = "FAIL"
    try:
        if "操作失败" in str(uiautomation.TextControl(AutomationId="65535").Name):
            print("错误值检测PASS，返回检测失败！")
            log_toTxt("错误值检测PASS，返回检测失败！")
            value = "PASS"
    except LookupError:
        print("错误值检测FAIL，返回检测失败！")
        log_toTxt("错误值检测FAIL，返回检测失败！")
        value = "FAIL"
    finally:
        return value


# 边界值到达检测
def checkBorderOver():
    value = "FAIL"
    try:
        if "当前已到达边界" in str(uiautomation.TextControl(AutomationId="65535").Name):
            print("当前已到达边界，弹框出现")
            log_toTxt("当前已到达边界，弹框出现")
            value = "PASS"
    except LookupError:
        print("当前已到达边界，弹框未出现")
        log_toTxt("当前已到达边界，弹框未出现")
        value = "FAIL"
    finally:
        return value


def getZoomLogData(com_obj):
    original_data = re.findall("setEPTZZoom x:(.*), y: (.*), w:(.*), h:(.*)", getWaitingData(com_obj))
    result_x = str(original_data[0][0]).strip()
    result_y = str(original_data[0][1]).strip()
    result_w = str(original_data[0][2]).strip()
    result_h = str(original_data[0][3]).strip().split("\\")[0]
    after_data = [result_x, result_y, result_w, result_h]
    print(after_data)
    log_toTxt(after_data)
    return after_data


# 缩放正确值log检测
def checkZoomCorrectLog(type, w, h, step):
    """
        1、放大的公式：w=w1-step*64，h=h1-step*36
        2、缩小的公式：w=w1+step*64，h=h1+step*36
        3、右移动的公式：x=x1+step*32, y=y1
    """
    after_data = getZoomLogData(com_obj)
    value = ""
    print(w, h)
    log_toTxt([w, h])
    if type == 1:
        if int(after_data[2]) == w - step * 64:
            if int(after_data[3]) == h - step * 36:
                value = "PASS"
        else:
            value = "FAIL"
    if type == 2:
        if int(after_data[2]) == w + step * 64:
            if int(after_data[3]) == h + step * 36:
                value = "PASS"
        else:
            value = "FAIL"
    return value, after_data[0], after_data[1]


def getMoveLogData(com_obj):
    original_data = re.findall("setEPTZMove x:(.*), y: (.*), w:(.*), h:(.*)", getWaitingData(com_obj))
    result_x = str(original_data[0][0]).strip()
    result_y = str(original_data[0][1]).strip()
    result_w = str(original_data[0][2]).strip()
    result_h = str(original_data[0][3]).strip().split("\\")[0]
    after_data = [result_x, result_y, result_w, result_h]
    print(after_data)
    log_toTxt(after_data)
    return after_data


# 向右移动正确值log检测
def checkRightMoveCorrectLog(x, y, step):
    after_data = getMoveLogData(com_obj)
    value = ""
    print(x, y)
    log_toTxt([x, y])
    if int(after_data[0]) == x + step * 32:
        if int(after_data[1]) == y:
            value = "PASS"
    else:
        value = "FAIL"
    return value


# 从excel中读取数据并返回（element）
def read_excel_for_page_element(form="./doc/数码变焦测试用例V2.0.xlsx", sheet_name="数码变焦case自动化部分"):
    print("从excel中读取数据（测试数据case）并返回（element）")
    log_toTxt("从excel中读取数据（测试数据case）并返回（element）")
    df = pd.read_excel(form, sheet_name=sheet_name, index_col="CaseNumber", engine="openpyxl")
    test_case_list = []
    for i in range(1, df.shape[0] + 1):
        original_data = df.loc[i, "测试点"]
        test_case_list.append([i, original_data])
    return test_case_list


def write_into_excel(form="./doc/数码变焦测试用例V2.0.xlsx", sheet_name="数码变焦case自动化部分", row=1, column=1, value="PASS"):
    print("将测试结果写入excel表格对应Case的行 - 测试结果处：【{}】".format(value))
    log_toTxt("将测试结果写入excel表格对应Case的行 - 测试结果处：【{}】".format(value))
    wb = openpyxl.load_workbook(form)
    ws = wb[sheet_name]
    ws.cell(row + 1, column).value = value
    wb.save(form)


def log_toTxt(result):
    try:
        with open("./自动化变焦测试CaseRunningLog.log", "a+") as f:
            f.write(str(result) + "\n")
    except (AttributeError, TypeError) as ex:
        print("【Error need check, maybe not important】 : \r\n{}\r\n".format(str(ex)))
        f.write("【Error need check, maybe not important】 : \r\n{}\r\n".format(str(ex)))


# Case分配主控测试区域
"""
    0 - 错误值测试case - [1, '0,MJPG 3840×2160P 30(P 16:9),-1']
    1 - 放大测试case - [2, '1,MJPG 3840×2160P 30(P 16:9),5']
    2 - 缩小测试case - [22, '2,MJPG 3840×2160P 30(P 16:9),40,-1']
"""


def TestControlArea():
    # serial area
    global com_obj
    com_obj = initCom(getConnectCOMs()[0], baud_rate=115200)
    enterPSD(com_obj)
    dmesg_n5(com_obj)
    for case in read_excel_for_page_element(form=form, sheet_name=sheet_name):
        case_row = int(case[0])
        print("================【case{}】测试开始================\n".format(case_row))
        log_toTxt("================【case{}】测试开始================\n".format(case_row))
        original_data = case[1].split(",")
        case_type = int(original_data[0])
        case_resolution = str(original_data[1])
        if len(original_data) >= 4:
            step1 = abs(int(original_data[2]))
            step2 = abs(int(original_data[3]))
            # 2 step 分支：
            # 正确值 缩小
            if case_type == 2:
                caseZoomOut(case_type, case_row, case_resolution, step1, step2)
            # 2 step 分支：
            # 错误值 缩小
            if case_type == 0:
                case_40_53_errorValue(case_row, case_resolution, step1, step2)
        else:
            # 1 step 分支：
            # 错误值 无变焦缩小1
            # 错误值 无变焦放大53
            step = abs(int(original_data[2]))
            if case_type == 0:
                case_1or53_errorValue(case_row, case_resolution, step)
            # 1 step 分支：
            # 正确值 放大
            if case_type == 1:
                caseZoomIn(case_type, case_row, case_resolution, step)
        print("================【case{}】测试结束================\n".format(case_row))
        log_toTxt("================【case{}】测试结束================\n".format(case_row))


if __name__ == '__main__':
    potplayer_path = r"D:\PotPlayer\PotPlayerMini64.exe"
    hidtool_path = r"D:\HIDTools_2.5\HIDTool_2_5.exe"
    form = "./doc/数码变焦测试用例V2.0.xlsx"
    sheet_name = "数码变焦case自动化部分_Test"
    # 测试结果所在列索引
    column = 7
    TestControlArea()
