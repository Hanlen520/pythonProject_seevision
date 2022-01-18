# coding = utf8
import os

from windows_control.PerformanceTestScript.grabImage import grab_StopWatch, grab_CameraStopWatch
from windows_control.PerformanceTestScript.readNumberFromPictrure import ReadNumberFromPicture

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:performance_test_enterance.py
    @Author:十二点前要睡觉
    @Date:2022/1/17 18:52
"""

"""
    性能测试主入口：now function is image recognize to analysis the data then make calculate
"""


class PerformanceTestEnterance:

    def __init__(self):
        pass

    def performance_view_delay_test_GET_TIME(self, imgPath):
        # 获取到图片中windows实际时间和camera预览时间
        windowsImgPath = grab_StopWatch(imgPath)
        cameraImgPath = grab_CameraStopWatch(imgPath)
        if os.path.exists(windowsImgPath) and os.path.exists(cameraImgPath):
            rnfp = ReadNumberFromPicture()
            windows_stopwatch_time = rnfp.readPicture(windowsImgPath)
            camera_stopwatch_time = rnfp.readPicture(cameraImgPath)
            return {"windows_stopwatch_time": windows_stopwatch_time, "camera_stopwatch_time": camera_stopwatch_time}

    def performance_view_delay_test_DATA_OPTIMIZE(self, time_list):
        pass


if __name__ == '__main__':
    PT = PerformanceTestEnterance()
    time_list = PT.performance_view_delay_test_GET_TIME(
        imgPath=r"D:\PycharmProjects\pythonProject_seevision\windows_control\PerformanceTestScript\Sample\Seventh\xxx_00007.jpg")
    print(time_list)
