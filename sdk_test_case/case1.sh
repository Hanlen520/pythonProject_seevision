#!/bin/bash
i=1
sum=0
nohup ./svcam3dn_sim_tm 192.168.0.200 192.168.0.201 >./log/device_running_log_0_MAIN.log 2>&1 &
sleep 3s
while [ $i -le 5 ]
do
    echo 'test times: '$i
    nohup ./svcam3dn_sim_tm 192.168.0.200 192.168.0.201 >./log/device_running_log_$i.log 2>&1 &
    let i++
    sleep 10s
    ps -ef | grep svc | grep -v grep | awk '{print $2}' | sed -n '2p'
    ps -ef | grep svc | grep -v grep | awk '{print $2}' | sed -n '2p' | xargs kill -9
    echo 'run second sdk program done'
done
echo 'All test finished!, close first main sdk process now!'
ps -ef | grep svc | grep -v grep | awk '{print $2}' | xargs kill -9


