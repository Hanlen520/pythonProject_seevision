import os

os.path.abspath(".")
from PIL import Image

import numpy as np

"""
    搭配读取数字 图片的截取类
"""


def grab_StopWatch(imgPath):
    # 实际windows秒表的内容
    image = Image.open(imgPath)  # 用PIL中的Image.open打开图像
    windows_targetimg = imgPath.replace(".jpg", "_windows_grab.jpg")
    image_arr = np.array(image)  # 转化成numpy数组
    # 设置截取的帧图片的读取范围，范围越小，OCR读取越精准，此处Windows秒表是左半张图片，且只截取中间时间部分
    image_tar = image_arr[int(image_arr.shape[0] / 3):int(2 * image_arr.shape[0] / 3),
                int(image_arr.shape[1] / 2):int(2 * image_arr.shape[1] / 2), :]
    im = Image.fromarray(image_tar)
    im.save(windows_targetimg)
    return windows_targetimg


def grab_CameraStopWatch(imgPath):
    # 摄像头录制秒表的内容
    image = Image.open(imgPath)  # 用PIL中的Image.open打开图像
    camera_targetimg = imgPath.replace(".jpg", "_camera_grab.jpg")
    image_arr = np.array(image)  # 转化成numpy数组
    # 设置截取的帧图片的读取范围，范围越小，OCR读取越精准，此处摄像头录制秒表是右半张图片，且只截取中间时间部分
    image_tar = image_arr[int(image_arr.shape[0] / 3):int(2 * image_arr.shape[0] / 3),
                int(image_arr.shape[1] / 10050.2):int(2 * image_arr.shape[1] / 3.9), :]
    im = Image.fromarray(image_tar)
    im.save(camera_targetimg)
    return camera_targetimg


if __name__ == '__main__':
    grab_StopWatch(
        imgPath=r"D:\PycharmProjects\pythonProject_seevision\windows_control\PerformanceTestScript\Sample\Seventh\xxx_00005.jpg")
    grab_CameraStopWatch(
        imgPath=r"D:\PycharmProjects\pythonProject_seevision\windows_control\PerformanceTestScript\Sample\Seventh\xxx_00005.jpg")
