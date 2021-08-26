# coding = utf8
import os
from time import sleep

os.path.abspath(".")

import uiautomator2 as u2

# d = u2.connect("192.168.50.109:5555")
d = u2.connect("1f56d837")
for i in range(101):
    d(text="它物云门店").click()
    sleep(5)
    d(text=">>模拟采集").click()
    sleep(5)
    d(text="激活").click()
    sleep(5)
    d(text="开始采集").click()
    sleep(10)
    test_result = "OK"
    # # 截图
    # file_name = "./screenshot/{}.jpg".format(str(i))
    # d.screenshot(filename=file_name)
    # sleep(3)
    # normal_picture = imagehash.average_hash(Image.open("./normal_picture.jpg"))
    # screenshot_picture = imagehash.average_hash(Image.open(file_name))
    # if normal_picture == screenshot_picture:
    #     test_result = "Same picture {}".format(str(i))
    # else:
    #     test_result = "Different picture {}".format(str(i))
    #     break
    print("Test times is：{} -- result is {}".format(str(i), test_result))
    d.press("back")
    d.press("back")
    d.press("back")
    sleep(5)
