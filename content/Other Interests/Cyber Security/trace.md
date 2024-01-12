- Determine if TRACE is available
```
(base) root@kali:~# nmap -p80 --script http-methods,http-trace --script-args http-methods.retest 192.168.86.154  
Starting Nmap 7.80 ( https://nmap.org ) at 2020-04-08 16:03 EDT  
Nmap scan report for 192.168.86.154  
Host is up (0.00060s latency).  
  
PORT   STATE SERVICE  
80/tcp open  http  
| http-methods:   
|   Supported Methods: HEAD GET POST OPTIONS TRACE  
|   Potentially risky methods: TRACE  
|   Status Lines:   
|     POST: HTTP/1.1 200 OK  
|     TRACE: HTTP/1.1 200 OK  
|     GET: HTTP/1.1 200 OK  
|     OPTIONS: HTTP/1.1 200 OK  
|_    HEAD: HTTP/1.1 200 OK  
|_http-trace: TRACE is enabled  
MAC Address: 08:00:27:BF:52:95 (Oracle VirtualBox virtual NIC)
```

- Try to pull out information using telnet
	- type the following after you connect
```
_TRACE / HTTP/1.1  
Host: foo.bar  
X-Header: test_
```
**See the code in action below:**
```
(base) root@kali:~# telnet 192.168.86.154 80  
Trying 192.168.86.154...  
Connected to 192.168.86.154.  
Escape character is '^]'.  
TRACE / HTTP/1.1  
Host: foo.bar  
X-Header: test
```
- Try to pull out info using nc
	- curl -X TRACE 192.168.86.154
	- curl -X TRACE -H "X-Header: test" 192.168.86.154

