#!/bin/sh
i=1
sum=0
while [ $i -le 50 ]
do
    echo 'looking for prog_tof_app pid, try times: '$i
    let i++
    ps -ef | grep tof | grep -v grep | awk '{print $1}'
    echo 'killing tof_app_proc'
	....ps查找tof进程并反向筛选掉包含grep的进程，然后awk执行print $1返回的结果即pid，xargs将前面的pid加到kill -9的后面，进行杀进程
    ps -ef | grep tof | grep -v grep | awk '{print $1}' | xargs kill -9
    sleep 1s
    echo 'restart tof app'
	....nohup 不挂断运行prog_tof_app，并一直输出到null里面，即不输出，&表示在后台运行，即使当前prog_tof_app是独立在后台继续运行的进程
    nohup /customer/prog_tof_app >> /dev/null &
    sleep 120s
done


