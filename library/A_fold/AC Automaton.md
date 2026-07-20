---
tags:
  - type/permanent
  - status/in-progress
  - topic/learning
  - attr/concept
---

## Definition

In algorithm contests (e.g., CSP, NOIP), the problem "given length N, fill positions with 26 letters, count the number of strings that satisfy or do not satisfy certain substring conditions" is a very classic pattern.

You don't need to brainstorm the state transitions from scratch each time — use a universal template: **AC automaton + bitmask DP** to apply mechanically.

---

### Core idea of the template
> The **AC automaton** handles "which prefix is currently matched";
> the **`mask` (bitmask)** handles "which patterns have been collected / whether a required order is satisfied".

Use the following four steps to solve these problems easily:

---

### Step 1: Memorize the "universal AC construction" template (no modification needed)

Put this template (which builds failure pointers automatically) in your header. It converts complex suffix relationships into an O(1) transition array `tr[u][c]`.

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MOD = 998244353;
const int MAX_NODES = 205; // upper bound on nodes: sum of lengths of patterns to match (e.g. ccf 3 + cspark 6 = 9, 205 is safe)

int tr[MAX_NODES][26], fail[MAX_NODES];
int match_mask[MAX_NODES]; // match_mask[u] is a bitmask indicating which target patterns are matched by node u
int tot = 0; // node counter for the automaton

// Simple insertion: s is the pattern, id is its index (e.g. ccf -> 1, cspark -> 2)
void insert(string s, int id) {
    int u = 0;
    for (char c : s) {
        int idx = c - 'a';
        if (!tr[u][idx]) tr[u][idx] = ++tot;
        u = tr[u][idx];
    }
    match_mask[u] |= (1 << (id - 1)); // mark that node u matches pattern id
}

// Build failure pointers (BFS template)
void build_AC() {
    queue<int> q;
    for (int i = 0; i < 26; i++) {
        if (tr[0][i]) q.push(tr[0][i]);
    }
    while (!q.empty()) {
        int u = q.front(); q.pop();

        // Crucial: inherit matched patterns from the fail link
        match_mask[u] |= match_mask[fail[u]];

        for (int i = 0; i < 26; i++) {
            if (tr[u][i]) {
                fail[tr[u][i]] = tr[fail[u]][i];
                q.push(tr[u][i]);
            } else {
                tr[u][i] = tr[fail[u]][i]; // fast transition: follow fail links on mismatch
            }
        }
    }
}
```

---

### Step 2: Customize the `mask` according to the problem

After each step, when you arrive at a new node `v`, use `match_mask[v]` (which patterns are matched at `v`) to update the global `mask`.

#### Case A: the problem forbids any target pattern from appearing
* Design: no `mask` needed. If the next node `v` has `match_mask[v] != 0`, the string is invalid; discard that transition.

#### Case B: the problem requires that both pattern 1 and pattern 2 appear (in any order)
* Design: `mask` ranges from 0..3 (binary 00,01,10,11).
* Transition logic:

```cpp
int get_next_mask(int mask, int v) {
    return mask | match_mask[v]; // bitwise OR to add newly found patterns
}
```

#### Case C: the problem requires "pattern 1 appears before pattern 2" (this problem)
* Design: five states: `0` (none), `1` (only 1), `2` (only 2), `3` (both but order was 2 then 1), `4` (both and order 1 then 2 — success).
* Transition logic:

```cpp
int get_next_mask(int mask, int v) {
    int found = match_mask[v]; // which patterns are found at node v (bit 1 = pattern1, bit 2 = pattern2)
    bool has_1 = (found & 1);
    bool has_2 = (found & 2);

    if (has_1) {
        if (mask == 0) mask = 1;
        if (mask == 2) mask = 3;
    }
    if (has_2) {
        if (mask == 0) mask = 2;
        if (mask == 1 || mask == 3) mask = 4; // if we see pattern 2 and previously had 1, enter success state
    }
    return mask;
}
```

---

### Step 3: Write the DP skeleton

With the components above, the DP loop becomes a pipeline. Suppose the automaton has `tot + 1` nodes and `mask` has `M_SIZE` possible values.

```cpp
// dp[u][mask]
int M_SIZE = 5; // this problem uses 5 mask states
vector<vector<long long>> dp(tot + 1, vector<long long>(M_SIZE, 0));
dp[0][0] = 1; // start at root node 0 with mask 0

for (int i = 1; i <= n; i++) {
    vector<vector<long long>> next_dp(tot + 1, vector<long long>(M_SIZE, 0));

    if (is_fixed[i]) { // if the current character is fixed (e.g., '#')
        // reset automaton state to 0 (cannot cross boundary), but keep current mask
        for (int mask = 0; mask < M_SIZE; mask++) {
            long long sum = 0;
            for (int u = 0; u <= tot; u++) sum = (sum + dp[u][mask]) % MOD;
            next_dp[0][mask] = sum;
        }
    } else {
        // general case: try all 26 letters
        for (int u = 0; u <= tot; u++) {
            for (int mask = 0; mask < M_SIZE; mask++) {
                if (dp[u][mask] == 0) continue;

                for (int c = 0; c < 26; c++) {
                    int v = tr[u][c]; // next automaton node
                    int nmask = get_next_mask(mask, v); // update mask

                    next_dp[v][nmask] = (next_dp[v][nmask] + dp[u][mask]) % MOD;
                }
            }
        }
    }
    dp = move(next_dp);
}
```

---

### Step 4: Collect the answer

After DP finishes, sum up all states that are success states. For this problem, any state where `mask == 4` is a valid string, regardless of the automaton node.

```cpp
long long ans = 0;
for (int u = 0; u <= tot; u++) {
    ans = (ans + dp[u][4]) % MOD; // sum solutions in success state (mask == 4)
}
cout << ans << "\n";
```

### Exam strategy summary
When you encounter similar counting problems in contests:

1. Memorize the `insert` and `build_AC` template.
2. In `main`, call `insert("pattern1", 1)`, `insert("pattern2", 2)`, then `build_AC()`.
3. Think about how to represent the `mask` (often a 2-bit mask 0..3; sometimes a small custom state machine like the 5-state example).
4. Plug in the DP skeleton and submit.

---
## Related
