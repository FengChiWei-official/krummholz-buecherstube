---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---

## Text

$Q(s,a) = \mathbb{E}(R(S{t+1} + \gamma Q(S_{t+1}, A_{t+1})|S_t = s, A_t = a)$
$Q(s,a) = \sum_{s', r} p(s', r| s, a) (R+ \gamma \sum_{a'} \pi(a'|s')Q(s', a'))$
$V(s) = \sum_a \pi(a|s) (r+\gamma \sum_{a'} p(s'|s, a)V(s', a'))$

---

## Thoughts