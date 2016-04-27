#!/bin/sh

while [ true ]
do
    python /root/SBUCourseMonitor/notifyer.py > notify.log
    echo "notify rn"
    sleep 300
done
