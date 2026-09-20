---
tags:
  - type/permanent
  - status/archive
  - topic/kaoyan
  - topic/cs
created: 2026-09-18
data-date: 2026-09-18
source:
  - "OpenAlex API（works search + institutions/venue group_by，40 次成功 GET，2026-09-18）"
  - "OpenAIRE API（导师发文代偿核实，14 次，2026-09-18）"
  - "Semantic Scholar Graph API（导师会场与年份，28 次，2026-09-18）"
  - "Europe PMC REST（机构锚定核实，1 次，2026-09-18）"
  - "Bing 中文搜索（web_search 工具，18 次，2026-09-18）"
  - "官网/教师主页（10 页：HFUT/HIT/SZU/SUSTech/SHU/Xidian/SWJTU，2026-09-18）"
  - "知识库：kaoyan-scores.md、mlsys-tiered-teams.md、kaoyan-labs-matrix.md、mlsys-risks.md、kaoyan-11408-process.md、kaoyan-sources.md"
---

# 考研「易发文方向」判定（2027 考季 · 11408）

> 事实 `[F]` / 判断 `[J]` 分区。分数线与招生数据以 2026 为最新基线，**报考年须复核**。
> 本卡配套课题组矩阵：[[kaoyan-easypub-groups]]；方法与访问日志见该文件 §5–§6。

---

## 0. 本次择向标准与判据（前置，不在执行中更改）

**标准（用户 2026-09 更新）**：好毕业 + 好发文（目标 1–2 篇 CCF-A/B 或 SCI 1–2 区）+ 经费充足 + 上岸有保证为主；就业出口降为次级。

**判据（元计划给定）**

| 判据 | 阈值 | 数据来源 |
|------|------|---------|
| ① 发文可及性（校池覆盖） | 候选校池 15 校中 **≥3 校各 ≥3 篇**该方向论文 | OpenAlex `works?search=<方向>&filter=publication_year:2023-2026,institutions.id:<15 校>` + `group_by=institutions.id` |
| ② 会场供给 | 会场 top-20 中 **≥3 个 CCF-A/B 会场**（或中科院 SCI 1–2 区按 A/B 等价折算） | OpenAlex `group_by=primary_location.source.id` + CCF 2022 目录映射 |
| ③ 最终选取 | 存活方向中**发文可及性最高**（= 15 校池内该方向 2023–2026 论文总数）的 3 个；并列时按 D1>D2>D3>D4>N1>N2>N3 | 判据①的分组计数求和 |

---

## 1. 七方向存活判定 `[F]`

### 1.1 发文可及性（15 校池内 2023–2026 论文数）

| 代号 | 方向 | 检索式（逐字） | 池内论文总数 | 池内 ≥3 篇的校数 | 判据① | 池内 Top5 校（篇数） |
|------|------|---------------|------------|----------------|-------|-------------------|
| N1 | 医学影像 AI | `medical image analysis deep learning` | **8285** | 14 | ✅ | 华科 1442、成电 1270、深大 880、哈工大 806、西电 576 |
| D1 | 计算机视觉/多模态 | `visual recognition multimodal` | **5637** | 14 | ✅ | 哈工大 892、成电 705、华科 613、深大 544、北邮 533 |
| N2 | 遥感智能解译 | `remote sensing image interpretation` | **1706** | 15 | ✅ | 西电 214、哈工大 211、成电 189、西南交大 167、南科大 162 |
| D2 | 联邦学习/边缘智能 | `federated learning edge intelligence` | 1641 | 14 | ✅ | 北邮 306、成电 226、西电 182、华科 146、哈工大 125 |
| D4 | 强化学习应用（网络调度/智能通信） | `reinforcement learning network scheduling resource allocation` | 1500 | 15 | ✅ | 北邮 291、西电 161、成电 158、南邮 127、华科 123 |
| D3 | 数据挖掘/AI4DB | `data mining database query optimization` | 1196 | 14 | ✅ | 成电 169、华科 168、哈工大 162、北邮 138、深大 114 |
| N3 | 时空数据挖掘/城市计算 | `spatiotemporal data mining urban computing` | 525 | 14 | ✅ | 西南交大 71、成电 65、深大 65、华科 49、南科大 41 |

