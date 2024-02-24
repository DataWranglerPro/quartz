
# Uninstall Distro
``` sh
wsl --list
wsl --unregister kali-linux
```

# PowerShell
- wsl --list --verbose
- wsl --list --online
- wsl --install -d kali-linux

Err:1 http://kali.download/kali kali-rolling InRelease
sudo nano /etc/apt/sources.list

FROM:
deb http://http.kali.org/kali kali-rolling main non-free contrib

TO:
deb https://kali.download/kali kali-rolling main contrib non-free

ctrl+x
y
enter

# Run these commands for key signature errors:
$ sudo apt remove kali-archive-keyring
$ sudo apt update -oAcquire::AllowInsecureRepositories=true
$ sudo apt install kali-archive-keyring


# Update Kali
``` sh
sudo apt-get clean 
sudo apt-get update 
sudo apt-get upgrade -y 
```


# to shutdown vm:
``` sh
wsl --shutdown
wsl -l -v
```

 
# getting bridge mode (does not work)
- loginto kali
- run commands
``` sh
sudo rm /etc/resolv.conf
sudo bash -c 'echo "nameserver 8.8.8.8" > /etc/resolv.conf'
sudo bash -c 'echo "[network]" > /etc/wsl.conf'
sudo bash -c 'echo "generateResolvConf = false" >> /etc/wsl.conf'
sudo chattr +i /etc/resolv.conf
```
- git clone https://github.com/pawelgnatowski/WSL2-Network-Fix.git
