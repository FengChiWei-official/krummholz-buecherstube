---
tags:
  - type/permanent
  - topic/learning
  - status/archive
  - attr/concept
aliases:
  - Address Resolution Protocol
---
## Belonging
between [[Network Access Layer of Network|Network Access Layer]] and [[Internet Layer of Network|Internet Layer]]
## Define
ARP (Address Resolution Protocol) is the **"glue"** that connects the **Internet Layer ([[IP Address]])** to the **Network Access Layer ([[MAC Address]])**. It allows a host to discover the hardware identity of a neighbor using only its logical IP address.

## Basis
It is running in [[OS Kernel]]
## Steps
all data are sent by [[Ethernet Frame]]
1. check [[ARP Cache]]
2. send [[ARP Request]] (*[[Broadcast]]*)
3. get [[ARP Reply]] (*[[Unicast]]*）
4. update [[ARP Cache]]
**NOTE**： ARP won't be used when `Target IP` not in **Local Network**.

## Datagram
### Request
```
Ethernet II (Link Layer Header)
├─ Destination: ff:ff:ff:ff:ff:ff (Broadcast)
├─ Source:      aa:bb:cc:dd:ee:05 (Sender's MAC)
└─ Type:        0x0806 (ARP)

Address Resolution Protocol (ARP Message)
├─ Hardware type:        Ethernet (1)
├─ Protocol type:        IPv4 (0x0800)
├─ Hardware size:        6 bytes
├─ Protocol size:        4 bytes
├─ Opcode:               Request (1)
├─ Sender MAC address:   aa:bb:cc:dd:ee:05
├─ Sender IP address:    192.168.1.5
├─ Target MAC address:   00:00:00:00:00:00 (Placeholder)
└─ Target IP address:    192.168.1.1

```

**raw ARP Message**
```
# Ethernet Header (Dest MAC: Broadcast, Source MAC, Type: ARP)
ff ff ff ff ff ff  aa bb cc dd ee 05  08 06

# ARP Message (Hardware Type, Protocol, Sizes, Opcode: Request)
00 01  08 00  06  04  00 01

# Addresses (Sender MAC, Sender IP, Target MAC [Zeroes], Target IP)
aa bb cc dd ee 05  c0 a8 01 05 
00 00 00 00 00 00  c0 a8 01 01
```

### Reply
```
[ Ethernet Frame Header ]
Target MAC:   aa:bb:cc:dd:ee:05 (The host that asked)
Source MAC:   00:11:22:33:44:55 (The Gateway/Responder)
EtherType:    0x0806 (ARP)

[ ARP Payload ]
Hardware Type:       0x0001 (Ethernet)
Protocol Type:       0x0800 (IPv4)
Hardware Size:       0x06
Protocol Size:       0x04
Opcode:              0x0002 (Reply)
Sender MAC Address:  00:11:22:33:44:55 (The answer!)
Sender IP Address:   192.168.1.1       (Gateway IP)
Target MAC Address:  aa:bb:cc:dd:ee:05 (Host MAC)
Target IP Address:   192.168.1.5       (Host IP)

```
**raw**
```
# Ethernet Header (Dest MAC: Host, Source MAC: Gateway, Type: ARP)
aa bb cc dd ee 05  00 11 22 33 44 55  08 06

# ARP Message (Hardware Type, Protocol, Sizes, Opcode: Reply)
00 01  08 00  06  04  00 02

# Addresses (Sender is now Gateway, Target is now Host)
00 11 22 33 44 55  c0 a8 01 01 
aa bb cc dd ee 05  c0 a8 01 05

```

## E.g.
**Scenario**: Host A (`192.168.1.5`) wants to send an HTTP request to Host B (`192.168.1.10`) on the same Local Area Network (LAN). 

1. **Check [[ARP Cache]]**:  
    Host A checks its internal table. If no entry for `192.168.1.10` exists, it triggers the resolution process.
2. **Send [[ARP Request]]**:  
    Host A sends a **Broadcast Frame** to the network:
    - **Source MAC**: `AA:BB:CC:11:22:33` (Host A)
    - **Destination MAC**: `FF:FF:FF:FF:FF:FF` (**Everyone**)
    - **Message**: "Who has IP `192.168.1.10`? Tell `192.168.1.5`."
3. **Get [[ARP Reply]]**:  
    Host B recognizes its IP and sends a **Unicast Frame** back to Host A:
    - **Source MAC**: `DD:EE:FF:44:55:66` (Host B)
    - **Destination MAC**: `AA:BB:CC:11:22:33` (Host A)
    - **Message**: "I am `192.168.1.10`, and my MAC is `DD:EE:FF:44:55:66`."
4. **Update [[ARP Cache]]**:  
    Host A saves the mapping: 
	    `192.168.1.10` $\to$ `DD:EE:FF:44:55:66`. 
    Now the Ethernet Frame can be fully encapsulated and sent.

---

## **related**：
