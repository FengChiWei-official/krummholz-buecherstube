---
tags:
  - type/permanent
  - status/evergreen
  - attr/principle
  - topic/learning
aliases:
  - EUI-48
---

## definition
a **Physical Identity** for [[NIC]].

## How does it looks like?
it is **48bits integer**(6bytes).


|       | [[OUI]] | [[NIC Specific]] |
| ----- | ------- | ---------------- |
| range | 0~24    | 24~48            |
| owner | IEEE    | Companies        |
|       |         |                  |


---

在計算機科學中，位址長度的設計通常是在「定址空間」與「硬體開銷」之間取得平衡。以下是為什麼選擇 48 位元的技術原因： 

1. 2^n 的字節對齊 (Byte Alignment) 

計算機處理數據是以 **Byte (8-bit)** 為最小單位。 

- 48 bits = **6 Bytes**。
- 雖然它不是 2、4、8 這種「2 的次方數」個字節，但它符合 8 的倍數，方便硬體電路進行偏移計算和存儲。
- 在 1970 年代 Xerox PARC 開發乙太網路時，32 位元被認為太短（僅 42 億個地址，容易重複），而 64 位元在當時的硬體資源下顯得過於浪費空間。 

2. 龐大的定址空間 (Address Space) 

![](data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==)

$2^{48}$ 是一個天文數字，大約等於 **281 兆 (281 Trillion)** 個唯一地址。 

- 這足以為地球上每個人分配超過 35,000 個裝置。
- 這種設計確保了在全球範圍內，任何兩張網卡的 MAC 位址衝突機率幾乎為零。 

3. 分層管理架構 (OUI + NIC) 

48 位元被精確地平分為兩半，這有利於行政管理： 

- **前 24 bits (OUI)**：交由 IEEE Registration Authority 管理，分配給廠商。
- **後 24 bits**：由廠商自行管理。
- 如果縮短到 32 位元，廠商能分配的地址就會變得極其有限，迫使廠商頻繁申請新的 OUI，增加管理成本。 

4. 歷史與相容性 (Legacy & EUI-64) 

- **標準化**：當乙太網路在 80 年代標準化時，48 位元（稱為 **MAC-48** 或 **EUI-48**）已經成為工業標準。
- **演進**：對於需要更長位址的協議（如 IPv6 或 FireWire），設計者推出了 EUI-64，這是真正的 8 字節（64 位元）地址。在 IPv6 中，48 位元的 MAC 位址可以透過插入 `FF:FE` 轉換為 64 位元的介面識別碼。 

總結 

48 位元不是隨機選的，它是 **「足夠大以避免衝突」** 與 **「足夠小以節省昂貴的 70 年代內存」** 之間的黃金折衷點。 


---
## **related**：
[[NIC]]
[[EUI-64]]