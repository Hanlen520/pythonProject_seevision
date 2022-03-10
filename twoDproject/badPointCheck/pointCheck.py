# coding = utf8
import os

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:pointCheck.py
    @Author:十二点前要睡觉
    @Date:2022/3/10 10:49
"""

"""
    Description:
    图片坏点检测：
    1、0 - 纯白图片检测：判断每个像素点Y亮度大于60即为坏点
    2、1 - 纯黑图片检测：判断每个像素点Y亮度小于-5即为坏点
    
    换算公式：
    Y(亮度)=(0.299*R)+(0.587*G)+(0.114*B)
    
    判断单张图片是否PASS：坏点数不超过0.002%
    
"""

from PIL import Image


class PointCheck:

    def __init__(self, picture_path, check_type):
        self.picture_path = picture_path
        self.check_type = check_type

    def getPictureSize(self):
        pass

    def getPicturePixels(self):
        img_src = Image.open(self.picture_path)
        img_src = img_src.convert("RGBA")
        pixel_list = img_src.load()
        return pixel_list


if __name__ == '__main__':
    picture_path = "./picture.jpg"
    check_type = 0
    pc = PointCheck(picture_path, check_type)
    print(pc.getPicturePixels()[0, 0])