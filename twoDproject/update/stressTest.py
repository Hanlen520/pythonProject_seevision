# coding = utf8
import multiprocessing
import os
import re
import subprocess
import threading
import time
from time import sleep

import serial
from serial import SerialException
from serial.tools.list_ports_windows import comports

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
        self.serial_no = ""

    def enterBootloaderMode(self):
        if self.checkPortOpen():
            print("进入BootLoader模式 - port open,current port info:[{} - {}]".format(self.port_obj.portstr,
                                                                                  self.port_obj.baudrate))
            self.toTxt("进入BootLoader模式 - port open,current port info:[{} - {}]".format(self.port_obj.portstr,
                                                                                       self.port_obj.baudrate))
            self.enterADPSD()
            self.port_obj.write("reboot-bootloader\r\n".encode("UTF-8"))
            # self.port_obj.close()
            sleep(3)
            return "boot loader done"
        else:
            self.toTxt("port not open")
            print("port not open")

    def enterADPSD(self):
        print("输入账号密码……")
        self.toTxt("输入账号密码……")
        self.port_obj.write("\r\n".encode("UTF-8"))
        self.port_obj.write("root\r\n".encode("UTF-8"))
        sleep(3)
        self.port_obj.write("bunengshuo\r\n".encode("UTF-8"))

    def flashModuleUpdate(self, image_path):
        print("Start MODULE upgrade")
        self.toTxt("Start MODULE upgrade")
        subprocess.Popen("fastboot -s {} flash lk {}lk.bin".format(self.serial_no, image_path),
                         shell=True).communicate()
        subprocess.Popen("fastboot -s {} flash boot {}boot.img".format(self.serial_no, image_path),
                         shell=True).communicate()
        subprocess.Popen("fastboot -s {} flash system {}system.img".format(self.serial_no, image_path),
                         shell=True).communicate()
        subprocess.Popen("fastboot -s {} oem finish_upgrade".format(self.serial_no), shell=True).communicate()
        subprocess.Popen("fastboot -s {} reboot".format(self.serial_no), shell=True).communicate()
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
                    # self.toTxt(data)
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
            self.port_obj.write(
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
                self.port_obj.write(
                    "dfu_i2c read_version\r\n".encode(
                        "UTF-8"))
                if self.port_obj.inWaiting() > 0:
                    data = str(self.port_obj.readline())
                    print(data)
                    # self.toTxt(data)
                    if "Version: 3.1.7" in data:
                        print("Xmos版本升级成功，版本匹配正确：Version: 3.1.7, 开始降级刷机到Version 3.1.6！")
                        self.toTxt("Xmos版本升级成功，版本匹配正确：Version: 3.1.7, 开始降级刷机到Version 3.1.6！")
                        return "Version: 3.1.7"
                    elif "Version: 3.1.6" in data:
                        print("Xmos版本升级成功，版本匹配正确：Version: 3.1.6, 开始降升级刷机到Version 3.1.7！")
                        self.toTxt("Xmos版本升级成功，版本匹配正确：Version: 3.1.6, 开始降升级刷机到Version 3.1.7！")
                        return "Version: 3.1.6"

    def falsh_into_SpecificVersion(self, image_path):
        bootloader_status = self.enterBootloaderMode()
        print(bootloader_status)
        self.toTxt(bootloader_status)
        flashMU = self.flashModuleUpdate(image_path)
        print(flashMU)
        self.toTxt(flashMU)
        self.getCurrentVersion()

    # def check_reboot_version(self):
    #     self.port_obj.write("reboot\r\n".encode("UTF-8"))
    #     sleep(60)

    def toTxt(self, result):
        try:
            with open("./【{}】Result.txt".format(self.port_obj.portstr), "a+") as f:
                f.write(result + "\n")
        except (AttributeError, TypeError):
            pass

    def check_SpecificField(self):
        print("Get specific field")
        self.toTxt("Get specific field")
        if self.checkPortOpen():
            while True:
                if self.port_obj.inWaiting() > 0:
                    field = str(self.port_obj.readline())
                    print("正在Get specific field : [{}]……".format(field))
                    # self.toTxt("正在Get specific field : [{}]……".format(field))
                    if "no need" in field:
                        return "结果获取完毕：xmos firmware no need for upgrade!!!"
                    elif "upgrade start" in field:
                        return "结果获取完毕：xmos firmware upgrade start!!!"
                    elif "timed out" in field:
                        return

    def getFastboot_devices(self):
        sleep(5)
        devices_stream = os.popen("fastboot devices")
        devices = devices_stream.read()
        serial_no = re.findall("(.*)\tfastboot", devices)
        devices_stream.close()
        return serial_no

    def setSerial_no(self):
        print(self.enterBootloaderMode())
        self.serial_no = self.getFastboot_devices()[0]
        print("serial is: {}".format(self.serial_no))
        subprocess.Popen("fastboot -s {} oem finish_upgrade".format(self.serial_no), shell=True).communicate()
        subprocess.Popen("fastboot -s {} reboot".format(self.serial_no), shell=True).communicate()
        sleep(20)


def test_area(oldversion, newversion, st_obj, cycle_times):
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
                st_obj.toTxt("Result：【第{}次测试: A->B升级成功】\n".format(str(i + 1)))
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
                st_obj.toTxt("Result：【第{}次测试: B->A降级成功】\n".format(str(i + 1)))
            # 需要执行刷机刷入Version3.1.6版本进行降级，旧版本Firmware刷入，需要手动执行刷入
    print("测试结束，请查看Result.txt查看结果")
    st_obj.toTxt("测试结束，请查看Result.txt查看结果")


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
                with open("./log/{}【{}】_serialLog.log".format(st_obj.port_obj.portstr, cur_time), "a+") as logF:
                    logF.write(data + "\n")
            else:
                continue
        except SerialException:
            continue


def initCOMTest(comNumber):
    # st_obj = StreeTest("COM3", 115200)
    st_obj = StreeTest(comNumber, 115200)
    cycle_times = 2
    # 需要先将每台设备的序列号存下来存到self.serial_no中
    需要增加映射，在测试前，先把所有的一起遍历一遍并存下对应的端口和序列号来进行设置
    st_obj.setSerial_no()
    """
        刷316,检测到done\Version: 3.1.6
        重启一次,需检测"未升级xmos"
        刷317,检测到done\Version: 3.1.7
        重启一次,需检测"未升级xmos"
    """
    oldversion = "./release_A/"
    newversion = "./release_B/"
    t1 = threading.Thread(target=test_area, args=(oldversion, newversion, st_obj, cycle_times,))
    t2 = threading.Thread(target=log_area, args=(st_obj,))
    t1.start()
    # 有缓冲了再启动log线程去获取写入log，保证log不会缺失，log机制是有log就存，没有就等
    sleep(10)
    t2.start()


if __name__ == '__main__':
    ports = []
    for port in list(comports()):
        if "Silicon Labs CP210x USB to UART Bridge" in str(port):
            current_port = re.findall("\((.*)\)", str(port))[0]
            ports.append(current_port)
    print(ports)
    test_pool = multiprocessing.Pool(len(ports))
    for coms in ports:
        # 每隔150s，是一台机器从刷339到xmos完成的时间，间隔开，这样就不会因为fastboot导致另外一台的339可能被中断的问题
        test_pool.apply_async(func=initCOMTest, args=(coms,))
        sleep(30)
    test_pool.close()
    test_pool.join()
