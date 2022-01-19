# coding = utf8
import os
import re
import subprocess
from time import sleep

import imagehash
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
        self.SaveScreenShot(i)
        ui.Click(record_size[0], record_size[1])
        sleep(0.5)
        self.StopCoolEdit()

    def SaveScreenShot(self, imgName):
        if not os.path.exists("./Screenshot/"):
            os.mkdir("./Screenshot/")
        pyautogui.screenshot("./Screenshot/{}.jpg".format(imgName))

    def ComparePic(self, standardImgPath, testImgPath):
        hash_standard = imagehash.average_hash(Image.open(standardImgPath))
        hash_test = imagehash.average_hash(Image.open(testImgPath))
        if hash_standard == hash_test:
            print("2 images has no different!")
        else:
            print("2 images has different!")

    def SaveToExcel(self):
        pass


if __name__ == '__main__':
    path = r"D:\coolpro2\coolpro2.exe"
    sts = StressTestSwitchOnOff(path)
    sts.ComparePic("./Screenshot/1.jpg", "./Screenshot/3.jpg")

    # for i in range(3):
    #     i += 1
    #     sts.SwitchOnOffStressTest(i)
