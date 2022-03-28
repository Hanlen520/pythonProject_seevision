# coding = utf8
import os
import re

import openpyxl
import pandas as pd
import uiautomation

from twoDproject.digitalZoom.serialControl import initCom, getConnectCOMs, enterPSD, getWaitingData, dmesg_n5
from twoDproject.digitalZoom.windowsControl import openHidTool, openPotplayer, enterDeviceSettings, switchResolution, \
    hidZoomIn

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


# Case 错误值 先放大40再缩小53
def case_40_53_errorValue(row, resolution, step1, step2):
    print("【case{}】测试类型【{}】测试分辨率【{}】测试步长1【{}】测试步长2【{}】".format(row, "错误值测试", resolution, step1, step2))


# case 放大 step
def caseZoomIn(row, resolution, step):
    # serial area
    print("【case{}】测试类型【{}】测试分辨率【{}】测试步长【{}】".format(row, "放大测试", resolution, step))
    enterPSD(com_obj)
    dmesg_n5(com_obj)

    # operate area
    openPotplayer(potplayer_path)
    enterDeviceSettings()
    switchResolution(resolution)
    openHidTool(hidtool_path)
    hidZoomIn(step)

    # check area
    # 所有分辨率都是以4K进行step缩放的
    check_result = checkZoomCorrectLog(3840, 2160, step)
    print("本次放大【{}】step测试比对结果为：【{}】".format(step, check_result))


# case 缩小 step
def caseZoomOut(row, resolution, step1, step2):
    print("【case{}】测试类型【{}】测试分辨率【{}】测试步长1【{}】测试步长2【{}】".format(row, "缩小测试", resolution, step1, step2))


# 错误值弹框检测
def checkErrorMessage():
    value = "FAIL"
    try:
        if "操作失败" in str(uiautomation.TextControl(AutomationId="65535").Name):
            print("错误值检测PASS，返回检测失败！")
            value = "PASS"
    except LookupError:
        print("错误值检测FAIL，返回检测失败！")
        value = "FAIL"
    finally:
        return value


# 缩放正确值log检测
def checkZoomCorrectLog(w, h, step):
    """
        1、放大的公式：w=w1-step*64，h=h1-step*36
        2、缩小的公式：w=w1+step*64，h=h1+step*36
        3、右移动的公式：x=x1+step*32, y=y1
    """
    original_data = re.findall("setEPTZZoom x:(.*), y: (.*), w:(.*), h:(.*)", getWaitingData(com_obj))
    print(original_data)
    result_x = str(original_data[0][0]).strip()
    result_y = str(original_data[0][1]).strip()
    result_w = str(original_data[0][2]).strip()
    result_h = str(original_data[0][3]).strip().split("\\")[0]
    after_data = [result_x, result_y, result_w, result_h]
    print(after_data)
    value = ""
    print(w, h)
    if int(result_w) == w - step * 64:
        if int(result_h) == h - step * 36:
            value = "PASS"
    else:
        value = "FAIL"
    return value


# 移动正确值log检测
def checkMoveCorrectLog():
    pass


# 从excel中读取数据并返回（element）
def read_excel_for_page_element(form="./doc/数码变焦测试用例V2.0.xlsx", sheet_name="数码变焦case自动化部分"):
    df = pd.read_excel(form, sheet_name=sheet_name, index_col="CaseNumber", engine="openpyxl")
    test_case_list = []
    for i in range(1, df.shape[0] + 1):
        original_data = df.loc[i, "测试点"]
        test_case_list.append([i, original_data])
    return test_case_list


def write_into_excel(form="./doc/数码变焦测试用例V2.0.xlsx", sheet_name="数码变焦case自动化部分", row=1, column=1, value="PASS"):
    wb = openpyxl.load_workbook(form)
    ws = wb[sheet_name]
    ws.cell(row + 1, column).value = value
    wb.save(form)


# Case分配主控测试区域
"""
    0 - 错误值测试case - [1, '0,MJPG 3840×2160P 30(P 16:9),-1']
    1 - 放大测试case - [2, '1,MJPG 3840×2160P 30(P 16:9),5']
    2 - 缩小测试case - [22, '2,MJPG 3840×2160P 30(P 16:9),40,-1']
"""


def TestControlArea():
    for case in read_excel_for_page_element(sheet_name="数码变焦case自动化部分_Test"):
        case_row = int(case[0])
        original_data = case[1].split(",")
        case_type = int(original_data[0])
        case_resolution = str(original_data[1])
        if len(original_data) >= 4:
            step1 = int(original_data[2])
            step2 = int(original_data[3])
            # 2 step 分支：
            # 正确值 缩小
            if case_type == 2:
                caseZoomOut(case_row, case_resolution, step1, step2)
            # 2 step 分支：
            # 错误值 缩小
            if case_type == 0:
                case_40_53_errorValue(case_row, case_resolution, step1, step2)
        else:
            # 1 step 分支：
            # 错误值 无变焦缩小1
            # 错误值 无变焦放大53
            step = int(original_data[2])
            if case_type == 0:
                case_1or53_errorValue(case_row, case_resolution, step)
            # 1 step 分支：
            # 正确值 放大
            if case_type == 1:
                caseZoomIn(case_row, case_resolution, step)

    # row = case_data[5][0]
    # write_into_excel(row=row, column=7, value="FAIL")


if __name__ == '__main__':
    # case_data = read_excel_for_page_element()
    # print(case_data)
    # TestControlArea()
    # print(checkErrorMessage())

    row = 1
    step = 5
    com_obj = initCom(getConnectCOMs()[0], baud_rate=115200)
    potplayer_path = r"D:\PotPlayer\PotPlayerMini64.exe"
    hidtool_path = r"D:\HIDTools_2.5\HIDTool_2_5.exe"
    resolution = "YUY2 960×540P 30(P 16:9)"
    caseZoomIn(row, resolution, step)
