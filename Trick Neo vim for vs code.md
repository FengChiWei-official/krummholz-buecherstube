---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---

## Text
1. `init.lua` (Neovim 配置文件)

**路径：** `C:\Users\你的用户名\AppData\Local\nvim\init.lua` (Windows) 或 `~/.config/nvim/init.lua` (Mac/Linux)

lua

```
-- 1. 基础设置：开启系统剪贴板同步
vim.g.mapleader = " "
vim.opt.clipboard = "unnamedplus" -- 核心：让 y/p 与系统剪贴板互通
vim.opt.ignorecase = true        -- 搜索忽略大小写
vim.opt.smartcase = true         -- 包含大写时精确匹配

-- 2. VS Code 环境专用配置
if vim.g.vscode then
    local vscode = require('vscode')

    -- 映射：空格+w 保存，空格+q 关闭
    vim.keymap.set('n', '<leader>w', function() vscode.action('workbench.action.files.save') end)
    vim.keymap.set('n', '<leader>q', function() vscode.action('workbench.action.closeActiveEditor') end)

    -- 跳转功能映射给 VS Code 原生 LSP
    vim.keymap.set('n', 'gd', function() vscode.action('editor.action.revealDefinition') end)
    vim.keymap.set('n', 'gr', function() vscode.action('editor.action.goToReferences') end)

    -- 注释功能 (gcc 注释行, gc 注释选区)
    vim.keymap.set('n', 'gcc', "<Plug>VSCodeCommentaryLine")
    vim.keymap.set('v', 'gc', "<Plug>VSCodeCommentary")
end
```

请谨慎使用此类代码。

---

2. `settings.json` (VS Code 设置文件)

**进入方式：** `Ctrl+Shift+P` -> 输入 `User Settings (JSON)`

json

```
{
    // 1. 指定 Neovim 程序位置 (如果已加环境变量，直接写 "nvim")
    "vscode-neovim.neovimExecutablePaths.win32": "nvim",

    // 2. 排除控制：让 VS Code 接管 Ctrl+F(搜索) 和 Ctrl+A(全选)
    // 注意：这里没有放进 "c" 和 "v"，所以 Ctrl+V 留给 Vim 做列编辑
    "vscode-neovim.ctrlKeysForNormalMode": [
        "f",
        "a"
    ],
    "vscode-neovim.ctrlKeysForInsertMode": [
        "f",
        "a"
    ],

    // 3. 快速逃逸：连按 jj 退出插入模式
    "vscode-neovim.compositeKeys": {
        "jj": {
            "command": "vscode-neovim.escape"
        }
    },

    // 4. 其他优化建议
    "vscode-neovim.sendRequestsToNeovim": true,
    "editor.lineNumbers": "relative", // 开启相对行号，方便 Vim 跳转
    "editor.cursorBlinking": "solid"  // 建议光标不闪烁，更有 Vim 感觉
}
```

请谨慎使用此类代码。

---

3. `keybindings.json` (VS Code 快捷键文件)

**进入方式：** `Ctrl+Shift+P` -> 输入 `Open Keyboard Shortcuts (JSON)`

json

```
[
    {
        "key": "ctrl+shift+c",
        "command": "editor.action.clipboardCopyAction",
        "when": "textInputFocus"
    },
    {
        "key": "ctrl+shift+v",
        "command": "editor.action.clipboardPasteAction",
        "when": "textInputFocus"
    },
    // 额外赠送：如果 Ctrl+C 依然无效，强制解除 Vim 对它的占用
    {
        "key": "ctrl+c",
        "command": "-extension.vim_ctrl+c",
        "when": "editorTextFocus && vim.active && vim.use<C-c> && !inDebugRepl"
    }
]
```

请谨慎使用此类代码。

**如何验证配置成功？**

1. **重启 VS Code**，确保右下角 Neovim 扩展状态正常。
2. **测试 `jj`**：在编辑模式下连按 `jj`，应立即回到 Normal 模式。
3. **测试复制粘贴**：选中一段文字按 `Ctrl+Shift+C`，到浏览器按 `Ctrl+V`，看是否成功。
4. **测试列块选择**：在 Normal 模式按 `Ctrl+V`，然后按 `j` 或 `k`，你应该能看到**垂直方块状**的选区。

如果遇到 `nvim` 路径找不到的报错，请告诉我你的 **Windows 用户名**，我帮你拼出完整的 `nvim.exe` 绝对路径。

---

## Thoughts