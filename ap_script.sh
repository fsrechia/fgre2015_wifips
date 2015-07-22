#!/bin/bash

interface=wlan0
driver=nl80211
country_code=BE
ssid=`hostname | awk 'BEGIN { FS = "." } ; { print $1 }'`_${interface}
hw_mode=g
channel=1

filename=/root/ap_cfg_${ssid}.cfg

echo "Configuring AP on iface: ${interface}, driver: ${driver}, country: ${country_code}"
echo "ssid: ${ssid}"
echo "hw_mode: ${hw_mode}"
echo "channel: ${channel}"


echo "interface=${interface}"           > ${filename}
echo "driver=${driver}"                 >> ${filename}
echo "country_code=${country_code}"     >> ${filename}
echo "ssid=${ssid}"                     >> ${filename}
echo "hw_mode=${hw_mode}"               >> ${filename}
echo "channel=${channel}"               >> ${filename}

echo "Starting AP using generated cfg at: ${filename}"
hostapd ${filename} &
