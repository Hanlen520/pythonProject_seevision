# coding = utf8
import os
import subprocess
import threading
import time
from time import sleep

import serial
from serial import SerialException

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:stressTest.py
    @Author:十二点前要睡觉
    @Date:2022/2/25 9:52
"""

"""
    脚本执行流程：
    设备连接串口线 + USB线
    1、获取到当前连接的设备的COM端口号，通过COM + baud rate控制对应的端口 -- 拿到该设备的连接对象 ->进入BootLoader模式
    2、fastboot进行刷机 -- 等待结束
    3、step2完成后，对XMOS进行刷机->等待刷机结束->本次刷机流程结束
"""

cur_time = time.strftime("%Y%m%d_%H%M%S")


class StreeTest:

    def __init__(self, com_id, baud_rate):
        self.com_id = com_id
        self.baud_rate = baud_rate
        self.port_obj = serial.Serial(self.com_id, baudrate=self.baud_rate)

    def enterBootloaderMode(self):
        if self.checkPortOpen():
            print("进入BootLoader模式 - port open,current port info:[{} - {}]".format(self.port_obj.portstr,
                                                                                  self.port_obj.baudrate))
            self.enterADPSD()
            self.port_obj.write("reboot-bootloader\r\n".encode("UTF-8"))
            self.port_obj.close()
            sleep(3)
            return "Enter Bootloader Done"
        else:
            print("port not open")

    def enterADPSD(self):
        print("输入账号密码……")
        self.port_obj.write("root\r\n".encode("UTF-8"))
        sleep(3)
        self.port_obj.write("bunengshuo\r\n".encode("UTF-8"))
        # self.port_obj.write("\r\n".encode("UTF-8"))

    def flashModuleUpdate(self, image_path):
        print("Start MODULE upgrade")
        subprocess.Popen("fastboot flash lk {}lk.bin".format(image_path), shell=True).communicate()
        subprocess.Popen("fastboot flash boot {}boot.img".format(image_path), shell=True).communicate()
        subprocess.Popen("fastboot flash system {}system.img".format(image_path), shell=True).communicate()
        subprocess.Popen("fastboot oem finish_upgrade", shell=True).communicate()
        subprocess.Popen("fastboot reboot", shell=True).communicate()
        print("MODULE upgrade done !!!")
        sleep(30)
        return "Flash Module Update Done"

    def checkPortOpen(self):
        if not self.port_obj.is_open:
            self.port_obj.open()
            self.enterADPSD()
            return True
        else:
            self.enterADPSD()
            return True

    def getCurrentVersion(self):
        print("Begin getCurrentVersion")
        if self.checkPortOpen():
            while True:
                # self.enterADPSD()
                sleep(1)
                self.port_obj.write("uname -a\r\n".encode("UTF-8"))
                data = str(self.port_obj.readline())
                print(data)
                if "Linux" in data:
                    print("版本升级成功！")
                    break
            self.port_obj.write("ls -l\r\n".encode("UTF-8"))
            sleep(0.5)

    # def log_process(self):
    #     print("Begin log process")
    #     if self.checkPortOpen():
    #         # while self.port_obj.inWaiting() > 0:
    #         while True:
    #             if self.port_obj.inWaiting() > 0:
    #                 sleep(0.1)
    #                 try:
    #                     data = str(self.port_obj.readline())
    #                 except AttributeError:
    #                     data = "empty"
    #                 if not os.path.exists("./log/"):
    #                     os.mkdir("./log/")
    #                 with open("./log/{}_serialLog.log".format(cur_time), "a+") as logF:
    #                     logF.write(data + "\n")
    #             else:
    #                 break
    #     else:
    #         print("NOK")


def test_area():
    for i in range(cycle_times):
        print("第{}次升级测试".format(str(i + 1)))
        print(st_obj.enterBootloaderMode())
        print(st_obj.flashModuleUpdate(image_path))
        st_obj.getCurrentVersion()


def log_area(st_obj):
    print("Begin log process")
    if not st_obj.port_obj.is_open:
        st_obj.port_obj.open()
        st_obj.enterADPSD()
    while True:
        try:
            if st_obj.port_obj.inWaiting() > 0:
                sleep(0.1)
                try:
                    data = str(st_obj.port_obj.readline())
                except AttributeError:
                    data = "empty"
                if not os.path.exists("./log/"):
                    os.mkdir("./log/")
                with open("./log/{}_serialLog.log".format(cur_time), "a+") as logF:
                    logF.write(data + "\n")
            else:
                sleep(1)
                continue
        except SerialException:
            continue


if __name__ == '__main__':
    image_path = "./release_images/"
    st_obj = StreeTest("COM3", 115200)
    cycle_times = 100
    # for i in range(cycle_times):
    #     try:
    #         print("第{}次升级测试".format(str(i + 1)))
    #         print(st_obj.enterBootloaderMode())
    #         print(st_obj.flashModuleUpdate(image_path))
    #         st_obj.getCurrentVersion()
    #     except Exception:
    #         pass
    #     finally:
    #         st_obj.log_process()
    t1 = threading.Thread(target=test_area)
    t2 = threading.Thread(target=log_area, args=(st_obj,))
    t1.start()
    sleep(10)
    t2.start()
