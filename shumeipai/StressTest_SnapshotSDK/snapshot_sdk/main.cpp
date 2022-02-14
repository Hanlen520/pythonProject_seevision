#include "svcontroller_factory.h"

#include <sys/time.h>
#include <iostream>

unsigned long long GetCurrentMillisecs()
{
    timeval tv;         
    gettimeofday(&tv, 0);
    unsigned long long ret = tv.tv_sec;
    return ret * 1000 + tv.tv_usec / 1000;
}

string get_date_string()
{
	time_t timep;
	char name[256] = {0};

	time(&timep);
	strftime(name, sizeof(name), "%Y-%m-%d_%H_%M_%S", localtime(&timep));

	return string(name);
}

int main()
{
	list<svdevice_info> lst = svcontroller_factory::get_svdevice_list();

	if(lst.size() == 0)
	{
		cout << "not find device!" << endl;
		return 1;
	}


	list<svdevice_info>::iterator it;

	for(it = lst.begin(); it != lst.end(); ++it)
	{
		cout << "vid = " << hex << (*it).vid << endl;
		cout << "pid = " << hex << (*it).pid << endl;
		cout << "index = " << (*it).index << endl;
	}

	//for test.
//	return 0;

	it = lst.begin();

	svcontroller_factory factory;
	svcontroller_interface* p_controller = factory.create_controller_interface( (*it));
	svsnapshoter_interface* p_snap = factory.create_snapshoter_interface( (*it) );

	if(p_controller == NULL)
	{
		cout << "open device fail!" << endl;
		return 2;
	}

//	if(p_snap == NULL)
//	{
//		cout <<" create snapshoter interface return NULL" << endl;
//		return 3;
//	}


	cout << "open device OK!" << endl;

	p_controller->enable_snapshot();

	string str_value;
	str_value = p_controller->get_serial_number();
	cout << "serial_number = " << str_value << endl;

	str_value = p_controller->get_camera_model();
	cout << "camera_model = " << str_value << endl;

	delete p_controller;

	if(p_snap == NULL)
	{
		cout <<"open snapshoter error!" << endl;
		return 3;
	}

	string str_file_name = get_date_string();

#define _TEST_SNAP 0
#if _TEST_SNAP
	str_file_name += ".jpg";

	unsigned long long time_start = GetCurrentMillisecs();
	p_snap->snapshot(str_file_name);
	unsigned long long time_stop = GetCurrentMillisecs();

	unsigned long long time_count = time_stop - time_start;

	cout << "get pic spend time = " << dec << time_count << " millisecs!" << endl;

#else

	str_file_name += "_his.jpg";
	//抓历史图片.只能在上面的snapshot接口已经抓到图片的情况下,才能成功取到图片.
	p_snap->get_history_picture(str_file_name, 1);

	cout << "get history pic" << endl;
#endif

	delete p_snap;

	return 0;
}

