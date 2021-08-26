# coding = utf8
import os
from time import sleep
import csv
os.path.abspath(".")
from PIL import Image
import imagehash
import uiautomator2 as u2
import time
cur_time = time.strftime("%Y%m%d_%H%M%S")

def result_calculate(data=[["1", "2", "3"], "1", "2", "3"], form_name="result.csv"):
    with open("./{}".format(form_name), "w", encoding="utf-8-sig") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["测试次数", "测试时间", "结果"])
        # 取出再写入
        for item in data:
            csv_writer.writerow(item)


def stress_test():
    try:
        d = u2.connect("192.168.50.107:5555")
        # d = u2.connect("1f56d837")
        csv_result = []
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
            # 截图
            file_name = "./screenshot/{}.jpg".format(str(i))
            d.screenshot(filename=file_name)
            sleep(3)
            normal_picture = imagehash.average_hash(Image.open("./normal_picture.jpg"))
            screenshot_picture = imagehash.average_hash(Image.open(file_name))
            if normal_picture == screenshot_picture:
                test_result = "Same picture {}".format(str(i))
            else:
                test_result = "Different picture {}".format(str(i))
                break
            print("Test times is：{} -- result is {}".format(str(i), test_result))
            csv_result.append([i, cur_time, test_result])
            d.press("back")
            d.press("back")
            d.press("back")
            sleep(5)
    except Exception as ex:
        print("Current test is happened error, please check and error code is :{}".format(str(ex)))
    finally:
        result_calculate(data=csv_result)
        sys.exit(0)


if __name__ == '__main__':
    stress_test()