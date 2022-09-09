# coding = utf8
import os

abspath = os.path.abspath(".")


def fastbot_monkey_cover_test():
    os.system("adb install ./adbkeyboard.apk")
    os.system("adb push ./max.config ./max.fuzzing.strings /sdcard")
    os.system(
        "adb push ./Fastbot_Android-main/fastbot-thirdpart.jar ./Fastbot_Android-main/framework.jar ./Fastbot_Android-main/monkeyq.jar /sdcard")
    os.system(
        "adb push ./Fastbot_Android-main/libs/arm64-v8a ./Fastbot_Android-main/libs/armeabi-v7a ./Fastbot_Android-main/libs/x86 ./Fastbot_Android-main/libs/x86_64 /data/local/tmp/")
    os.system("adb push ./abl.strings  /sdcard")
    os.system("adb push ./max.xpath.actions /sdcard")
    os.system(
        "adb shell CLASSPATH=/sdcard/monkeyq.jar:/sdcard/framework.jar:/sdcard/fastbot-thirdpart.jar exec app_process /system/bin com.android.commands.monkey.Monkey --agent reuseq  --act-blacklist-file /sdcard/abl.strings --bugreport --output-directory /sdcard/monkeyCrashLog/crash --ignore-crashes --ignore-timeouts --kill-process-after-error --ignore-security-exceptions  --running-minutes 3000 --throttle 500 -v -v")


if __name__ == '__main__':
    fastbot_monkey_cover_test()
