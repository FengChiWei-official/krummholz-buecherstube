---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---

## Text

---

``` mermaid
graph TD
    %% 50年代
    subgraph Era50 [1950年代：大爆炸与物理破圈]
        M_Elvis["【受众线】猫王 (Elvis Presley)<br>• 主张: 身体释放/青年身份<br>• 影响: 奠定摇滚大众商业化"]
        A_Blues["【影响线】电气蓝调/先驱 (Chuck Berry / Muddy Waters)<br>• 主张: 底层痛楚/吉他电气化<br>• 影响: 奠定摇滚三大件乐器范式"]
        Tech50["【技术/外力推手】<br>• 45转单曲黑胶唱片 (便宜易普及)<br>• 电吉他与真空管放大器<br>• 电视机普及 (视觉传播开始)"]
    end

    %% 60年代
    subgraph Era60 [1960年代：黄金时代的艺术分裂]
        M_Beatles["【受众线】披头士/滚石<br>• 主张: 集体认同/旋律宣泄<br>• 影响: 开启不列颠入侵与体育场狂热"]
        A_Dylan["【影响线】鲍勃·迪伦/地下丝绒 (VU)<br>• 主张: 诗意批判/噪音美学/拒绝娱乐<br>• 影响: 启蒙后世所有地下艺术与朋克"]
        Tech60["【技术/外力推手】<br>• 晶体管便携收音机<br>• 12寸LP密纹唱片 (开启专辑时代)<br>• 多轨磁带录音技术 (4轨-8轨)"]
    end

    %% 70年代
    subgraph Era70 [1970年代：视觉奇观与重型重组]
        M_Queen["【受众线】Queen / KISS<br>• 主张: 歌剧宏大/舞台视觉奇观/逃避现实<br>• 影响: 摇滚乐彻底沦为高门槛、昂贵的娱乐帝国"]
        A_Floyd["【影响线】平克·弗洛伊德/安息日/朋克先锋<br>• 主张: 社会异化/重型工业压抑/DIY自我拯救<br>• 影响: 开启重金属时代；而朋克则撕碎主流虚假繁荣"]
        Tech70["【技术/外力推手】<br>• 24轨大型录音室设备<br>• 早期合成器 (Moog/VCS3)<br>• 巨型体育场灯光与烟火音响系统<br>• 廉价日本吉他涌入 (降低乐手门槛)"]
    end

    %% 80年代
    subgraph Era80 [1980年代：MTV享乐主义与地下分化]
        M_Glam["【受众线】华丽金属 (枪花 / Bon Jovi)<br>• 主张: 派对享乐/性感旋律/偶像化<br>• 影响: 统治MTV电台/商业化达到顶峰"]
        A_Met["【影响线】Metallica / 独立与后朋 (Joy Division/Pixies)<br>• 主张: 速度力量/极度内省/静噪动态美学<br>• 影响: 为90年代垃圾摇滚和另类夺权积蓄力量"]
        Tech80["【技术/外力推手】<br>• MTV电视台成立 (音乐彻底视觉化)<br>• FM广播与车载音响爆发<br>• 高增益吉他放大器 (产生重金属音色)<br>• Walkman随身听与磁带交换网络"]
    end

    %% 90年代
    subgraph Era90 [1990年代：地下的夺权与科技时代焦虑]
        M_Oasis["【受众线】英伦摇滚 (Oasis)<br>• 主张: 劳动阶级乐观/吉他旋律复兴/Live Forever<br>• 影响: 拯救冷漠吉他摇滚/创造英国商业奇迹"]
        A_Nirvana["【影响线】涅槃 (Nirvana) / 电台司令 (Radiohead)<br>• 主张: 真实痛苦/拒绝商业虚伪/科技时代数字异化<br>• 影响: 彻底摧毁长发金属/带领先锋乐理走向解构"]
        Tech90["【技术/外力推手】<br>• CD激光唱片黄金期 (行业暴利)<br>• 户外大型摇滚音乐节产业化<br>• Pro Tools与数字音频工作站 (DAW)<br>• 早期互联网与MP3格式萌芽"]
    end

    %% 传承与相互影响关系 (实线代表直接传承/启发，虚线代表对立/反作用/洗牌)
    A_Blues --> M_Elvis
    A_Blues --> M_Beatles
    A_Blues --> A_Dylan
    
    A_Dylan <--> M_Beatles
    A_Dylan --> A_Floyd
    M_Beatles --> M_Queen
    
    M_Queen -. 繁复与昂贵催生朋克反叛 .-> A_Floyd
    M_Queen --> M_Glam
    
    A_Floyd --> A_Met
    A_Floyd --> A_Nirvana
    
    M_Glam -. 极度商业化引发厌恶 .-> A_Nirvana
    A_Met -- 独立美学/静噪动态直接启发 --> A_Nirvana
    
    M_Beatles --> M_Oasis
    
    %% 连接技术外力与时代
    Tech50 -. 催化 .-> Era50
    Tech60 -. 催化 .-> Era60
    Tech70 -. 催化 .-> Era70
    Tech80 -. 催化 .-> Era80
    Tech90 -. 催化 .-> Era90

```


---

## Thoughts