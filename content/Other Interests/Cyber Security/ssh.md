# How to connect to ssh?
- ssh USER@IP -p PORT
	- ie. ssh Summer@192.168.86.147 -p 22222

# For older ssh:
- If you see "Unable to negotiate with ip# port 22: no matching key exchange method found
	- ssh ip# -oKexAlgorithms-+diffie-hellman-group1-sha1 -c aes-128-cbc

# Resources
- [https://www.hackingarticles.in/ssh-penetration-testing-port-22/](https://www.hackingarticles.in/ssh-penetration-testing-port-22/)
