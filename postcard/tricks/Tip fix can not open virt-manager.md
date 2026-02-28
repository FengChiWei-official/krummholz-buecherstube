---
tags:
  - type/lit
  - topic/learning
  - status/archive
  - type/tips
source: 《卡片盒笔记法》 by Sönke Ahrens
---

## Text

``` Traceback
Traceback (most recent call last):  
File "/usr/bin/virt-manager", line 5, in <module>  
from virtManager import virtmanager  
File "/usr/share/virt-manager/virtManager/virtmanager.py", line 13, in <module>  
import gi  
ModuleNotFoundError: No module named 'gi'
```
## Thoughts

Obviously, it is a  **Python error**.
All [[Arch Linux]] python-based packages use pacman environment, so commandline-based call with [[Conda]] `base environment` will miss some module.

```
conda deactivate
```