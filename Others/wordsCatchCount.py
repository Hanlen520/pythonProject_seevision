# coding = utf8
import os

import pandas as pd

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:wordsCatchCount.py
    @Author:十二点前要睡觉
    @Date:2022/5/10 14:53
"""

if __name__ == '__main__':

    sync_word_list = []
    with open("./sync帧率&中途掉线", "r") as f:
        lines_words = f.readlines()
        for line in lines_words:
            if "sync" in line:
                print(line)
                sync_word_list.append(line)

    df = pd.DataFrame({"sync字段出现次数": sync_word_list})
    df.to_excel("./syncWords.xlsx")
