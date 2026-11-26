# Index of Computer Network

## 时间轴

| 世代 | 年份 | 代表 | 这一代解决了什么 |
|---|---|---|---|
| 分组交换 | 1969 | ARPANET 四节点 | 网络可以没有中心：转发代替建链 |
| 网际互联 | 1983 | TCP/IP 切换（flag day） | 异构网由 IP 层抹平，传输层才谈端到端 |
| 应用爆发 | 1991 | WWW / HTTP | 会话与表示搬进应用层，中间设备不必理解 |
| 无类寻址 | 1993–1994 | CIDR、NAT | 地址不再按类切分；私网可复用公网出口 |
| 控制分离 | 2010s | SDN / OpenFlow | 路由决策与转发分离，转发表由外部下发 |

## 地图

| 挂点 | 合同 / 部件 | 回答的张力 |
|---|---|---|
| [[Structure of Computer Network]] | 分层 + 封装 | 分层凭什么能各自演进 |
| [[TCP-IP]] | 四层模型 / 沙漏 | 中间最窄的那层为何承担全部互联 |
| [[Encapsulation]] | 每层加头 | 同一串字节凭什么有四层解释 |
| [[OSI 与 TCP-IP-分层对照与功能反查]] | 7 vs 4 层功能对照 | 一个功能落在哪层，谁持有状态 |
| [[Computer Network 计算题]] | 奈氏 / 香农 / 时延带宽积 | 速率上限由哪个公式给 |
| [[Network Access Layer of Network]] | 一跳之内（MAC + 帧） | 一段链路上谁先说话 |
| [[Ethernet Frame]] | 帧边界 + FCS | 一帧凭什么知道起止、凭什么判错 |
| [[ARP]] | IP → MAC 解析 | IP 已知，链路地址从哪来 |
| [[Switching Methods]] | 电路 / 报文 / 分组 | 换交换方式换的是什么代价 |
| [[MTU]] | 一帧的载荷上限 | 超了之后谁负责切 |
| [[Internet Layer of Network]] | 寻址 + 转发 | 跨网一跳怎么找到下一跳 |
| [[IP Address]] | 网络部分 + 主机部分 | 地址为什么必须分层 |
| [[IP Datagram(IPv4)]] | 分组格式 | 首部里哪几位真的影响转发 |
| [[NAT]] | 地址复用 | 私网凭什么出得去、回来怎么认 |
| [[Transport Layer of Network]] | 端到端 | 进程之间靠什么配对 |
| [[TCP Header]] | 序号 / 确认 / 窗口 / 标志位 | 可靠交付靠哪几个字段 |
| [[Three Way Handshake]] | 建连三步 | 为什么必须是三次 |
| [[控制与载荷-计组与计网的分平面同构]] | 控制平面 vs 数据平面（SDN） | 转发决策为何不与转发走同一条路 |

## 卡片

暂无 Links 卡。跨区卡的成员除计网侧外还需计组侧桥（`控制与载荷-计组与计网的分平面同构` 尚未挂点），否则落在同一区（I2）。

## Related

- [[Raw Index of Computer Network]] — 登记主干（trunk），本 Index 是它的语义树。
- [[Structure of Computer Network]] — 分层与封装总卡。
- [[Index of Computer Organization]] — 跨区对照的计组侧。
- [[408 Links 转化 Todo]] — 待成卡成员与挂点裁决记录。
