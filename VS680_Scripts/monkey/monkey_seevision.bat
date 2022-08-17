@echo START Monkey...
adb push ./Fastbot_Android-main/Fastbot_Android-main/fastbot-thirdpart.jar ./Fastbot_Android-main/Fastbot_Android-main/framework.jar ./Fastbot_Android-main/Fastbot_Android-main/monkeyq.jar /sdcard
adb push ./Fastbot_Android-main/Fastbot_Android-main/libs/arm64-v8a ./Fastbot_Android-main/Fastbot_Android-main/libs/armeabi-v7a ./Fastbot_Android-main/Fastbot_Android-main/libs/x86 ./Fastbot_Android-main/Fastbot_Android-main/libs/x86_64 /data/local/tmp/
adb push ./abl.strings  /sdcard
adb -s 130040A22272800120A shell CLASSPATH=/sdcard/monkeyq.jar:/sdcard/framework.jar:/sdcard/fastbot-thirdpart.jar exec app_process /system/bin com.android.commands.monkey.Monkey  --agent reuseq  --act-blacklist-file /sdcard/abl.strings --running-minutes 1 --throttle 500 -v -v
@echo Monkey DONE!!!
pause
