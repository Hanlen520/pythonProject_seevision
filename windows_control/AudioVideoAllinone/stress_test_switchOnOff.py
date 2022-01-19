# coding = utf8
import logging
import os
import re
import subprocess
import time
from time import sleep

import imagehash
import pandas as pd
import pyautogui
from PIL import Image

os.path.abspath(".")
import uiautomation as ui

"""
    @Project:pythonProject_seevision
    @File:stress_test_switchOnOff.py
    @Author:十二点前要睡觉
    @Date:2022/1/19 10:12
"""
# 实时获取时间
cur_time = time.strftime("%Y%m%d_%H%M%S")


class StressTestSwitchOnOff:

    def __init__(self, path):
        self.path = path

    def GetRecordButton(self):
        controlPanel = ui.PaneControl(searchDepth=4, Name="Transport")
        controlPanelBoundingRectangle = str(controlPanel.BoundingRectangle)
        cp_right_bottom_corner = (
            int(re.findall("(.*),(.*),(.*),(.*)", controlPanelBoundingRectangle)[0][2]),
            int(re.findall("(.*),(.*),(.*),(.*)", controlPanelBoundingRectangle)[0][3].split(")")[0]))
        cp_size = (int(str(re.findall("\[(.*)\]", controlPanelBoundingRectangle)[0]).split("x")[0]),
                   int(str(re.findall("\[(.*)\]", controlPanelBoundingRectangle)[0]).split("x")[1]))

        position = (
            int(cp_right_bottom_corner[0] - (cp_size[0] / 10)), int(cp_right_bottom_corner[1] - (cp_size[1] / 4)))
        logger.info("获取录制按钮位置")
        print("获取录制按钮位置")
        return position

    def GetWaveDisplayArea(self):
        controlPanel = ui.PaneControl(searchDepth=4, Name="WaveCtrl")
        controlPanelBoundingRectangle = str(controlPanel.BoundingRectangle)
        rex = re.findall("(.*),(.*),(.*),(.*)\[.*\]", controlPanelBoundingRectangle)[0]
        # ('(218', '105', '913', '928)')
        x1 = rex[0].split("(")[1]
        y1 = rex[1]
        x2 = rex[2]
        y2 = rex[3].split(")")[0]
        print("获取频率波形图")
        logger.info("获取频率波形图")
        return (x1, y1, x2, y2)

    def ChooseRecordProperties(self):
        print("选择16000采样率，Stereo类型，16-bit进行录制参数")
        logger.info("选择16000采样率，Stereo类型，16-bit进行录制参数")
        ui.ListItemControl(searchDepth=4, Name="16000").Click()
        ui.RadioButtonControl(searchDepth=3, Name="Stereo").Click()
        ui.RadioButtonControl(searchDepth=3, Name="16-bit").Click()
        ui.ButtonControl(searchDepth=3, Name="OK").Click()

    def LaunchCoolEdit(self):
        global cooledit_process
        cooledit_process = subprocess.Popen(self.path)
        print("打开CoolEdit应用程序")
        logger.info("打开CoolEdit应用程序")
        try:
            ui.ButtonControl(searchDepth=3, Name="Delete").Click()
            print("不是第一次打开，需要删除上一次Session")
            logger.info("不是第一次打开，需要删除上一次Session")
            sleep(3)
        except Exception:
            pass
        finally:
            print("窗口最大化")
            logger.info("窗口最大化")
            ui.ButtonControl(searchDepth=3, Name="最大化").Click()

    def StopCoolEdit(self):
        if cooledit_process:
            print("关闭CoolEdit应用程序")
            logger.info("关闭CoolEdit应用程序")
            cooledit_process.kill()
            sleep(1)

    def SwitchOnOffStressTest(self, i):
        self.LaunchCoolEdit()
        record_size = self.GetRecordButton()
        ui.Click(record_size[0], record_size[1])
        self.ChooseRecordProperties()
        sleep(10)
        screenshot_path = self.SaveScreenShot(i)
        ui.Click(record_size[0], record_size[1])
        sleep(0.5)
        self.StopCoolEdit()
        return screenshot_path

    def SaveScreenShot(self, imgName):
        if not os.path.exists("./Screenshot/"):
            os.mkdir("./Screenshot/")
        print("开始区域范围截图，截取频率波形图")
        logger.info("开始区域范围截图，截取频率波形图")
        screenshot_path = "./Screenshot/{}.jpg".format(imgName)
        pyautogui.screenshot(screenshot_path, region=self.GetWaveDisplayArea())
        sleep(0.5)
        return screenshot_path

    def ComparePic(self, standardImgPath, testImgPath):
        hash_standard = imagehash.average_hash(Image.open(standardImgPath))
        hash_test = imagehash.average_hash(Image.open(testImgPath))
        print("进行图片比对，将标准图片与测试图片进行Hash比对")
        logger.info("进行图片比对，将标准图片与测试图片进行Hash比对")
        if hash_standard == hash_test:
            print("Frequence PASS!")
            logger.info("Frequence PASS!")
            return "Frequence PASS!"
        else:
            print("Frequence FAIL!")
            logger.info("Frequence FAIL!")
            return "Frequence FAIL!"

    def SaveToExcel(self, result):
        if not os.path.exists("./Result/"):
            os.mkdir("./Result/")
        recordList = []
        compareList = []
        standardList = []
        for singleResult in result:
            recordList.append(singleResult["Record image"])
            compareList.append(singleResult["Compare result"])
            standardList.append("standard.png")
        print("保存结果至Excel表格中！")
        logger.info("保存结果至Excel表格中！")
        df = pd.DataFrame({"录制音频频率图": recordList, "标准频率图": standardList, "对比结果": compareList})
        df.to_excel("./Result/{}_CompareResult.xlsx".format(cur_time))

    def logger_config(self, log_path, logging_name):
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


if __name__ == '__main__':
    path = r"D:\coolpro2\coolpro2.exe"
    sts = StressTestSwitchOnOff(path)
    if not os.path.exists("./Log/"):
        os.makedirs("./Log/")
    logger = sts.logger_config(log_path="./Log/{}_{}_{}.log".format(cur_time, "StressTestSwitchOnOff", "mainLog"),
                               logging_name="StressTestSwitchOnOff")
    result = []
    logger.info("测试开始:")
    print("测试开始:")
    for i in range(5):
        i += 1
        logger.info("Curren test count: {}".format(str(i)))
        screenshot_path = sts.SwitchOnOffStressTest(i)
        logger.info("该轮测试完成")
        print("该轮测试完成")
        compare_result = sts.ComparePic("./standard.png", screenshot_path)
        logger.info("结果比对完成")
        print("结果比对完成")
        result.append({"Record image": screenshot_path, "Compare result": compare_result})
    if result:
        sts.SaveToExcel(result)
        logger.info("测试结果输出完成！")
        print("测试结果输出完成！")
