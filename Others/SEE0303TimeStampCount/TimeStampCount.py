# coding = utf8
import os

import pandas as pd

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:TimeStampCount.py
    @Author:十二点前要睡觉
    @Date:2022/7/28 16:26
"""


def readFileName(folder_path):
    pictures = []
    picture_name = os.listdir(folder_path)
    for i in picture_name:
        if str(i).endswith(".png"):
            picture = str(i).replace("_depth.png", "")
            pictures.append(picture)
    if pictures:
        return pictures


def subCalculator(pictures):
    result = []
    for i in range(0, len(pictures) - 1):
        number_i = int(pictures[i])
        number_j = int(pictures[i + 1])
        if i == len(pictures) - 1:
            break
        result_z = abs(number_i - number_j)
        # print(number_i, number_j, result_z, end="\n")
        result.append([number_i, number_j, result_z])
    if result:
        return result


def write_intoExcel(result):
    if not os.path.exists("./Result/"):
        os.mkdir("./Result/")
    # [{'windows_stopwatch_time': 3931130, 'camera_stopwatch_time': 3930894, 'delay_time': 236}, {'windows_stopwatch_time': 3931209, 'camera_stopwatch_time': 3930972, 'delay_time': 237}]
    number_iList = []
    number_jList = []
    result_zList = []
    for singleResult in result:
        number_iList.append(singleResult[0])
        number_jList.append(singleResult[1])
        result_zList.append(singleResult[2])
    df = pd.DataFrame(
        {"时间戳1": number_iList, "时间戳2": number_jList, "时间间隔": result_zList})
    df.to_excel("./Result/result.xlsx")


if __name__ == '__main__':
    folder_path = r"./20220728开启算法/"
    pictures = readFileName(folder_path)
    result = subCalculator(pictures)
    print(result)
    write_intoExcel(result)
