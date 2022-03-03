@pushd %~dp0
@set DIR=dir .\firmware/B
@set READ=.\xmos_tool\dfu_usb.exe read_version

@call :cmd %DIR%
@if "%result%"=="" (
	color 4
	echo=
	echo 未检测到固件！！！
	echo=
	set /p show=请确保固件在 xmos_tool文件夹下的firmware文件夹内！！！
) else (
	echo 已找到固件：固件版本为%result:~-11,3%
	set /p show=请连接设备，点击“回车键”开始刷录！！
)

@:loop
	@cls
	@color 0F

	@call :cmd %DIR%
	@if "%result%"=="" (
		color 4
		echo=
		echo 未检测到固件！！！
		echo=
		set /p show=请确保固件在 xmos_tool文件夹下的firmware文件夹内！！！
		goto :loop
	)

	@set new=%result%
	@call :getV
	@set new=%new:~0,3%
	@echo 固件版本：%new%
	@echo=

	@call :cmd %READ%
	@if "%result:~1,1%"=="t" (
		color 4
		echo=
		echo 未连接设备 ！！！
		echo=
		@set /p show=请连接好设备后敲击回车键重新启动刷机: 
		goto :loop	
	)
	@set per=%result:~9%
	@set per_v=%per:~0,1%%per:~2,1%%per:~4,1%
	@echo 设备当前版本：%per_v%

	@if "%new%"=="%per_v%" (
		color 4
		echo=
		set /p show=固件版本与设备版本一致！！！
		goto :loop
	)

	@call :cmd %DIR%
	.\xmos_tool\dfu_usb.exe write_upgrade .\firmware\%result%

	.\xmos_tool\dfu_usb.exe reboot
	@echo 版本校验中......
	@ping /n 3 127.0.0.1 >nul
	@ping /n 3 127.0.0.1 >nul

	@call :cmd %READ%
	@set v=%result:~9%

	@echo=

	@if "%v%"=="3.0.4" (
		color 4
		echo 烧录发生错误，版本回退为3.0.4 ！！！
		@echo=
		@set /p show=请敲击回车键重新启动刷机: 
	) else (
		color 2
		echo 烧录成功，当前版本为%v% ！！！
		@echo=
		@set /p show=请切换设备后敲击回车键重新启动刷机: 
	)
@goto :loop

::获取执行命令的结果
@:cmd
	@for /f "delims=" %%t in ('%1 %2') do @set result=%%t
@goto :eof

::通过固件名截取版本号
@:getV
	@if not "%new:V=%"=="%new%" set new=%new:*V=%&goto :getV
@goto :eof