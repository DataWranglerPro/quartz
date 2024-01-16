# Download and install Virtualbox

## Get Kali Linux VirtualBox image
- https://www.kali.org/get-kali/#kali-virtual-machines

## What version of Kali is installed
``` sh
$ lsb_release -a
```

## Update Kali
``` sh
$ sudo apt-get clean 
$ sudo apt-get update 
$ sudo apt-get upgrade -y 
$ sudo apt-get dist-upgrade -y
```

## Get terminator
``` sh
$ sudo apt-get install terminator
```

## install anaconda
``` sh
bash ~/Downloads/FILE_NAME_GOES_HERE
close shell
conda update conda
conda update anaconda
conda clean -t
conda clean -p
```

## Push all web traffic through tor
- pip3 install requests
- git clone https://github.com/SusmithKrishnan/torghost.git
- cd torghost # go inside the downloaded directory
- chmod +x build.sh
- ./build.sh
- python3 torghost.py --start Torghost
- to go back to normal
	- python3 torghost.py --stop Torghost

## If your internet gets messed up:
- Manually add a nameserver to resolve.conf (this is so you can fetch packages from the Ubuntu repos):
- sudo vi /etc/resolv.conf
- Add nameserver 8.8.8.8 to the file.
- reboot
- Reinstall the network-manager, libnss-resolve, and resolvconf packages:
apt install --reinstall resolvconf network-manager libnss-resolve

## If you need to install guest additions:
- http://download.virtualbox.org/virtualbox/6.1.0_RC1/
- Mount the drive, Devices > Insert Guest additions image
- Open terminal
	- cd /media/cdrom0/
	- sudo sh ./VBoxLinuxAdditions.run
- reboot machine

