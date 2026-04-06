---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---

## Text
```


void dfs(状态参数, vector<int>& path) {
    // 1. 【终点】：完成任务了吗？
    if (满足终止条件) {
        记录/输出答案;
        return;
    }

    // 2. 【剪枝】：这条路还有救吗？
    if (不满足可行性) return;

    // 3. 【分叉】：面前有几条路可以走？
    for (各个备选选项) {
        if (合法性检查) {
            
            // 4. 【做选择】：迈出一步
            path.push_back(当前选项);
            
            // 5. 【递归】：去下一层看看
            dfs(更新后的状态, path);
            
            // 6. 【撤销】：退回这一步（回溯）
            path.pop_back(); 
        }
    }
}


```



--- 

```

/**
 * DFS 模板：进入前检查 (Check before recursion)
 * 特点：使用递归（系统栈），一路走到底再回溯
 */
void dfs(int curr, const vector<vector<int>>& adj, vector<int>& vis, int& count) {
    // 逻辑流派：在进入 dfs 之前已经由调用方标记了 vis[curr] 和 count++
    
    // 1. 遍历当前节点的所有邻居
    for (const int& nxt : adj[curr]) {
        // 2. 核心：递归前检查标记
        if (!vis[nxt]) {
            // 3. 标记并进入
            vis[nxt] = 1;
            count++;
            dfs(nxt, adj, vis, count);
        }
    }
}

// 调用方式：
// vis[start] = 1; count = 1;
// dfs(start, adj, vis, count);


```

---

## Thoughts