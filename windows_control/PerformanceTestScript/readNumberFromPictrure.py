# coding = utf8
import os
import re

from windows_control.temp.picture_compare.grabImage import grab_StopWatch, grab_CameraStopWatch

os.path.abspath(".")
import pytesseract
import sys
from PIL import Image

"""
    @Project:PycharmProjects
    @File:readNumberFromPictrure.py
    @Author:十二点前要睡觉
    @Date:2022/1/6 11:48
"""


class ReadNumberFromPicture:

    def __int__(self):
        pass

    def readFromPic(self, path=""):
        text = pytesseract.image_to_string(Image.open(path), lang="eng", config="--psm 6")
        return text

    def readWindowsStopWatch(self):
        """
            Windows StopWatch读取流程：
            1、裁剪
            2、OCR读取文字：得到实际值
        """
        # imgPath = "./number_analysis/1/xxx_00001.jpg"
        rootName = "number_analysis"
        folderName = "1"
        for imgName in os.listdir("./{}/{}".format(rootName, folderName)):
            imgPath = "./{}/{}/{}".format(rootName, folderName, imgName)
            print(imgPath)
            targetimg = grab_StopWatch(imgPath)
            read_string = self.readFromPic(path=targetimg).replace("\n", "").strip().replace(" ", "")
            print(read_string)

    def readCameraStopWatch(self):
        """
            Camera StopWatch读取流程：
            1、裁剪
            2、OCR读取文字：得到实际值
        """
        # imgPath = "./number_analysis/1.png"
        imgPath = "./numberPic.jpg"
        rootName = "number_analysis"
        folderName = "1"
        for imgName in os.listdir("./{}/{}".format(rootName, folderName)):
            imgPath = "./{}/{}/{}".format(rootName, folderName, imgName)
            print(imgPath)
            # c_targetimg = grab_StopWatch(imgPath)
            read_string = self.readFromPic(path=imgPath.format(imgName)).replace("\n", "").strip().replace(" ", "")
            print(read_string)
            print("\n seperate line \n")
            match_string = re.findall("(.*):(.*):(.*).(.*)", read_string)
            print(match_string)
        # c_targetimg = grab_CameraStopWatch(imgPath)
        # c_read_string = self.readFromPic(path=imgPath).replace("\n", "").strip().replace(" ", "")
        # print(c_read_string)

    def readOnePicture(self):
        # imgPath = "./xxx_00016.jpg"
        # imgPath = r"D:\PycharmProjects\pythonProject_seevision\windows_control\temp\temp_test\Sample\FourthStopWatchModel_lowResolution\xxx_00001_grab.jpg"
        # imgPath = r"D:\PycharmProjects\pythonProject_seevision\windows_control\temp\temp_test\Sample\FourthStopWatchModel_lowResolution\xxx_00001_C_grab.jpg"
        # imgPath = r"D:\PycharmProjects\pythonProject_seevision\windows_control\temp\temp_test\Sample\Seventh\xxx_00246_grab.jpg"
        imgPath = r"D:\PycharmProjects\pythonProject_seevision\windows_control\temp\temp_test\Sample\Seventh\xxx_00246_C_grab.jpg"
        c_read_string = self.readFromPic(path=imgPath).replace("\n", "").strip().replace(" ", "")
        print(c_read_string)
        print("\n seperate line \n")
        # match_string = re.findall("(.*):(.*):(.*).(.*)", c_read_string)
        # print(match_string)

    def readListPicture(self):
        imgPath = r"D:\PycharmProjects\pythonProject_seevision\windows_control\temp\temp_test\Sample\FourthStopWatchModel_lowResolution\\"
        for imgName in os.listdir(imgPath):
            print(imgName)
            c_read_string = self.readFromPic(path=imgPath + imgName).replace("\n", "").strip().replace(" ", "")
            print(c_read_string)
            print("seperate line\n")
            # match_string = re.findall("(.*):(.*):(.*).(.*)", c_read_string)
            # print(match_string, end="\n\n")


if __name__ == '__main__':
    rnfp = ReadNumberFromPicture()
    # rnfp.readCameraStopWatch()
    rnfp.readOnePicture()
    # rnfp.readListPicture()
