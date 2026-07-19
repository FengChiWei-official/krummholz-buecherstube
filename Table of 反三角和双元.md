---
tags:
  - type/permanent
  - status/in-progress
  - topic/learning
  - attr/concept
---
    h
## Definition

### 双元实例

圆双元

$u = x$, $v = \sqrt{a^2 - x^2}$
> \* $u = x$, $v = \sqrt{-a^2 - x^2}$

双曲双元

$u = x$, $v = \sqrt{a^2 + x^2}$
> $u = \sqrt{-a^2 + x^2}$, $v = x$


### 反三角函数
> 双曲双元得反三角函数
> 圆双元得反双曲函数

$\int \frac{1}{a^2+x^2} dx = \frac{1}{a} \arctan {\frac{x}{a}}+C$
>\*$\int \frac{1}{-a^2+x^2} dx = \frac{1}{ai} \arctan {\frac{x}{ai}}+C$
>推荐转化为下面的式子

$\int \frac{1}{a^2-x^2} dx = \frac{1}{a} \tanh^{-1} {\frac{x}{a}}+C = \frac{1}{a} \ln \mid \frac {a+x}{a-x}\mid + C$

### 标准双元

圆双元

$\int \frac{1}{\sqrt{a^2-x^2}} dx = \arcsin(\frac{x}{a})+C$

$\sqrt{a^2 - x^2}dx = \frac{x \sqrt{a^2 - x^2}}{2} +  \frac{a^2}{2} \int \frac{dx}{\sqrt{a^2 - x^2}}$

双曲双元
$\int \frac{1}{\sqrt{a^2+x^2}} dx = \tanh^{-1}(\frac{u}{v}) = \ln \mid x + \sqrt {a^2 + x^2}\mid +C$
$\int \frac{1}{\sqrt{x^2-a^2}} dx = \tanh^{-1}(\frac{u}{v}) = \ln \mid x + \sqrt {x^2 - a^2}\mid +C$

$\sqrt{a^2 + x^2}dx = \frac{x \sqrt{a^2 + x^2}}{2} +  \frac{a^2}{2} \int \frac{dx}{\sqrt{a^2 + x^2}}$
$\sqrt{x^2 - a^2}dx = \frac{x \sqrt{x^2 - a^2}}{2} -  \frac{a^2}{2} \int \frac{dx}{\sqrt{x^2 - a}}$

---
## **Related**