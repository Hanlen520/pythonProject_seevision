# coding = utf8
import os

from windows_control.temp.temp_test.grabImage import grab_StopWatch, grab_CameraStopWatch

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
        imgPath = "./number_analysis/1.png"
        rootName = "number_analysis"
        folderName = "1"
        for imgName in os.listdir("./{}/{}".format(rootName, folderName)):
            imgPath = "./{}/{}/{}".format(rootName, folderName, imgName)
            print(imgPath)
            # c_targetimg = grab_StopWatch(imgPath)
            read_string = self.readFromPic(path=imgPath.format(imgName)).replace("\n", "").strip().replace(" ", "")
            print(read_string)
        # c_targetimg = grab_CameraStopWatch(imgPath)
        # c_read_string = self.readFromPic(path=imgPath).replace("\n", "").strip().replace(" ", "")
        # print(c_read_string)


if __name__ == '__main__':
    rnfp = ReadNumberFromPicture()
    rnfp.readCameraStopWatch()
