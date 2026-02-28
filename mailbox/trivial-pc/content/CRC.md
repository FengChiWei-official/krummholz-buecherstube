---
tags:
  - type/permanent
  - status/evergreen
  - attr/principle
  - topic/learning
aliases:
  - Cyclic Redundancy Check
---
## basis
- [[Modulo-2 Division]]
- [[the Magic Polynomials]]
	> **CRC-32 (乙太網路使用)**：`0x04C11DB7`。它能保證偵測到所有 **1、2、3 位元** 的錯誤，以及所有長度小於 32 的**突發性錯誤 (Burst Errors)**。
	一个长4的多项式，rank为3
## CRC 的極限

雖然 CRC 算力強大，但它有兩個「不能」：

1. **不能修正錯誤**：它只能告訴你「數據壞了」，然後網卡會直接丟棄訊框。這就是為什麼需要 **[[TCP Retransmission]]**（重新傳送）。
2. **不具備安全性**：CRC 不是加密算法。黑客可以修改數據後，計算出一個匹配新數據的 CRC 值。防範竄改需要使用 HMAC 等加密機制。

## 發送端流程 (Transmission: Step-by-Step) 

當你的瀏覽器發出數據，最終到達網路層時： 

1. **數據準備 (Kernel)**：內核將 **[[IP Datagram(IPv4)|IP Datagram]]** 傳遞給網卡驅動程式。
2. **決定多項式 (Standard)**：網卡根據通訊協議（如 IEEE 802.3 乙太網路）選定 **CRC-32** 生成多項式。
3. **位元流移位 (Hardware)**：網卡將數據（Header + Payload）以 **Bit（位元）** 為單位移入 LFSR (移位暫存器)。
	1. 原始数据**在后面补零**，
	2. 补的数量为**多项式的阶数（长度-1）**
4. **執行模 2 除法 (XOR)**：
    - 數據流過時，硬體根據多項式結構自動進行一連串 **XOR 運算**。
5. **生成 FCS (Trailer)**：數據全部移完後，暫存器中剩餘的 32 位元即為 **CRC 餘數**。
6. **封裝發送**：網卡將這 32 位元（长度和**阶数**相当）附加在數據末尾，作為 **[[FCS|FCS (Frame Check Sequence)]]**，並發送至物理介質。 

---

2. 接收端流程 (Reception: Step-by-Step) 

當網卡從物理線路（如 Wi-Fi 或有線電信號）接收到訊框時： 

1. **接收訊框**：網卡接收完整的 **[[Ethernet Frame]]**。
2. **同步計算 (Hardware)**：在數據進入網卡緩衝區的同時，硬體**同步**對收到的整段數據（含 FCS）再次執行相同的 **模 2 除法**。
3. **檢驗餘數**：
    - **餘數為 0**：代表數據在傳輸中沒有位元翻轉（Bit Flip），數據是**完整的**。
    - **餘數不為 0**：代表數據已損毀。
4. **處理決策**：
    - **通過**：網卡剝離 Ethernet Header 和 FCS，將乾淨的 IP 封包傳遞給 **作業系統內核**。
    - **丟棄 (Silent Drop)**：網卡直接**丟棄**損毀的訊框，不會通知 CPU。這就是為什麼 TCP 需要 Retransmission（重傳） 機制。 

---

💡 核心重點 

- **計算位置**：通常在 **[[NIC]]** 硬體中，因為硬體處理 XOR 速度最快。
- **主要目的**：檢測物理層傳輸引發的噪音、電磁干擾或同步問題。 

你想了解為什麼有些高效能網卡會支援 **[[Checksum Offload]]**，讓網卡連內部的 **TCP Checksum** 也順便算掉嗎？ 

---
## **related**：