**判据①结论**：15 校池在 7 个方向全部满足「≥3 校各 ≥3 篇」，**7/7 存活**。该判据在本题语境下几乎无区分度——211/双非 CS 学院在这些应用型方向上 2023–2026 均有稳定产出。区分度来自 §1.2 与排名。

**口径定义 `[F]`**：上表「池内论文总数」= 15 校各自计数之**和**。同一论文若由两所池内校合作会被计两次，故它略高于去重后的匹配总数（例：N2 分组和 1706，`meta.count` 去重后 1636）。判据①用分组和（体现「哪些校有产出」）。

**复现抽查 `[F]`**：以 N2 检索式重发一次（2026-09-18 当日），返回 池内总数 1636、西电 214、哈工大 211、西南交大 167，与本卡记录逐项一致。

**方法学限制 `[J]`**：分组只返回前 25 个机构，未进前 25 的池内学校（如西安邮电在 N1/D1 未进榜）计为 0，故上表总数为**下界**。已核验该截断不影响 Top3 边界：D2 若补入西安邮电最大增量 <26 篇（其分组第 25 位为 26），上限 1667 < N2 的 1706。

### 1.2 会场供给（`type:article`，2023–2026，全球）

| 代号 | 会场 top-8（篇数） | CCF-A/B 或 SCI 1–2 区命中数 | 判据② |
|------|------------------|------------------------|-------|
| D1 | Scientific Reports 3732、Sensors 2478、Applied Sciences 1770、IEEE Access 1350、Electronics 1208、PLoS ONE 938、Remote Sensing 778、Nature Communications 497 | SR(2 区)、IEEE Access(2 区)、Remote Sensing(2 区)、Nature Communications(1 区) = **4** | ✅ |
| D2 | Scientific Reports 1605、Sensors 877、IEEE Access 788、Electronics 732、Applied Sciences 592、Future Internet 294、IEEE Internet of Things Journal 209、Mathematics 202 | SR(2 区)、IEEE Access(2 区)、IoT-J(1 区)、Mathematics(2 区) = **4** | ✅ |
| D3 | Scientific Reports 763、Applied Sciences 624、IEEE Access 605、Electronics 408、Sensors 355、**Proceedings of the ACM on Management of Data 263**、Nature Communications 244、**ACM Computing Surveys 181** | PACMMOD(CCF-A)、CSUR(CCF-A)、Nature Communications(1 区)、Briefings in Bioinformatics(1 区)、SR(2 区)、IEEE Access(2 区) = **6** | ✅ |
| D4 | Scientific Reports 996、Sensors 653、IEEE Access 621、Electronics 607、Applied Sciences 522、Energies 491、Drones 221、IEEE Internet of Things Journal 138 | IoT-J(1 区)、SR(2 区)、IEEE Access(2 区)、Mathematics(2 区)、IEEE OJ-COMS(2 区) = **5** | ✅ |
| N1 | Scientific Reports 10408、Sensors 3814、IEEE Access 3375、Applied Sciences 3258、PLoS ONE 2807、Diagnostics 2520、Nature Communications 2145、npj Digital Medicine 1037 | Nature Communications(1 区)、npj Digital Medicine(1 区)、SR(2 区)、Remote Sensing(2 区)、IEEE Access(2 区)、Frontiers in Oncology(2 区)、Cancers(2 区) ≥ **7** | ✅ |
| N2 | Remote Sensing 3462、Scientific Reports 2286、Sensors 1523、Sustainability 1319、Applied Sciences 1014、Land 854、IEEE JSTARS 493、Nature Communications 402 | Remote Sensing(2 区)、SR(2 区)、Land(2 区)、JSTARS(2 区)、Nature Communications(1 区) ≥ **5** | ✅ |
| N3 | Scientific Reports 560、Sustainability 518、Remote Sensing 397、ISPRS IJGI 179、IEEE Access 127、International Journal of Digital Earth 77、JSTARS 49、Transactions in GIS 47 | SR(2 区)、Remote Sensing(2 区)、ISPRS IJGI(2 区)、IEEE Access(2 区)、IJDE(2 区)、JSTARS(2 区) = **6** | ✅ |

