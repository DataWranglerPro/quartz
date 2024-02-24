# Installing ZeroTier in Kali Linux

``` sh
curl -s https://install.zerotier.com | sudo bash
```

You will then get this error:
``` sh
*** Enabling and starting ZeroTier service...
Synchronizing state of zerotier-one.service with SysV service script with /usr/lib/systemd/systemd-sysv-install.
Executing: /usr/lib/systemd/systemd-sysv-install enable zerotier-one
System has not been booted with systemd as init system (PID 1). Can't operate.
Failed to connect to bus: Host is down

*** Package installed but cannot start service! You may be in a Docker
*** container or using a non-standard init service.
```

It will complain about some package named libssl.so.1.1:
``` sh
└─$ service zerotier-one restart
Restarting ZeroTier One: zerotier-oneStopping ZeroTier One: zerotier-one.
Starting ZeroTier One: zerotier-one/usr/sbin/zerotier-one: error while loading shared libraries: libssl.so.1.1: cannot open shared object file: No such file or directory
 failed!
```

So just get it installed:
``` sh
wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb
sudo dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb
```
Start the service:
``` sh
└─$ sudo service zerotier-one start
Starting ZeroTier One: zerotier-one.
```

Connect to your network:
``` sh
sudo zerotier-cli join NETWORK_ID
200 join OK
```

