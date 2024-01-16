# How to download and setup hashcat:
- https://hashcat.net/hashcat/
   - download hashcat binaries
- https://www.7-zip.org/
   - download and install
- unzip the hashcat-6.2.4.7z file with 7zip
- https://www.nvidia.com/Download/index.aspx
   - enter your GPU info, download drivers, and install
   - 471.96-notebook-win10-win11-64bit-international-dch-whql.exe
- https://developer.nvidia.com/cuda-toolkit
   - download the toolkit and install
   - cuda_11.4.2_471.41_win10.exe
- https://hashcat.net/wiki/doku.php?id=timeout_patch
   - create a file called wddm_timeout_patch.reg with the following contents:
```
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\GraphicsDrivers]
"TdrLevel"=dword:00000000
```
- Run this registry file as Administrator and reboot.

# Note about the handshake file:
- The handshake does not contain any information that will help us get the password
- It can only be used to check if a password is valid or not

# Note about WPA password:
- minimum length is 8

# How to crack WPA2:
- /usr/share/hashcat-utils/cap2hccapx.bin test-01.cap wpa2_handshake.hccapx
   - converts to a file named wpa2_handshake.hccapx
- Copy the wpa2.hccapx to hashcat folder in Windows
   - where you have the exe saved
- If you are going to use a wordlist, also add that file in the hashcat folder
- Open command prompt
   - navigate to hashcat directory
- hashcat.exe -I
   - to see gpus available in the computer
   - if using PS, type .\hashcat.exe -I
- hascat.exe -m 2500 -d 2 wpa2_handshake.hccapx passwords.txt  
   - -m 2500 = hash type, tell hashcat to crack WPA/WPA2
   - -d 1 = use device #1, tell hashcat to use GPU
- hashcat.exe -m 2500 -d 2 -a 3 wpa2_handshake.hccapx ?d?d?d?d?d?d?d?d
   - press s to see the status

## To get a hc22000 file:
- https://hashcat.net/cap2hashcat/

``` sh
.\hashcat.exe -m 22000 -d 2 wpa2_handshake.hc22000 mywordlist.txt
.\hashcat.exe -a 3 -m 22000 -d 2 wpa2_handshake.hc22000 ?d?d?d?d?d?d?d?d?d?d
```

## More ways to send passwords to hashcat:
``` sh
.\hashcat.exe -m 22000 -d 2 -r rules/best64.rule spectrum.hc22000 rockyou.txt
```

``` sh
crunch 8 8 | john --stdin --session=my_session --stdout | hashcat -m 2500 -d 1 Jobs\BDO_firemni_wifi\handshake04.hccapx 
```
