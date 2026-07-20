---
tags:
  - type/permanent
  - status/in-progress
  - topic/learning
  - attr/concept
aliases:
  - LCA
---

## Definition

``` cpp
#include <vector>
#include <utility>
#include <algorithm>

// 保持你的类型别名习惯（如果你的全局模版中已有，可自行删去此行）
using vec = std::vector<int>;
using Img = std::vector<vec>;

template <typename Graph = Img>
class Lca {
private:
    int max_depth;
    vec depths;
    Img parents;

public:
    // 构造函数：接受任意符合邻接表结构的图/树
    Lca(const Graph &edges, int root_id = 0) {
        int n = edges.size();
        max_depth = 1;
        while ((1 << max_depth) <= n) {
            max_depth++;
        }

        depths = vec(n, 0);
        parents = Img(n, vec(max_depth, 0));

        // 根节点初始化
        for (int i = 0; i < max_depth; i++) {
            parents[root_id][i] = root_id;
        }

        // 使用栈进行非递归 DFS 遍历，建立倍增表
        vec stack = {root_id};
        while (!stack.empty()) {
            int node_id = stack.back();
            stack.pop_back();

            for (int son_id : edges[node_id]) {
                // 防止往父节点方向回溯
                if (son_id == parents[node_id][0]) {
                    continue;
                }
                
                parents[son_id][0] = node_id;
                depths[son_id] = depths[node_id] + 1;
                
                // 动态规划计算倍增祖先
                for (int i = 1; i < max_depth; i++) {
                    parents[son_id][i] = parents[parents[son_id][i - 1]][i - 1];
                }
                stack.push_back(son_id);
            }
        }
    }

    // 获取最近公共祖先 (修正了拼写)
    int ancestor(int a, int b) {
        if (depths[a] < depths[b]) {
            std::swap(a, b);
        }

        // 1. 先将 a 提到与 b 相同的深度
        int diff_depth = depths[a] - depths[b];
        for (int i = 0; i < max_depth; i++) {
            if (diff_depth & (1 << i)) {
                a = parents[a][i];
            }
        }

        if (a == b) {
            return a;
        }

        // 2. 两人同时向上倍增跳转，直到他们刚好在 LCA 的下一层
        for (int i = max_depth - 1; i >= 0; i--) {
            if (parents[a][i] != parents[b][i]) {
                a = parents[a][i];
                b = parents[b][i];
            }
        }
        return parents[a][0];
    }

    // 获取 a 的第 2^depth 级祖先（默认为直接父亲）
    int parent(int a, int depth = 0) {
        return parents[a][depth];
    }
    
    // 获取节点深度
    int get_depth(int a) {
        return depths[a];
    }
};



#include <iostream>
#include <vector>

// 假设已经引入了上面的 Lca 模板类...

int main() {
    // 建立一棵包含 5 个节点的树（0 到 4）
    // 结构如下：
    //       0 (Root)
    //      / \
    //     1   2
    //    / \
    //   3   4
    Img edges(5);
    edges[0] = {1, 2};
    edges[1] = {0, 3, 4}; // 双向边
    edges[2] = {0};
    edges[3] = {1};
    edges[4] = {1};

    // 1. 实例化模板（指定根节点为 0）
    Lca<Img> lca(edges, 0);

    // 2. 查询深度
    std::cout << "Depth of root(0): " << lca.get_depth(0) << std::endl; // 输出: 0
    std::cout << "Depth of node(3): " << lca.get_depth(3) << std::endl; // 输出: 2

    // 3. 查询最近公共祖先
    std::cout << "LCA of 3 and 4: " << lca.ancestor(3, 4) << std::endl; // 输出: 1
    std::cout << "LCA of 3 and 2: " << lca.ancestor(3, 2) << std::endl; // 输出: 0

    // 4. 查询倍增祖先
    std::cout << "Parent of 3: " << lca.parent(3, 0) << std::endl;       // 3 的 2^0 级祖先，输出: 1
    std::cout << "Grandparent of 3: " << lca.parent(3, 1) << std::endl;  // 3 的 2^1 级祖先，输出: 0

    return 0;
}
```

---
## **Related**