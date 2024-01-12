- Find DNS servers
	- dig +short ns ENTER_URL_HERE
- Initiate an AXFR request to get a copy of the zone from the primary server
	- dig axfr ENTER_URL_HERE @ENTER_URL_FROM_STEP_01

- **Resources:**
	- https://www.acunetix.com/blog/articles/dns-zone-transfers-axfr/
