#!/bin/bash

set -e

IMAGE_DIR=$(pwd)

if [ ! -d ${IMAGE_DIR} ];then
    echo "${IMAGE_DIR} no such directory!"
    exit 1
fi
echo "the images path is $IMAGE_DIR"
fastboot flash lk ${IMAGE_DIR}/lk.bin
fastboot flash boot ${IMAGE_DIR}/boot.img
fastboot flash system ${IMAGE_DIR}/system.img

fastboot oem finish_upgrade
fastboot reboot