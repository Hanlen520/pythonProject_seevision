import os

os.path.abspath(".")
from PIL import Image

import numpy as np

"""
    搭配读取数字 图片的截取类
"""


def grab_StopWatch(imgPath="./number_analysis/1/xxx_00001.jpg"):
    # 实际windows的内容
    image = Image.open(imgPath)  # 用PIL中的Image.open打开图像
    targetimg = imgPath.replace(".jpg", "_grab.jpg")
    image_arr = np.array(image)  # 转化成numpy数组
    image_tar = image_arr[int(image_arr.shape[0] / 3):int(2 * image_arr.shape[0] / 3),
                int(image_arr.shape[1] / 2):int(2 * image_arr.shape[1] / 2), :]
    im = Image.fromarray(image_tar)
    im.save(targetimg)
    return targetimg


def grab_CameraStopWatch(imgPath="./number_analysis/1/xxx_00001.jpg"):
    # 摄像头的内容
    image = Image.open(imgPath)  # 用PIL中的Image.open打开图像
    c_targetimg = imgPath.replace(".jpg", "_C_grab.jpg")
    image_arr = np.array(image)  # 转化成numpy数组
    image_tar = image_arr[int(image_arr.shape[0] / 3):int(2 * image_arr.shape[0] / 3),
                int(image_arr.shape[1] / 10050.2):int(2 * image_arr.shape[1] / 3.9), :]
    im = Image.fromarray(image_tar)
    im.save(c_targetimg)
    return c_targetimg


if __name__ == '__main__':
    grab_StopWatch(imgPath=r"D:\PycharmProjects\pythonProject_seevision\windows_control\temp\temp_test\Sample\Seventh\xxx_00246.jpg")
    grab_CameraStopWatch(imgPath=r"D:\PycharmProjects\pythonProject_seevision\windows_control\temp\temp_test\Sample\Seventh\xxx_00246.jpg")
