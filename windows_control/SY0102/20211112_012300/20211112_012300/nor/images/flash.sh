#!/bin/bash

set -e

IMAGE_DIR=$(pwd)

fastboot flash IPL ${IMAGE_DIR}/ipl_s.bin 
fastboot flash IPL_CUST ${IMAGE_DIR}/ipl_cust_s.bin 
fastboot flash MXPT ${IMAGE_DIR}/boot/MXP_SF.bin
fastboot flash UBOOT ${IMAGE_DIR}/uboot_s.bin
fastboot flash UBOOT_ENV ${IMAGE_DIR}/BOOTENV.bin
fastboot flash KERNEL ${IMAGE_DIR}/kernel
fastboot flash rootfs ${IMAGE_DIR}/rootfs.sqfs
fastboot flash miservice ${IMAGE_DIR}/miservice.sqfs
fastboot flash customer ${IMAGE_DIR}/customer.jffs2

fastboot oem finish_upgrade
fastboot reboot

