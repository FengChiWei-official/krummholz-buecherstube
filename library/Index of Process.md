---
tags:
  - type/permanent
  - attr/principle
  - topic/learning
  - status/evergreen
---
## Life of Process
![[ProcessState.jpg]]
### birth
call a system call `fork()`, 
1. System call(Trap)
2. Build up Entity for [[Process]] , which is called [[Process Control Block]]
3. is allocated resources, and Ready
### Ready
when a process ready, cpu might not available
1. [[Scheduler for Process]]: decide which is the next.
2. [[Context Shift]]:  CPU recover from ruption
3. 时间片轮训

### 协作与冲突
1. [[IPC|进程间通信]]
2. [[Synchronization & Mutual Exclusion|同步与互斥]]
3. [[Deadlock|死锁]]
第四阶段：等待与唤醒（I/O 与阻塞）

### 进程运行过程中可能需要读取硬盘文件或等待用户输入：

1. **阻塞态**：进程发起 I/O 请求，因为机械/外设太慢，进程主动放弃 CPU，进入**阻塞态（等待态）**。
2. **多道程序设计**：此时 CPU 不会闲着，而是立即切换到另一个就绪进程，这就是**多道程序设计**提升吞吐量的核心逻辑。
3. **中断唤醒**：当硬件完成读取，发出一个硬件**中断**，操作系统将原进程改回**就绪态**，重新排队等 CPU。
## 知识点逻辑

- **资源层**（[[Process Control Block]]、内存、[[IPC]]）：解决进程“是什么、有什么”的问题。
- **动力层**（[[Scheduler for Process|调度]]、状态转换）：解决进程“怎么跑、跑多快”的问题。
- **管理层**（[[Synchronization & Mutual Exclusion|同步互斥]]、[[Deadlock|死锁]]）：解决进程“怎么不打架”的问题。
- **交互层**（Trap、系统调用、Shell）：解决“人如何控制进程”的问题。

---
## **related**：
