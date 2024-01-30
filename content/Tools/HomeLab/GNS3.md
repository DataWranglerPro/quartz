# Startup
- Please allow the local host and the VM to completely load up before opening or creating a project

# VPCs
**Note: **VPCs are deprecated and it is recommended to use Docker images instead

- How to add an ip address?
	- ip 10.11.12.1/24 10.11.12.254
		- This sets up a subnet of 10.11.12/24, assigns the PC the IP address 10.11.12.1, with a default gateway of 10.11.12.254 (which is the ip of router)
- How to show current ip configuration?
	- show ip
- How to save configuration on VPC?
	- save
	- Note: If you do not save the configuration, it will be erased when you shut down the node
- How to view arp table
	- show arp
- How to change DNS server
	- ip dns \<dns-server\>

# Routing
How to Get Routing Information.
## For Linux
- sudo route -n
- netstat -rn
- ip route list

## For Windows
- route print

## For Mikrotik
- ip route print

## How to set a static route:

For Linux:
- sudo ip route add 20.30.40.0/24 via 192.168.86.144
- sudo ip route add 10.11.12.0/24 via 192.168.86.144

For Windows:
- route ADD 10.11.12.0 MASK 255.255.255.0 192.168.56.1
- route delete 20.30.40.0

For Mikrotik:
- ip route add dst-address=192.168.86.0/24 gateway=10.11.12.254
- ip route add dst-address=192.168.122.0/24 gateway=10.11.12.254
- ip route remove [find gateway="10.11.12.254"]

## How to set a default gateway:
- Linux: route add default gw {IP-ADDRESS} {INTERFACE-NAME}

# Trace IP Address

For Linux:
- Traceroute ENTER_IP_ADDRESS_HERE

# RouterOS

[https://help.mikrotik.com/docs/display/ROS/Getting+started](https://help.mikrotik.com/docs/display/ROS/Getting+started)

Limitations:
- Free edition speed limit = 1Mbit

How to get your CHR (Cloud Hosted Router) licensed?
[https://wiki.mikrotik.com/wiki/Manual:CHR#Free_licenses](https://wiki.mikrotik.com/wiki/Manual:CHR#Free_licenses)

| License | Speed limit | Price |
| ---- | ---- | ---- |
| Free | 1Mbit | FREE |
| P1 | 1Gbit | $45 |
| P10 | 10Gbit | $95 |
| P-Unlimited | Unlimited | $250 |

# Set IP Address
Linux: ifconfig eth0 192.168.86.143 netmask 255.255.255.0 up

Mikrotik:
- ip address add address=10.11.12.254/24 interface=ether2
- ip address add address=20.30.40.254/24 interface=ether3


# Firewall
You need to add NAT rule so that hosts under the router can talk to the internet

- ip firewall nat add chain=srcnat action=masquerade out-interface=ether1
- Ether1 represents the interface facing the internet. The internet knows how to get to this ip, it does not know how to get to the internal ips.

# DNS
For Linux:
- cd into /etc/resolv.conf
- vi resolv.conf
	- nameserver 8.8.8.8
	- Press escape key
		- :x
	- cat resolv.conf to confirm
	- You should now be able to ping google.com


# Redis
- Download redis docker image
	- Redis
- Add to topology
- Right click and edit config
	- Set ip/gw
- Make sure you can ping it from another machine
- Install redis on another machine
- Connect to redis server
	- redis-cli -h 20.30.40.1 -p 6379
	- Type ping to test


# Jupyter Lab
- Start the docker container
	- jupyter lab --ip 0.0.0.0 --no-browser --allow-root
- On another host that can ping this machine
	- 20.30.40.1:8888

# Vboxmanage.exe
/usr/local/lib/python3.6/dist-packages/gns3server/compute/virtualbox

# Qemu
- Download win utitility
	- [https://cloudbase.it/qemu-img-windows/](https://cloudbase.it/qemu-img-windows/)
- Convert from vdi to qcow2
	- qemu-img convert -p -f vdi -O qcow2 Alpine.vdi Alpine.qcow2
	- .\qemu-img convert -p -f vdi -O qcow2 Kali-Linux-2021.3-vbox-amd64-disk001.vdi Kali-Linux-2021.3.qcow2

# VirtualBox
-  How to enable virtualization
	- Cd C:\Program Files\Oracle\VirtualBox
	- VBoxManage modifyvm VM-name --nested-hw-virt on

[https://sites.google.com/view/eangineer](https://sites.google.com/view/eangineer)

To fix gns3 vm issue:
``` sh
sudo dpkg --configure -a
Sudo apt install xubuntu-desktop
```

# Alpine Linux
- How to enable virtualization
	- Cd C:\Program Files\Oracle\VirtualBox
	- VBoxManage modifyvm VM-name --nested-hw-virt on
- A bunch of stuff to get a gui going
- Apk update && apk add gns3-server
- Apk add docker

Set up ssh
``` sh
apk add openssh
apk add openrc
rc-update add sshd
rc-status
/etc/init.d/sshd start
vi /etc/ssh/sshd_config
```

1. Look for #PermitRootLogin prohibit-password
2. Press I in order to activate vi editing mode.
3. Remove the # at the beginning of the line and change prohibit-password to yes:
4. Now save and exit by pressing Esc and then pressing :wq and Enter.

``` sh
service sshd restart
```


# Setup Mikrotik
- Log into router
- Interface
- Type the following commands
	- set 0 name=ether1
	- set 1 name=ether2
	- set 2 name=ether3
	- set 3 name=ether4
- Type print to verify changes

# Kali
- Create a docker image
	- kalilinux/kali
- Add password
	- passwd
- apt-get install curl
- apt-get install apt-transport-https
- apt-get install vim
- apt-get install wget
- wget [http://download.zerotier.com/debian/buster/pool/main/z/zerotier-one/zerotier-one_1.6.6_amd64.deb](http://download.zerotier.com/debian/buster/pool/main/z/zerotier-one/zerotier-one_1.6.6_amd64.deb)
- Apt install ./zerotier-one_1.6.6_amd64.deb
- update-rc.d zerotier-one enable
- service zerotier-one start
- zerotier-cli join XXXXXXXX

Set up ssh
- apt-get install openssh-server
- update-rc.d -f ssh remove
- update-rc.d -f ssh defaults
- /etc/ssh/sshd_config
	- PermitRootLogin yes
- Service ssh restart
- update-rc.d -f ssh enable 2 3 4 5

