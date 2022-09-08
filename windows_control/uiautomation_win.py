# coding = utf8

import os
import re
import subprocess
import traceback
from time import sleep

import pyautogui

os.path.abspath(".")

import uiautomation
import pandas as pd
import time
import logging

# 实时获取时间
cur_time = time.strftime("%Y%m%d_%H%M%S")

"""
    绝大多数Windows软件的自动化控件操作等可以用uiautomation库来实现：
    1、Python-UIAutomation-for-Windows-master + uiautomation
    2、 automation.py（搜索控件）
    3、 pyautogui模拟键盘操作，快捷键等，对于一些uiautomation搜索不到的UI控件
"""
"""
    @param:
    @description:logger构建器
        log_path:log生成路径
        logging_name:log名称
"""



def logger_config(log_path, logging_name):
    # 获取logger对象,取名
    logger = logging.getLogger(logging_name)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_path, encoding='UTF-8')
    # 生成并设置文件日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # 为logger对象添加句柄
    logger.addHandler(handler)

    return logger


# 打开Potplayer，传入potplayer启动exe路径
def openPotplayer(potplayer_path="D:\PotPlayer\PotPlayerMini64.exe"):
    global potplayer
    potplayer = subprocess.Popen(potplayer_path)
    sleep(2)
    if uiautomation.TextControl(searchDepth=3, Name="检查更新：").Exists():
        pyautogui.press("esc")


# 进入Potplayer设备连接设置页面
def enterDeviceSettings():
    global potplayer_frame
    global settings_frame
    potplayer_frame = uiautomation.WindowControl(searchDepth=1, Name="PotPlayer")
    pyautogui.hotkey("alt", "d")
    settings_frame = uiautomation.WindowControl(searchDepth=2, Name="设备设置")


# 获取当前摄像头支持的格式
def getFormatList():
    settings_frame.ComboBoxControl(AutomationId="3008").Click()
    sleep(1)
    format_list = settings_frame.ListControl(searchDepth=5, Name="格式：")
    all_format = format_list.GetChildren()
    formatList = []
    for format in all_format:
        # 筛选掉重复的分辨率格式
        if (str(format) != "开始播放时选择格式") | (str(format) != "默认格式(推荐)"):
            if "(P" in str(format):
                formatList.append(format.Name)
    return formatList


# 遍历格式切换所有分辨率
def switchResolution(resolution="YUY2 960×540P 30(P 16:9)"):
    settings_frame.ComboBoxControl(AutomationId="3008").Click()
    sleep(1)
    find = False
    count = 0
    while not find:
        if resolution:
            resolution_checked = settings_frame.ListItemControl(searchDepth=6, Name=resolution)
            findResolution = str(re.findall("Rect:(.*)(\[)", str(resolution_checked))[0][0]).strip()
            if findResolution != "(0,0,0,0)":
                find = True
                resolution_checked.Click()
                break
        else:
            print("Resolution error")
        if count < 10:
            pyautogui.scroll(500)
            sleep(0.5)
        else:
            pyautogui.scroll(-500)
            sleep(0.5)
        count += 1
        sleep(0.5)
    sleep(1)
    settings_frame.ButtonControl(searchDepth=3, Name="打开设备(O)").Click()
    # -- Need Modified, 等待时间
    sleep(5)  # sleep(3)


# 获取当前分辨率下的摄像头的帧率和位率并返回一个list
def getPlayerInformation():
    pyautogui.hotkey("ctrl", "f1")
    # -- Need Modified, 等待时间
    sleep(8)  # sleep(3)
    player_information = uiautomation.WindowControl(searchDepth=1, Name="播放信息")
    current_frameRate = player_information.TextControl(AutomationId="3201").GetWindowText()
    current_bitRate = player_information.TextControl(AutomationId="3386").GetWindowText()
    framerate = re.findall("->(.*)", current_frameRate)[0]
    bitrate = re.findall("\/(.*)\skbps", current_bitRate)[0]
    print("帧率：{} fps".format(framerate), end=" -- ")
    print("位率：{} kbps".format(bitrate))
    print("")
    return framerate, bitrate


# 关闭Potplayer
def closePotplayer():
    potplayer.kill()


