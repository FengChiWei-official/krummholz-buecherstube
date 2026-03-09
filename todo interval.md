---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---

## Text

Here is a professional summary of Interval Greedy Algorithms based on our discussion. You can use this as a "cheat sheet" for your LeetCode journey.

## 1. The Core Duality (Your Golden Rule)

The choice of sorting depends entirely on your goal: Efficiency vs. Continuity.

- Goal: Maximum Disjoint Intervals (LC 435, 452)
    
    - Strategy: "Look Left, Sort Right."
    - Logic: To fit as many intervals as possible, you must prioritize the one that ends earliest. This leaves the maximum "free space" for subsequent intervals.
    - Sorting: `sort` by Right End ascending.
    - Iteration: Keep track of the current `end` time; if `next_start >= end`, keep it.
    
- Goal: Continuity & Coverage (LC 56, 2406, 1024)
    
    - Strategy: "Look Right, Sort Left."
    - Logic: To merge or group intervals, you must process them in the order they appear (chronologically). You then monitor the "potential" of their Right Ends.
    - Sorting: `sort` by Left Start ascending.
    - Iteration: Check if the current `start` can "connect" to the existing `max_end` or `heap.top()`.
    

---

## 2. The Toolset: When to use what?

|Tool|Common Use Case|Why?|
|---|---|---|
|Simple Variable (`end`)|LC 435, 56|When you only care about the most recent boundary (Single-line logic).|
|Min-Heap (`priority_queue`)|LC 2406, 253|When you have multiple parallel lines (groups) and need to find the one that "finishes first" ($O(1)$ lookup).|
|Scanning Line (Diff)|Large Overlaps|When you only care about the maximum density of overlapping intervals at any point.|

---

## 3. C++ Technical Implementation Tips

- The `sort` Lambda:  
    Always use `const auto&` to avoid copying large vectors:
    
    ```cpp
    sort(intervals.begin(), intervals.end(), [](const vector<int>& a, const vector<int>& b) {
        return a[0] < b[0]; // Standard Left-Start sorting
    });
    ```
    
- The `priority_queue` Trap:  
    Remember that `priority_queue<int>` is a Max-Heap by default. For interval grouping, you almost always need a Min-Heap:
    
    ```cpp
    priority_queue<int, vector<int>, greater<int>> pq; // Min-Heap
    ```
    
- The `const` Operator:  
    When using custom `structs` in a heap, the comparison operator must be `const` to satisfy STL requirements:
    
    ```cpp
    bool operator>(const Node& other) const { return val > other.val; }
    ```
    

---

## 4. Common Pitfalls to Avoid

1. Coordinate Range: Watch out for negative coordinates. Initialize your `end` or `max_reach` with `intervals[0]` or `INT_MIN`, never `0`.
2. Boundary Conditions: Read carefully—does `[1, 2]` and `[2, 3]` overlap?
    
    - If No: Use `current_start >= last_end`.
    - If Yes: Use `current_start > last_end`.
    
3. Sorting Stability: In some advanced problems (like Interval Coverage), if Left Starts are equal, you might need to sort by Right End descending to find the longest reach first.

Would you like to put these experiences to the test with a final "Boss Level" problem (like LC 1024. Video Stitches), or are you ready to move on to another topic?

---

## Thoughts