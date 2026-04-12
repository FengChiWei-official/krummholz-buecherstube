---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---

## Text

Here is a professional and concise introduction to Two-Pointer techniques in English, organized by your "Design the Details" logic:

## 1. Core Concept: Defining Boundaries

Two-pointer techniques are primarily used to optimize O(N²) nested loops into O(N) linear time complexity. The essence is to use two variables (pointers) to represent dynamic boundaries or specific relationships within a data structure.

---

## 2. Common Models (The Three Types)

## Type A: Fast & Slow Pointers (The "Scanner" Model)

- Best for: In-place modification, removing duplicates, or finding cycles.
- Logic: The Fast pointer scans every element, while the Slow pointer marks the boundary of the "processed" or "valid" sub-array.
- Typical Problems: _Move Zeroes_, _Remove Duplicates_, _Linked List Cycle_.

## Type B: Left & Right Pointers (The "Colliding" Model)

- Best for: Sorted arrays, searching for pairs, or reversing sequences.
- Logic: Pointers start at both ends (`0` and `n-1`) and move toward the center (collide) based on a specific condition.
- Typical Problems: _Two Sum II_, _3Sum_, _Reverse String_, _Container With Most Water_.

## Type C: Sliding Window (The "Range" Model)

- Best for: Subarrays or substrings with specific constraints (length, sum, characters).
- Logic: Both pointers move in the same direction, but the "window" between them expands or shrinks to satisfy the criteria.
- Typical Problems: _Longest Substring Without Repeating Characters_, _Minimum Size Subarray Sum_.

---

## 3. Design the Details (Your Unified Thinking)

When designing a Two-Pointer solution, focus on these details:

- Initialization: Where do the pointers start? (Same end vs. Opposite ends).
- Movement Criteria: What triggers `left++`, `right--`, or `slow++`? (e.g., `if (nums[fast] != 0)`).
- Stop Condition: When is the task complete? (e.g., `while (left < right)` or `fast == n`).
- Relationship: Is one pointer "absorbing" the other, or are they "searching" for a target together?

---

## 4. Summary for Interviews

> "I use Two Pointers to achieve O(N) time complexity by maintaining two indices that represent a valid range or a processed boundary. This avoids redundant scans and allows me to solve the problem in a single pass."

Would you like to try applying the "Colliding Model" (Type B) to a problem like [[167. Two Sum II]] to see how the logic differs from the "Fast & Slow" one?


---

## Thoughts
