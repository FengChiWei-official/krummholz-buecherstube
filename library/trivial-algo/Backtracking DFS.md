---
tags:
  - type/permanent
  - topic/learning
  - attr/concept
  - status/evergreen
aliases:
  - Backtracking DFS
---

## Backtracking / Full-path DFS

Purpose: enumerate or build complete paths/solutions (permutations, combinations, path lists). Problems include permutations, subsets, N-Queens, all simple paths, and path-sum enumerations.

Visited semantics:
- Use path-local or temporary visited marking when necessary: mark before descending into a branch and unmark (backtrack) after returning. This allows exploring other branches that reuse nodes.

Canonical backtracking template

```
void backtrack(path) {
    if (terminal_condition) { answer.push_back(path); return; }

    for (option : choices) {
        if (invalid(option)) continue;
        // choose
        use(option);
        backtrack(path + option);
        // undo choice (un-use)
        undo(option);
    }
}
```

Key patterns
- Mark/unmark around recursion when node/state can be reused across different path branches.
- When generating permutations, swap/un-swap; when generating subsets, push/pop from path vector.

Common pitfalls
- Marking permanently (global visited) will prevent exploring other permutations or paths.
- Forgetting to undo state changes (leading to corrupted path/state for siblings).

Examples
- Permutations, subsets, combination-sum, N-Queens, path enumeration problems.

Related
- See [[Connectivity DFS]] for component/reachability problems where visited is global and permanent.
