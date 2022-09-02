# coding = utf8
import os
import re
import subprocess

"""
    @File:permissionGrant.py
    @Author:Bruce
    @Date:2020/12/23
    @Description:设备批量授权函数
"""

os.path.abspath(".")


def list_permission(package_name):
    # 判断没有启动界面就放出来进行授权
    # 优化后app数量：67个，优化前app数量：330个
    if str(subprocess.Popen('adb shell "dumpsys package {} | grep category.LAUNCHER"'.format(package_name), shell=True,
                            stdout=subprocess.PIPE).communicate()[0]).replace(" ", "").replace(" ", "").replace("b''",
                                                                                                                "") is not None:
        permission_list = str(
            subprocess.Popen(
                'adb shell "dumpsys package {} | grep permission | grep granted=false"'.format(package_name),
                shell=True,
                stdout=subprocess.PIPE).communicate()[0])
        permission_list = re.findall("\s*([a-zA-Z0-9_.]*):\sgranted", permission_list)
        if len(permission_list) == 0:
            print("当前应用程序无需再授权啦！")
        else:
            pass
            # print(permission_list)
    return permission_list


"""
    @description:进行授权操作
    @param:
        devices:设备
"""


def grant_permission(app_list):
    print("机器正在授权中，请稍后")
    app_permission = data_deal(app_list)
    for app_ in app_permission:
        for permission_ in app_[1]:
            try:
                print("正在对app【{}】的【{}】权限授权完成！".format(app_[0], permission_))
                os.system("adb shell pm grant {} {}".format(app_[0], permission_))
            except Exception:
                print("该权限无法授权，较敏感，跳过操作！")


"""
    @description:筛选掉无需授权的应用权限
    @param:
        app_list:所有应用
        devices:设备
"""


def data_deal(app_list):
    app_permission = []
    for package_name in app_list:
        permission_name = list_permission(package_name)
        app_permission.append([package_name, permission_name])
    return app_permission
