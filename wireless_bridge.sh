#!/bin/bash
killall dhclient
/sbin/ifconfig eth0 0.0.0.0
/sbin/ifconfig wlan1 0.0.0.0
/sbin/brctl addbr br0
/sbin/brctl addif br0 eth0
/sbin/brctl addif br0 wlan1
dhclient br0

