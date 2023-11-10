#!/bin/bash

#ping the router to check the wifi connection
/bin/ping -c2 192.168.1.1

# if exit code ($?) of the ping command is failed (not 0) then reconnect
if  [ $? != 0 ]
then

	sudo /sbin/ifconfig wlan0 down
	sleep 30
	sudo /sbin/ifconfig wlan0 up
	echo 'try wlan up'
fi
