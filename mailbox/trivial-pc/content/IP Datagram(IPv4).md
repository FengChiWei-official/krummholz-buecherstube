---
tags:
  - type/permanent
  - status/evergreen
  - attr/principle
  - topic/learning
aliases:
  - IP Datagram
---
## length
[[MTU]] is `1500Bytes`.
for `header` is `20Bytes`, data limited by `1480Byte`.
## structure
1. [[IP Header]]
2. Data
## IP Datagram 的生命週期 (Lifecycle)

1. **Encapsulation（封裝）**：  
    內核將 TCP Segment 加上 IP Header，形成 Datagram。
2. **Routing（路由選擇）**：  
    路由器讀取 **Destination IP**，查詢路由表決定下一跳（Next Hop）。
3. **Fragmentation（分片，可選）**：  
    如果 Datagram 大於路徑上的 MTU (最大傳輸單元)，路由器或主機會將其切割。
4. **Reassembly（重組）**：  
    分片後的 Datagram 只有在到達**最終目的地**後，才會由目標主機的內核根據 _Identification_ 欄位進行重組。


---
## **related**：
[[IP Header]]