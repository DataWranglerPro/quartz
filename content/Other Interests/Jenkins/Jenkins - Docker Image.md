Here are the steps to get Jenkins up and running using Docker and [[Containerlab]].

- Open up your Kali or Linux distro
- Create a containerlab file
``` sh
touch cicd.clab.yml
```
- Open the .yml file and add the following code
	- vim cicd.clab.yml

``` sh
name: cicd_topo

topology:
  nodes:
    jenkins:
      kind: linux
      image: jenkins/jenkins
      ports:
        - 8080:8080
```

For some reason I had to restart the Docker service.
``` sh
└─$ sudo service docker start
Starting Docker: docker.
```

- Start containerlab using the yml file we just created
``` sh
└─$ sudo containerlab deploy --topo cicd.clab.yml
INFO[0000] Containerlab v0.51.1 started
INFO[0000] Parsing & checking topology file: cicd.clab.yml
INFO[0000] Creating docker network: Name="clab", IPv4Subnet="172.20.20.0/24", IPv6Subnet="2001:172:20:20::/64", MTU='ל'
WARN[0000] errors during iptables rules install: not available
INFO[0000] Could not read docker config: open /root/.docker/config.json: no such file or directory
INFO[0000] Pulling docker.io/jenkins/jenkins:latest Docker image
INFO[0014] Done pulling docker.io/jenkins/jenkins:latest
WARN[0014] Unable to init module loader: stat /lib/modules/5.15.133.1-microsoft-standard-WSL2/modules.dep: no such file or directory. Skipping...
INFO[0014] Creating lab directory: /home/kali/clab/clab-cicd_topo
INFO[0015] Creating container: "jenkins"
INFO[0015] Adding containerlab host entries to /etc/hosts file
INFO[0015] Adding ssh config for containerlab nodes
```

| #   | Name                   | Container ID | Image           | IPv4 Address   |
| --- | ---------------------- | ------------ | --------------- | -------------- |
| 1   | clab-cicd_topo-jenkins | 977474949fd1 | jenkins/jenkins | 172.20.20.2/24 |

When I navigate to http://localhost:8080/ I get the following message.

![[Pasted image 20240512091236.png]]

- Let's shell into the docker image and get that password.
``` sh
┌──(kali㉿LAPTOP-AF9MIU0S)-[~/clab]
└─$ sudo docker exec -it clab-cicd_topo-jenkins sh
$ cat /var/jenkins_home/secrets/initialAdminPassword
24667f370db24643bc5143969782497a
```

![[Pasted image 20240512091649.png]]


I then clicked the **Start using Jenkins** button as shown above and we are in!


![[Pasted image 20240512091729.png]]