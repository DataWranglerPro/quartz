**Ping** - A network utility that is used to test reachability.

**Command**:
ping IP_ADDRESS_GOES_HERE

**ICMP** - Internet Control Message Protocol

# Here is the ping process:
- ICMP Echo Request - This request is sent to a specific host, it is not broadcasted out.
- ICMP Echo Reply - Reply is only send to requester

When you ping another computer, if the device doing the pinging does not know the MAC Address of the destination IP address, it will need to send an ARP request to all other hosts first.