
#ifndef _SVCONTROLLER_FACTORY_H_
#define _SVCONTROLLER_FACTORY_H_

#include "svcontroller_interface.h"
#include "svsnapshoter_interface.h"

#include <list>
#include <string>

#ifdef __cplusplus
extern "C"
{
#endif

	using namespace std;

	typedef struct _svdevice_info {
		uint8_t bnum;
		uint8_t pnum;
		uint8_t dnum;
		int vid;
		int pid;
		int index;	//如果在一个系统内,连接了多个sv设备,因为vid,pid相同,会有无法控制多个设备的情况发生,所以加一个索引,让用户指定打开哪一个.
		string serial_number;	//将来可以通过sn号来区分.
		int ifcontrol;
		int ifsnap;
	} svdevice_info;

	class svcontroller_factory {
		public:
			svcontroller_factory ();
			~svcontroller_factory();

			static list<svdevice_info> get_svdevice_list();
			//创建控制接口svcontroller_interface.
			svcontroller_interface* create_controller_interface(svdevice_info& dev_info);
			//创建抓图接口svsnapshoter_interface
			svsnapshoter_interface* create_snapshoter_interface(svdevice_info& dev_info);
	};

#ifdef __cplusplus
}
#endif

#endif
