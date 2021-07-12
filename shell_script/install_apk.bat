@ECHO off
@REM @SET PATH=%PATH%,%CD%\Adb
@REM SET PATH

@REM Cycle mark
:LOOP

ECHO wait for your device connected:
adb wait-for-device

@REM Cycle install all apk in current folder
FOR %%i IN (*.apk) DO (
ECHO Installing:%%i
adb install %%i
)

@echo off
ECHO Installing success please connect another device:
PAUSE
GOTO LOOP

@ECHO on

