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
            self.toTxt("进入BootLoader模式 - port open,current port info:[{} - {}]".format(self.port_obj.portstr,
                                                                                       self.port_obj.baudrate))
            self.enterADPSD()
            self.port_obj.write("reboot-bootloader\r\n".encode("UTF-8"))
            self.port_obj.close()
            sleep(3)
            return "Enter Bootloader Done"
        else:
            self.toTxt("port not open")
            print("port not open")

    def enterADPSD(self):
        print("输入账号密码……")
        self.toTxt("输入账号密码……")
        self.port_obj.write("root\r\n".encode("UTF-8"))
        sleep(3)
        self.port_obj.write("bunengshuo\r\n".encode("UTF-8"))

    def flashModuleUpdate(self, image_path):
        print("Start MODULE upgrade")
        self.toTxt("Start MODULE upgrade")
        subprocess.Popen("fastboot flash lk {}lk.bin".format(image_path), shell=True).communicate()
        subprocess.Popen("fastboot flash boot {}boot.img".format(image_path), shell=True).communicate()
        subprocess.Popen("fastboot flash system {}system.img".format(image_path), shell=True).communicate()
        subprocess.Popen("fastboot oem finish_upgrade", shell=True).communicate()
        subprocess.Popen("fastboot reboot", shell=True).communicate()
        print("MODULE upgrade done !!!")
        self.toTxt("MODULE upgrade done !!!")
        fieldCheckR = self.check_SpecificField()
        self.toTxt(fieldCheckR)
        print(fieldCheckR)
        # sleep(30)
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
        self.toTxt("Begin getCurrentVersion")
        if self.checkPortOpen():
            while True:
                sleep(0.1)
                self.port_obj.write("uname -a\r\n".encode("UTF-8"))
                if self.port_obj.inWaiting() > 0:
                    data = str(self.port_obj.readline())
                    self.toTxt(data)
                    print(data)
                    if "Linux" in data:
                        print("339版本刷机成功！")
                        self.toTxt("339版本刷机成功！")
                        break
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
        self.toTxt("Begin XMOS Upgrade")
        if self.checkPortOpen():
            st_obj.port_obj.write(
                "dfu_i2c write_upgrade /customer/vendor/app_vf_stereo_base_i2c_i8o2_I2Sref_I2ScommOutputDOATX1J_24bit_V316dfu.bin\r\n".encode(
                    "UTF-8"))
            # while True:
            #     sleep(0.1)
            #     print("正在XMOS刷机……")
            #     if self.port_obj.inWaiting()>0:
            #         data = str(self.port_obj.readline())
            #         print(data)
            #         if "done" in data:
            #             print("Xmos版本升级成功！")
            #             break
            print("正在XMOS刷机……")
            self.toTxt("正在XMOS刷机……")
            sleep(60)
            print("Xmos版本升级成功！")
            self.toTxt("Xmos版本升级成功！")

    def getXmosVersion(self):
        print("Begin XMOS version： getXmosVersion")
        self.toTxt("Begin XMOS version： getXmosVersion")
        if self.checkPortOpen():
            while True:
                sleep(0.1)
                self.toTxt("正在获取当前XMOS版本……")
                print("正在获取当前XMOS版本……")
                st_obj.port_obj.write(
                    "dfu_i2c read_version\r\n".encode(
                        "UTF-8"))
                if self.port_obj.inWaiting() > 0:
                    data = str(self.port_obj.readline())
                    print(data)
                    self.toTxt(data)
                    if "Version: 3.1.7" in data:
                        print("Xmos版本升级成功，版本匹配正确：Version: 3.1.7, 开始降级刷机到Version 3.1.6！")
                        self.toTxt("Xmos版本升级成功，版本匹配正确：Version: 3.1.7, 开始降级刷机到Version 3.1.6！")
                        return "Version: 3.1.7"
                    elif "Version: 3.1.6" in data:
                        print("Xmos版本升级成功，版本匹配正确：Version: 3.1.6, 开始降升级刷机到Version 3.1.7！")
                        self.toTxt("Xmos版本升级成功，版本匹配正确：Version: 3.1.6, 开始降升级刷机到Version 3.1.7！")
                        return "Version: 3.1.6"

    def falsh_into_SpecificVersion(self, image_path):
        enterBootLM = self.enterBootloaderMode()
        print(enterBootLM)
        self.toTxt(enterBootLM)
        flashMU = self.flashModuleUpdate(image_path)
        print(flashMU)
        self.toTxt(flashMU)
        self.getCurrentVersion()

    # def check_reboot_version(self):
    #     self.port_obj.write("reboot\r\n".encode("UTF-8"))
    #     sleep(60)

    def toTxt(self, result):
        with open("./Result.txt", "a+") as f:
            f.write(result + "\n")

    def check_SpecificField(self):
        print("Get specific field")
        self.toTxt("Get specific field")
        if self.checkPortOpen():
            while True:
                if self.port_obj.inWaiting() > 0:
                    field = str(self.port_obj.readline())
                    print("正在Get specific field : [{}]……".format(field))
                    self.toTxt("正在Get specific field : [{}]……".format(field))
                    if "no need" in field:
                        return "结果获取完毕：xmos firmware no need for upgrade!!!"
                    elif "upgrade start" in field:
                        return "结果获取完毕：xmos firmware upgrade start!!!"