# 标准数据和测试数据生成使用该方法生成，传入测试次数和测试结果列表进行每次测试数据的excel表格生成
def standard_test_DataGenerate(test_number="", result_list=[]):
    resolution_list = []
    frame_rate_list = []
    bit_rate_list = []
    for result in result_list:
        resolution_list.append(result[0])
        frame_rate_list.append(result[1])
        bit_rate_list.append(result[2])
    df = pd.DataFrame({"分辨率": resolution_list, "帧率": frame_rate_list, "位率": bit_rate_list})
    df.to_excel("./第{}次测试_resolutionTest.xlsx".format(test_number))


# 根据标准数据和测试数据对比返回过来的结果list进行生成最终的测试结果表格
def generateResult(checked_list=[]):
    resolution_list = []
    s_frame_rate_list = []
    s_bit_rate_list = []
    t_frame_rate_list = []
    t_bit_rate_list = []
    frame_gap_value_list = []
    bitRate_gap_value_list = []
    compare_result_list = []
    # [[分辨率、标准帧率、标准位率、测试帧率、测试位率、帧率差、位率差、结果]、[]、[]……]
    for result in checked_list:
        resolution_list.append(result[0])
        s_frame_rate_list.append(result[1])
        s_bit_rate_list.append(result[2])
        t_frame_rate_list.append(result[3])
        t_bit_rate_list.append(result[4])
        frame_gap_value_list.append(result[5])
        bitRate_gap_value_list.append(result[6])
        compare_result_list.append(result[7])
    df = pd.DataFrame(
        {"分辨率": resolution_list, "标准帧率": s_frame_rate_list, "标准位率": s_bit_rate_list, "测试帧率": t_frame_rate_list,
         "测试位率": t_bit_rate_list, "帧率差": frame_gap_value_list, "位率差": bitRate_gap_value_list,
         "测试结果": compare_result_list})
    df.to_excel("compare_result_{}.xlsx".format(str(cur_time)))


# 传入potplayer启动exe路径
def test_standard_test_data(potplayerPath):
    if not os.path.exists("./log/"):
        os.makedirs("./log/")
    logger = logger_config(log_path="./log/{}_{}_{}.log".format(cur_time, "resolutionSwitchStress", "mainLog"),
                           logging_name="resolutionSwitchStress")
    result_list = []
    for i in range(1):
        try:
            openPotplayer(potplayer_path=potplayerPath)
            enterDeviceSettings()
            formatList = []
            all_format = getFormatList()
            print("\n 当前存在{}种分辨率，即将对这些分辨率格式开始测试……".format(len(all_format)))
            logger.info("\n 当前存在{}种分辨率，即将对这些分辨率格式开始测试……".format(len(all_format)))
            print(all_format)
            closePotplayer()
            i = 0
            for format in all_format:
                i += 1
                logger.info("第{}次测试 -- 当前测试分辨率为：{}".format(str(i), format))
                print("第{}次测试 -- 当前测试分辨率为：{}".format(str(i), format))
                openPotplayer(potplayer_path=potplayerPath)
                enterDeviceSettings()
                switchResolution(format)
                list_cur = getPlayerInformation()
                logger.info("\t帧率：{} fps".format(list_cur[0]))
                logger.info("\t位率：{} kbps".format(list_cur[1]))
                closePotplayer()
                result_list.append([format, list_cur[0], list_cur[1]])
        except Exception as ex:
            logger.error("Some error happened : {}".format(str(ex)))
            logging.error("\n" + traceback.format_exc())
            print("Some error happened : {}".format(str(ex)))
            closePotplayer()
            continue
        finally:
            standard_test_DataGenerate(test_number=str(1), result_list=result_list)
            result_list = []
            closePotplayer()


