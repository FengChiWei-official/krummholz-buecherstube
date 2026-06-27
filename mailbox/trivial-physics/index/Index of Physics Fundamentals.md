---
tags:
  - type/permanent
  - topic/learning
  - attr/views
  - status/in-progress
---
## Definition
### 1. The Geometric Foundation & Parametrization
* **[[Trace of a Curve]]**: The fundamental, static geometric entity in space (the set of points occupied by the curve, independent of any parametrization).
* **[[Trajectory Equation]] (or [[Parametric Curve]])**: A [[Vector-valued Function]] that introduces a parameter `t`(e.g., time) to map a real interval onto the [[Trace of a Curve]].

### 2. Kinematic Derivations (Time-Domain)
By differentiating the [[Trajectory Equation]] with respect to the parameter \(t\), we naturally define the fundamental kinematic vectors:
1. **[[Displacement]]** : The change in the position vector.
2. **[[Velocity]]** : The first derivative of position, representing the instantaneous rate of change and direction of motion.
3. **[[mailbox/trivial-physics/Acceleration]]** : The second derivative of position.

### 3. Geometric Metric & Infinitesimal Elements
For physical and geometric measurements, we require not only the linear distance ([[Displacement]]), but also the actual path length traveled along the curve ([[Arc Length]]).

* **[[Arc Length]]** (s): Defined strictly via the geometric method (the limit of inscribed polygons) to avoid circular definition with speed.
* **[[Arc Length Function]]** : Tracks the cumulative distance traveled from a starting point as a function of the parameter `t`.
* **[[Arc Length Element]]** : The infinitesimal arc length. In a space (Euclidean space), it obeys the infinitesimal Pythagorean theorem:
  $$ (ds)^2 = (dx)^2 + (dy)^2 + (dz)^2 $$

### 4. Derived Concepts Based on \(ds\)
The introduction of the [[Arc Length Element|ds]] allows us to bridge geometry and kinematics, leading to:
1. **[[Speed]]** : The scalar rate of motion.
2. **[[Frenet-Serret Frame]]**

---
## Related
