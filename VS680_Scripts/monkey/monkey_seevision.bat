@echo START Monkey...
adb push ./Fastbot_Android-main/Fastbot_Android-main/fastbot-thirdpart.jar ./Fastbot_Android-main/Fastbot_Android-main/framework.jar ./Fastbot_Android-main/Fastbot_Android-main/monkeyq.jar /sdcard
adb push ./Fastbot_Android-main/Fastbot_Android-main/libs/arm64-v8a ./Fastbot_Android-main/Fastbot_Android-main/libs/armeabi-v7a ./Fastbot_Android-main/Fastbot_Android-main/libs/x86 ./Fastbot_Android-main/Fastbot_Android-main/libs/x86_64 /data/local/tmp/
adb push ./abl.strings  /sdcard
adb shell CLASSPATH=/sdcard/monkeyq.jar:/sdcard/framework.jar:/sdcard/fastbot-thirdpart.jar exec app_process /system/bin com.android.commands.monkey.Monkey  --agent reuseq --pct-rotation 0  --act-blacklist-file /sdcard/abl.strings --bugreport --output-directory /sdcard/monkeyCrashLog --ignore-crashes --ignore-timeouts --kill-process-after-error --ignore-security-exceptions  --running-minutes 1 --throttle 500 -v -v
@echo Monkey DONE!!!
@echo 开始导出Log：
:: 设置CMD显示的编码格式为UTF-8(防止中文乱码)
chcp 65001

:: @echo off 表示不回显执行的命令
@echo off
::一定要看下当前日期的格式，不同的windows系统，打印的当前时间格式可能不一样(这样的年月日截取的开始位置就不一样)，防止被坑
set ORIGINAL_DATE=%date%
echo %ORIGINAL_DATE%
:: 日期截取遵从格式 %date:~x,y%，表示从第x位开始，截取y个长度(x,y的起始值为0)
:: 可以看到打印出来的当前日期ORIGINAL_DATE:周一 2022/03/21
:: 年份从第3位开始截取4位，月份从第5位开始截取2位，日期从第8位开始截取2位
set YEAR=%date:~3,4%
set MONTH=%date:~8,2%
set DAY=%date:~11,2%
:: 时间截取遵从格式 %time:~x,y%，表示从第x位开始，截取y个长度(x,y的起始值为0)
:: 时钟从第0位开始截取2位，分钟从第3位开始截取2位，秒钟从第6位开始截取2位
set HOUR=%time:~0,2%
set MINUTE=%time:~3,2%
set SECOND=%time:~6,2%
:: 毫秒
set MILLISECIOND=%time:~9,2%
:: 当时钟小于等于9时,前面有个空格，这时我们少截取一位，从第1位开始截取
set TMP_HOUR=%time:~1,1%
set NINE=9
set ZERO=0
:: 处理时钟是个位数的时候前面补上一个0, LEQ表示小于等于
:: if 和 set 一定要在同一行
if %HOUR% LEQ %NINE% set HOUR=%ZERO%%TMP_HOUR%
set CURRENT_DATE_TIME_STAMP=%YEAR%%MONTH%%DAY%_%HOUR%%MINUTE%%SECOND%%MILLISECIOND%
mkdir %CURRENT_DATE_TIME_STAMP%
timeout /T 1
adb root
adb remount
adb shell dmesg > ./%CURRENT_DATE_TIME_STAMP%/dmesg.txt
adb shell dumpsys meminfo > ./%CURRENT_DATE_TIME_STAMP%/sysmeminfo.txt
adb shell dumpsys > ./%CURRENT_DATE_TIME_STAMP%/dumpsys.txt
adb shell dumpsys activity activities > ./%CURRENT_DATE_TIME_STAMP%/activity.txt
adb shell dumpsys SurfaceFlinger > ./%CURRENT_DATE_TIME_STAMP%/SurfaceFlinger.txt
adb pull /d/binder/ .\%CURRENT_DATE_TIME_STAMP%\binder
adb pull /data/anr/ .\%CURRENT_DATE_TIME_STAMP%\anr
adb pull /data/tombstones .\%CURRENT_DATE_TIME_STAMP%/tombstones
adb shell cat proc/meminfo > ./%CURRENT_DATE_TIME_STAMP%/meminfo.txt
adb shell procrank > ./%CURRENT_DATE_TIME_STAMP%/procrank.txt
adb shell dumpsys window > ./%CURRENT_DATE_TIME_STAMP%/dump_window.txt
adb pull /sdcard/crash-dump.log ./%CURRENT_DATE_TIME_STAMP%
adb pull /sdcard/monkeyCrashLog ./%CURRENT_DATE_TIME_STAMP%
@echo START Catch log from device...
@echo Catch log Finished!!!!!!!!，【开始导出adb logcat和top日志Ctrl + C结束后，再执行top，两次Ctrl +C即可完成导出所有的Log】
adb shell logcat -b all>./%CURRENT_DATE_TIME_STAMP%/logcat.log
@echo 【请再次点击Ctrl + C】
adb shell top -m 10>./%CURRENT_DATE_TIME_STAMP%/top.txt
@echo 【所有log导出完毕，Monkey全模块测试结束！】
pause
