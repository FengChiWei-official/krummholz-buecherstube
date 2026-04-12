---
tags:
  - type/permanent
  - status/in-progress
  - topic/learning
  - attr/principle
---

## 扫描结果总结（2024年4月10日）

### Part 1: library 主题目录 Map 卡收敛

**发现**：
- library 的主题目录中原本**没有**显式标记的 map 卡
- 已创建三个新的标准化索引卡，统一命名风格为 `Index of [Topic].md`

**完成的操作**：
1. ✅ **Index of Algorithm Problem Types.md** (library/trivial-algo/)
   - 来源：迁移自 View of Algorithm.md（archive 文献笔记）
   - 结构：7 个主题类别（基础、线性、搜索数学、图论、优化、数论、位运算）
   - 标签：attr/map, status/evergreen

2. ✅ **Index of Abstract Algebra.md** (library/trivial-algebra/)
   - 结构：5 个大类（基础结构、同态映射、特殊结构、代数性质、应用例子）
   - 涵盖：70+ 个代数概念卡的导航
   - 标签：attr/map, status/evergreen

3. ✅ **Index of Physics Fundamentals.md** (library/trivial-physics/)
   - 结构：4 个大类（坐标系、向量函数、运动学、动力学）
   - 涵盖：30+ 个物理概念卡的导航
   - 标签：attr/map, status/evergreen

**未创建索引的目录**：
- trivial-thoughts: 仅 5 个文件，已有 Operating Rules 和 View 卡，不需要索引
- trivial-classic: 4 个文件，高度专向（诗律相关），太小
- trivial-computer-network: 3 个文件，太小
- trivial-ml: 2 个文件，太小

---

### Part 2: mailbox 中的 View 卡稳定度评估

**扫描发现：共 6 个 view 卡**

| 卡片名称 | 路径 | 当前标签 | 稳定度 | 建议 |
|--------|------|---------|--------|------|
| View of Algorithm | mailbox/algo/ | type/lit, status/archive | ✅ 已迁移 | 已迁移为 Index of Algorithm Problem Types |
| View of Addtive Group of Integer | mailbox/algebra/ | attr/principle, status/in-progress | ❌ | 保留在 mailbox，继续完善 |
| View of Cyclic Subgroup or Group | mailbox/algebra/ | attr/principle, status/in-progress | ❌ | 保留在 mailbox，继续完善 |
| View of Group | mailbox/algebra/ | attr/principle, status/in-progress | ❌ | 保留在 mailbox，继续完善 |
| View of Vector-valued Function | mailbox/trivial-physics/ | attr/principle, status/in-progress | ❌ | 保留在 mailbox，继续完善 |
| View of Rigid Body Kinematics | mailbox/trivial-physics/ | attr/concept, status/in-progress | ❌ | 保留在 mailbox，继续完善 |

**关键发现**：
- mailbox algebraView 卡标记为 `attr/principle` 而非 `attr/views`（标签错误）
- 所有 in-progress 卡内容均不完整，需要继续迭代

---

### Part 3: 互链补充

**已完成**：
- 新创建的三个 topic-level map 卡互相链接
- 每个 map 卡的 Related 部分包含：
  - 相关主题的其他 map 卡链接
  - 对应的 mailbox view 卡链接（进行中的版本）
  - library 中的 view 卡链接（稳定版本）

**示例关联**：
```
trivial-algo Index ←→ trivial-algebra Index ←→ trivial-physics Index
        ↓                  ↓                        ↓
  View of Knapsack    AM-GM Inequality    Vector-valued Function
```

---

## 后续待办

### 短期（优先）
- [ ] 在 _index_ 的总索引卡中添加指向新 topic-level map 卡的链接
- [ ] 修正 mailbox algebra 中三个 view 卡的标签：attr/principle → attr/views
- [ ] 为 mailbox algebra View 卡的内容补全（完成定义、示例等）

### 中期
- [ ] 评估是否需要为其他小目录（trivial-classic, trivial-computer-network, trivial-ml）创建索引
- [ ] 当 mailbox algebra/physics view 卡达到 status/evergreen 时，迁移到 library

### 相关链接
- [[Knowledge Base Operating Rules]] - 操作规则与 map/view 定义
- [[Index of Algorithm Problem Types]] - 新创建的算法索引
- [[Index of Abstract Algebra]] - 新创建的代数索引  
- [[Index of Physics Fundamentals]] - 新创建的物理索引
