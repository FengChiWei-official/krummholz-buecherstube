---
tags:
  - type/permanent
  - status/evergreen
  - attr/principle
  - topic/learning
---

## Define
[[435. Non-overlapping Intervals]]
[[56. Merge Intervals]]
[[452. Minimum Number of Arrows to Burst Balloons]]
[[2406. Divide Intervals Into Minimum Number of Groups]]

## How do you solve it?

Unified template is:
1. Sort by end/start of intervals.
2. Edges: Intervals having common edge `[1,2], [2,3]` is under consideration or not?
3. Update last start/end.
4. Count Ans.

## How do you Design the Details

### Model
Given former interval, consider the relationship between current one and former one.

### Sort
**Sorting by Start** implies that preceding intervals are more likely to be **Long**, giving them higher priority to **absorb** with succeeding ones;
**Sorting by End** implies that preceding intervals are more likely to be short, greedy picking them helps to **reserve** more space for succeeding ones.


---
## **Related**

[[Todo Interval]]