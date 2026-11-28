## Definition

存储结构 = 逻辑结构在内存里的落地方式。同一份逻辑（线性表、树、图），换存储就换代价：[[Data Structure]] = [[Abstract Data Type in Data Structure|ADT]] + 存储结构。

## 四种基本方式

| 方式 | 关系记在哪 | 代表 |
|---|---|---|
| 顺序存储 | 下标相邻**隐含**关系 | [[Sequential List]]、[[Binary Tree]] §顺序存储 |
| 链式存储 | 指针**显式**记关系 | [[Linked List]]、[[Storage of Tree]]、[[Adjacency List]] |
| 索引存储 | 主表 $+$ 索引表（关键字 → 地址） | 408 只考概念 |
| 散列存储 | 散列函数**算出**地址 | [[Hash Table]] |

## 判据

- 关系能由下标算出（完全形、定长、静态）→ 顺序存储。
- 关系随数据变、频繁插删 → 链式存储。
- 要按关键字直接定位、不要求有序 → 散列存储。
- 要按关键字定位又要有序 → 索引 / B 树那一侧（[[B Tree]]）。

## 两个容易走偏的直觉

- 「顺序 = 数组，链式 = 链表」不完整：树与图都有两种以上的落地（[[Adjacency Matrix]] vs [[Adjacency List]]、[[Binary Tree]] 的两节）。
- 存储结构不是数据结构的同义词：ADT 定操作，存储定代价，两者的对照见 [[Sequential List vs. Linked List]]。

## 相关

[[Data Structure]] · [[Linear List]] · [[Sequential List vs. Linked List]]
