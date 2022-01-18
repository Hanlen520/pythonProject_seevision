# coding = utf8
import os
import re
import time

import pandas as pd

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
# 实时获取时间
cur_time = time.strftime("%Y%m%d_%H%M%S")


class PerformanceTestEnterance:

    def __init__(self):
        if not os.path.exists("./Sample/"):
            os.mkdir("./Sample/")

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
        windows_stopwatch_time = time_list["windows_stopwatch_time"]
        camera_stopwatch_time = time_list["camera_stopwatch_time"]
        # print(windows_stopwatch_time, camera_stopwatch_time)
        try:
            if windows_stopwatch_time and camera_stopwatch_time:

                w_temp = int(
                    re.sub("\D", "", windows_stopwatch_time))
                c_temp = int(
                    re.sub("\D", "", camera_stopwatch_time))
                delay_time = abs(w_temp - c_temp)
                if 100 <= delay_time <= 250:
                    return {"windows_stopwatch_time": w_temp,
                            "camera_stopwatch_time": c_temp,
                            "delay_time": delay_time}
        except ValueError:
            # print("skip it!")
            pass

    def DELAY_TEST_MAIN(self, imgPath):
        time_list = self.performance_view_delay_test_GET_TIME(imgPath)
        # print(time_list)
        result_delay_list = self.performance_view_delay_test_DATA_OPTIMIZE(time_list)
        if result_delay_list:
            print(result_delay_list)
            return result_delay_list

    def write_intoExcel(self, test_resolution, data):
        if not os.path.exists("./Result/"):
            os.mkdir("./Result/")
        # [{'windows_stopwatch_time': 3931130, 'camera_stopwatch_time': 3930894, 'delay_time': 236}, {'windows_stopwatch_time': 3931209, 'camera_stopwatch_time': 3930972, 'delay_time': 237}]
        windowsList = []
        cameraList = []
        delayList = []
        for singleResult in data:
            windowsList.append(singleResult["windows_stopwatch_time"])
            cameraList.append(singleResult["camera_stopwatch_time"])
            delayList.append(singleResult["delay_time"])
        df = pd.DataFrame(
            {"windows stopwatch time": windowsList, "camera_stopwatch_time": cameraList, "delay_time": delayList})
        df.to_excel("./Result/{}_result_{}.xlsx".format(test_resolution, str(cur_time)))

    def cut_videoFrame(self, video_path, videoName):
        if not os.path.exists(video_path + videoName):
            os.mkdir(video_path + videoName)
        command = r"ffmpeg -i {}\{}.mp4 -q:v 1 -f image2 {}\{}\xxx_%05d.jpg".format(video_path, videoName, video_path,
                                                                                    videoName)
        os.system(command)


if __name__ == '__main__':
    videoName = "MJPEG1080P_NORMALMODE"
    video_path = "D:\PycharmProjects\pythonProject_seevision\windows_control\PerformanceTestScript\Sample\\"

    PT = PerformanceTestEnterance()
    PT.cut_videoFrame(video_path, videoName)
    result = []
    for imgPath in os.listdir(video_path + videoName):
        singleImagePath = video_path + videoName + "\\" + imgPath
        single_result = PT.DELAY_TEST_MAIN(singleImagePath)
        if len(result) >= 10:
            break
        if single_result is not None:
            result.append(single_result)
    print(result)
    PT.write_intoExcel(videoName, result)
