---
tags:
  - type/permanent
  - status/in-progress
  - topic/learning
  - attr/concept
---

## Definition

```
string hex_to_bin(const string& hex_str) {
    string bin = "";
    for (char c : hex_str) {
        int val = 0;
        if (c >= '0' && c <= '9') val = c - '0';
        else if (c >= 'a' && c <= 'f') val = c - 'a' + 10;
        else if (c >= 'A' && c <= 'F') val = c - 'A' + 10;
        
        // 转换为 4 位二进制并拼接到结果中
        for (int i = 3; i >= 0; --i) {
            bin += ((val >> i) & 1) ? '1' : '0';
        }
    }
    return bin;
}
```
---
## **Related**