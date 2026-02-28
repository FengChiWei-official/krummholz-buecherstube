---
tags:
  - type/permanent
  - status/evergreen
  - attr/principle
  - topic/learning
---

## qwq
- **Step 1: Learning (學習)**  
    當一個 [[ETH Frame]] 進入埠口 (Port) 1，交換機會查看其 **Source MAC**。如果表中沒有，就將 `MAC A <-> Port 1` 存入 **CAM Table**（內容定址記憶體表）。
- **Step 2: Flooding (泛洪)**  
    如果 **Destination MAC** 不在表中，交換機會將訊框發送到除來源埠口外的**所有埠口**。
- **Step 3: Filtering & Forwarding (過濾與轉發)**  
    一旦目標 MAC 被學習，下次再有發往該 MAC 的訊框，交換機會直接「過濾」掉其他埠口，僅從對應的特定埠口「轉發」。


---
## **related**：
[[Switch]]