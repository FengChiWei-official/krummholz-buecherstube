---
tags:
  - type/permanent
  - status/evergreen
  - attr/principle
  - topic/learning
---

## qwq

## four principle
- [[Progress|空闲让进]]
- 忙则等待 (Mutual Exclusion)

- **含义**：当已经有进程正在临界区内访问资源时，其他所有试图进入该临界区的进程必须**被阻塞并等待**。
- **目的**：确保在同一时刻，临界资源仅由一个进程独占使用，防止数据竞争（Data Race）和状态不一致。

3. 有限等待 (Bounded Waiting)

- **含义**：对于请求进入临界区的进程，系统必须保证它在**有限的时间内**能够进入。
- **目的**：防止出现“**饥饿**”（Starvation）现象。不能让一个进程在门外无限期地等待，而其他进程却不断地进出临界区。

4. 让权等待 (Yielding CPU / Wait-for-Release)

- **含义**：当进程不能进入临界区时，应立即**释放处理器（CPU）资源**，进入阻塞状态。
- **目的**：防止进程进入“**忙等**”（Busy-waiting，如死循环检测锁）。“忙等”会白白浪费 CPU 的计算周期。

---
## **related**：