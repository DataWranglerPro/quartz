Routers are used to forward traffic between different networks. Switches are used to forward traffic within a LAN.

**WAN (Wide Area Network)** - A network that extends over a large geographical area

# IP Routing Process
For simplicity we will be ignoring Layer 2 (MAC Address) and ARP and only concentrate of the Layer 3.

# If PC1 wanted to send data to PC4, below is the process to make that happen

- Is the destination in the same network?
	- Dest: 192.168.4.1
	- Src: 192.168.1.1
	- Since these two networks are /24 networks, I have highlighted the network address. Since they are different, they are not in the same network. This means PC1 cannot sent the packet directly to PC4 and will need the help of a router.
- PC1 sends the packet to the default gateway (which is normally the router) since the destination IP Address is in another network.
	- In our example, PC1 sends the packet to R1.
- R1 will compare the destination IP Address to its Routing Table
	- The routing table contains a list of destination IP Addresses and how to reach those destinations
		- Example: 192.168.4.0/24 via 192.168.12.2, Gi0/0
			- The destination network followed by the next destination to the path (called next hop) and finally the interface which R1 will send the packet through
- R2 receives the packet since it was the next hop on the list. R2 will compare the destination IP Address to its Routing Table and follow the same process R1 took.
	- In our example the next hop is 192.168.4.0/24 via 192.168.24.4, Gi0/1
		- This means R2 will send the packet to R4
- R4 receives the packet since it was the next hop on the list. R4 will compare the destination IP Address to its Routing Table and follow the same process R1/R2 took.
	- In our example the next hop is 192.168.4.0/24 is directly connected, Gi0/2
		- This means R4 is in the same network as the destination IP Address
		- R4 then sends the packet to Switch4
- Switch4 will then forward the packet to PC4

# Static Routing
A static route is a route you manually configure yourself

- If a router receives an IP Address that does not match any entry in its routing table, it will drop the packet.
- End hosts have a routing table but only needs a Gateway of last resort (default route) so that it can forward traffic to an IP Address not already in its routing table
	- Default Route
		- IP Address = 0.0.0.0
		- Mask = 0.0.0.0
		- The set up above 0.0.0.0/0 covers all possible IP Addresses (0.0.0.0 - 255.255.255.255)

