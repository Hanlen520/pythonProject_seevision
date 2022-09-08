# coding = utf8
import os
from time import sleep

import openpyxl
import pandas as pd
import pyautogui
import pytesseract
from PIL import Image, ImageEnhance
from jieba import xrange

pyautogui.FAILSAFE = True
# pyautogui.PAUSE = 0.5
os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:ocr_script.py
    @Author:十二点前要睡觉
    @Date:2022/4/12 11:41
"""


# bin:D:\PycharmProjects\pythonProject_seevision\HW_Scripts\OCR_PADS\Mentor PADS VX2.5\PADS_2.5\PADSVX.2.5\SDD_HOME\common\win32\bin\powerpcb.exe
# pcb_file:D:\PycharmProjects\pythonProject_seevision\HW_Scripts\OCR_PADS\pcb_file

# 打开Potplayer，传入potplayer启动exe路径
# 先在C盘创建文件夹：flexlm->将LICENSE.DAT放入文件夹中，后续脚本打开授权检测用
# def openPADSLayout(
#         padsLayout_path=r"D:\PycharmProjects\pythonProject_seevision\HW_Scripts\OCR_PADS\Mentor PADS VX2.5\PADS_2.5\PADSVX.2.5\SDD_HOME\common\win32\bin\powerpcb.exe"):
#     global padsLayout
#     padsLayout = subprocess.Popen(padsLayout_path)
#     sleep(5)
#
#
# def openPcbFile(
#         pcb_path=r"D:\PycharmProjects\pythonProject_seevision\HW_Scripts\OCR_PADS\pcb_file\S00703_V01_20220409.pcb"):
#     pyautogui.hotkey("ctrl", "o")
#     ui.ButtonControl(searchDepth=8, Name="上一个位置").Click()
#     pyautogui.press("delete")
#     ui.PaneControl(AutomationId="41477").SendKeys(pcb_path)
#     ui.ButtonControl(searchDepth=3, Name="打开(O)").Click()
#     ui.ButtonControl(searchDepth=3, Name="最大化").Click()
#     pyautogui.press("HOME")


def openSearchBox(name="D15"):
    pyautogui.press("s")
    pyautogui.press("s")
    pyautogui.typewrite(" {}".format(name))
    pyautogui.press("enter")
    pyautogui.hotkey("ctrl", "w")
    for i in range(6):
        pyautogui.doubleClick()
    pyautogui.hotkey("ctrl", "w")


def resize_home():
    pyautogui.press("HOME")


def catchFramePicture(name):
    if not os.path.exists("./screenshot/"):
        os.mkdir("./screenshot/")
    x, y = pyautogui.position()
    imagePath = "./screenshot/{}.jpeg".format(name)
    catch_x, catch_y = x - GoodX / 2, y - GoodY / 2
    catch_w, catch_h = GoodX, GoodY
    # pyautogui.screenshot(imagePath, region=(x - 325, y - 200, 650, 350))
    pyautogui.screenshot(imagePath, region=(catch_x, catch_y, catch_w, catch_h))
    return imagePath


# def ocr_analysis(name, img, row):
#     text = pytesseract.image_to_string(Image.open(img), lang="test1", config="--psm 7").replace("\n",
#                                                                                               "").strip().replace(
#         " ", "").replace(".", "").replace(")", "")
#     print("【{}】 -- 【{}】".format(name.replace(".jpeg", ""), text))
#     if name.replace(".jpeg", "") == text:
#         print("image:{} text is:{},result is 【{}】".format(img, text, "PASS"))
#         write_into_excel(form="./sytj0101/工作簿1.xlsx", sheet_name="Sheet1", row=row, column=12, value="PASS")
#     else:
#         print("image:{} text is:{},result is 【{}】".format(img, text, "FAIL"))
#         write_into_excel(form="./sytj0101/工作簿1.xlsx", sheet_name="Sheet1", row=row, column=12, value="FAIL")
#     write_into_excel(form="./sytj0101/工作簿1.xlsx", sheet_name="Sheet1", row=row, column=13, value=text)


# def picture_Fixed(name, imagePath="./screenshot/C93.jpeg"):
#     # turn to black and white picture
#     img = Image.open(imagePath)
#     img_gray = img.convert("L")
#     if not os.path.exists("./screenshot/Gray/"):
#         os.mkdir("./screenshot/Gray/")
#     if not os.path.exists("./screenshot/BLACK&WHITE/"):
#         os.mkdir("./screenshot/BLACK&WHITE/")
#     img_gray.save("./screenshot/Gray/【Gray】{}".format(name))
#     img_black_white = img_gray.point(lambda x: 0 if x > 200 else 255)
#     bw = "./screenshot/BLACK&WHITE/【BLACK&WHITE】{}".format(name)
#     img_black_white.save(bw)
#     sleep(1)
#
#     # noise optimize
#     # img_cv = cv2.imread(bw)
#     # im = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
#     # cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 1)
#     #
#     # img = Image.open(bw)
#     # last_picture = "./screenshot/[code_result]{}".format(name)
#     # h, w = img.shape[:2]
#     # for y in range(0, w):
#     #     for x in range(0, h):
#     #         if y == 0 or y == w - 1 or x == 0 or x == h - 1:
#     #             img[x, y] = 255
#     #             continue
#     #         count = 0
#     #         if img[x, y - 1] == 255:
#     #             count += 1
#     #         if img[x, y + 1] == 255:
#     #             count += 1
#     #         if img[x - 1, y] == 255:
#     #             count += 1
#     #         if img[x + 1, y] == 255:
#     #             count += 1
#     #         if count > 2:
#     #             img[x, y] = 255
#     #     cv2.imwrite(last_picture, img)
#     # return name, last_picture
#
#     im = Image.open(bw)
#     enhancer = ImageEnhance.Contrast(im)
#     im = enhancer.enhance(2)
#     im = im.convert("1")
#     data = im.getdata()
#     w, h = im.size
#     black_point = 0
#     for x in xrange(1, w - 1):
#         for y in xrange(1, h - 1):
#             mid_pixel = data[w * y + x]  # 中央像素点像素值
#             if mid_pixel == 0:  # 找出上下左右四个方向像素点像素值
#                 top_pixel = data[w * (y - 1) + x]
#                 left_pixel = data[w * y + (x - 1)]
#                 down_pixel = data[w * (y + 1) + x]
#                 right_pixel = data[w * y + (x + 1)]
#                 # 判断上下左右的黑色像素点总个数
#                 if top_pixel == 0:
#                     black_point += 1
#                 if left_pixel == 0:
#                     black_point += 1
#                 if down_pixel == 0:
#                     black_point += 1
#                 if right_pixel == 0:
#                     black_point += 1
#                 if black_point >= 3:
#                     im.putpixel((x, y), 0)
#                 black_point = 0
#     last_picture = "./screenshot/[code_result]{}".format(name)
#     im.save(last_picture)
#     sleep(1)
#     return name, last_picture


"""
    test form read - excel operate
