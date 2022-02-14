SDK使用方法
====

1.系统配置
---
因为LINUX对系统内的所有设备都有访问权限控制,对非授权用户,系统内的设备无法正常访问.  
要正常操作视熙摄像头,需要对SDK进行访问授权.

授权方式:

1. 把`66-sxusb.rules`文件,放到`/etc/udev/rules.d/`目录下.
2. 重启系统.

2.使用方法
---

要使用SDK实现抓图功能,需要先配置让摄像头的预览功能跑起来.

可以使用系统自带的`VLC`多媒体程序,通过菜单"Media -> Open Capture Device"打开设备面板.
在"Capture Device"面板的"Video device name"下拉列表里,选择"/dev/video0",选好设备好,点"Play"按键,摄像头的预览功能即可正常开启.


打开了摄像头的预览功能后,就可以按如下方法进行抓图.

1. 通过svcontroller_factory::get_svdevice_list()查询系统连接的视熙摄像头
2. 创建svcontroller_factory类实例.
3. 通过svcontroller_factory类实例创建二个接口:
	1. svcontroller_interface, 用于控制打开抓图功能
	2. svsnapshoter_interface, 用于实现抓图.
4. svcontroller_interface::enable_snapshot(),启动抓图功能
5. svsnapshoter_interface::snapshot(),抓取一张图片.


3.运行环境
----
使用SDK开发的应用,需要额外的支持库才能成功运行

1. libusb
2. hidapi-libusb

可以通过如下命令安装:

```
sudo apt install libusb-1.0-0-dev libhidapi-dev
```

DEMO编译方法
---

DEMO程序使用cmake工具编译.
具体编译命令如下:

```
mkdir build
cd build
cmake ..
make
```