**判据②限制 `[F/J]`**：`type:article` 会滤掉全部会议论文（CVPR/ICCV/MICCAI 属 `proceedings-article`），因此上表只能反映期刊侧；加发一轮「全类型」与「会议型（`primary_location.source.type:conference`）」会场查询后，OpenAlex 对中文机构的会议记录覆盖不足——15 校会议型命中仅 AAAI 一个会场（D1 297 篇、N1 205 篇、D3 53 篇、D2 36 篇、D4 6 篇、N2 13 篇、N3 5 篇）。因此**判据②按「期刊侧 SCI 分区折算」执行**，会议侧 A/B 证据不依赖全网计数，而由 §2 的导师级会场核实承担（每条均带 venue + year）。

### 1.3 排名与最终 3 方向 `[F]`

按 §1.1 池内论文总数降序（7/7 存活，无并列）：

| 排名 | 方向 | 池内论文总数 | 结果 |
|------|------|------------|------|
| 1 | **N1 医学影像 AI** | 8285 | ✅ 入选 |
| 2 | **D1 计算机视觉/多模态** | 5637 | ✅ 入选 |
| 3 | **N2 遥感智能解译** | 1706 | ✅ 入选 |
| 4 | D2 联邦学习/边缘智能 | 1641 | ❌ 备选 |
| 5 | D4 强化学习应用 | 1500 | ❌ 备选 |
| 6 | D3 数据挖掘/AI4DB | 1196 | ❌ 备选 |
| 7 | N3 时空数据挖掘/城市计算 | 525 | ❌ 备选 |

**结论**：最终 3 方向 = **医学影像 AI（N1） / 计算机视觉·多模态（D1） / 遥感智能解译（N2）**。三者均为**应用型 + 公开数据集驱动 + 单卡可完成实验**，正对应用户新标准的「好毕业 + 好发文」。

**歧义与已排除的替代读法 `[J]`**：若把判据①按「OpenAlex 机构分组 top-25 榜内」严格解读（不补池内总数），存活者仅 D1/D2/D3/D4，最终 3 个会变成 D1/D2/D4。本次采用补全校池计数的读法——严格读法的淘汰是**分页截断造成的假阴性**（N1/N2/N3 的池内校在榜外并非无产出）。两种读法的分界证据：补全后 N1 池内 14 校有产出、N2 池内满 15 校、N3 池内 14 校，均远超「≥3 校各 ≥3 篇」。

**对第 3/4 名分界（N2 vs D2，1706 vs 1641）的稳健性说明 `[J]`**：N2 在**保底/稳妥层的覆盖密度**明显优于 D2：N2 池内 桂电 53、重邮 45、西邮 36、南邮 52、上大 46；D2 池内 桂电 60、重邮 79、南邮 120、西邮 <26。两者在保底层均可用，但 N2 的院校分布更抗「某校导师临时停招」的单点风险；且 N2 的会场（TGRS/JSTARS/ISPRS JPRS）竞争池远小于 TWC/TIFS/IoT-J。故 N2 取第 3 席。

---

## 2. 最终三方向判定卡

### 2.1 N1 · 医学影像 AI `[F/J]`

| 项 | 内容 |
|----|------|
| **存活证据** | 池内 8285 篇（15 校中 14 校进榜，全部 ≥3 篇）；会场：Nature Communications(1 区)、npj Digital Medicine(1 区)、SR/IEEE Access/Remote Sensing/Frontiers in Oncology/Cancers(2 区)；导师级 CCF-A/B 实证：IEEE TMI（CCF-B/1 区）、Medical Image Analysis（CCF-B/1 区）、MICCAI（CCF-B）、AAAI/ICCV/CVPR/TIP（CCF-A） |
| **毕业工程量** | **低–中**。公开数据集充足（ADNI、MIMIC、ISLES、眼底 OCT、BraTS 等），单卡（RTX 3090/4090）即可完成分割/分类/多模态融合实验；MICCAI（年 1 次、审稿 3–5 月）+ 医学影像期刊（TMI/MedIA/JBHI，审稿 3–6 月）双通道，硕士 2 年出 1–2 篇 CCF-B/1 区现实 |
| **报考竞争** | 低于纯 CV。医学影像在 985 内多挂「生物医学工程」学科，计算机考生视为跨考，报名密度低 |
| **风险** | (a) 部分组要求医学/生物背景（西电生科院部分方向明确「限生物或医学背景」）；(b) 临床数据合作依赖医院关系，纯算法组产出更快 |
| **代表课题组** | 西电 缑水平（冲刺）、南科大 刘江（稳妥）、上大 蒋皆恢（稳妥）、杭电 秦飞巍（稳妥）、深大 黄炳升（保底）、重邮 舒禹程（保底）→ 详见 [[kaoyan-easypub-groups]] |