# 对比标准和测试数据并返回一个最终结果list -- Need modified
def compare2StandardDataTest():
    # 进行第二次测试，完善与第一次测试的数据比较并得出结果
    # 完善好后，学习PyQt5，将其转换成单独的工具：
    # 1、功能分开
    # 2、接口独立
    # 第二次测试和第一次测试数据进行读取后比较，再生成一个测试结果的Excel表格 -- ongoing
    standard_result = readStandardResultExcel(path="./标准值表格.xlsx")
    test_result = readExcel(path="./第1次测试_resolutionTest.xlsx")
    checked_list = []
    if len(standard_result) == len(test_result):
        print("Test result is the same count!")
        for j in range(0, len(test_result)):
            for i in range(0, len(standard_result)):
                item_list = []
                item_result = "FAIL"
                """
                    此处判断是否是同一个格式的结果 -- Need Modified，需要改成两层遍历，因为是打乱的，所以每个格式都要遍历一遍标准值列表的格式title再进行结果判断
                    先判断帧率是否在30帧左右，帧率不小于29，则再进行下一步判断
                    将标准值范围进行划分两个列，判断在之间即PASS，否则FAIL
                """
                if standard_result[i][1] == test_result[j][1]:
                    print("Same row compare:当前check分辨率为：{}".format(test_result[j][1]))
                    t_frame = int(test_result[j][2])
                    t_bitRate = int(test_result[j][3])
                    if standard_result[i][2] == "\\":
                        print("Current standard value is not give!")
                        item_result = "Current standard value is not give!"
                        # 每行结果拼接：[分辨率、标准帧率、标准位率、测试帧率、测试位率、帧率差、位率差、结果]
                        item_list.append(test_result[j][1])
                        item_list.append("\\")
                        item_list.append("{}~{}".format("\\", "\\"))
                        item_list.append(t_frame)
                        item_list.append(t_bitRate)
                        item_list.append(str(t_frame - 30))
                        item_list.append("{}~{}".format("\\", "\\"))
                        item_list.append(item_result)
                        checked_list.append(item_list)
                        continue
                    s_bitRate_minimum = int(standard_result[i][2])
                    s_bitRate_maximum = int(standard_result[i][3])
                    print(t_frame, t_bitRate, s_bitRate_minimum, s_bitRate_maximum)
                    if t_frame >= 29:
                        if s_bitRate_minimum <= t_bitRate <= s_bitRate_maximum:
                            item_result = "PASS"
                            print("Pass")
                        else:
                            item_result = "FAIL"
                    else:
                        item_result = "FAIL"
                    # 每行结果拼接：[分辨率、标准帧率、标准位率、测试帧率、测试位率、帧率差、位率差、结果]
                    item_list.append(test_result[j][1])
                    item_list.append("30")
                    item_list.append("{}~{}".format(s_bitRate_minimum, s_bitRate_maximum))
                    item_list.append(t_frame)
                    item_list.append(t_bitRate)
                    item_list.append(str(t_frame - 30))
                    item_list.append("{}~{}".format(t_bitRate - s_bitRate_minimum, t_bitRate - s_bitRate_maximum))
                    item_list.append(item_result)
                    checked_list.append(item_list)
    else:
        print("Compare data length is different , please check your orignial data")
    if checked_list:
        print("Compare finished!")
        return checked_list
    else:
        return "Somethings error , please check your original data"


# 按结果格式，读取Excel表格
def readExcel(path="./第1次测试_resolutionTest.xlsx"):
    read = pd.read_excel(io=path, header=0, names=["", "分辨率", "帧率", "位率"], sheet_name="Sheet1", engine="openpyxl")
    # print(read.values)  # 结果为[[],[],[]……]形式
    result = read.values
    return result
    # for i in read.values:
    # 分辨率
    # print(i[0])
    # 帧率
    # print(i[1])
    # 位率
    # print(i[2])


def readStandardResultExcel(path="./标准值表格.xlsx"):
    read = pd.read_excel(io=path, header=0, names=["", "分辨率", "位率Minimum", "位率Maximum"], sheet_name="Sheet1",
                         engine="openpyxl")
    return read.values


if __name__ == '__main__':
    sleep(3)
    potplayerPath = "D:\PotPlayer\PotPlayerMini64.exe"
    try:
        test_standard_test_data(potplayerPath)
    except Exception as ex:
        print("Main program has error please check: {}".format(str(ex)))
    finally:
        print("Test Finished!")
        compareResult = compare2StandardDataTest()
        generateResult(compareResult)
