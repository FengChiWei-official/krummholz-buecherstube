---
tags:
	- type/permanent
	- topic/learning
	- attr/map
  - status/evergreen
---

#entity/abstract #cs

## Definition
The Network Abstraction Model is a hierarchical layering architecture that progressively abstracts physical hardware. It decomposes complex network communication into multiple relatively independent layers. Each layer interacts with its adjacent layers through standardized interfaces and protocols, ensuring that higher-level applications do not need to manage the complexities of physical signal transmission or routing.
## [[Term Hyponym|Hyponym]] (The [[TCP-IP]] Stack)
The model is categorized into four primary layers, each with a specific scope:
 - [[Application Layer of Network|Application Layer]]: Process-to-Process communication.
 - [[Transport Layer of Network|Transport Layer]]: Host-to-Host logical connectivity and reliability.
 - [[Internet Layer of Network|Internet Layer]]: Path determination and logical addressing (IP).
 - [[Network Access Layer of Network|Network Access Layer]]: Hardware-specific framing and physical transmission.
The **"Onion-like"** Workflow ([[Encapsulation]])
1. **Data Generation (Application Layer)**
	 * **Request Construction**: A process (e.g., a Browser) generates a RAW HTTP Message.
	 * **Formatting**: The application attaches [[HTTP Header|headers]] (e.g., User-Agent, Content-Type) to the [[HTTP Message]].
	 * **[[System Call]]**: The application triggers a System Call to the [[POSIX]] Sockets API (e.g., `send()`,` write()`). This marks the transition where the data moves from User Space to the OS Kernel (Kernel Space).
2. **Segmentation and Connection (Transport Layer)**
	 * **Segmentation**: The OS Kernel breaks the application data into smaller, manageable [[chunks]] called [[TCP Segment]].
	 * **Encapsulation**: The kernel adds [[TCP Header|TCP Headers]] *(Source/Destination Ports, Sequence Numbers)*.
	 * **Connection Management**: Before data flows, TCP establishes a reliable connection via the [[Three Way Handshake]].
	 * **Resource Management**: The kernel handles **Retransmission** (if a packet is lost) and **Congestion Control** (adjusting speed based on network traffic).
3. IP Packetizing (Internet Layer with [[IP (Protocol)]])
	 * **Encapsulation**: The kernel wraps the TCP Segment into an [[IP Datagram(IPv4)]] (Packet).
	 * **Addressing**: Based on the Routing Table, the kernel fills the [[IP Header]] with Source and Destination [[IP Address|IP Addresses]].
	 * **Protocol ID**: The header is marked with "Protocol 6" to notify the receiver that the payload is TCP.
	 * **TTL Setting**: A [[Time to Live|TTL]] value is set to prevent the packet from looping infinitely in the network.
4. **Data Link Framing (Network Access Layer)**
		Before sending the data to the [[NIC]], the kernel performs the final wrapping:
	 * **ARP Lookup**: The kernel checks the [[ARP]] Cache to find the [[MAC Address]] of the Next Hop (the gateway or the next router).
	 * **Framing**: The IP Packet is encapsulated into an [[Ethernet Frame]].*there are where [[CRC]] happened*.
	 * **Error Detection**: An Ethernet Header ([[MAC Address|MAC Addresses]]) and an [[FCS|FCS (Frame Check Sequence)]] are added to detect data corruption during physical transmission.
## Related
- [[Gin Framework]]
	The **Onion-like** structure in the Gin middleware pattern is a direct conceptual relative to the network stack:
	 * Layering: Just as a packet must pass through the Transport and Internet layers, a web request in Gin passes through "layers" of middleware (Logger, Auth, Recovery).
	 * [[Encapsulation]]: Each middleware can modify the "Context" (adding metadata), similar to how each network layer adds a Header.
	 * Transparency: The final Business Logic (Handler) doesn't need to know how the Auth middleware verified the user, just as the Application Layer doesn't need to know how the Network Access Layer handled the MAC address.
Would you like me to explain the "Decapsulation" process (the reverse flow on the receiving side) or dive deeper into how the POSIX Sockets buffer works?

