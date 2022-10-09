# coding = utf8
import os
import re

import bs4

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:downloadTop100.py
    @Author:十二点前要睡觉
    @Date:2022/10/8 15:58
"""
import requests

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 '
                  'Safari/537.36'}

"""
    全部：http://zhushou.360.cn/list/index/cid/1/
    影音视听：http://zhushou.360.cn/list/index/cid/14/
    
"""


def catch360AppMarketLinks(typePage="http://zhushou.360.cn/list/index/cid/14"):
    rq = requests.get(url=typePage)
    rq.encoding = rq.apparent_encoding
    demo = rq.text
    soup = bs4.BeautifulSoup(demo, "html.parser")
    apk_list = []
    try:
        for link in soup.find_all("a"):
            print("Catch apk from specific link now:")
            if "zhushou360://type=apk" in str(link):
                apk_download_name = re.findall("name=(.*)&icon", link.get("href"))[0]
                apk_download_link = re.findall("url=(.*).apk", link.get("href"))[0] + "apk"
                print("【{}】 - 【{}】".format(apk_download_name, apk_download_link))
                apk_list.append({apk_download_name: apk_download_link})
                print("APK 【{}】 catch success !".format(apk_download_name), end="\n\n")
    except:
        print("Can not analysis current link to get download link need check !")
    if apk_list:
        return apk_list


def catchUrlFromLink(apk_download_name, apk_download_link):
    try:
        print("\n ===================== Downloading 【{}】 …… ,Please Wait ! =====================".format(
            apk_download_name))
        r = requests.get(apk_download_link, headers=header, allow_redirects=True, timeout=720)
        status_code = r.status_code
        if status_code == 200 or status_code == 206:
            with open("./apks/{}.apk".format(apk_download_name), "wb") as df:
                df.write(r.content)
                print("Download 【{}】 Finished ! ".format(apk_download_name))
    except:
        print("Can not download current APK 【{}】!".format(apk_download_name))


def downloadApkList(apk_list):
    if not os.path.exists("./apks/"):
        os.mkdir("./apks/")
    for temp in apk_list:
        for apk_download_name, apk_download_link in temp.items():
            catchUrlFromLink(apk_download_name, apk_download_link)


if __name__ == '__main__':
    apk_list = catch360AppMarketLinks()
    downloadApkList(apk_list)
