┌──(kali㉿LAPTOP-AF9MIU0S)-[~]
└─$ nmap -Pn 50.225.249.5
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-01-26 12:05 EST
Nmap scan report for dc4-ccm-fmg.cb-es.comcast.com (50.225.249.5)
Host is up (0.057s latency).
Not shown: 998 closed tcp ports (conn-refused)
PORT     STATE    SERVICE
541/tcp  open     uucp-rlogin
9999/tcp filtered abyss

# install rlogin
┌──(kali㉿LAPTOP-AF9MIU0S)-[~]
└─$ sudo apt install rsh-client

# Tried to login as root
┌──(kali㉿LAPTOP-AF9MIU0S)-[~]
└─$ rlogin -l root -p 541 50.225.249.5
rcmd: 50.225.249.5: Connection reset by peer

