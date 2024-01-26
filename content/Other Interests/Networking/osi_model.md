OSI means Open Systems Interconnection. It is a conceptual framework on how application communicate over a network. Note that we use the TCP/IP model in practice but the OSI model is still used for planning, marketing, explaining, and troubleshooting. The OSI model still influences how network engineers think and talk about networks.

| Layers  | Description  |
|---|---|
|7|Application|
|6|Presentation|
|5|Session|
|4|Transport|
|3|Network|
|2|Data Link|
|1|Physical|
# Layers

- **Application**
	- Closest to the end user
	- Interacts with software applications like your web browser
	- HTTP/HTTPS are layer 7 protocols
- **Presentation**
	- Data needs to be translated into a format it can be transferred over the network
	- Layer 6 job is to translate between application and network formats
- **Session**
	- Controls sessions between communicating hosts
	- Establishes, manages, and terminates connections between the local and remote applications
	
Application developers work with Layers 5, 6, and 7 of the OSI model to connect their applications over the network.

- **Transport**
	- Segments and reassembles data for communication between end hosts
	- Breaks large pieces of data into smaller segments which can be more easily send over the network
	- Provides host-to-host communication
- **Network**
	- Provides connectivity between hosts on different networks
	- Provides logical addressing (IP addresses)
	- Provides path selection between source and destination
	- Routers are layer 3 devices
- **Data Link**
	- Provides node-to-node connectivity and data transfer (i.e. PC to switch, switch to router, router to router)
	- Detects and corrects physical layer errors
	- Uses MAC addresses instead of IP addresses (layer 3)
	- Switches are generally layer 2 devices
- **Physical**
	- Voltage levels, maximum transmission distances, physical connectors, cable specifications, etc.
	- Digital bits are converted into electrical (for wired connections) or radio (for wireless connections) signals
 
# Acronyms to help you remember the OSI model
- **A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing
- **P**lease **D**o **N**ot **T**each **S**tudents **P**ointless **A**cronyms