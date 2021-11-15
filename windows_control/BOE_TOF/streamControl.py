# coding = utf8
import os

os.path.abspath(".")

"""
    控制BOE_TOF上位机开关
    1、连接固件，检查端口和更新驱动程序，SecureCRTPortable连接端口
    2、运行脚本进行测试，打开相机，关闭相机
    3、第一场景，关闭相机5秒后打开相机
    4、第二场景，关闭相机20秒后打开相机
    5、持续运行两小时，查看下位机开关流是否正常：SecureCRTPortable查看是否存在ldxldx sig"	"1、不同场景下，打开或关闭相机，下位机运行正常
    2、下位机开关流正常，每一个场景的log中不存在ldxldx sig"
"""
