Notes on the Jenkins file system.

# Shell into Docker image
We will first need to shell into the docker image Jenkins is running in.

- Steps to get Jenkins running in docker below
	- [[Jenkins - Docker Image]]

``` sh
┌──(kali㉿LAPTOP-AF9MIU0S)-[~/clab]
└─$ sudo docker exec -it clab-cicd_topo-jenkins sh
$ ls
bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```

- now we cd into our jenkins_home directory
``` sh
$ cd /var/jenkins_home
$ ls -ltra
total 88
drwxr-xr-x  1 root    root    4096 May  7 15:20 ..
-rw-r--r--  1 jenkins jenkins   50 May 12 13:04 copy_reference_file.log
drwxr-xr-x 10 jenkins jenkins 4096 May 12 13:04 war
drwxr-xr-x  3 jenkins jenkins 4096 May 12 13:04 .cache
drwxr-xr-x  3 jenkins jenkins 4096 May 12 13:04 .java
-rw-r--r--  1 jenkins jenkins   64 May 12 13:04 secret.key
-rw-r--r--  1 jenkins jenkins    0 May 12 13:04 secret.key.not-so-secret
drwxr-xr-x  2 jenkins jenkins 4096 May 12 13:04 plugins
-rw-r--r--  1 jenkins jenkins  156 May 12 13:04 hudson.model.UpdateCenter.xml
-rw-r--r--  1 jenkins jenkins  171 May 12 13:04 jenkins.telemetry.Correlator.xml
drwxr-xr-x  2 jenkins jenkins 4096 May 12 13:04 userContent
-rw-r--r--  1 jenkins jenkins 1037 May 12 13:04 nodeMonitors.xml
drwxr-xr-x  3 jenkins jenkins 4096 May 12 13:04 users
-rw-r--r--  1 jenkins jenkins    0 May 12 13:05 .lastStarted
drwxr-xr-x  2 jenkins jenkins 4096 May 12 13:05 updates
-rw-r--r--  1 jenkins jenkins 1758 May 12 13:15 config.xml
-rw-r--r--  1 jenkins jenkins    5 May 12 13:16 jenkins.install.UpgradeWizard.state
-rw-r--r--  1 jenkins jenkins    5 May 12 13:16 jenkins.install.InstallUtil.lastExecVersion
-rw-r--r--  1 jenkins jenkins    1 May 13 14:25 .owner
drwxr-xr-x  3 jenkins jenkins 4096 May 13 15:06 jobs
drwxr-xr-x  3 jenkins jenkins 4096 May 13 15:16 workspace
-rw-r--r--  1 jenkins jenkins  258 May 13 15:17 queue.xml
drwxr-xr-x 12 jenkins jenkins 4096 May 13 15:17 .
drwx------  2 jenkins jenkins 4096 May 13 15:17 secrets
```

- To see where our jobs are located, we need to go to the workspace folder

In my test instance, I have created one [[Jenkins - Freestyle Jobs|Freestyle project]] named "test_david". Notice how Jenkins creates a folder with the same name as your project. 

> [!NOTE]
> **Pro Tip:** Do not include spaces in your project names as these will be used to create folders

``` sh
$ cd workspace
$ ls -ltra
total 12
drwxr-xr-x  2 jenkins jenkins 4096 May 13 15:16 test_david
drwxr-xr-x  3 jenkins jenkins 4096 May 13 15:16 .
drwxr-xr-x 12 jenkins jenkins 4096 May 13 15:17 ..
```
I won't cd into the test_david folder as it will be empty. If I created any files, those will show up there. 

- Folders/files of interest
	- **plugins** - This folder contains installed Jenkins plugins
	- **updates** - where all the updates go and may be used to troubleshoot update errors
	- **users** - This folder contains user data, including user settings and configurations
	- **workspace** - This folder contains the workspace for building and running jobs
	- **secrets** - This folder contains encrypted secrets, such as credentials and API keys
	- **jobs** - This folder is frequently accessed by Jenkins admins to manage and configure jobs
	- **config.xml** - This file is frequently edited by Jenkins admins to configure Jenkins settings.

