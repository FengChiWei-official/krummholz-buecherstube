---
tags:
  - status/evergreen
  - topic/learning
  - type/tips
  - type/lit
---

# preparation
you need ntfs-3g

# params
- exec: if you would like to play game, you should add it.
- windows_names: making sure the name in windows style
```
UUID=3333478E2F670171   /mnt/sharedDS   ntfs    nofail,users,ui  
d=1000,gid=1000,windows_names,exec   0 0
```

# weakeness
can handle linux's [[soft link]]
# to play steam games
1. make sure the fs **not mounted** by root
2. mount with param `exec`
3. move the `SteamLibrary/steamapps/compatdata/` into any linux fs
4. make a link from linux fs to ntfs for `compatdata`
[[Trick UMU set up]]

---
## **related**：