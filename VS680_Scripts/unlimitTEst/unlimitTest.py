# coding = utf8
import os

abspath = os.path.abspath(".")

"""
    先安装adbkeyboard.apk
    push max.config & max.fuzzing.strings
    对用户能接触到的APP进行极限测试
    1、特殊字符输入压力测试 -- max.fuzzing.strings
    2、点击控件开关覆盖压测 -- max.config
    3、指定APP对应高频控件、逻辑压测: -- max.xpath.actions
        腾讯会议：设置按钮、微信登录按钮、加入会议按钮
        飞书：手机号输入框、下一步按钮、SSO登录按钮
        电子白板：撤销按钮、反撤销按钮、笔刷按钮、笔按钮、擦皮按钮、剪切按钮、材质按钮、删除按钮、分享按钮、悬浮窗按钮
        设置：各类开关、各种可点击项、拖动条
        audio router：选项切换
        File：不同类别文件项、文件icon
        Meeting Record：菜单建议按钮
        Screencasting：video按钮、document按钮、mirroring按钮、lebo按钮、设备信息按钮、网络信息按钮
        用户手册：各项手册类型页
        微信：登录按钮、注册按钮、语言按钮、输入框、确认框
        USB无线投屏：按钮
"""


def fastbot_monkey_cover_test():
    os.system("adb install ./adbkeyboard.apk")
    os.system("adb push ./max.config ./max.fuzzing.strings /sdcard")
    os.system(
        "adb push ./Fastbot_Android-main/fastbot-thirdpart.jar ./Fastbot_Android-main/framework.jar "
        "./Fastbot_Android-main/monkeyq.jar /sdcard")
    os.system(
        "adb push ./Fastbot_Android-main/libs/arm64-v8a ./Fastbot_Android-main/libs/armeabi-v7a "
        "./Fastbot_Android-main/libs/x86 ./Fastbot_Android-main/libs/x86_64 /data/local/tmp/")
    os.system("adb push ./abl.strings  /sdcard")
    os.system("adb push ./max.xpath.actions /sdcard")
    os.system(
        "adb shell CLASSPATH=/sdcard/monkeyq.jar:/sdcard/framework.jar:/sdcard/fastbot-thirdpart.jar exec app_process "
        "/system/bin com.android.commands.monkey.Monkey --agent reuseq  --act-blacklist-file /sdcard/abl.strings "
        "--bugreport --output-directory /sdcard/monkeyCrashLog/crash --ignore-crashes --ignore-timeouts "
        "--kill-process-after-error --ignore-security-exceptions  --running-minutes 4000 --throttle 500 -v -v")


if __name__ == '__main__':
    fastbot_monkey_cover_test()
