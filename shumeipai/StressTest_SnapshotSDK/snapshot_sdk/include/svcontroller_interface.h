
#ifndef _SVCONTROLLER_INTERFACE_H_
#define _SVCONTROLLER_INTERFACE_H_

#include <string>

#ifdef __cplusplus
extern "C"
{
#endif

class svcontroller_interface
{
	public:
		//启动抓图功能,如果没有启用,svsnapshoter接口的抓图功能不生效.
		virtual bool enable_snapshot() = 0;
		//取摄像头模组的序列号
		virtual std::string get_serial_number() = 0;
		//取摄像头模组名.
		virtual std::string get_camera_model() = 0;
		virtual ~svcontroller_interface() {};
};

#ifdef __cplusplus
}
#endif
#endif
