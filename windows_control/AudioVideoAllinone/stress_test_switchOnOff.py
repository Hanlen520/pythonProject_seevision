# coding = utf8
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
        return (x1, y1, x2, y2)

    def ChooseRecordProperties(self):
        ui.ListItemControl(searchDepth=4, Name="16000").Click()
        ui.RadioButtonControl(searchDepth=3, Name="Stereo").Click()
        ui.RadioButtonControl(searchDepth=3, Name="16-bit").Click()
        ui.ButtonControl(searchDepth=3, Name="OK").Click()

    def LaunchCoolEdit(self):
        global cooledit_process
        cooledit_process = subprocess.Popen(self.path)
        try:
            ui.ButtonControl(searchDepth=3, Name="Delete").Click()
            sleep(3)
        except Exception:
            pass
        finally:
            ui.ButtonControl(searchDepth=3, Name="最大化").Click()

    def StopCoolEdit(self):
        if cooledit_process:
            cooledit_process.kill()
            sleep(1)

    def SwitchOnOffStressTest(self, i):
        self.LaunchCoolEdit()
        record_size = self.GetRecordButton()
        ui.Click(record_size[0], record_size[1])
        self.ChooseRecordProperties()
        sleep(3)
        screenshot_path = self.SaveScreenShot(i)
        ui.Click(record_size[0], record_size[1])
        sleep(0.5)
        self.StopCoolEdit()
        return screenshot_path

    def SaveScreenShot(self, imgName):
        if not os.path.exists("./Screenshot/"):
            os.mkdir("./Screenshot/")
        screenshot_path = "./Screenshot/{}.jpg".format(imgName)
        pyautogui.screenshot(screenshot_path, region=self.GetWaveDisplayArea())
        sleep(0.5)
        return screenshot_path

    def ComparePic(self, standardImgPath, testImgPath):
        hash_standard = imagehash.average_hash(Image.open(standardImgPath))
        hash_test = imagehash.average_hash(Image.open(testImgPath))
        if hash_standard == hash_test:
            print("Frequence is same!")
            return "Frequence is same!"
        else:
            print("Frequence is different!")
            return "Frequence is different!"

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
        df = pd.DataFrame({"录制音频频率图": recordList, "标准频率图": standardList, "对比结果": compareList})
        df.to_excel("./Result/{}_CompareResult.xlsx".format(cur_time))


if __name__ == '__main__':
    path = r"D:\coolpro2\coolpro2.exe"
    sts = StressTestSwitchOnOff(path)
    result = []
    for i in range(5):
        i += 1
        screenshot_path = sts.SwitchOnOffStressTest(i)
        compare_result = sts.ComparePic("./standard.png", screenshot_path)
        result.append({"Record image": screenshot_path, "Compare result": compare_result})
    if result:
        sts.SaveToExcel(result)
