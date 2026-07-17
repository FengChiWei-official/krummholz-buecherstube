---
tags:
  - type/permanent
  - status/evergreen
  - topic/learning
  - attr/technique
---

## Definition

A linear coordinate transformation is a mapping between coordinate representations of vectors induced by a linear map. Concretely, if `A` is an n×n matrix and `x` is a coordinate column vector in R^n, the transformed coordinates `x'` are given by

$$
x' = A x
$$

If `A` is invertible (`det(A) \neq 0`), the transformation is bijective and the inverse transformation is

$$
x = A^{-1} x'.
$$

Geometrically, linear coordinate transformations include rotations, scalings, reflections, shears, and compositions of these — all represented by matrices.

## Usage
1. [[Proof of Reversed Trigonometric Inequality]]
2. [[Sum to Product for Trigonometric Function]]

---
## **Related**

- Matrix representation: apply `A` to coordinate vectors.
- Change of basis: converting coordinates between bases (see "Change of basis" section below).
- Homogeneous coordinates: represent affine transforms as linear maps in one higher dimension.

## Matrix form and properties

- Composition: two linear transforms with matrices `A` and `B` compose to `BA` (apply `A` then `B`).
- Invertibility: `A` is invertible iff `det(A) \neq 0`.
- Determinant: `det(A)` scales oriented volumes; `|det(A)|` gives volume scaling factor.

## Change of basis (coordinates between bases)

Let `B = {b1, ..., bn}` be a basis with matrix `P` whose columns are the basis vectors in the standard coordinates. For a vector `v`, let `[v]_B` be its coordinates in basis `B`. Then

$$
v = P [v]_B.
$$

To convert from coordinates in basis `B` to coordinates in the standard basis use `P`. To go from standard coordinates to basis-`B` coordinates:

$$
[v]_B = P^{-1} v.
$$

If `A` represents a linear map in the standard basis, its matrix in basis `B` is

$$
[A]_B = P^{-1} A P.
$$

## Homogeneous coordinates (affine transforms)

Affine transformations `x \mapsto Mx + t` can be written as a single linear map in homogeneous coordinates by augmenting vectors and matrices:

$$
\begin{pmatrix}x'\\1\end{pmatrix} = \begin{pmatrix}M & t\\0 & 1\end{pmatrix} \begin{pmatrix}x\\1\end{pmatrix}.
$$

This lets translations be expressed and composed using matrix multiplication.

## Examples

- Rotation in 2D by angle `\theta`:

$$
R(\theta)=\begin{pmatrix}\cos\theta & -\sin\theta\\\sin\theta & \cos\theta\end{pmatrix},
\quad x' = R(\theta)x.
$$

- Scaling by `s_x, s_y` in 2D:

$$
S=\begin{pmatrix}s_x & 0\\0 & s_y\end{pmatrix}.
$$

- Shear (x-shear by `k`):

$$
H=\begin{pmatrix}1 & k\\0 & 1\end{pmatrix}.
$$

Example: to rotate a point `(1,0)` by 90° use `R(\pi/2)` giving `(0,1)`.

## How to compute coordinate change between two bases B and C

Let `P` be columns of basis `B` in standard coordinates and `Q` columns of basis `C`. To convert coordinates `[v]_B` to `[v]_C`:

1. Recover standard coordinates: `v = P [v]_B`.
2. Convert to `C`-coordinates: `[v]_C = Q^{-1} v = Q^{-1} P [v]_B`.

So the coordinate-change matrix from `B` to `C` is `Q^{-1} P`.

## Quick checklist / tips

- Always check whether a matrix is invertible before attempting `A^{-1}`.
- Use homogeneous coordinates for translations and other affine maps.
- For numerical work prefer orthonormal bases (matrices are orthogonal, inverse = transpose) to reduce numerical error.

---

**See also**: [Linear Coordinate Transformation.md](Linear%20Coordinate%20Transformation.md)