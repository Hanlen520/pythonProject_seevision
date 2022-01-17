# coding = utf8
import os

os.path.abspath(".")
import pytesseract
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

    def OCR_Model(self, path=""):
        """
        pytesseract OCR文字识别模块
        :param path:传入待读取的图片路径
        :return:返回读取并处理过的时间
        """
        text = pytesseract.image_to_string(Image.open(path), lang="eng", config="--psm 6")
        return text

    def readPicture(self, imgPath):
        """
        读取图片上的秒表时间文字信息
        :param imgPath:传入待读取的图片路径
        :return:返回读取并处理过的时间
        """
        c_read_string = self.OCR_Model(path=imgPath).replace("\n", "").strip().replace(" ", "")
        print(c_read_string)
        print("\n seperate line \n")
        return c_read_string


if __name__ == '__main__':
    camera_imgPath = r"D:\PycharmProjects\pythonProject_seevision\windows_control\PerformanceTestScript\Sample\Seventh\xxx_00007_camera_grab.jpg"
    windows_imgPath = r"D:\PycharmProjects\pythonProject_seevision\windows_control\PerformanceTestScript\Sample\Seventh\xxx_00007_windows_grab.jpg"
    rnfp = ReadNumberFromPicture()
    rnfp.readPicture(camera_imgPath)
    rnfp.readPicture(windows_imgPath)
