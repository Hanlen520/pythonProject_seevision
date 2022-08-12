# coding = utf8
import os
import re
import time

from uiautomation_win import openPotplayer, enterDeviceSettings, switchResolution, closePotplayer

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:catch_storage_usage.py
    @Author:十二点前要睡觉
    @Date:2022/7/24 18:34
"""

import serial
from serial.tools.list_ports_windows import comports


class CatchStorageUsage:

    def __init__(self, com_id, baud_rate):
        self.com_id = com_id
        self.baud_rate = baud_rate
        self.port_obj = serial.Serial(self.com_id, self.baud_rate)

    def sendPortCommand(self, command):
        self.port_obj.write(command.encode("UTF-8"))

    def readData(self):
        if self.port_obj.inWaiting() > 0:
            result = self.port_obj.read_all()
            # result = str(self.port_obj.read(16))
            print(result)
            return result

    def toTxt(self, result, resolution):
        try:
            with open("./[{}][{}]CatchStorageUsageResult.txt".format(resolution, self.port_obj.portstr), "a+") as f:
                f.write(result + "\n")
        except (AttributeError, TypeError) as ex:
            print("【Error need check, maybe not important】 : \r\n{}\r\n".format(str(ex)))
            f.write("【Error need check, maybe not important】 : \r\n{}\r\n".format(str(ex)))

    def login_root(self):
        self.sendPortCommand("root\r\n")
        time.sleep(1)
        self.sendPortCommand("bunengshuo\r\n")


def getAllPorts():
    ports = []
    for port in list(comports()):
        if "Silicon Labs CP210x USB to UART Bridge" or "USB Serial Port" in str(port):
            current_port = re.findall("\((.*)\)", str(port))[0]
            ports.append(current_port)
    return ports


if __name__ == '__main__':
    catch_gap_time = 300
    print("开始持续抓取内存使用情况，自定义抓取间隔时间，当前间隔时间为【{}】秒".format(catch_gap_time))
    ports = getAllPorts()
    print(ports)
    csu = CatchStorageUsage(ports[1], "115200")
    csu.login_root()
    # change the resolution as your own project's behaviour.
    TEST_RESOLUTIONS = ["MJPG 3840×2160P 30(P 16:9)", "MJPG 1920×1080P 30(P 16:9)",
                        "MJPG 1280×720P 30(P 16:9)", "H264 3840×2160P 30(P 16:9)",
                        "YUY2 960×540P 30(P 16:9)"]
    for resolution in TEST_RESOLUTIONS:
        potplayerPath = "D:\PotPlayer\PotPlayerMini64.exe"
        openPotplayer(potplayer_path=potplayerPath)
        enterDeviceSettings()
        switchResolution(resolution)
        for i in range(1, 7):
            resolution_name = resolution.strip().replace(" ", "_").replace(":", "_")
            csu.toTxt("第【{}】轮测试数据：".format(i), resolution_name)
            csu.sendPortCommand("cat /proc/mi_modules/mi_sys_mma/mma_heap_name0\r\n")
            time.sleep(1)
            mma_heap_name0_data = csu.readData()
            csu.toTxt("【Data 1】 mma_heap_name0_data:\n {}".format(mma_heap_name0_data), resolution_name)

            csu.sendPortCommand("cat /proc/meminfo\r\n")
            time.sleep(1)
            meminfo_data = csu.readData()
            csu.toTxt("【Data 2】 meminfo_data:\n {}".format(meminfo_data), resolution_name)
            time.sleep(catch_gap_time)
        closePotplayer()
