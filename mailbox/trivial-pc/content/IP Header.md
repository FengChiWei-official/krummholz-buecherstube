---
tags:
  - type/permanent
  - status/evergreen
  - attr/principle
  - topic/learning
---

## ## frontpage
a standard IPv4 Datagram header is **20Bytes**. there can be Options.
## Fields

| Field                   | length(bits) | 单位     | Available Values         | Description                              |
| ----------------------- | ------------ | ------ | ------------------------ | ---------------------------------------- |
| version                 | 4            | 1      | 4\|6                     | for `IPv4` or `IPv6`                     |
| IHL                     | 4            | 4Bytes | `IHL` $\ge 5$*(20Bytes)* | Header Length                            |
| Type of Service         | 8            | 1      |                          |                                          |
| Total Length            | 16           | Byte   |                          |                                          |
| Identification          | 16           | 1      |                          | for **Reassembly** for all Fragmentation |
| Flags & Fragment Offset | 16           | 1      |                          |                                          |
| TTL                     | 8            | jump   |                          |                                          |
| Protocol                | 8            | 1      | 6(TCP)｜17(UDP)           |                                          |
| Header Checksum         | 16           | 1      |                          |                                          |
| Source IP Address       | 32           | 1      |                          |                                          |
| Destination IP Address  | 32           | 1      |                          |                                          |


## flags

| name               | length | value |         |
| ------------------ | ------ | ----- | ------- |
| Reserved bit       | 1      | 0     | 永远为0    |
| DF(Don't Fragment) | 1      | 0\|1  | 1表示不准分片 |
| MF（More Fragments） | 1      | 0\|1  | 1表示还有分片 |
| Fragment Offset    |        |       |         |

## header for Fragmentation
### Still Fields

1. Identification(16bits):這是分片的「身分證號」。所有來自同一個原始封包的分片，其 Identification 數值必須一致，否則接收端無法重組。
2. **Source / Destination IP**：起點與終點位址。
3. **Protocol**：上層協議（如 TCP 或 UDP）標識。
### Changed Fields


| Fields          | id     |                | Rule                                    |
| --------------- | ------ | -------------- | --------------------------------------- |
| Total Length    | -      | 1Byte          | header included.                        |
| Flags           | MF     | More Fragments | 0: last one 1: there are more fragments |
| Flags           | DF     | Don't Fragment | 0 means allow to fragment.              |
| Fragment Offset | Offset |                | 8Bytes based                            |
| Header Checksum |        |                |                                         |

---
## **related**：
[[IP Datagram(IPv4)|IP Datagram]]