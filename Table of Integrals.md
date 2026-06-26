---
tags:
  - type/permanent
  - status/in-progress
  - topic/learning
  - attr/concept
---

## Definition


为您整理了这 23 个经典积分公式的总结。为了便于记忆和复习，我将它们分为了以下五个板块。在所有公式中，$C$ 均表示任意常数。

---

### 一、 幂函数与指数函数基本积分

#### 1. $\int x^k \, dx$
* 当 $k \neq -1$ 时：
  $$\int x^k \, dx = \frac{x^{k+1}}{k+1} + C$$
* 当 $k = -1$ 时：
  $$\int x^{-1} \, dx = \ln|x| + C$$

#### 2. $\int \frac{1}{x} \, dx$
$$\int \frac{1}{x} \, dx = \ln|x| + C$$

#### 3. $\int e^x \, dx$
$$\int e^x \, dx = e^x + C$$

---

### 二、 三角函数基本积分（一次项）

#### 4. $\int \sin x \, dx$
$$\int \sin x \, dx = -\cos x + C$$

#### 5. $\int \cos x \, dx$
$$\int \cos x \, dx = \sin x + C$$

#### 6. $\int \tan x \, dx$
$$\int \tan x \, dx = -\ln|\cos x| + C = \ln|\sec x| + C$$

> 

#### 7. $\int \cot x \, dx$
$$\int \cot x \, dx = \ln|\sin x| + C$$

#### 8. $\int \frac{1}{\sin x} \, dx$ （即 $\int \csc x \, dx$）
$$\int \frac{1}{\sin x} \, dx = \ln|\csc x - \cot x| + C = \ln\left|\tan\frac{x}{2}\right| + C$$

#### 9. $\int \frac{1}{\cos x} \, dx$ （即 $\int \sec x \, dx$）
$$\int \frac{1}{\cos x} \, dx = \ln|\sec x + \tan x| + C = \ln\left|\tan\left(\frac{x}{2} + \frac{\pi}{4}\right)\right| + C$$

---

### 三、 三角函数导数公式的反向积分

#### 10. $\int \sec^2 x \, dx$
$$\int \sec^2 x \, dx = \tan x + C$$

#### 11. $\int \sec x \tan x \, dx$
$$\int \sec x \tan x \, dx = \sec x + C$$

#### 12. $\int \csc^2 x \, dx$
$$\int \csc^2 x \, dx = -\cot x + C$$

#### 13. $\int \csc x \cot x \, dx$
$$\int \csc x \cot x \, dx = -\csc x + C$$

---

### 四、 含有常数 $a$ 的代数与根式积分（重点难点）
*(以下公式中均假设 $a > 0$)*

#### 14. $\int \frac{1}{a^2+x^2} \, dx$
$$\int \frac{1}{a^2+x^2} \, dx = \frac{1}{a} \arctan\frac{x}{a} + C$$

#### 15. $\int \frac{1}{\sqrt{a^2 - x^2}} \, dx$
$$\int \frac{1}{\sqrt{a^2 - x^2}} \, dx = \arcsin\frac{x}{a} + C$$

#### 16. $\int \frac{1}{\sqrt{a^2 + x^2}} \, dx$
$$\int \frac{1}{\sqrt{a^2 + x^2}} \, dx = \ln\left|x + \sqrt{a^2 + x^2}\right| + C$$

#### 17. $\int \frac{1}{\sqrt{x^2 - a^2}} \, dx$
$$\int \frac{1}{\sqrt{x^2 - a^2}} \, dx = \ln\left|x + \sqrt{x^2 - a^2}\right| + C$$

#### 18. $\int \frac{1}{x^2 - a^2} \, dx$
$$\int \frac{1}{x^2 - a^2} \, dx = \frac{1}{2a} \ln\left|\frac{x-a}{x+a}\right| + C$$

#### 19. $\int \sqrt{a^2 - x^2} \, dx$
$$\int \sqrt{a^2 - x^2} \, dx = \frac{x}{2}\sqrt{a^2-x^2} + \frac{a^2}{2}\arcsin\frac{x}{a} + C$$

---

### 五、 三角函数二次幂的积分

#### 20. $\int \sin^2 x \, dx$
*(利用降幂公式 $\sin^2 x = \frac{1-\cos 2x}{2}$ 求解)*
$$\int \sin^2 x \, dx = \frac{x}{2} - \frac{\sin 2x}{4} + C$$

#### 21. $\int \cos^2 x \, dx$
*(利用降幂公式 $\cos^2 x = \frac{1+\cos 2x}{2}$ 求解)*
$$\int \cos^2 x \, dx = \frac{x}{2} + \frac{\sin 2x}{4} + C$$

#### 22. $\int \tan^2 x \, dx$
*(转化为 $\sec^2 x - 1$ 求解)*
$$\int \tan^2 x \, dx = \tan x - x + C$$

#### 23. $\int \cot^2 x \, dx$
*(转化为 $\csc^2 x - 1$ 求解)*
$$\int \cot^2 x \, dx = -\cot x - x + C$$

---
## **Related**