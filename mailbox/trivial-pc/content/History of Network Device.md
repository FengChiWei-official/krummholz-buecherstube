---
tags:
  - type/permanent
  - status/evergreen
  - attr/principle
  - topic/learning
---

## Linking Devices
### [[Hub]]

2. 接線器 / 集線器 (Hub) —— Layer 1 (Physical Layer)

「接線器」通常指傳統的 **Hub (集線器)**，它完全沒有「演算法」可言，屬於 **實體層 (Physical Layer)**。

- **運作邏輯**：**盲目廣播 (Blind Flooding / Repeating)**。
- **運作機制**：
    - 它只是物理電信號的「複製器」。
    - 當一個訊號從 Port A 進來，它會不加思考地將電壓訊號複製到**所有其他連接埠**。
- **特性**：所有連接的設備都在同一個碰撞網域。如果有兩個人同時講話，訊號就會在物理層直接發生「碰撞 (Collision)」。

### [[Switch]] 
1. 交换機 (Switch) —— Layer 2 (Data Link Layer)

交換機的運作邏輯（即其演算法）屬於 **數據鏈路層 (Data Link Layer)**。

- **核心演算法**：**MAC 地址學習與過濾 ([[MAC Learning & Filtering]])**。
- **運作機制**：
    - 交換機內部維護一張 **MAC 地址表 (CAM Table)**。
    - 它會檢查傳入 [[ETH Frame]] 的 **Destination MAC**。
    - **演算法決策**：根據表項決定要將訊框從哪個特定連接埠（Port）轉發出去，還是直接丟棄。
- **特性**：它能隔離 **碰撞網域 (Collision Domain)**，讓多個設備可以同時收發而不互相干擾。

---

📝 對比總結 (Layer Comparison)

|設備|英文|運作層次|處理單位|核心邏輯|
|---|---|---|---|---|
|**交換機**|**Switch**|**Layer 2**|**[[ETH Frame]]**|根據 **MAC 地址** 進行精準轉發。|
|**集線器**|**Hub**|**Layer 1**|**Bits (0/1)**|物理電信號的**全體廣播**。|
### [[Router]]


---
## **related**：