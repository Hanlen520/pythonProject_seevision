# coding = utf8
import os
import re
import time

import serial
from serial.tools.list_ports_windows import comports

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:captureStressTest.py
    @Author:十二点前要睡觉
    @Date:2022/5/10 11:34
"""

COMPORT_COMMAND_TAKE_PICTURE_REQUEST = [0xFE, 0x55, 0x01, 0x00, 0x04, 0x02, 0x02, 0x14, 0x00, 0x03, 0x03, 0x36, 0x00,
                                        0x00,
                                        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                        0x00,
                                        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                        0x00,
                                        0x00,
                                        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                        0x00,
                                        0x00, 0x00, 0x00, 0x6D, 0x54]
COMPORT_COMMAND_STOP_CONTINOUS_REPORT_REQUEST = [0xFE, 0x55, 0x01, 0x00, 0x04, 0x02, 0x02, 0x14, 0x01, 0xFE, 0x01,
                                                 0x02, 0x01,
                                                 0x00, 0x2C, 0xAA]


class CaptureStressTest:
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

    def sendPortCommand(self, command):
        self.port_obj.write(command)
        # result = self.port_obj.read(13)
        # if self.port_obj.inWaiting() > 0:
        #     result = self.port_obj.read_all()
        #     print(result)

    def readData(self):
        if self.port_obj.inWaiting() > 0:
            # result = self.port_obj.read_all()
            result = str(self.port_obj.read(16))
            print(result)
            return result

    def toTxt(self, result):
        try:
            with open("./[{}]Result.txt".format(self.port_obj.portstr), "a+") as f:
                f.write(result + "\n")
        except (AttributeError, TypeError) as ex:
            print("【Error need check, maybe not important】 : \r\n{}\r\n".format(str(ex)))
            f.write("【Error need check, maybe not important】 : \r\n{}\r\n".format(str(ex)))


def getAllPorts():
    ports = []
    for port in list(comports()):
        if "Silicon Labs CP210x USB to UART Bridge" in str(port):
            current_port = re.findall("\((.*)\)", str(port))[0]
            ports.append(current_port)
    return ports


if __name__ == '__main__':
    print("等待10s机器上电并初始化完成，再进行测试，请稍等，会自行结束等待……")
    time.sleep(10)
    ports = getAllPorts()
    print(ports)
    cst = CaptureStressTest(ports[0], "115200")
    i = 1
    success_count = 0
    fail_count = 0


    """
        测试次数
    """
    test_count = 1000

    for i in range(test_count):
        print("第{}次测试……".format(i + 1))
        cst.toTxt("第{}次测试……".format(i + 1))
        cst.sendPortCommand(COMPORT_COMMAND_STOP_CONTINOUS_REPORT_REQUEST)
        time.sleep(1)
        if cst.readData() == r"b'\xfeU\x01\x01\x02\x14\x04\x02\x01\xfe\x01\x02\x00\x00\x89\xa5'":
            print("串口持续数据上报关闭成功……")
            cst.toTxt("串口持续数据上报关闭成功……")
        time.sleep(1)
        cst.sendPortCommand(COMPORT_COMMAND_TAKE_PICTURE_REQUEST)
        time.sleep(1)
        if cst.readData() == r"b'\xfeU\x01\x01\x02\x14\x04\x02\x00\x03\x036\x00\x00\x00\x00'":
            print("拍照成功……")
            cst.toTxt("拍照成功……")
            success_count += 1
        else:
            fail_count += 1
        time.sleep(6)
        cst.port_obj.read_all()
        print("\n\n")
        cst.toTxt("\n\n")
    print("测试结束，总计测试[{}]次，成功[{}]次，失败[{}]次，请检查SD卡中对应照片的数量，以及照片的拍摄情况是否正常".format(i + 1, success_count, fail_count))
    cst.toTxt("测试结束，总计测试[{}]次，成功[{}]次，失败[{}]次，请检查SD卡中对应照片的数量，以及照片的拍摄情况是否正常".format(i + 1, success_count, fail_count))
