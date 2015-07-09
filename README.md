# fgre2015_wifips


we can get the position of the robots from http://robotcontrol.wilab2.ilabt.iminds.be:5056/Robot/LocationsMem


the following link contains the ruby script developed by Vincent
https://www.dropbox.com/s/5rf3hhgduoyqq6a/RobotCTRLComm.rb?dl=0


configure a robot to connect to a management AP.

robot should also have sudo pip install mysql-python

Robot config:
-------------
iwconfig wlan0 mode managed
iwconfig wlan0 essid Fproject_mgmt
ifconfig wlan0 172.16.0.2/24
# ip forward is already enabled. 10.11.17.1 is our mysql server
route add 10.11.17.1 gw 172.16.0.1
ping 10.11.17.1

AP config:
----------
root@zotace2:~# cat hostapd_management.conf
interface=wlan1
driver=nl80211
country_code=BE
ssid=Fproject_mgmt
hw_mode=g
channel=1

ifconfig wlan1 172.16.0.1/24
hostapd /root/hostapd_management.conf

