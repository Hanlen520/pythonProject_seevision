#!/bin/sh
adb reboot bootloader
sleep 1
fastboot devices
fastboot flashing unlock
fastboot -w
fastboot update $1
fastboot reboot

