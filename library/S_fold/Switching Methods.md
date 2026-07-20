---
tags:
  - type/permanent
  - attr/principle
  - topic/learning
  - status/evergreen
---

## qwq

1. 知識點歸類：底層設計哲學

這不只是一個技術參數，它是 **網絡架構 (Network Architecture)** 的最高指導原則。它決定了資源如何分配、數據如何流動。

- **屬於層次**：主要跨越 **實體層 (Layer 1)** 與 **數據鏈路層 (Layer 2)**，但其思想影響到整個 [TCP/IP 棧](https://www.fortinet.com/resources/cyberglossary/tcp-ip)。

2. 技術地位：現代網路的「分水嶺」

它是區分「傳統電信」與「現代網路」的分水嶺：

- **地位一：定義網路類型**。如果你選擇 **電路交換 (Circuit Switching)**，你建構的是電話網；如果你選擇 **分組交換 (Packet Switching)**，你建構的是 Internet。
- **地位二：效能優化的源頭**。所有的網路延遲（Latency）、抖動（Jitter）和丟包（Packet Loss），根源都在於分組交換中的「存儲轉發」與「排隊機制」。

3. 在你筆記中的角色

在你目前整理的筆記（從 MAC、ARP 到 CRC）中，**交換方式是「總綱」**：

- 因為我們採用了 **分組交換**，所以才需要 **[[IP Datagram]]** 進行定址。
- 因為分組在鏈路上共享，所以才需要 **[[CRC]]** 確保每個分段的完整性。
- 因為交換機需要決定分組往哪走，所以才演化出 **[[MAC Learning]]**。

---
## **related**：
