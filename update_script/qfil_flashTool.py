# coding = utf8
import os
import subprocess
from time import sleep

import uiautomation

os.path.abspath(".")


def openQFil(path=r"D:\Qualcomm\QPST\bin\QFIL.exe"):
    print("Open QFIL")
    global qfil
    qfil = subprocess.Popen(path)
    sleep(2)


def closeQFil():
    print("Close QFIL")
    qfil.kill()


def device_into_edl_and_port_online():
    while True:
        port_status = uiautomation.TextControl(AutomationId="lblSelectPort").Name
        if "QDLoader" in port_status:
            print("当前端口连接成功：{}".format(port_status))
            return True
        else:
            reboot_edl = subprocess.Popen("adb reboot edl", shell=True,
                                          stdout=subprocess.PIPE).communicate()[0]


def flash_into_device(path=r"D:\PycharmProjects\pythonProject_seevision\update_script\meizu_package"):
    # ControlType: RadioButtonControl    ClassName: WindowsForms10.BUTTON.app.0.190610d_r7_ad1    AutomationId: radioFlatBuild    Rect: (125,209,200,230)[75x21]    Name: Flat Build    Handle: 0x700AB4(7342772)    Depth: 3
    # SelectionItemPattern.IsSelected: False    SupportedPattern: InvokePattern LegacyIAccessiblePattern SelectionItemPattern
    flat_build = uiautomation.RadioButtonControl(AutomationId="radioFlatBuild").Click()
    sleep(1)


"""
    暂定不搞QFIL的
"""

if __name__ == '__main__':
    openQFil()

    device_into_edl_and_port_online()
    sleep(3)
    # closeQFil()
