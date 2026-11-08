# Praat 声学分析 — 参考资料卡

> **本文件不是知识笔记**：它是 `a_sticker/or/`（AI 材料区）里的参考资料，供你自己书写卡片；不进 `library/`。
> **来源**：2026-11-08 在本机的实测（Praat 7.0.02、PipeWire 1.6.10、WirePlumber、EasyEffects、DJI Wireless Mic Rx）。命令名凡标「已验证」的，都在本机二进制或实测中确认过；标「未核对」的是长期存在的菜单项，但没逐字验证文案。
> **本文件夹是 deck**（插件 `convertFoldersToDecks`）：本卡刻意不写「问题 + 双冒号 + 答案」的闪卡结构，避免被当成卡片导入；要转卡时自己加。

## 0. 一句话

Praat 的声学分析是**先取数、后作图**：所有图的数据都来自「光标处的查询」，图形只是把 CSV 画出来。

## 1. 本机录音链路（先把信号弄对）

| 事实 | 证据 |
|---|---|
| 麦克风 = DJI Wireless Mic Rx（USB），**只支持 48 kHz** | PortAudio 打开 44100 → `Invalid sample rate`；48000 → 成功 |
| 设备被 PipeWire 占用时不能直连 `hw:2,0` | 并发采集下打开 → `Invalid number of channels` |
| `(ALSA:) pulse` 在 44.1k / 48k 都能开，跟随系统默认输入源 | 两种采样率实测均可录到信号 |
| 板载 ALC287 的输入是空置插孔 | 2 s 采样：DC 偏置 8582、峰值 32767（削顶）、能量集中在 0–3 Hz |
| Praat 输入走 PortAudio/ALSA，输出走 PulseAudio | `~/.config/praat/Preferences.txt` 中 `Audio.inputSoundSystem: ALSA or JACK via PortAudio`、`Audio.outputSoundSystem: PulseAudio` |

**SoundRecorder 正确选法**：`New > Record mono Sound...` → 右侧 `Sampling frequency` 选 **48000 Hz** → 左侧 Input source 选 **`(ALSA:) pulse`**。

- 不要选 `Wireless Mic Rx: USB Audio (hw:2,0)`：44100 下必失败，且并发采集时独占冲突。
- 不要选 `HD-Audio Generic: ALC287 Analog`：空插孔，录出来是直流与低频嗡声。
- 录前看 Meter 电平条；峰值控制在 −6 dBFS 左右，进红区就是削波。
- 命令行等价物：`~/praat/record_take.sh 5`（录完自动跑 Praat 测量并写 CSV）。

## 2. 三个窗口

| 窗口 | 作用 |
|---|---|
| Objects | 对象列表；双击 Sound 打开编辑器；选中对象后出现对应的 `Draw` 菜单 |
| View & Edit | 波形 / 频谱图 / 共振峰 / 基频 / 强度 / 声门脉冲，取数值的地方 |
| Picture | 作图画布；`Erase all` 清屏；`File` 菜单存 PNG（300 / 600 dpi） |

编辑器 `View` 菜单的显示开关：`Show spectrogram`、`Show formants`、`Show pitch`、`Show intensity`、`Show pulses`（`Show pulses` 一项已在手册交叉引用中确认）。

## 3. 元音

### 3.1 取点规则

1. 光标放在元音**稳定段中点**，距首尾各留 30–50 ms。
2. `Formant > Formant listing`（**已验证**，手册页名即 `Formant listing`）：Info 窗口打印该时刻 F1–F4 与带宽。
3. 同一元音换 3 个点各测一次，取中位数；数值抖动大 = 取点在过渡上。

### 3.2 看轨迹

选中 Sound → `Formant > To Formant (burg)...` → 选中生成的 Formant → `Draw > Draw tracks...`（**已验证命令存在**）。画「时间 × 频率」的 F1–F4 轨迹。

多个元音叠加：不要 `Erase all`，逐个 `Draw tracks` 会画在同一张图上，最后用 `Draw > Text...` 标注。

### 3.3 元音图（F1 × F2 散点）

1. `New > Table > Create Table with column names...`，列名 `F1 F2`，行数 = 元音数。
2. 双击 Table 打开表格编辑器，逐行填每个元音的 F1、F2。
3. 选中 Table → `Draw > Scatter plot...`（**已验证命令存在**），Horizontal column 选 `F1`，Vertical column 选 `F2`。
4. 元音图的惯例是**坐标反向**（F1 从 1000 到 200，F2 从 3000 到 500）。反向范围是否被表单接受**未核对**；若被拒绝，按正常方向画，读图时把轴反着想。

读图：**F1 越高 = 开口越大；F2 越高 = 舌位越前；圆唇使 F2 下降**。

> 现实做法：Praat 的散点较朴素，论文里的元音四边形多把 F1/F2 导出到 Excel/R 画；Praat 内更常用的是 3.2 的轨迹图加 3.1 的数值。

