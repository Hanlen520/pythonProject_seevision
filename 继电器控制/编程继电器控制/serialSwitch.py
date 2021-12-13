# coding = utf8

import os

os.path.abspath(".")

import serial

com_id = "COM22"


class SerialSwitch(object):

    def __init__(self, com_id):
        self.s_obj = serial.Serial(com_id, baudrate=115200)

    def switch_pin1_on(self):
        self.s_obj.write([0xFE, 0x05, 0x00, 0x00, 0xFF, 0x00, 0x98, 0x35])
        print(self.s_obj.read())

    def switch_pin1_off(self):
        self.s_obj.write([0xFE, 0x05, 0x00, 0x00, 0x00, 0x00, 0xD9, 0xC5])
        print(self.s_obj.read())

    def close(self):
        self.s_obj.close()


if __name__ == "__main__":
    switch_obj = SerialSwitch(com_id)
    switch_obj.switch_pin1_on()
    # switch_obj.switch_pin1_off()
    # os.system("pause")
    print("OK - test - No")
