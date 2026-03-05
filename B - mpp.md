---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---
[B - mpp](https://atcoder.jp/contests/abc447/tasks/abc447_b)
## Text

``` cpp
#include<iostream>
#include<vector>
#include <string>
using namespace std;

int main () {
	ios::sync_with_stdio(0); cin.tie(0);
    // size fix, so vector > unorder_map
    vector<int> map(26, 0);

    string s;
    cin >> s;

    int Ms = -1;
    //mvector<int> cnts;cnts.reserve(26);

    // find max (min) is easier than sort, o(n)
    //you can find max while handling
    for (int i = 0; i < s.size(); i++) {
        int id = s[i] - 'a';
        map[id] ++;
        Ms = map[id]>Ms? map[id]: Ms;   
    }
    
    string ans;
    for (int i = 0; i < s.size(); i++) {
        char cur = s.at(i);
        int cur_id = cur - 'a';
        if (map[cur_id] >= Ms) {}
        else ans.push_back(cur); 
    }

    cout << ans;


    return 0;
}
```

---

## Thoughts

### Techs
[[Frequency Array]]
[[PP_Fast_IO_Template]]
[[Two_Pass_Scanning_Strategy]]
[[Lookup_Table_vs_Search]]