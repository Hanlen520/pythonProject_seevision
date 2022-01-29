# coding = utf8
import logging
import os
import re
import subprocess

import traceback

os.path.abspath(".")
"""
    @Project:PycharmProjects
    @File:streeTest_bug.py
    @Author:十二点前要睡觉
    @Date:2022/1/12 17:32
"""

import pyautogui
import uiautomation
from time import sleep, strftime

# 实时获取时间
cur_time = strftime("%Y%m%d_%H%M%S")


def logger_config(log_path, logging_name):
    # 获取logger对象,取名
    logger = logging.getLogger(logging_name)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_path, encoding='UTF-8')
    # 生成并设置文件日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # 为logger对象添加句柄
    logger.addHandler(handler)

    return logger


if __name__ == '__main__':
    if not os.path.exists("./log/"):
        os.makedirs("./log/")
    logger = logger_config(log_path="./log/{}_{}_{}.log".format(cur_time, "codecSwitchTest", "mainLog"),
                           logging_name="codecSwitchTest")
    logger.info("压测轮数：6000")
    print("压测轮数：6000")
    for i in range(6000):
        try:
            logger.info(
                "=====================================第{}次Amcap MJPEG 1080P->H264 4K分辨率切换压测=====================================".format(
                    str(i)))
            print(
                "=====================================第{}次Amcap MJPEG 1080P->H264 4K分辨率切换压测=====================================".format(
                    str(i)))
            logger.info("查找Capture Application (Sample)应用图标")
            amcap = uiautomation.ButtonControl(searchDepth=5, Name="Capture Application (Sample)")
            logger.info("点击图标：Capture Application (Sample)应用图标")
            amcap.Click()
            logger.info("查找Options菜单")
            option = uiautomation.MenuItemControl(searchDepth=3, Name="Options")
            logger.info("点击菜单：Options")
            option.Click()
            logger.info("查找Video Capture Pin...菜单")
            video_capture_pin = uiautomation.MenuItemControl(searchDepth=3, Name="Video Capture Pin...")
            logger.info("点击菜单：Video Capture Pin...")
            video_capture_pin.Click()
            logger.info("查找格式选择列表")
            format_list = uiautomation.ComboBoxControl(AutomationId="1058", Depth=5)
            logger.info("点击展开格式选择列表")
            format_list.Click()
            logger.info("查找H264格式选项")
            h264 = uiautomation.ListItemControl(Depth=7, Name="H264")
            logger.info("点击选择H264格式")
            h264.Click()
            logger.info("查找分辨率选择列表")
            resolution_list = uiautomation.ComboBoxControl(AutomationId="1059", Depth=5)
            logger.info("点击展开分辨率选择列表")
            resolution_list.Click()
            logger.info("滚动查找4K分辨率")
            pyautogui.scroll(3000)
            four_k = uiautomation.ListItemControl(Depth=7, Name="3840 x 2160  (default)")
            logger.info("点击选择4K分辨率")
            four_k.Click()
            logger.info("查找确定按钮")
            open_button = uiautomation.ButtonControl(Depth=3, Name="确定")
            logger.info("点击确定按钮")
            open_button.Click()
            sleep(3)
            logger.info("截取当前4K分辨率显示情况")
            pyautogui.screenshot("./bugVerified/{}.jpg".format(i))
            sleep(0.5)
            logger.info("关闭Amcap应用程序")
            pid_get = subprocess.Popen("tasklist | grep amcap", shell=True, stdout=subprocess.PIPE).communicate()[0]
            pid = re.findall("amcap v3.0.9.exe(.*)Console", str(pid_get))[0].strip(" ")
            os.system("taskkill /pid {}".format(pid))
        except Exception as ex:
            logging.error("\n" + traceback.format_exc())
            logger.error("Some error happened : {}".format(str(ex)))
            print("Some error happened : {}".format(str(ex)))
            pid_get = subprocess.Popen("tasklist | grep amcap", shell=True, stdout=subprocess.PIPE).communicate()[0]
            try:
                pid = re.findall("amcap v3.0.9.exe(.*)Console", str(pid_get))[0].strip(" ")
                os.system("taskkill /pid {}".format(pid))
            except Exception as ex:
                logger.error("Amcap not launch!")
                logger.error("i-1，重新开始本轮测试，以满足总轮数， -- 重跑机制")
                logging.error("\n" + traceback.format_exc())
                print("Amcap not launch!")
                i -= 1
                continue
            logger.error("i-1，重新开始本轮测试，以满足总轮数， -- 重跑机制")
            i -= 1
            continue
        print("Test Finished！")
