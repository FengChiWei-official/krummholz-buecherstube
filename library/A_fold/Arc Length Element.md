---
tags:
  - type/permanent
  - topic/learning
  - attr/concept
  - status/in-progress
aliases:
  - Infinitesmal Arc Length
  - ds - the Arc Length Element
  - ds
---

## Definition

For a parameterized curve $\mathbf{r}(t)$, the arc length element $ds$ intuitively represents the infinitesimal distance traveled along the curve:

$$
\begin{align}
ds &= \|\mathbf{v}(t)\| \, dt \\
&= \left\| \frac{d\mathbf{r}(t)}{dt} \right\| \, dt \\
&= \frac{ds(t)}{dt} \, dt
\end{align}
$$

where $s(t) = \int_{t_0}^t \|\mathbf{v}(\tau)\| d\tau$ is the **accumulated arc length function** from $t_0$ to $t$.

>[!tip] Conceptual Distinction: $ds$ vs. $ds(t)$ / Exact Differential
> 1. **On the 1D parameter space $t$**: $ds$ is the standard differential of the scalar function $s(t)$, i.e., $ds = ds(t) = s'(t) dt$.
> 2. **On a manifold / in multi-dimensional space**: $ds$ is **not** a global exact 1-form on the manifold, as there is no global scalar field $s(x^1, x^2, \dots)$ such that $ds = \nabla s \cdot d\mathbf{r}$ (due to path dependence).
> 3. Strictly speaking, $ds$ is a formal notation obtained by taking the square root of the **line element square** $ds^2$.

---

## Connection with Metric Tensor

The fundamental definition of the norm (length) $\|\cdot\|$ originates from the **metric tensor** ([[Metric Tensor]]) $g$.

In Riemannian geometry, the norm of a tangent vector $\mathbf{v} = \frac{d\mathbf{x}}{dt} = \frac{dx^i}{dt} \frac{\partial}{\partial x^i}$ is defined as:

$$
\|\mathbf{v}\| = \sqrt{g(\mathbf{v}, \mathbf{v})} = \sqrt{g_{ij} v^i v^j} = \sqrt{g_{ij} \frac{dx^i}{dt} \frac{dx^j}{dt}}
$$

Therefore, the quadratic line element can be expanded as a quadratic form of the metric tensor:

$$
ds^2 = g_{ij} \, dx^i dx^j
$$

Taking the square root yields the general expression for the line element:

$$
ds = \sqrt{g_{ij} \, dx^i dx^j} = \sqrt{g_{ij} \frac{dx^i}{dt} \frac{dx^j}{dt}} \, dt = \|\mathbf{v}\| \, dt
$$

>[!note] Special Case: Euclidean Space
> In the standard Cartesian coordinates of Euclidean space $\mathbb{R}^n$, the metric tensor is $g_{ij} = \delta_{ij}$ (Kronecker delta / identity matrix), so:
> $$ds^2 = (dx^1)^2 + (dx^2)^2 + \dots + (dx^n)^2$$
> which is the infinitesimal form of the Pythagorean theorem.

---

## **Related**

- [[Metric Tensor]]
- [[Arc Length Parametrization]]
- [[First Fundamental Form]]
- [[Riemannian Manifold]]
- [[Geodesics]] — curves that minimize $\int ds$