### 2.2 D1 · 计算机视觉 / 多模态 `[F/J]`

| 项 | 内容 |
|----|------|
| **存活证据** | 池内 5637 篇（14 校进榜，全部 ≥3 篇，哈工大 892 / 成电 705 / 华科 613 / 深大 544 / 北邮 533）；导师级 CCF-A/B 实证：TPAMI、IJCV、TIP、TIFS、TCSVT、TMM（期刊）+ CVPR、ICCV、ECCV、NeurIPS、ICLR、AAAI、ACM MM、WWW、SIGIR（会议） |
| **毕业工程量** | **低**。ImageNet/COCO/VG/LAION 等公开集，单卡可完成微调与消融；会议审稿 3–5 月，一年两轮投稿窗口（CVPR/ICCV/ECCV/AAAI/MM） |
| **报考竞争** | **最高**。CV 是考研计算机最热方向，同校 CV 组报录比通常高于学院均值；导师名额竞争激烈 |
| **风险** | (a) 同质化严重，创新点内卷，A 类会议命中率不稳定；(b) 热门组对初试分与机试要求高；(c) 算力需求随多模态/大模型化上升，双非组可能只有 1–2 张卡，需选「小模型 + 公开集」课题（如底层视觉、轻量多模态） |
| **代表课题组** | 哈工大 左旺孟（冲刺）、合工大 汪萌（稳妥）、深大 沈琳琳（保底）→ 见 [[kaoyan-easypub-groups]] |

### 2.3 N2 · 遥感智能解译 `[F/J]`

| 项 | 内容 |
|----|------|
| **存活证据** | 池内 1706 篇（**15 校全部进榜且 ≥3 篇**，西电 214 / 哈工大 211 / 成电 189 / 西南交大 167 / 南科大 162 / 深大 160）；会场：IEEE TGRS、JSTARS、ISPRS JPRS、Remote Sensing、ISPRS IJGI、IJDE（中科院 2 区为主，ISPRS JPRS/TGRS 为 1 区）；CCF 目录内无对口 A/B，按 SCI 分区折算为 A/B 等价 |
| **毕业工程量** | **低**。Sentinel/Landsat/高分/GF 系列 + LEVIR-CD/WHU-CD/Potsdam 等公开集；实验以分类/变化检测/配准/语义分割为主，单卡可完成；期刊审稿 3–6 月，无会议截稿压力 |
| **报考竞争** | **低**——选题冷、需一定测绘/信号基础，计算机考生少；西电、西南交大、桂电、深大有传统沉淀 |
| **风险** | (a) CCF 目录不含遥感专刊，「CCF-A/B」需按 SCI 1–2 区自证，读博/大厂算法岗需解释等价性；(b) 顶级成果偏工程化系统（星上处理、测绘生产），纯算法创新天花板低于 CV |
| **代表课题组** | 西电 焦李成（冲刺）、西电 张向荣（冲刺）、哈工大 张腊梅（冲刺）、西南交大 叶沅鑫（稳妥）、桂电 吴军（保底）→ 见 [[kaoyan-easypub-groups]] |

---

## 3. 未入选方向说明

### 3.1 MLSys 降级说明（引用 [[mlsys-risks]] + [[mlsys-tiered-teams]]）`[F/J]`