"""


# 从excel中读取数据并返回（element）

def read_excel_for_page_element(form="./sytj0101/SEE0102M_V01_0415.xlsx", sheet_name="Sheet1"):
    """
    通过Pandas模块读取case测试点内容，用于后续遍历case执行测试
    :param form:待读取case Excel文件路径
    :param sheet_name:待读取case Excel文件指定sheet表名
    :return:返回对应case所在行以及对应改行case测试点
    """
    print("从excel中读取数据（测试数据case）并返回（element）")
    df = pd.read_excel(form, sheet_name=sheet_name, index_col="number", engine="openpyxl")
    test_case_list = []
    for i in range(1, df.shape[0] + 1):
        part_type = df.loc[i, "PartType"]
        ref_des = df.loc[i, "RefDes"]
        layer = df.loc[i, "Layer"]
        orientation = df.loc[i, "Orient."]
        test_case_list.append([i, part_type, ref_des, layer, orientation])
    return test_case_list


def write_into_excel(form="./sytj0101/工作簿1.xlsx", sheet_name="Sheet1", row=1, column=12, value="PASS"):
    """
    通过openpyxl模块将每一行case的测试结果写入对应每一行的结果列中
    :param form:待写入case Excel文件路径
    :param sheet_name:待写入case Excel文件指定sheet表名
    :param row:待写入case测试结果所在行
    :param column:待写入case测试结果所在列
    :param value:待写入测试结果
    :return:None
    """
    print("将测试结果写入excel表格对应Case的行 - 测试结果处：【{}】".format(value))
    wb = openpyxl.load_workbook(form)
    ws = wb[sheet_name]
    ws.cell(row + 1, column).value = value
    wb.save(form)


if __name__ == '__main__':
    element_list = read_excel_for_page_element()
    print(element_list)
    screenX, screenY = pyautogui.size()
    GoodX = screenX * 0.2
    GoodY = screenY * 0.15
    # print(GoodX, GoodY)
    # sleep(5)
    # """
    #     转tiff->Merge->analysis picture->train picture->put data into tesseract tool
    # """
    # fixed_imageList = []
    # row_list = []
    # for demo in element_list:
    #     row = demo[0]
    #     demo = demo[1]
    #     print("row is {} and demo is {}".format(row, demo))
    #     row_list.append({"demo": row})
    #     openSearchBox(demo)
    #     imagePath = catchFramePicture(demo)
    #     resize_home()
