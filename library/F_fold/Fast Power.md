---
tags:
  - type/permanent
  - status/in-progress
  - topic/learning
  - attr/concept
---

## Definition

$$
k^{(\sum_iw_i 2^i)_2} = \prod_{w_i=1} k^{a_i}
$$

```

LL exp;
    LL res = 1;
    // 26^{1011_2} = 26^{1000}*26^{10}*26
    LL dig = 26;
    while (exp>0) {
        // c_exp = k
        if (exp%2==1) res =res*dig;
        // cexp = k+1
        dig = dig*dig;
        exp>>=1;
    }

```

---
## **Related**