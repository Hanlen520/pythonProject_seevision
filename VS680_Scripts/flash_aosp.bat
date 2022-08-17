@echo START UPGRADE...
adb reboot bootloader
fastboot devices
fastboot flashing unlock
fastboot -w
fastboot update %1
fastboot reboot
@echo UPGRADE DONE!!!
pause
