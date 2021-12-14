# coding = utf8
import os

os.path.abspath(".")
"""
    @Project:PycharmProjects
    @File:serialControl.py
    @Author:十二点前要睡觉
    @Date:2021/12/14 10:11
"""

from serial import SerialException

import serial
from time import sleep

com_id = "COM22"


class SerialSwitch(object):

    def __init__(self, com_id):
        self.s_obj = serial.Serial(com_id, baudrate=9600)

    def switch_pin1_on(self):
        self.s_obj.write([0xFE, 0x05, 0x00, 0x00, 0xFF, 0x00, 0x98, 0x35])
        print(self.s_obj.readall())

    def switch_pin1_off(self):
        self.s_obj.write([0xFE, 0x05, 0x00, 0x00, 0x00, 0x00, 0xD9, 0xC5])
        print(self.s_obj.readall())

    def check_all_status(self):
        self.s_obj.write([0xFE, 0x01, 0x00, 0x00, 0x00, 0x10, 0x29, 0xC9])
        print(self.s_obj.readall())

    def close(self):
        self.s_obj.close()


if __name__ == "__main__":
    """
        Tip:Serial comport deliver in and Operation wait
    """
    try:
        switch_obj = SerialSwitch(com_id)
        for i in range(10):
            print("Begin relay power on/off test")
            switch_obj.switch_pin1_on()
            sleep(1)
            switch_obj.switch_pin1_off()
            sleep(1)
    except SerialException:
        print("Not find Serial or somthing went wrong please check connection.")
        os.system("pause")
