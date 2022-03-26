# coding = utf8
import os

os.path.abspath(".")
"""
    @Project:pythonProject_seevision
    @File:digitalZoomTest.py
    @Author:十二点前要睡觉
    @Date:2022/3/23 10:33
    @Description:自动化测试点分解：
        1、6个分辨率：
            MJPG 3840*2160
            MJPG 1920*1080
            MJPG 1280*720
            H264 3840*2160
            H264 1920*1080
            H264 1280*720
        2、测试点：
            a、错误值：
                无缩放状态->缩小1step
                无缩放状态->过度放大53step
                放大40step状态->过度缩小53step
            b、有效值：
                放大->移动画面：
                    放大5step
                    放大10step
                    放大14step
                    放大17step
                    放大20step
                    放大23step
                    放大25step
                    放大27step
                    放大28step
                    放大30step
                    放大31step
                    放大33step
                    放大34step
                    放大35step
                    放大36step
                    放大37step
                    放大38step
                    放大39step
                    放大40step
                    放大53step
                缩小：
                    缩小1step
                    缩小2step
                    缩小3step
                    缩小4step
                    缩小5step
                    缩小6step
                    缩小7step
                    缩小8step
                    缩小9step
                    缩小10step
                    缩小12step
                    缩小13step
                    缩小15step
                    缩小18step
                    缩小20step
                    缩小23step
                    缩小26step
                    缩小30step
                    缩小35step
                    缩小40step
"""





