# encoding = utf8

import os
import subprocess

os.path.abspath(".")

"""
    将需要测试的update.zip、ota.py包放到脚本目录下
"""
if __name__ == "__main__":
    print("OK1")
    # device = connect_device("android:///{}?cap_method=javacap&touch_method=adb".format("c59a06bf"))
    # poco = AndroidUiautomationPoco(device, use_airtest_input=True, screenshot_each_action=False)
    update_command_write = subprocess.Popen("python ota.py update.zip", stdout=subprocess.PIPE).communicate()[0]
    with open("update.txt", "w") as update_command_file:
        update_command_file.write(update_command_write.decode())
    update_command = "update.txt"
    update_command_execute = subprocess.Popen("adb shell < {}".format(update_command), shell=True, stdout=subprocess.PIPE).communicate()[0]
    print("OK2")
