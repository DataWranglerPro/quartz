- [[networking_basics]]
- [[osi_model]]
- [[TCP_IP_Suite|TCP/IP Suite]]
- [[ethernet_lan_switching]]
- [[static_routing]]
- [[ipv4_addressing]]
- [[ping]]



# Containerlab

## Installation
I am going to install everything inside my wsl Kali Linux image
- Install docker
``` sh
sudo apt update
sudo apt install -y docker.io
docker -v
```
- Install containerlab
``` sh
bash -c "$(curl -sL https://get.containerlab.dev)"
```
- To upgrade
``` sh
sudo -E containerlab version upgrade
```

# Create yml file
- Create folder named clab
``` sh
mkdir ~/clab
cd clab
```
- Create file named apline.clab.yml
``` sh
touch apline.clab.yml
vim apline.clab.yml
```
I had to manually type the info in then ESC shift+ZZ to save and exit

``` yaml
name: apline_connect

topology:
  kinds:
    linux:
      image: alpine:latest
  nodes:
    alpine1:
      kind: linux
    alpine2:
      kind: linux

  links:
    - endpoints: ["alpine1:eth1", "alpine2:eth1"]
```

# Running containerlab
``` sh
sudo containerlab deploy --topo apline.clab.yml
```

Unfortunately I got:
``` sh
└─$ sudo containerlab deploy --topo apline.clab.yml
INFO[0000] Containerlab v0.49.0 started
INFO[0000] Parsing & checking topology file: apline.clab.yml
Error: Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```
- Since I am running Kali in WSL
``` sh
curl -L https://gist.githubusercontent.com/hellt/e8095c1719a3ea0051165ff282d2b62a/raw/1dffb71d0495bb2be953c489cd06a25656d974a4/docker-install.sh | \ [](https://containerlab.dev/install/#__codelineno-11-2)bash

sudo service docker start
```

- Trying containerlab again
``` sh
└─$ sudo containerlab deploy --topo apline.clab.yml
INFO[0000] Containerlab v0.49.0 started
INFO[0000] Parsing & checking topology file: apline.clab.yml
INFO[0000] Could not read docker config: open /root/.docker/config.json: no such file or directory
INFO[0000] Pulling docker.io/library/alpine:latest Docker image
INFO[0001] Done pulling docker.io/library/alpine:latest
WARN[0001] Unable to init module loader: stat /lib/modules/5.15.133.1-microsoft-standard-WSL2/modules.dep: no such file or directory. Skipping...
INFO[0001] Creating lab directory: /home/kali/clab/clab-apline_connect
INFO[0002] Creating container: "alpine2"
INFO[0002] Creating container: "alpine1"
INFO[0003] Creating link: alpine1:eth1 <--> alpine2:eth1
INFO[0003] Adding containerlab host entries to /etc/hosts file
INFO[0003] Adding ssh config for containerlab nodes
```

| # | Name | Container ID | Image | Kind | State | IPv4 Address | IPv6 Address |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| 1 | clab-apline_connect-alpine1 | c23e6177f93d | alpine:latest | linux | running | 172.20.20.3/24 | 2001:172:20:20::3/64 |
| 2 | clab-apline_connect-alpine2 | 36699476f882 | alpine:latest | linux | running | 172.20.20.2/24 | 2001:172:20:20::2/64 |


# Connecting to endpoints
I was not able to log into the Alpines images. I needed to add the Kali user to the docker group.

``` sh
sudo usermod -aG docker $USER
exit
```

Once I reopened Kali, the containerlab was still up and I was not in the Docker group.
``` sh
┌──(kali㉿LAPTOP-AF9MIU0S)-[~]
└─$ groups
kali adm cdrom sudo dip plugdev users docker
```

Now I was able to connect to each alpine machine.
``` sh
┌──(kali㉿LAPTOP-AF9MIU0S)-[~/clab]
└─$ docker exec -it clab-apline_connect-alpine1 sh

/ # whoami
root

┌──(kali㉿LAPTOP-AF9MIU0S)-[~/clab]
└─$ docker exec -it clab-apline_connect-alpine2 sh

/ # whoami
root
```

I have internet access and can ping the other alpine image! amazing
``` sh
┌──(kali㉿LAPTOP-AF9MIU0S)-[~/clab]
└─$ docker exec -it clab-apline_connect-alpine2 sh
/ # whoami
root
/ # ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: seq=0 ttl=55 time=28.917 ms
64 bytes from 8.8.8.8: seq=1 ttl=55 time=27.977 ms
^C
--- 8.8.8.8 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 27.977/28.447/28.917 ms
/ #
/ #
/ # ping 172.20.20.3
PING 172.20.20.3 (172.20.20.3): 56 data bytes
64 bytes from 172.20.20.3: seq=0 ttl=64 time=0.217 ms
64 bytes from 172.20.20.3: seq=1 ttl=64 time=0.143 ms
^C
--- 172.20.20.3 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 0.143/0.180/0.217 ms
```

# Connecting to the outside world
I tried pinging it via my local windows machine but no luck.

TO DO: Try installing zerotier in wsl and see if we can see the network that way


# Commands
- See a summary of the network
``` sh
sudo containerlab inspect
```

- see a visual summary of the topology
	- Open browser in Windows machine
		- i.e. http://localhost:50080/
``` sh
sudo containerlab graph
```

![[Pasted image 20240126155140.png]]

- destroying a lab
``` sh
sudo containerlab destroy --topo apline.clab.yml
```

