# coding = utf8
import json
import multiprocessing
import os
import re
import subprocess
import threading
import time
from time import sleep

import serial
from serial.tools.list_ports_windows import comports

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:stressTest.py
    @Author:十二点前要睡觉
    @Date:2022/2/25 9:52
"""

cur_time = time.strftime("%Y%m%d_%H%M%S")


class StreeTest:

    def __init__(self, com_id, baud_rate):
        """
        串口初始化函数，每台设备对应一个串口，初始化一个串口压测object
        self.serial_no在初始化获取对应串口设备的序列号后第一次进行赋值
        :param com_id:串口号
        :param baud_rate:波特率
        """
        self.com_id = com_id
        self.baud_rate = baud_rate
        self.port_obj = serial.Serial(self.com_id, baudrate=self.baud_rate)
        self.serial_no = ""

    def enterBootloaderMode(self):
        """
        设备进入BootLoader模式：
        1、通过串口发送输入root账号密码的指令
        2、通过串口刷入reboot-bootloader进入
        :return:返回设备进入BootLoader模式操作已完成
        """
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
        """
        通过串口发送账号密码进行串口通信授权
        :return:None
        """
        print("输入账号密码……")
        self.toTxt("输入账号密码……")
        self.port_obj.write("\r\n".encode("UTF-8"))
        self.port_obj.write("root\r\n".encode("UTF-8"))
        sleep(3)
        self.port_obj.write("bunengshuo\r\n".encode("UTF-8"))

    def reboot_device(self):
        """
        通过串口发送reboot指令进行设备重启
        :return:None
        """
        sleep(20)
        self.enterADPSD()
        self.enterADPSD()
        self.port_obj.write("reboot\r\n".encode("UTF-8"))
        sleep(20)
        self.enterADPSD()
        self.enterADPSD()

    def flashModuleUpdate(self, image_path):
        """
        固件刷写操作，通过fastboot指令将设备固件刷入，指定对应设备刷入，防止其他设备执行fastboot影响其他设备的xmos静默升级导致i2c接口丢失
        1、刷完后检测是否有对应字段上报，以判断下一步操作是否需要等待xmos静默升级
        2、xmos升级完成后，对设备进行重启使版本字段更新
        :param image_path:固件版本路径
        :return:返回当前固件刷写操作已完成
        """
        print("Start MODULE upgrade for serial : {}".format(self.serial_no))
        self.toTxt("Start MODULE upgrade for serial : {}".format(self.serial_no))
        subprocess.Popen("fastboot -s {} flash lk {}lk.bin".format(self.serial_no, image_path),
                         shell=True).communicate()
        subprocess.Popen("fastboot -s {} flash boot {}boot.img".format(self.serial_no, image_path),
                         shell=True).communicate()
        subprocess.Popen("fastboot -s {} flash system {}system.img".format(self.serial_no, image_path),
                         shell=True).communicate()
        subprocess.Popen("fastboot -s {} oem finish_upgrade".format(self.serial_no), shell=True).communicate()
        subprocess.Popen("fastboot -s {} reboot".format(self.serial_no), shell=True).communicate()
        print("MODULE upgrade done sleep 60s to wait!!!")
        self.toTxt("MODULE upgrade done sleep 60s to wait!!!")
        # 刷完339等20s系统启动后，再去读取specificfield
        fieldCheckR = self.check_SpecificField()
        print(fieldCheckR)
        self.toTxt(fieldCheckR)
        self.reboot_device()
        sleep(3)
        # sleep(30)
        return "Flash Module Update Done"

    def checkPortOpen(self):
        """
        检测串口通信是否处于打开的状态
        1、如果当前串口通信未打开，将串口打开，并输入账号密码授权
        2、如果已经是打开状态，也输入一次账号密码授权以防刷机操作那边授权失效
        :return:返回串口状态检测操作已完成
        """
        if not self.port_obj.is_open:
            self.port_obj.open()
            self.enterADPSD()
            return True
        else:
            self.enterADPSD()
            return True

    def getCurrentVersion(self):
        """
        获取当前模组固件的版本，此处因为没有API，所以通过获取Linux的版本来判断当前模组固件是否已经启动
        1、检测端口打开
        2、通过串口写入读取Linux版本指令
        3、判断是否模组已经启动完成
        :return:None
        """
        print("Begin getCurrentVersion")
        self.toTxt("Begin getCurrentVersion")
        if self.checkPortOpen():
            self.enterADPSD()
            while True:
                self.port_obj.write("uname -a\r\n".encode("UTF-8"))
                if self.port_obj.inWaiting() > 0:
                    data = str(self.port_obj.read_all())
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
    #                     data = str(self.port_obj.read_all())
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

    # def writeXmosUpgrade(self):
    #     print("Begin XMOS Upgrade")
    #     self.toTxt("Begin XMOS Upgrade")
    #     if self.checkPortOpen():
    #         self.port_obj.write(
    #             "dfu_i2c write_upgrade /customer/vendor/app_vf_stereo_base_i2c_i8o2_I2Sref_I2ScommOutputDOATX1J_24bit_V316dfu.bin\r\n".encode(
    #                 "UTF-8"))
    #         # while True:
    #         #     sleep(0.1)
    #         #     print("正在XMOS刷机……")
    #         #     if self.port_obj.inWaiting()>0:
    #         #         data = str(self.port_obj.read_all())
    #         #         print(data)
    #         #         if "done" in data:
    #         #             print("Xmos版本升级成功！")
    #         #             break
    #         print("正在XMOS刷机……")
    #         self.toTxt("正在XMOS刷机……")
    #         sleep(60)
    #         print("Xmos版本升级成功！")
    #         self.toTxt("Xmos版本升级成功！")

    def getXmosVersion(self):
        """
        获取Xmos模组的版本：
        1、通过串口发送读取xmos版本的指令
        2、循环读取直到对应版本上报数据接收到，版本刷机完成
        :return:返回当前读取到的xmos版本号
        """
        print("Begin XMOS version： getXmosVersion")
        self.toTxt("Begin XMOS version： getXmosVersion")
        if self.checkPortOpen():
            self.enterADPSD()
            while True:
                self.toTxt("正在获取当前XMOS版本……")
                print("正在获取当前XMOS版本……")
                self.port_obj.write(
                    "dfu_i2c read_version\r\n".encode(
                        "UTF-8"))
                if self.port_obj.inWaiting() > 0:
                    data = str(self.port_obj.read_all())
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
                    # 如果出现timeout的情况，重启设备，出现getXmoVersion
                    # elif "timed out" in data:
                    #     print("Happened timed out in get xmos version, need give to check!")
                    #     self.toTxt("Happened timed out in get xmos version, need give to check!")
                    #     self.enterBootloaderMode()
                    #     subprocess.Popen("fastboot -s {} reboot".format(self.serial_no), shell=True).communicate()
                    #     sleep(20)
                    #     self.enterADPSD()
                    #     continue

    def falsh_into_SpecificVersion(self, image_path):
        """
        指定对应版本刷写的过程定义函数
        1、启动Bootloader
        2、刷入固件
        3、将刷机结果写入文件
        :param image_path:刷入固件路径
        :return:None
        """
        bootloader_status = self.enterBootloaderMode()
        print(bootloader_status)
        self.toTxt(bootloader_status)
        flashMU = self.flashModuleUpdate(image_path)
        print(flashMU)
        self.toTxt(flashMU)
        self.getCurrentVersion()

    def toTxt(self, result):
        """
        结果写入函数：将每次的结果追加写入各自串口的结果文本中
        :param result:每次刷机后版本判断结果
        :return:None
        """
        try:
            with open("./【{}】Result.txt".format(self.port_obj.portstr), "a+") as f:
                f.write(result + "\n")
        except (AttributeError, TypeError) as ex:
            print("【Error need check, maybe not important】 : \r\n{}\r\n".format(str(ex)))
            f.write("【Error need check, maybe not important】 : \r\n{}\r\n".format(str(ex)))

    def check_SpecificField(self):
        """
        该函数用于判断当前xmos版本是否需要刷写，检测对应上报字段来进行判断
        1、检测端口开启
        2、持续获取字段并进行筛选
        3、如果是no need说明是无需升级无需等待，如果是firmware upgrade说明需要xmos静默升级需要等待70s
        :return:返回是否需要等待xmos静默升级
        """
        print("Get specific field")
        self.toTxt("Get specific field")
        if self.checkPortOpen():
            self.enterADPSD()
            while True:
                if self.port_obj.inWaiting() > 0:
                    field = str(self.port_obj.read_all())
                    print("正在Get specific field : [{}]……".format(field))
                    self.toTxt("正在Get specific field : [{}]……".format(field))
                    if "no need" in field:
                        print("xmos无需升级，等待20s后会进行reboot")
                        self.toTxt("xmos无需升级，等待20s后会进行reboot")
                        sleep(20)
                        return "结果获取完毕：xmos firmware no need for upgrade!!!"
                    elif "firmware upgrade" in field:
                        print("xmos需要升级，等待70s后会进行reboot")
                        self.toTxt("xmos需要升级，等待70s后会进行reboot")
                        sleep(70)
                        return "结果获取完毕：xmos firmware upgrade start!!!"
                    elif "timed out" in field:
                        continue

    def getFastboot_devices(self):
        """
        获取不同串口设备的唯一序列号
        通过fastboot devices获取当前所连接的设备的序列号数据信息（只有在bootloader模式的设备才能被获取到，因此逐个获取再与串口对应名称进行映射）
        :return:返回当前所有的序列号数据
        """
        sleep(5)
        devices_stream = os.popen("fastboot devices")
        devices = devices_stream.read()
        serial_no = re.findall("(.*)\tfastboot", devices)
        devices_stream.close()
        return serial_no

    def getSerial_no(self):
        """
        获取设备序列号并写入json文件过程函数
        1、设备进入bootloader模式
        2、获取当前设备序列号
        3、将设备退出bootloader模式
        :return:返回该设备序列号
        """
        enter_mode = self.enterBootloaderMode()
        self.toTxt(enter_mode)
        print(enter_mode)
        # self.serial_no = self.getFastboot_devices()[0]
        serialNo = self.getFastboot_devices()[0]
        # print("serial is: {}".format(self.serial_no))
        print("serial is: {}".format(serialNo))
        self.toTxt("serial is: {}".format(serialNo))
        subprocess.Popen("fastboot -s {} oem finish_upgrade".format(serialNo), shell=True).communicate()
        subprocess.Popen("fastboot -s {} reboot".format(serialNo), shell=True).communicate()
        sleep(20)
        return serialNo


def test_area(oldversion, newversion, st_obj, cycle_times, serialNo):
    """
    升降级刷机压力测试过程函数
    :param oldversion:旧版本路径
    :param newversion:新版本路径
    :param st_obj:串口对象
    :param cycle_times:测试次数
    :param serialNo:设备序列号
    :return:None
    """
    """
        1、先刷入旧Firmware版本，循环测试开始
    """
    image_path = oldversion
    st_obj.serial_no = serialNo
    st_obj.falsh_into_SpecificVersion(image_path)
    print("【{}】第一次旧设备刷机完成,即将开始刷机循环测试！".format(st_obj.serial_no))
    st_obj.toTxt("【{}】第一次旧设备刷机完成,即将开始刷机循环测试！".format(st_obj.serial_no))
    for i in range(cycle_times):
        print("第{}次升降级反复刷机从【Version: 3.1.6】->【Version: 3.1.7】测试".format(str(i + 1)))
        st_obj.toTxt("第{}次升降级反复刷机从【Version: 3.1.6】->【Version: 3.1.7】测试".format(str(i + 1)))
        # 下一步 xmos刷机流程，需要发送指令过去执行刷机操作，每次写入之前需要输入一次密码,xmos的固件奇哥暂时刷入到339的vendor里面了，但不是正式的提测固件，先验证dfu_i2c的功能在脚本压测正常
        # sbin/dfu_i2c -> write upgrade-> reboot-> read version
        # \\file.ad.seevision.cn\DailyBuild\sytj0101\sytj0101\20220226_172822_for_xmos_ota

        # 会自动升级到3.1.7,新版本Firmware刷入,自动输入xmos，339刷完等待60s即可xmos自动完成，获取版本对比
        """
            2、检测当前Xmos版本，如果是旧版本，则开始刷入新Firmware然后等待70sxmos自动升级完成
        """
        if st_obj.getXmosVersion() == "Version: 3.1.6":
            # 刷入newversion
            image_path = newversion
            st_obj.falsh_into_SpecificVersion(image_path)
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
            # st_obj.writeXmosUpgrade()
            print("Xmos version Flash done : to 3.1.6")
            st_obj.toTxt("Xmos version Flash done : to 3.1.6")
            if st_obj.getXmosVersion() == "Version: 3.1.6":
                print("B->A降级成功")
                st_obj.toTxt("Result：【第{}次测试: B->A降级成功】\n".format(str(i + 1)))
            # 需要执行刷机刷入Version3.1.6版本进行降级，旧版本Firmware刷入，需要手动执行刷入
    print("测试结束，请查看Result.txt查看结果")
    st_obj.toTxt("测试结束，请查看Result.txt查看结果")


# def log_area(st_obj):
#     print("Begin log process")
#     if not st_obj.port_obj.is_open:
#         st_obj.port_obj.open()
#         st_obj.enterADPSD()
#     while True:
#         try:
#             sleep(0.1)
#             if st_obj.port_obj.inWaiting() > 0:
#                 try:
#                     data = str(st_obj.port_obj.readline())
#                 except (AttributeError, TypeError):
#                     data = "empty"
#                 if not os.path.exists("./log/"):
#                     os.mkdir("./log/")
#                 with open("./log/{}【{}】_serialLog.log".format(st_obj.port_obj.portstr, cur_time), "a+") as logF:
#                     logF.write(data + "\n")
#             else:
#                 continue
#         except SerialException:
#             continue


def serial2COM(ports):
    """
    串口与序列号映射并写入json文件函数
    :param ports:当前串口号
    :return:json文件路径
    """
    # Warning !
    global st_obj
    serialDict = {}
    for port in ports:
        print("正在获取{}端口的序列号……".format(port))
        st_obj = StreeTest(port, 115200)
        serialNo = st_obj.getSerial_no()
        serialDict[port] = serialNo
        print("当前端口{}的序列号是：{}".format(port, serialDict[port]))
        st_obj.toTxt("当前端口{}的序列号是：{}".format(port, serialDict[port]))
        st_obj.port_obj.close()
    f_path = "./serialNos.json"
    with open(f_path, "w") as f:
        print("正在写入序列号……")
        st_obj.toTxt("正在写入序列号……")
        json.dump(serialDict, f)

    return f_path


def readJson(f_path):
    """
    json文件读取函数
    :param f_path:json文件路径
    :return:返回字典形式的信息
    """
    with open(f_path, "r") as f:
        # print("序列号列表获取")
        serialDict = json.load(f)
        # print("序列号列表：{}".format(serialDict))
    return serialDict


def initCOMTest(comNumber, serialNo):
    """
    测试前初始化区域
    :param comNumber:串口号
    :param serialNo:序列号
    :return:None
    """
    # st_obj = StreeTest("COM3", 115200)
    st_obj = StreeTest(comNumber, 115200)
    cycle_times = 2000
    # 需要先将每台设备的序列号存下来存到self.serial_no中
    # 需要增加映射，在测试前，先把所有的一起遍历一遍并存下对应的端口和序列号来进行设置

    """
        此处通过com获取到对应的serialno
    """

    """
        刷316,检测到done\Version: 3.1.6
        重启一次,需检测"未升级xmos"
        刷317,检测到done\Version: 3.1.7
        重启一次,需检测"未升级xmos"
    """
    oldversion = "./release_A/"
    newversion = "./release_B/"
    t1 = threading.Thread(target=test_area, args=(oldversion, newversion, st_obj, cycle_times, serialNo,))
    t1.start()
    sleep(5)


if __name__ == '__main__':
    """
        Main函数，给每台设备分配一个独立进程，完全隔离开：目的在通过线程对不同设备的执行测试过程进行控制，互相不干扰又能够同时执行，提高测试效率
    """
    ports = []
    for port in list(comports()):
        if "Silicon Labs CP210x USB to UART Bridge" in str(port):
            current_port = re.findall("\((.*)\)", str(port))[0]
            ports.append(current_port)
    print(ports)
    f_path = serial2COM(ports)
    # f_path = "./serialNos.json"
    serialDict = readJson(f_path)
    test_pool = multiprocessing.Pool(len(ports))
    for coms in ports:
        print("{}端口对应序列号为：{}".format(coms, serialDict[coms]))
        # 每隔150s，是一台机器从刷339到xmos完成的时间，间隔开，这样就不会因为fastboot导致另外一台的339可能被中断的问题
        test_pool.apply_async(func=initCOMTest, args=(coms, serialDict[coms],))
        sleep(40)
    test_pool.close()
    test_pool.join()
    # st_obj = StreeTest("COM35", 115200)
    # print(st_obj.getXmosVersion())
