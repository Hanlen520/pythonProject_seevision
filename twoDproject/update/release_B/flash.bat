@echo START UPGRADE...
fastboot flash lk lk.bin
fastboot flash boot boot.img
fastboot flash system system.img

fastboot oem finish_upgrade
fastboot reboot
@echo UPGRADE DONE!!!
pause
