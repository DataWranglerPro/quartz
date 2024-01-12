# What is Cloudflare?
CloudFlare protects and accelerates any website online. Once your website is a part of the CloudFlare community, its web traffic is routed through our intelligent global network. We automatically optimize the delivery of your web pages so your visitors get the fastest page load times and best performance. We also block threats and limit abusive bots and crawlers from wasting your bandwidth and server resources. The result: CloudFlare-powered websites see a significant improvement in performance and a decrease in spam and other attacks.  
  
This service will hide the real IP address behind one or many Cloudflare IPs. This means when you run a nmap scan on a Cloudflare site, you are actually scanning Cloudflare and not the actual target.  

# How to detect Cloudflare?  
- ping ENTER_YOUR_DOMAIN_HERE
	- Navigate to the site using the IP number  
  
![[Pasted image 20240110220122.png]]
  
- curl -I ENTER_URL_HERE  
![[Pasted image 20240110220350.png]]
  
- nmap scans will return cloudflare references  
	PORT STATE SERVICE VERSION  
	80/tcp open http cloudflare  
  
- nikto -h ENTER_IP_ADDRESS_HERE  
	\+Server: cloudflare  
  
# How do we find the targets real IP?  
- Use 3rd party websites  
	- [https://securitytrails.com/](https://securitytrails.com/)  
		- Go to the “Historical Data” Block.  
		- Go to the “Historical Data” Block and to the NS tab  
			- dig @targetnameservers targetdomain (ie. dig @ns1.quickserve.com boozt.com)  
	- [https://sitereport.netcraft.com/?url=](https://sitereport.netcraft.com/?url=)  
	- Go to the hosting history section  
	- [http://www.crimeflare.org:82/cfs.html](http://www.crimeflare.org:82/cfs.html)  
	- [https://censys.io](https://censys.io)  
	- [https://www.shodan.io](https://www.shodan.io/)  
	- [https://www.zoomeye.org/](https://www.zoomeye.org/)  
	- [https://suip.biz/?act=domainiphistory](https://suip.biz/?act=domainiphistory)  
	- [http://ptrarchive.com/](http://ptrarchive.com/)  
	- [https://whoisrequest.com/history/](https://whoisrequest.com/history/)  
- dig  
	- dig ANY ENTER_URL_HERE  
		- If you find any odd looking urls, ping them to see if you can find the real ip  
- Send email to target  
	- send a mail to anyfakename@targetdomain.com you may get an error from the real IP address, check the error mail click "Show Original" then search for " Google tried to deliver your message, but it was rejected by the server for the recipient domain targetdomain.com by targetdomain.com. 
- Registering an account  
	- Once you receive an email reply view its source code and search for the sender’s client-IP 
- Using the “forgot password” feature  
	- Once you receive an email reply view its source code and search for the sender’s client-IP 
- Sending a real question or comment through the target site contact form.  
	- Once you receive an email reply view its source code and search for the sender’s client-IP 
- ``` nmap --script dns-brute -sn <target> ```  

# How to edit hosts file to automatically point to real ip address?  
- Windows  
	- c:\\windows\\system32\\drivers\\etc\\ 
- Linux  
	- sudo vim /etc/hosts  
- Edit the "hosts" file and make a DNS entry as shown below  
	- IP followed by the url (ie. 127.0.0.1 locahost)  
  
# Issues for Target Owners  
- It is quite possible to find the real IP address of a web server protected by Cloudflare, but in general if you're using Cloudflare, you want to prevent this at all costs. Even if you use iptables to block all traffic that's not from either your home IP or Cloudflare's IP range, you're still leaving yourself vulnerable to one of the primary reasons to use Cloudflare in the first place: DDoS. If they have your real IP address, it becomes much harder to defend against many kinds of DDoS attacks, especially ones that are bandwidth-based.