## 4. 辅音

### 4.1 时间分辨率

`Spectrogram settings...`：看塞音/擦音把 window length 改成 **0.005 s**（宽带）；看元音改回 0.025–0.03 s。频率上限看擦音要 0–8000 Hz。

### 4.2 塞音与 VOT

`Pulses > Show pulses`（已验证）打开声门脉冲。

1. 找**爆破点**：频谱图上竖直的能量冲激。
2. 找**浊音起点**：第一个规则脉冲。
3. VOT = 两者时间差（拖选该段，编辑器顶部显示选区时长）。

参考：不送气清塞音 < 30 ms，送气 50–100 ms，浊塞音可为负值。

### 4.3 擦音与谱矩

选中擦音**中段 50%**（避开与元音的交界），在编辑器的 Spectrum 菜单生成该选区的频谱切片（即 `Intro 3.6 Viewing a spectral slice` 那条路径；具体菜单文案**未核对**），得到 Spectrum 对象后查询（**四个查询均已验证存在**）：

| 查询 | 含义 | 经验值 |
|---|---|---|
| `Get centre of gravity` | 谱重心 | s 约 6–8 kHz；ʃ 约 3–4 kHz；f 更低 |
| `Get standard deviation` | 谱分散度 | s 比 ʃ 更集中 |
| `Get skewness` | 偏度 | 分布形状 |
| `Get kurtosis` | 峰度 | 分布形状 |

### 4.4 鼻音、边音、清浊

- 鼻音：F1 低（约 250–300 Hz），F2/F3 被削弱、出现反共振「空洞」。
- 边音：F1 也低，但 F2/F3 相对完整。
- 清浊：`To Harmonicity (cc)...`（已验证）画 HNR 随时间变化；清音段 HNR 低、脉冲不规则。

## 5. 嗓音与录音质量

| 要看什么 | 命令 | 读什么 |
|---|---|---|
| 嗓音稳定性 | `Pulses > Voice report`（已验证） | F0 统计、jitter（%）、shimmer（%）、HNR（dB）、unvoiced 比例 |
| HNR 随时间 | Sound → `To Harmonicity (cc)...` → `Draw` | 曲线越高越干净 |
| 整体音色 | Sound → `To Ltas...` → `Draw`（已验证） | 高频滚降是否过陡 |
| 录音本身 | 看波形 | 顶部削平 = 削波；整体偏离中线 = DC 偏置；静音段 > −60 dB = 底噪高 |

`Voice report` 的数值依赖 `Pitch settings...`：测嗓音建议 floor 75 Hz、ceiling 600 Hz，或勾 `Optimize for voice analysis`，否则 jitter 虚高。

## 6. 参数速查

| 项目 | 元音 | 辅音 |
|---|---|---|
| Spectrogram window | 0.025–0.03 s | 0.005 s |
| 显示频率上限 | 0–5000 Hz（男）/ 0–8000（女、儿童） | 0–8000 Hz |
| Formant max formant | 5500（女/一般）、5000（男）、8000（儿童） | 同左 |
| Formant number | 5 | 5 |
| Pitch 范围 | 75–600 Hz | 清辅音段可关掉 |

## 7. 常见错误

1. **F1 追踪错**：max formant 设小了会把 F2 当 F1；改设置后看轨迹是否平滑。
2. **取点在过渡上**：元音头尾 50 ms 的共振峰在滑动，必须取中段平台。
3. **削波未察觉**：波形顶部变平后所有谱矩失真；录音前盯电平条。
4. **采样率不匹配**（本机特有）：48 kHz-only 的设备在 44100 下打开失败，Praat 会自动回退到列表第一项，也就是板载空插孔 —— 这正是「只能选 HD-Audio、音质差」的成因。
5. **输出被效果器染色**（本机特有）：默认 sink 是 `easyeffects_sink`，Praat 回放会经过 EasyEffects 的 EQ。要听原声就临时 `pactl set-default-sink alsa_output.pci-0000_03_00.6.analog-stereo`。

## 8. 相关文件

- `~/praat/measure_sound.praat` — GUI：选中 Sound 即测时长、F1–F3、F0，写 CSV。
- `~/praat/measure_file.praat` — 命令行测单个文件。
- `~/praat/extract_formants.praat` — 按文件夹批量测。
- `~/praat/record_take.sh` — 录一段 + 报电平 + 自动测量。
- `~/praat/mic_level.sh` — 只查电平。

## 9. 待办

- [ ] 用真实录音核对本卡的取点与数值（录 a/i/u 各 3 次，填 Table 画第一张元音图）。
- [ ] 决定这张卡是否升级为 `library/` 的正式 Node（需要 owner 批准的书面计划；届时还要定 Raw Index 登记边）。
