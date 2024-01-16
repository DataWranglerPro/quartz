# Change MAC Address:
- ifconfig
	- ether = MAC Address
- first disable the interface
	- ifconfig wlan0 down
- ifconfig wlan0 hw ether 00:11:22:33:44:55
	- start with 00
- enable the interface
	- ifconfig wlan0 up
- ifconfig

