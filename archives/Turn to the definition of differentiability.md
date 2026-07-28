---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---


### **Problem Statement**

**Problem:**  
Let $z = f(x,y)$ be a function that is differentiable at the origin $(0,0)$, with $f(0,0) = 0$. Let $\mathbf{n}$ denote a normal vector to the surface $z = f(x,y)$ at the origin $(0,0,0)$. 

Evaluate the following limit:
$$\lim_{(x,y) \to (0,0)} \frac{\mathbf{n} \cdot (x, y, f(x,y))}{\sqrt{x^2 + y^2}}$$

---

### **Solution**

#### **Step 1: Express $f(x,y)$ using the definition of differentiability**
Since $f$ is differentiable at $(0,0)$ and $f(0,0) = 0$, by definition, $f(x,y)$ can be expressed via a first-order Taylor expansion as:
$$f(x,y) = f_x(0,0)x + f_y(0,0)y + o\left(\sqrt{x^2 + y^2}\right)$$
where $o\left(\sqrt{x^2 + y^2}\right)$ denotes a little-$o$ term satisfying:
$$\lim_{(x,y) \to (0,0)} \frac{o\left(\sqrt{x^2 + y^2}\right)}{\sqrt{x^2 + y^2}} = 0$$

#### **Step 2: Determine the normal vector $\mathbf{n}$**
The surface $z = f(x,y)$ can be represented implicitly by $F(x,y,z) = f(x,y) - z = 0$.  
A normal vector to the surface at the origin $(0,0,0)$ is given by the gradient vector $\nabla F(0,0,0)$:
$$\mathbf{n} = \left( f_x(0,0), \, f_y(0,0), \, -1 \right)$$
*(Note: Any non-zero scalar multiple $k\mathbf{n}$ is also a valid normal vector and will not affect whether the limit equals zero.)*

#### **Step 3: Calculate the dot product**
Substituting $\mathbf{n}$ and the position vector $\mathbf{r} = (x, y, z)$ into the dot product gives:
$$\mathbf{n} \cdot (x, y, z) = f_x(0,0)x + f_y(0,0)y - z$$

Substituting $z = f(x,y) = f_x(0,0)x + f_y(0,0)y + o\left(\sqrt{x^2 + y^2}\right)$ into the expression:
$$\mathbf{n} \cdot (x, y, z) = f_x(0,0)x + f_y(0,0)y - \left[ f_x(0,0)x + f_y(0,0)y + o\left(\sqrt{x^2 + y^2}\right) \right]$$

Simplifying yields:
$$\mathbf{n} \cdot (x, y, z) = -o\left(\sqrt{x^2 + y^2}\right)$$

#### **Step 4: Evaluate the limit**
Let $\rho = \sqrt{x^2 + y^2}$. As $(x,y) \to (0,0)$, $\rho \to 0^+$.  

Substituting the simplified dot product into the limit:
$$\lim_{(x,y) \to (0,0)} \frac{\mathbf{n} \cdot (x, y, z)}{\sqrt{x^2 + y^2}} = \lim_{\rho \to 0^+} \frac{-o(\rho)}{\rho} = 0$$

---

### **Conclusion**

$$\lim_{(x,y) \to (0,0)} \frac{\mathbf{n} \cdot (x, y, z)}{\sqrt{x^2 + y^2}} = 0$$

---

### **Geometric Remark (Optional for context)**
Geometrically, the dot product $\frac{\mathbf{n} \cdot (x,y,z)}{\|\mathbf{n}\|}$ represents the **signed perpendicular distance** from the point $P(x,y,z)$ on the surface to the tangent plane at the origin. The denominator $\sqrt{x^2+y^2}$ represents the distance from $(x,y)$ to the origin in the domain. 

The fact that the limit is $0$ expresses the fundamental geometric property of differentiability: **a differentiable surface is locally flat**, meaning the distance from the surface to its tangent plane vanishes at a rate faster than the distance to the point of tangency in the domain.

---

## Thoughts