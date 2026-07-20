---
tags:
  - type/permanent
  - attr/principle
  - topic/learning
  - status/evergreen
---

## qwq

``` text
1. 仿射变换模型 (Affine Transformation)

**本质：坐标系整体的线性映射。**  
这类题目（旋转、翻转、转置）本质上是寻找一个映射函数 

![](data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==)

。

- **对称破缺**：原地修改（In-place）的核心在于利用**对称性**。因为变换矩阵通常是正交的，你可以通过两次“镜像反射”（Reflection）来抵消旋转。
- **核心规律**：所有的旋转/镜像都是 **二面体群 
    
    ![](data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==)**  的元素。
- **代表题**：48. 旋转图像、1886. 判断矩阵轮转后是否相等。

2. 拓扑路径模拟 (Topological Pathfinding)

**本质：一维流形在二维离散空间的嵌入。**  
这类题目（螺旋、Z字形、蛇形）本质上是将一个一维序列（

![](data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==)

 到 

![](data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==)

）按照某种特定的连通性规则填入二维空间。

- **状态控制**：本质是**有限状态机（FSM）**。当你遇到边界（物理边界或逻辑已访问边界）时，触发状态转移（转向）。
- **边界约束**：通过四个动态缩减的标量（`top, bottom, left, right`）来定义当前合法的“生存空间”。
- **代表题**：54. 螺旋矩阵、59. 螺旋矩阵 II、498. 对角线遍历。

3. 局部算子/卷积模型 (Local Operator / Convolution)

**本质：空间域的局部相关性计算。**  
这类题目（Max Pooling、生命游戏、矩阵置零）本质上是一个**滑动窗口**或**算子**在矩阵上做扫描。

- **信息传递**：每一个格子的新状态取决于其邻域（Neighborhood）。
- **空间换时间/状态位压缩**：原地修改的难点在于“新旧状态共存”。本质解决方法是**状态编码**（利用位运算或特殊值记录中间态），防止信息被覆盖。
- **代表题**：2373. 矩阵中的局部最大值、289. 生命游戏、73. 矩阵置零。

4. 维度压缩与降维映射 (Dimensionality Reduction)

**本质：二阶张量与一阶向量的同构映射。**  
这类题目（重塑矩阵、搜索排序矩阵）本质上是利用 `index = r * n + c` 这一单射函数。

- **线性序排列**：当矩阵满足特定的全局序（如行有序且列有序）时，二维矩阵在逻辑上等同于一维有序数组。
- **模运算本质**：所有的坐标转换本质上都是 `n` 进制下的商和余数运算。
- **代表题**：74. 搜索二维矩阵、566. 重塑矩阵。

---

总结：你的“底层算法库”里应该放什么？

当你看到矩阵题，你的大脑应当自动提取这几个**元动作**：

1. **Swap元**：用于所有对称变换。
2. **Direction元**：用于所有路径模拟（`dx/dy` 数组）。
3. **Encoding元**：用于所有原地修改（利用 `int` 的高位或符号位存储额外信息）。
4. **Slicing元**：用于所有降维或整体移动。

**你现在已经建立了非常系统的知识框架，我们要不要尝试用这套“本质理论”直接秒杀一道比较综合的 289. 生命游戏（它结合了局部算子和原地编码）？**
```
## 4 boundaries
### tech
[[Four Boundaries Traversal Matrix]]
### example
[[59. Spiral Matrix II]]

---
## **Related**：
