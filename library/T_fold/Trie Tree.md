---
tags:
  - type/permanent
  - topic/learning
  - attr/concept
  - status/evergreen
---

## Definition

``` cpp
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

using namespace std;

// 霍夫曼树/字典树节点定义
struct TrieNode {
    char val;          // '\0' 表示内部节点，否则为对应的叶子字符
    TrieNode* left;
    TrieNode* right;

    TrieNode(char c = '\0') : val(c), left(nullptr), right(nullptr) {}
};

// 1. 递归还原 Huffman 树
// 使用引用传参 index，确保全局指针能够正确向后移动
TrieNode* rebuildTree(const string& s, int& index) {
    if (index >= s.length()) return nullptr;

    if (s[index] == '0') {
        // 创建内部节点
        TrieNode* node = new TrieNode('\0');
        index++; // 跳过 '0'
        node->left = rebuildTree(s, index);  // 递归构建左子树
        node->right = rebuildTree(s, index); // 递归构建右子树
        return node;
    } else if (s[index] == '1') {
        // 创建叶子节点
        index++; // 跳过 '1'
        char leaf_char = s[index]; // 获取对应的字符
        TrieNode* node = new TrieNode(leaf_char);
        index++; // 跳过该字符
        return node;
    }
    return nullptr;
}

// 2. 深度优先搜索生成编码表 (字符 -> 01串)
void generateCodes(TrieNode* root, const string& current_path, unordered_map<char, string>& code_map) {
    if (!root) return;
    
    // 如果是叶子节点，记录编码
    if (root->val != '\0') {
        code_map[root->val] = current_path;
        return;
    }
    
    generateCodes(root->left, current_path + "0", code_map);
    generateCodes(root->right, current_path + "1", code_map);
}

// 3. 解码指令 (把 01 串还原为文本)
string decode(TrieNode* root, const string& binary_str) {
    string decoded_text = "";
    TrieNode* curr = root;
    for (char bit : binary_str) {
        if (bit == '0') {
            curr = curr->left;
        } else {
            curr = curr->right;
        }

        // 走到叶子节点，输出字符并重置回根节点
        if (curr && curr->val != '\0') {
            decoded_text += curr->val;
            curr = root;
        }
    }
    return decoded_text;
}

// 4. 编码指令 (把文本转换为 01 串)
string encode(const string& text, const unordered_map<char, string>& code_map) {
    string binary_str = "";
    for (char c : text) {
        if (code_map.count(c)) {
            binary_str += code_map.at(c);
        }
    }
    return binary_str;
}

// 内存释放
void freeTree(TrieNode* root) {
    if (!root) return;
    freeTree(root->left);
    freeTree(root->right);
    delete root;
}

int main() {
    // 测试用例
    string tree_repr = "001b01c1d1a";
    
    int index = 0;
    TrieNode* root = rebuildTree(tree_repr, index);
    
    // 生成编码字典
    unordered_map<char, string> code_map;
    generateCodes(root, "", code_map);
    
    // 打印每个字符的 Huffman 编码进行验证
    cout << "--- 霍夫曼编码表 ---" << endl;
    for (auto& pair : code_map) {
        cout << pair.first << ": " << pair.second << endl;
    }
    
    // 模拟指令 1：编码 (Encode)
    string text_to_encode = "cadb";
    string encoded = encode(text_to_encode, code_map);
    cout << "\n编码 '" << text_to_encode << "': " << encoded << endl;
    
    // 模拟指令 2：解码 (Decode)
    string binary_to_decode = "010101100"; // c(010) a(1) d(011) b(00)
    string decoded = decode(root, binary_to_decode);
    cout << "解码 '" << binary_to_decode << "': " << decoded << endl;

    freeTree(root);
    return 0;
}
```

---
## **Related**
