``` sh
$ iwconfig  
lo no wireless extensions.  
  
eth0 no wireless extensions.  
  
wlan0 unassociated ESSID:"" Nickname:"<WIFI@REALTEK>"  
Mode:Monitor Frequency=2.422 GHz Access Point: Not-Associated  
Sensitivity:0/0  
Retry:off RTS thr:off Fragment thr:off  
Power Management:off  
Link Quality=0/100 Signal level=0 dBm Noise level=0 dBm  
Rx invalid nwid:0 Rx invalid crypt:0 Rx invalid frag:0  
Tx excessive retries:0 Invalid misc:0 Missed beacon:0  
```

# What the columns mean:    
- **BSSID** - MAC address  
- **PWR** - Signal strength of the network. The bigger the number, the closer we are to it  
- **Beacons** - Frames sent by the network to broadcast its existence  
- **\#Data** - Data frames currently being sent by the network  
- **\#/s** - The number of packets collected in the last 10 seconds  
- **CH** - current channel the network works on  
- **MB** - Maximum speed supported by the network  
- **ENC** - Encryption used by the network. OPN means we do not need a password to connect to it.  
- **CIPHER** - cipher used in the network  
- **AUTH** - The kind of authentication used by the network  
- **ESSID** - Name of wireless network  
  
``` sh
$ sudo airodump-ng wlan0  

BSSID PWR Beacons #Data, #/s CH MB ENC CIPHER AUTH ESSID  
  
00:00:00:00:00:00 -1 0 0 0 -1 -1 <length: 0>  
F4:17:B8:0D:72:4C -1 0 0 0 36 -1 <length: 0>  
58:D9:D5:1A:7B:79 -1 0 2 0 1 -1 WPA <length: 0>  
E6:F0:42:E8:13:00 -23 58 0 0 11 130 WPA2 CCMP PSK test-guest  
E4:F0:42:E8:13:00 -23 67 4 0 11 130 WPA2 CCMP PSK test  
00:25:F0:77:0D:FC -26 53 29 0 11 130 WPA2 CCMP PSK tl770dfc  
E4:F0:42:E8:13:6E -43 30 0 0 6 130 WPA2 CCMP PSK test  
E6:F0:42:E8:13:6C -44 43 0 0 6 130 WPA2 CCMP PSK test-guest  
E6:F0:42:E8:13:08 -13 34 0 0 6 130 WPA2 CCMP PSK test-guest  
8C:85:80:82:FC:B8 -48 27 0 0 3 130 WPA2 CCMP PSK <length: 0>  
E4:F0:42:E8:13:0B -70 60 0 0 6 130 WPA2 CCMP PSK test  
D8:07:B6:A9:D8:45 -47 26 1 0 10 270 WPA2 CCMP PSK VR217-FDF0_EXT  
42:2B:50:20:0D:F1 -49 18 0 0 1 195 WPA2 CCMP PSK GreenFamily_Guest  
60:B7:6E:70:8F:B9 -80 22 0 0 6 130 WPA2 CCMP PSK G_ATT7MSvttA  
12:93:97:30:03:F2 -50 7 0 0 1 195 WPA2 CCMP PSK <length: 18>  
A8:9A:93:98:28:0E -52 32 12 0 1 195 WPA2 CCMP PSK MySpectrumWiFi08-2G  
0E:EA:C9:CD:92:C2 -52 3 0 0 1 195 WPA2 CCMP PSK <length: 18>  
40:2B:50:20:0D:F0 -53 21 4 0 1 195 WPA2 CCMP PSK Green Family  
42:2B:50:20:0D:F2 -53 9 0 0 1 195 WPA2 CCMP PSK <length: 18>  
0C:EA:C9:CD:92:C0 -53 5 0 0 1 195 WPA2 CCMP PSK ATTBk4qsKI  
3C:5C:F1:1D:B4:C8 -53 9 0 0 10 360 OPN <length: 0>  
98:1E:19:4C:29:E6 -53 8 0 0 1 195 WPA2 CCMP PSK MySpectrumWiFie0-2G  
7C:DB:98:9B:34:11 -53 6 0 0 1 720 WPA2 CCMP PSK MySpectrumWiFi13-2G  
3C:5C:F1:1D:B4:C6 -53 12 1 0 10 360 WPA2 CCMP PSK thao  
88:71:B1:47:98:40 -53 19 84 0 11 195 WPA2 CCMP PSK ATT7MSvttA  
58:D9:D5:1A:7B:89 -54 26 13 0 11 130 WPA2 CCMP PSK Offner  
3C:5C:F1:1D:B4:C4 -54 8 0 0 10 360 WPA3 CCMP SAE <length: 0>  
88:96:4E:8A:20:70 -55 0 4 0 1 -1 WPA <length: 0>  
C8:B4:22:79:57:47 -55 3 0 0 1 720 WPA2 CCMP PSK TierneyP-2G  
F0:81:75:EF:1C:16 -55 8 3 0 6 195 WPA2 CCMP PSK SpectrumSetup-10  
10:DA:43:1F:3E:BD -56 1 0 0 1 130 WPA2 CCMP PSK NETGEAR08  
C0:25:E9:88:FD:F0 -56 2 1 0 10 270 WPA2 CCMP PSK VR217-FDF0  
F4:17:B8:B5:9C:FB -56 3 0 0 11 130 WPA2 CCMP PSK UNCW4LIFE  
0A:9E:08:FC:F4:10 -58 10 0 0 6 130 WPA3 CCMP SAE bhrshvrtz-guest  
60:D2:48:29:62:D0 -58 23 6 1 11 195 WPA2 CCMP PSK ATTHqJPkcI  
3C:84:6A:C6:B5:F7 -58 11 68 2 9 270 WPA2 CCMP PSK TP-Link_B5F7  
38:94:ED:99:72:D5 -59 2 0 0 1 130 WPA2 CCMP PSK MySpectrumWiFi96-2G_2GEXT  
60:B7:6E:70:92:F2 -60 3 0 0 1 130 WPA2 CCMP PSK G_ATT7MSvttA  
12:62:E5:FA:01:56 -63 2 0 0 36 270 WPA2 CCMP PSK DIRECT-56-HP ENVY Photo 7800  
86:71:B1:47:98:43 -67 2 0 0 36 1733 WPA2 CCMP PSK ATT7MSvttA  
88:71:B1:47:98:43 -67 3 0 0 36 1733 WPA2 CCMP PSK <length: 0>  
58:D9:D5:1A:7B:8C -68 7 1 0 40 866 WPA2 CCMP PSK Offner  
10:93:97:30:03:F3 -70 8 1 0 48 1733 WPA2 CCMP PSK <length: 0>  
06:93:97:30:03:F3 -71 8 2 0 48 1733 WPA2 CCMP PSK ATTAtQia22  
```
  