| 降级理由 | 证据出处 |
|---------|---------|
| **算力门槛**：双非/211 课题组普遍无 A100/H100 级算力，训练系统类实验无法展开 | [[mlsys-risks]] §风险 2（严重度：高）；[[mlsys-tiered-teams]] 保底层「重邮、西邮、桂电基本无大卡」 |
| **发表周期长**：OSDI/SOSP/EuroSys 从选题到录用平均 12–18 个月，硕士 2–3 年拿 1 篇 A/B 的难度高于应用型方向 | [[mlsys-risks]] §风险 3 |
| **冲刺层出身不确定**：冲刺层 4 校中 3 所（华科/成电/哈工大）评黄，无实证歧视证据但无法排除；强组集中在复试出身敏感的 985 层 | [[mlsys-tiered-teams]] §歧视信号专项；[[mlsys-risks]] §风险 1 |
| **新标准下排序函数变化**：标准由「方向前景」换成「发文可及性 × 毕业工程量」后，MLSys 在「毕业工程量」与「双非可达性」两项失分 | 本卡 §0 |

**处置**：MLSys 降级为「仅当就业出口优先级回升时的备选」，不占本次最终 3 席。其系统技能（C++/分布式/OS）的退路价值仍成立（[[mlsys-risks]] §2 最坏情况可接受性判定）。

### 3.2 存活但未入选的 4 个方向（备选池）`[F/J]`

| 方向 | 池内总数 | 未入选原因 | 何时启用 |
|------|---------|-----------|---------|
| D2 联邦学习/边缘智能 | 1641 | 与 N2 仅差 65 篇；会场（TIFS/TDSC/TWC/IoT-J）竞争池更大；数学化程度高、实验多为仿真而非公开数据集基准 | 若用户偏好通信网络底子、或 2027 年 N2 目标校导师停招 |
| D4 强化学习应用 | 1500 | 实验以仿真环境为主，缺少统一公开基准，成果可比性弱；AAAI/NeurIPS 竞争激烈 | 若目标锁定重邮本校/南邮/西邮，D4 是这三校产出最密的应用型方向（重邮 82、南邮 127、桂电 66、西邮 42） |
| D3 数据挖掘/AI4DB | 1196 | 会场质量最高（PACMMOD/CSUR 均为 CCF-A），但池内产出集中在冲刺层 4 校（成电/华科/哈工大/北邮），保底层覆盖薄 | 若初试可稳 350+ 且愿冲 985 |
| N3 时空数据挖掘 | 525 | 池内总量最低，保底层除西南交大外弱 | 若转向「城市计算/交通」就业口径 |

**三方向共有的结构性优势 `[F]`**：N1/D1/N2 在**保底层**（重邮 266/152/45、桂电 309/164/53、杭电 412/301/68、南邮 259/195/52）与**稳妥层**（深大、上大、西南交大、南科大）均有实测产出，可从保底一路铺到冲刺，不依赖单一院校。

---

## 4. 待核实事项（报考年前必须复核）

1. **分数线=2026 基线**：所有分数线与统考名额来自 [[kaoyan-scores]] 与 [[mlsys-tiered-teams]]，标注为估计值；2027 报考年须以各校研招网复试录取工作办法为准。
2. **导师 2027 招生计划**：矩阵每条均为「2022–2026 有产出且经费可查」，不等于 2027 有统考硕士名额（部分大牛只招博士/推免）。见 [[kaoyan-easypub-groups]] §5 亲读清单。
3. **冲刺层复试结构风险**：西电、哈工大 2026 复试均为初试 50% + 复试 50%，未达本计划设定的「初试权重 ≥60%」优选线——详见 [[kaoyan-easypub-groups]] §4。
4. **OpenAlex 免费额度与限流**：执行中段 OpenAlex 对新的 `search` 类查询返回 429（响应头 `x-ratelimit-limit-usd: 0.1/日`、`x-ratelimit-remaining-usd: 0.0002`），导师级发文核实改用 OpenAIRE / Semantic Scholar / Europe PMC 代偿；随后个别查询恢复 200（复现抽查成功）。若需重跑，建议错峰或直接复用本文档 §1 的检索式。

### 4.1 校池构造缺陷：被结构性遗漏的强 CV/遥感 985（例：南开 · 程明明团队）

