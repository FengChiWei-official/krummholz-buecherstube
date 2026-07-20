---
tags:
  - type/permanent
  - status/evergreen
  - topic/learning
  - attr/technique
---

## Definition

[[Logarithmic Functions]]

## Recognizance

$\lim_{x \to +\infty} \ln (1 + 2^x) \ln (1+ \frac{1}{x})$

$$
\begin{align}

& = && \lim_{x \to +\infty} \ln (2^x(1+2^{-x})) \ln (1+\frac{1}{x})\\
& = && \lim_{x \to +\infty} (x \ln 2 + \ln (1+\frac{1}{2^x})) \ln (1+ \frac{1}{x}) \\
& = && \lim_{x \to +\infty} \frac{x \ln 2 + \ln (1+\frac{1}{2^x})}{x} \\
& = && \lim_{x \to +\infty} \frac{x \ln 2 }{x}  \lim_{x \to +\infty} \frac{\ln (1+\frac{1}{2^x})}{x}  \\
& = && ln 2
\end{align}
$$

---
## **Related**