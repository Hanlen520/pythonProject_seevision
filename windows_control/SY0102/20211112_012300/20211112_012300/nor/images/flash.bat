@echo START UPGRADE...
fastboot flash IPL ipl_s.bin
fastboot flash IPL_CUST ipl_cust_s.bin 
fastboot flash MXPT boot/MXP_SF.bin
fastboot flash UBOOT uboot_s.bin
fastboot flash UBOOT_ENV BOOTENV.bin
fastboot flash KERNEL kernel
fastboot flash rootfs rootfs.sqfs
fastboot flash miservice miservice.sqfs
fastboot flash customer customer.jffs2

fastboot oem finish_upgrade
fastboot reboot
@echo UPGRADE DONE!!!
pause