def test_area():
    """
        1、先刷入旧Firmware版本，循环测试开始
    """
    image_path = oldversion
    st_obj.falsh_into_SpecificVersion(image_path)
    for i in range(cycle_times):
        print("第{}次升降级反复刷机从【Version: 3.1.6】->【Version: 3.1.7】测试".format(str(i + 1)))
        st_obj.toTxt("第{}次升降级反复刷机从【Version: 3.1.6】->【Version: 3.1.7】测试".format(str(i + 1)))
        # 下一步 xmos刷机流程，需要发送指令过去执行刷机操作，每次写入之前需要输入一次密码,xmos的固件奇哥暂时刷入到339的vendor里面了，但不是正式的提测固件，先验证dfu_i2c的功能在脚本压测正常
        # sbin/dfu_i2c -> write upgrade-> reboot-> read version
        # \\file.ad.seevision.cn\DailyBuild\sytj0101\sytj0101\20220226_172822_for_xmos_ota

        # 会自动升级到3.1.7,新版本Firmware刷入,自动输入xmos，339刷完等待60s即可xmos自动完成，获取版本对比
        """
            2、检测当前Xmos版本，如果是旧版本，则开始刷入新Firmware然后等待60sxmos自动升级完成
        """
        if st_obj.getXmosVersion() == "Version: 3.1.6":
            # 刷入newversion
            image_path = newversion
            st_obj.falsh_into_SpecificVersion(image_path)
            sleep(60)
            print("Xmos version Flash done : to 3.1.7")
            st_obj.toTxt("Xmos version Flash done : to 3.1.7")
            if st_obj.getXmosVersion() == "Version: 3.1.7":
                print("A->B升级成功")
                st_obj.toTxt("第{}次测试: A->B升级成功".format(str(i + 1)))
        else:
            """
                3、检测当前Xmos版本，如果是新版本，则开始刷入旧Firmware然后手动刷入Xmos旧版本等待降级完成
            """
            image_path = oldversion
            st_obj.falsh_into_SpecificVersion(image_path)
            sleep(60)
            # st_obj.writeXmosUpgrade()
            print("Xmos version Flash done : to 3.1.6")
            st_obj.toTxt("Xmos version Flash done : to 3.1.6")
            if st_obj.getXmosVersion() == "Version: 3.1.6":
                print("B->A降级成功")
                st_obj.toTxt("第{}次测试: B->A降级成功".format(str(i + 1)))
            # 需要执行刷机刷入Version3.1.6版本进行降级，旧版本Firmware刷入，需要手动执行刷入


def log_area(st_obj):
    print("Begin log process")
    if not st_obj.port_obj.is_open:
        st_obj.port_obj.open()
        st_obj.enterADPSD()
    while True:
        try:
            sleep(0.1)
            if st_obj.port_obj.inWaiting() > 0:
                try:
                    data = str(st_obj.port_obj.readline())
                except (AttributeError, TypeError):
                    data = "empty"
                if not os.path.exists("./log/"):
                    os.mkdir("./log/")
                with open("./log/{}_serialLog.log".format(cur_time), "a+") as logF:
                    logF.write(data + "\n")
            else:
                continue
        except SerialException:
            continue


if __name__ == '__main__':
    st_obj = StreeTest("COM3", 115200)
    cycle_times = 10
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
    # 最好的方式还是，关闭log线程，因为线程会两边获取导致部分数据不全，关闭log线程，只有test运行，然后输出内容重定向到文件中即可，tail实时查看输出内容
    # 从A版本升级到B版本
    # 如果当前是316版本，就执行升级到317版本
    # 如果当前是317版本，就执行刷机到316版本

    # A版本:fw version 316
    # B版本:fw version 317
    """
        刷316,检测到done\Version: 3.1.6
        重启一次,需检测"未升级xmos"
        刷317,检测到done\Version: 3.1.7
        重启一次,需检测"未升级xmos"
    """
    oldversion = "./release_A/"
    newversion = "./release_B/"
    t1 = threading.Thread(target=test_area)
    t2 = threading.Thread(target=log_area, args=(st_obj,))
    t1.start()
    # 有缓冲了再启动log线程去获取写入log，保证log不会缺失，log机制是有log就存，没有就等
    sleep(10)
    t2.start()
