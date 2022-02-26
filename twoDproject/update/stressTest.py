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

    def writeXmosUpgrade(self):
        print("Begin XMOS Upgrade")
        if self.checkPortOpen():
            st_obj.port_obj.write(
                "dfu_i2c write_upgrade /customer/vendor/app_vf_stereo_base_i2c_i8o2_I2Sref_I2ScommOutputDOATX1J_24bit_V316dfu.bin\r\n".encode(
                    "UTF-8"))
            while True:
                sleep(1)
                print("正在XMOS刷机……")
                data = str(self.port_obj.readline())
                print(data)
                if "done" in data:
                    print("Xmos版本升级成功！")
                    break
            sleep(0.5)

    def getXmosVersion(self):
        print("Begin XMOS Upgrade getXmosVersion")
        if self.checkPortOpen():
            while True:
                st_obj.port_obj.write(
                    "dfu_i2c read_version\r\n".encode(
                        "UTF-8"))
                sleep(1)
                print("正在获取XMOS版本……")
                data = str(self.port_obj.readline())
                print(data)
                if "Version: 3.1.6" in data:
                    print("Xmos版本升级成功，版本匹配正确：Version: 3.1.6！")
                    break
            sleep(0.5)


def test_area():
    for i in range(cycle_times):
        print("第{}次升级测试".format(str(i + 1)))
        print(st_obj.enterBootloaderMode())
        print(st_obj.flashModuleUpdate(image_path))
        st_obj.getCurrentVersion()

        # 下一步 xmos刷机流程，需要发送指令过去执行刷机操作，每次写入之前需要输入一次密码,xmos的固件奇哥暂时刷入到339的vendor里面了，但不是正式的提测固件，先验证dfu_i2c的功能在脚本压测正常
        # sbin/dfu_i2c -> write upgrade-> reboot-> read version
        # \\file.ad.seevision.cn\DailyBuild\sytj0101\sytj0101\20220226_172822_for_xmos_ota

        st_obj.writeXmosUpgrade()
        st_obj.getXmosVersion()


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
                except (AttributeError, TypeError):
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
    cycle_times = 321
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
    # 有缓冲了再启动log线程去获取写入log，保证log不会缺失，log机制是有log就存，没有就等
    sleep(10)
    t2.start()
