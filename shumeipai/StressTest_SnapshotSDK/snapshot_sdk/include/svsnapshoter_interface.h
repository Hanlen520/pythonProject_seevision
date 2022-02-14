
#ifndef _SVSNAPSHOTER_INTERFACE_H_
#define _SVSNAPSHOTER_INTERFACE_H_

#include <string>

#ifdef __cplusplus
extern "C"
{
#endif

	using namespace std;

	class svsnapshoter_interface
	{
		public:
			//抓取一张图片.
			virtual bool snapshot(string str_file_name) = 0;
			//取历史缓存,上面的snapshot抓取图片的同时,会将图片缓存.
			//get_history_picture就是从缓存里取一张图片.
			//最多只有4张缓存图片.
			virtual bool get_history_picture(string str_file_name, uint32_t idx) = 0;
			virtual ~svsnapshoter_interface() {};
	};

#ifdef __cplusplus
}
#endif

#endif
