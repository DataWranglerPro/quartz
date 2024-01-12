# How to determine if anonymous login is enabled?
- Open msfconsole
- use auxiliary/scanner/ftp/anonymous
- msf auxiliary(anonymous) >set rhosts ENTER_IP_HERE
- msf auxiliary(anonymous) >exploit

![[Pasted image 20240111215914.png]]

Notice the text “Anonymous READ”, this means we can login using:
- user = anonymous
- pass = anonymous (blank or any other password works)

# How do we log in?
- ftp ENTER_IP_HERE
- use “anonymous” for user and just press enter for pass

![[Pasted image 20240111220103.png]]

# You can also connect via your web browser
- ftp://192.168.86.147/
- If you are using Chrome, the browser will try to log in as anonymous user

# How to read a file?
- read ENTER_FILE_NAME_HERE
	- downloaded file is located in root

# How to list files?
- ls, just like linux

# How to change dir?
- cd, just like linux
- cd .., just like linux

# Resources
- https://shahmeeramir.com/penetration-testing-of-an-ftp-server-19afe538be4b
- https://www.cs.colostate.edu/helpdocs/ftp.html


