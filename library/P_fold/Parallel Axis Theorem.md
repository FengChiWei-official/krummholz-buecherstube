---
tags:
  - type/permanent
  - attr/principle
  - topic/learning
  - status/evergreen
---

## **Definition**

The **Parallel Axis Theorem** relates the [[Moment of Inertia]] of a rigid body about any axis to its moment of inertia about a parallel axis through its center of mass.

**Formula:**

$$
I = I_{\text{cm}} + md^2
$$

**Terms:**

- $I_{\text{cm}}$ : Moment of inertia about an axis through the **center of mass (CM)**. This is typically the smallest I for a given shape direction.
- $I$ : Moment of inertia about a **new, parallel axis**.
- $m$ : Total mass of the object.
- $d$ : **Perpendicular distance** between the two parallel axes.


**Core Insight:** The moment of inertia about any axis equals the moment about the CM axis **plus** the moment of inertia the object's total mass would have if it were a point mass at the CM, located a distance d from the new axis.

---

## **Usage: Procedure for Composite Objects**

This theorem is essential for finding the moment of inertia of complex objects.

### **Step-by-Step Method:**

1. **Decompose:** Break the composite object into simple parts (e.g., disks, rods, rectangles) whose **$I_{\text{cm}}$** formulas are known from standard tables.    
2. **Calculate Individual $I_{\text{cm}}$ :** For each part $i$ , calculate its $I_{\text{cm}, i}$ about **its own** center of mass.
3. **Apply Parallel Axis Theorem (if needed):** For each part, if its CM axis is **not** the common target axis, use the theorem:​​
	1. $I_{i} = I_{\text{cm}, i} + m_i d_i^2$
	2. Here, d_i is the perpendicular distance from the part's CM to the **common target axis**. This step "unifies" the axes.
    
4. **Summation:** The total moment of inertia about the target axis is the sum of all parts' contributions:
	1. $$I_{\text{total}} = \sum I_{i}$$


### **Example: A dumbbell made of two solid spheres and a thin rod.**

To find I about an axis through the rod's center (perpendicular to it):

1. **Parts:** Sphere 1, Sphere 2, the Rod.
2. **Find $I_{\text{cm}}$ :**
    - For a sphere about its own CM: $I_{\text{cm, sphere}} = \frac{2}{5}m_{\text{sphere}}R^2$ .
    - For a rod about its CM (center): $I_{\text{cm, rod}} = \frac{1}{12}m_{\text{rod}}L^2$ .
3. **Unify Axes:** The rod's CM is already on the target axis, so $I_{\text{rod}} = I_{\text{cm, rod}}$ . For each sphere, its CM is offset by $d = (L/2 + R)$ . Thus:
	1. $$I_{\text{sphere}} = \frac{2}{5}m_{\text{sphere}}R^2 + m_{\text{sphere}}d^2$$
---

## **Related Concepts & Notes**

- **Moment of Inertia ( I or J ):** A measure of rotational inertia. It depends on mass distribution relative to the axis. **It is not an intrinsic property** like mass; it depends on the chosen axis.
    
- **Additivity of Moment of Inertia:** The total I of a system is the sum of the I of its parts **about the same axis**. The parallel axis theorem enables this calculation.
    
- **Perpendicular Axis Theorem:** Applies to **planar laminas**. For axes in the plane (x, y) and perpendicular (z), I_z = I_x + I_y . This is used for flat plates, often in conjunction with the parallel axis theorem.
    
- **Radius of Gyration ( k ):** A single distance that characterizes an object's rotational inertia, defined by I = mk^2 . It is the "effective distance" all mass is from the axis.
    
- **Crucial Reminder:** The **axes must be parallel**. The theorem cannot directly relate moments about non-parallel axes. The distance d is always the **shortest (perpendicular)** distance between the axes.
