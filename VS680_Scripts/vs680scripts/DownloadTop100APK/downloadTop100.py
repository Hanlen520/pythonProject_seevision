# coding = utf8
import os

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
def catch360AppMarketLinks(typePage="http://zhushou.360.cn/list/index/cid/1/"):
    rq = requests.get(url=typePage)
    print(rq.text)


def catchUrlFromLink(downloadLink=""):
    try:
        apk_url = "http://s.shouji.qihucdn.com/220927/b60dacdbdfec24034d374ad87744f8a8/com.ss.android.ugc" \
                  ".aweme_220601.apk?en=curpage%3D%26exp%3D1665821573%26from%3DAppList_json%26m2%3D%26ts%3D1665216773" \
                  "%26tok%3Db6ff055a93a0a4f47c29cc44ba9ba55c%26v%3D%26f%3Dz.apk "
        print("Downloading …… ,Please Wait ! ")
        r = requests.get(apk_url, headers=header, allow_redirects=True, timeout=720)
        status_code = r.status_code
        if status_code == 200 or status_code == 206:
            with open("./douyin.apk", "wb") as df:
                df.write(r.content)
                print("Download Finished ! ")
    except:
        print("Can not download current APK!")
    os.system("pause")


if __name__ == '__main__':
    # catchUrlFromLink()
    catch360AppMarketLinks()