# coding = utf8
import os

from ralayControl import serialComportList

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

    def switch_on(self, COMPORT):
        self.s_obj.write(COMPORT)
        b = self.s_obj.read(8)
        print(b)

    def switch_off(self, COMPORT):
        self.s_obj.write(COMPORT)
        b = self.s_obj.read(8)
        print(b)

    def open_all_comport(self):
        self.s_obj.write(serialComportList.RELAY_CONTROL_COMPORT_OPEN_ALL)

    def close_all_comport(self):
        self.s_obj.write(serialComportList.RELAY_CONTROL_COMPORT_CLOSE_ALL)

    def close(self):
        self.s_obj.close()


if __name__ == "__main__":
    """
        Tip:Serial comport deliver in and Operation wait
    """
    com_id = "COM3"
    try:
        switch_obj = SerialSwitch(com_id)
        for i in range(10):
            print("Begin relay power on/off test")
            switch_obj.switch_on(serialComportList.RELAY_CONTROL_COMPORT_1_OPEN)
            sleep(1)
            switch_obj.switch_off(serialComportList.RELAY_CONTROL_COMPORT_1_CLOSE)
            sleep(1)
            switch_obj.open_all_comport()
            sleep(1)
            switch_obj.close_all_comport()
            sleep(1)
            switch_obj.switch_on(serialComportList.RELAY_CONTROL_COMPORT_16_OPEN)
            sleep(1)
            switch_obj.switch_off(serialComportList.RELAY_CONTROL_COMPORT_16_CLOSE)
            sleep(1)
    except SerialException:
        print("Not find Serial or somthing went wrong please check connection.")
        os.system("pause")