# To find 5G networks:  
``` sh
sudo airodump-ng --band a wlan0  
```
  
# To find 2G and 5G networks:  
``` sh
sudo airodump-ng --band abg wlan0  
  
BSSID PWR Beacons #Data, #/s CH MB ENC CIPHER AUTH ESSID  
  
00:00:00:00:00:00 -1 0 0 0 -1 -1 <length: 0>  
E4:F0:42:E8:12:FC -12 7 0 0 149 866 WPA2 CCMP PSK test  
E6:F0:42:E8:12:FD -13 1 0 0 149 866 WPA3 CCMP SAE <length: 0>  
E6:F0:42:E8:12:FC -13 8 0 0 149 866 WPA2 CCMP PSK test-guest  
E4:F0:42:E8:13:07 -29 5 0 0 149 866 WPA2 CCMP PSK test  
E6:F0:42:E8:13:04 -29 7 0 0 149 866 WPA2 CCMP PSK test-guest  
E6:F0:42:E8:13:68 -54 6 0 0 149 866 WPA2 CCMP PSK test-guest  
E4:F0:42:E8:13:6A -54 7 0 0 149 866 WPA2 CCMP PSK test  
E6:F0:42:E8:13:69 -57 1 0 0 149 866 WPA3 CCMP SAE <length: 0>  
3C:5C:F1:1D:B4:C5 -70 0 0 0 -1 -1 <length: 0>  
86:9D:7D:51:9C:B3 -71 8 2 0 108 1733 WPA2 CCMP PSK ATT235UWQs  
90:9D:7D:51:9C:B3 -71 8 1 0 108 1733 WPA2 CCMP PSK <length: 0>  
62:B7:6E:70:8F:B5 -72 1 14 0 149 866 WPA3 CCMP SAE <length: 0>  
60:B7:6E:70:8F:B5 -72 8 13 0 149 866 WPA2 CCMP PSK G_ATT7MSvttA  
62:B7:6E:8E:93:B9 -76 0 11 0 149 -1 WPA <length: 0>  
60:B7:6E:8E:93:B9 -76 7 6 0 149 866 WPA2 CCMP PSK G_ATT7MSvttA  
62:B7:6E:70:8E:C1 -77 0 11 0 149 -1 WPA <length: 0>  
60:B7:6E:70:8E:C3 -82 8 10 0 149 866 WPA2 CCMP PSK G_ATT7MSvttA  
E6:F0:42:E8:13:05 -83 0 0 0 -1 -1 <length: 0>  
62:B7:6E:70:92:ED -83 0 2 0 149 -1 WPA <length: 0>  
60:B7:6E:70:92:EE -84 1 7 0 149 866 WPA2 CCMP PSK G_ATT7MSvttA  
A8:9A:93:98:28:0F -85 14 4 0 36 1733 WPA2 CCMP PSK MySpectrumWiFi08-5G  
E4:F0:42:E8:13:00 0 49 7 0 11 130 WPA2 CCMP PSK test  
F4:17:B8:0D:72:4C -1 0 2 0 36 -1 WPA <length: 0>  
E6:F0:42:E8:13:00 -23 25 0 0 11 130 WPA2 CCMP PSK test-guest  
00:25:F0:77:0D:FC -23 51 7 0 11 130 WPA2 CCMP PSK tl770dfc  
E4:F0:42:E8:13:6E -43 20 0 0 6 130 WPA2 CCMP PSK test  
58:D9:D5:1A:7B:89 -47 24 3 0 11 130 WPA2 CCMP PSK Offner  
E4:F0:42:E8:13:0B -48 50 0 0 6 130 WPA2 CCMP PSK test  
E6:F0:42:E8:13:08 -48 49 0 0 6 130 WPA2 CCMP PSK test-guest  
60:B7:6E:70:8F:B9 -49 13 0 0 6 130 WPA2 CCMP PSK G_ATT7MSvttA  
F0:81:75:EF:1C:16 -49 12 4 0 6 195 WPA2 CCMP PSK SpectrumSetup-10  
60:B7:6E:70:8E:C7 -51 16 0 0 6 130 WPA2 CCMP PSK G_ATT7MSvttA  
A8:9A:93:98:28:0E -52 25 11 0 1 195 WPA2 CCMP PSK MySpectrumWiFi08-2G  
88:71:B1:47:98:40 -52 23 5 0 11 195 WPA2 CCMP PSK ATT7MSvttA  
A6:97:5C:78:12:44 -53 3 0 0 6 65 WPA2 CCMP PSK VTECH_5754_1244  
D8:07:B6:A9:D8:45 -54 25 0 0 10 270 WPA2 CCMP PSK VR217-FDF0_EXT  
60:B7:6E:8E:93:BD -54 13 9 0 6 130 WPA2 CCMP PSK G_ATT7MSvttA  
3C:5C:F1:8B:20:06 -55 3 0 0 10 360 OPN <length: 0>  
3C:5C:F1:1D:B4:C8 -56 4 0 0 10 360 OPN <length: 0>  
08:9E:08:FC:F4:11 -57 4 1 0 6 130 WPA3 CCMP SAE bhrshvrtz  
E8:ED:05:68:F7:D0 -57 2 0 0 6 195 WPA2 CCMP PSK Millie  
A4:11:62:B4:1B:02 -59 13 0 0 6 130 WPA2 CCMP PSK ARLO_VMB_5579447858  
F4:17:B8:3A:5C:B9 -59 2 0 0 11 130 WPA2 CCMP PSK ATTE3dkYs2
```

