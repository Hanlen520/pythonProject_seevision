# coding = utf8
import os

os.path.abspath("..")
"""
    @Project:pythonProject_seevision
    @File:ocr_identify.py
    @Author:十二点前要睡觉
    @Date:2022/2/16 9:38
"""

import ddddocr
import easyocr


def ddddocr_test():
    ocr = ddddocr.DdddOcr()
    for imageName in os.listdir("./"):
        if imageName.endswith(".jpg"):
            with open(imageName, "rb") as f:
                imageBytes = f.read()
            content = ocr.classification(imageBytes)
            print("识别到的内容：{}".format(content))


def easyocr_test():
    reader = easyocr.Reader(["ch_sim", "en"])
    for imageName in os.listdir("./"):
        if imageName.endswith(".jpg"):
            content = reader.readtext(imageName)
        print("识别到的内容：{}".format(content))


if __name__ == '__main__':
    # ddddocr_test()
    easyocr_test()