**问题 `[F]`**：本卡的候选校池是计划给定的 **15 校**（冲刺 华科/成电/哈工大/北邮/西电；稳妥 南邮/杭电/西南交大/合工大/上大/南科大；保底 重邮/西邮/桂电/深大）。该名单**继承自上一轮 MLSys 调研的院校表**（[[mlsys-tiered-teams]] 的 18 校），因此整条证据链——判据①的 `institutions.id` 过滤、判据③的排名、§2 的导师候选发现——**只在「MLSys 强校」范围内成立**。任何 CV/遥感/医学影像强、但 MLSys 弱的学校（典型如南开）在该框架下**不可能被看见**：它既不在 OR 过滤的 15 个机构 ID 里，也不会出现在池内作者分组中。

**这不是证据结论，而是取样范围 `[J]`**：南开出现在 [[kaoyan-scores]]（B 级，2026 学硕线 ~325 ⚠️，学硕~8 / 专硕~30，34 所自划线）却不在 [[mlsys-tiered-teams]]（无 MLSys 团队），于是被池子自动剔除。计划在第 1 步就固定了池子，执行中未做偏离——**这一步本该被质疑而没有**。

**被漏掉的代表性条目：南开大学 · 程明明（Ming-Ming Cheng）媒体计算组/MCG `[F]`**（本轮补查，OpenAIRE `author="Ming-Ming Cheng"` 精确匹配；注意同名的 `Mingming Cheng` 为旅游/酒店管理学者，已排除）：

| 方向映射 | 已核实会场 + 年份 |
|---------|-----------------|
| D1 计算机视觉/多模态 | TPAMI 2026（DFormer++）、IJCV 2026（MaTe3D）、TIP 2025、TMM 2026、TCSVT 2026；CVPR 2024（PhotoMaker）、CVPR 2025、ICCV 2025、AAAI 2026、SIGGRAPH Asia 2024 |
| N2 遥感智能解译 | AAAI 2026（SM3Det，多模态遥感统一模型）、TGRS 2026（AuxDet，全领域图像检测）、JSTARS 2025（多模态大模型 SAR 图像描述） |
| N1 医学影像 AI | 本轮未取到直接命中，**待核实** |

**若补入会怎样 `[J]`**：按「985 + 自划线 + 线 ~325」，程明明组应落在**冲刺层**，且论文证据强度（TPAMI/IJCV/CVPR/ICCV 连续）不低于本矩阵任一冲刺组，D1 与 N2 双向对口。但两项反向因素必须同时报出：(a) 南开计算机**统考名额极小**（学硕~8 / 专硕~30，[[kaoyan-scores]]），报录比高于西电/哈工大；(b) 头部队组吸引高质量生源，340–370 的初试在 CV 热门组内不构成优势。此外南开不在 [[mlsys-tiered-teams]]，出身友好度须按计划规则**默认黄**并补查负面信号；经费证据（NSFC 项目）本轮**未核实**。

**须用户决定 `[J]`**：补齐该条需要对池外加校重跑判据①（OpenAlex 机构过滤 + 池内计数），属**修改计划既定取样范围**，故本轮只登记、不擅自扩池。补入所需的最小工作量：判据①重跑（含南开等 4–6 所强 CV/遥感 985 的 OR 过滤，≈2–3 次 OpenAlex 查询）+ 导师经费核实（1–2 次 Bing 或 1 页官网）+ 出身友好度查询（1 次 Bing）。

**后续（已完成）**：用户随后提供了 OpenAlex API key，池外冷校方向已按「会场即方向」重做，产出 [[kaoyan-cold-groups]]——该文用 `doi_starts_with` 前缀锚定会场、用 `raw_affiliation_strings` 校验机构归属，覆盖 13 所冷校 × 5 主流方向，并暴露了 OpenAlex 的机构错挂缺陷（会把名校误判成冷校）。

---

**回链：** [[kaoyan-labs-matrix]] | [[kaoyan-scores]] | [[mlsys-risks]] | [[kaoyan-11408-index]] | [[kaoyan-easypub-groups]] | [[mlsys-tiered-teams]] | [[mlsys-what-and-why]]
