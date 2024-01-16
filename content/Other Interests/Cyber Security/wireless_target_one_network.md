- add parameter --write filename, to spool results
	- files created are (csv, kismet.netxml, cap, kismet.csv)
``` sh
$ sudo airodump-ng --bssid  00:25:F0:77:0D:FC --channel 11 --write test wlan0 

SSID                        PWR RXQ  Beacons    #Data, #/s  CH   MB    ENC    CIPHER  AUTH ESSID
00:25:F0:77:0D:FC  -27   0      48              4          0     11   130   WPA2 CCMP     PSK   tl770dfc                                                                                                                                                      

BSSID                      STATION                   PWR   Rate         Lost    Frames  Notes  Probes
00:25:F0:77:0D:FC  00:02:D1:66:1F:4E   -1       24e- 0      0        4  
```               

# What the columns mean:
- **BSSID** - The MAC address of the target network
- **STATION** - The MAC address of the device connected to the network
- **PWR** - Signal strength
- **Rate** - Rate of speed
- **Lost** - Packets lost
- **Frames** - Frames captured
- **Notes** -  
- **Probes** - Is the device probing for networks
 
- If you need to delete the files written:
``` sh
find  . -name 'Spectrum*' -exec rm {} \;     
```




