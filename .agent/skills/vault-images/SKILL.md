---
name: vault-images
description: "Host illustrations and assets for the vault on a public Cloudflare R2 bucket: upload images/pdf/epub with content-addressed keys, dedupe by hash, presign one-off uploads, verify credentials, and return the public URL plus a ready markdown embed. Use when a note needs a diagram, figure, screenshot, or a hosted file that must not be committed to the repo."
---

# vault-images

仓库是纯文本的：图与文件不提交，笔记里只存公开 URL。上传器是
`.agent/skills/vault-images/r2put.py`（纯标准库，无 boto3、无 aws cli）。

## 能力边界

- 桶是**公开**的，任何拿到 URL 的人都能读。只传笔记要用的图与文件，**不传私人内容**。
- 图片不进仓库，笔记只存 URL；`key` 内容寻址（`sha256` 前 20 位），同内容重复上传返回 `exists`，
  不发第二次 PUT。
- 仓库外唯一凭据文件：`~/.config/krummholz/r2.env`（mode 600，不进 git、不进同步盘）。
- 单文件上限 100 MiB（整文件读内存，不做分片）；更大的文件用 `--max-bytes` 自行放宽。
- 用的是 **R2 API token（S3 凭据：Access Key ID + Secret）**，不是 Cloudflare 管理面 API token。

## 装配（每台机器一次）

1. R2 → **Manage R2 API Tokens** → `Create User API token`（继承本人权限；`Account API token`
   只有 Super Admin 能建，用于账户级共享）→ Permissions 选 `Object Read & Write` →
   `Apply to specific buckets only` → `my-books-asset`。
2. 建完只显示**一次** `Access Key ID` + `Secret Access Key`，当场存进下面的文件。
3. 注意：Cloudflare 管理面 API Token 不能签 S3；`Object Read & Write` 只被 S3 API 承认。

```bash
install -d -m 700 ~/.config/krummholz
umask 077
$EDITOR ~/.config/krummholz/r2.env
```

文件内容（`R2_PREFIX` 留空即按 kind 用 `images/` 与 `files/` 默认）：

```ini
R2_ACCOUNT_ID=43ba2e71887e1e8ea5b67e866c3a53ef
R2_ACCESS_KEY_ID=<Access Key ID>
R2_SECRET_ACCESS_KEY=<Secret Access Key>
R2_BUCKET=my-books-asset
R2_PUBLIC_BASE=<桶 Settings → Public access 里的公开地址>
```

`R2_PUBLIC_BASE` 写全 URL 或裸域名都行（裸域名按 `https://` 处理）；它是**只读**的公开读取面，
上传始终走上面那个 S3 端点。`r2.dev` 地址有速率限制，长期链接用自定义域。

密钥丢失即**删 token 重建**（secret 不可再读）。多机各一份文件，不进仓库、不进同步盘。

可选键：`R2_PREFIX`（统一 key 前缀）、`R2_ENDPOINT`（自定义网关/测试）、
`R2_SESSION_TOKEN`（临时凭据；非空时签 `x-amz-security-token`）。

## 日常

```bash
python3 .agent/skills/vault-images/r2put.py check
```

```
ok  bucket my-books-asset reachable, credentials accepted
    endpoint https://43ba2e71887e1e8ea5b67e866c3a53ef.r2.cloudflarestorage.com
    public   https://<R2_PUBLIC_BASE>
```

`R2_PUBLIC_BASE` 含 `r2.dev` 时多一行 note（r2.dev 有速率限制，长期链接建议绑自定义域）。

```bash
python3 .agent/skills/vault-images/r2put.py put figure.svg
```

```
uploaded  images/0ea6867e76b7cebbe04b.svg  (96 B)
  https://pub-xxxx.r2.dev/images/0ea6867e76b7cebbe04b.svg
  ![](https://pub-xxxx.r2.dev/images/0ea6867e76b7cebbe04b.svg)
```

第三行按 kind 变：image → `![](url)`；asset / other → `[<文件 basename>](url)`：

```
uploaded  files/<40hex>.pdf  (12.3 MB)
  https://pub-xxxx.r2.dev/files/<40hex>.pdf
  [book.pdf](https://pub-xxxx.r2.dev/files/<40hex>.pdf)
```

大文件交给没有凭据的客户端（一次性直传）：

```bash
python3 .agent/skills/vault-images/r2put.py presign books/book.pdf --method PUT --expires 3600
curl -X PUT --upload-file book.pdf "<presign 打印的 URL>"
```

`--dry-run` 只打 key 不联网；`--any` 传其他扩展名（如 `.zip`，`application/octet-stream`，
不做魔数校验但**仍受大小上限约束**）；`--json` 给机器读。

## 失败对照

| 现象 | 原因 / 处置 |
|---|---|
| `exit 2` + `missing config: …` | 缺键：按 §装配 补齐 `r2.env`（或在环境里 export） |
| `check` 403 | token 权限不对、账户 id 错，或拿的是**管理面** token（管理面签不了 S3） |
| `check` 404 | 桶名错 |
| `PUT … 403` | token 没有限定到该桶（`Apply to specific buckets only` 里没勾 `my-books-asset`） |
| `curl -I <公开 URL>` 404 | 桶没开 Public access，或 `R2_PUBLIC_BASE` 不是这个桶 |
| `not an image or asset type (--any to override)` | 扩展名不在图/资产表里；确认要传就加 `--any` |
| `content does not look like .pdf` | 魔数与扩展名不符（文件不是 PDF/EPUB） |
| `network error: …` | 断网或 `R2_ENDPOINT` 写错 |

## 冷启动验收

```bash
python3 .agent/skills/vault-images/r2put.py check
```

出 `ok  bucket my-books-asset reachable, credentials accepted` 即装配成功。再用一张 SVG 走完整链路：

```bash
printf '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><rect width="10" height="10"/></svg>' > /tmp/probe.svg
python3 .agent/skills/vault-images/r2put.py put /tmp/probe.svg
curl -sI "<上面打印的 URL>" | head -3
```

期望 `200` 且 `content-type: image/svg+xml`；同文件再传一次应为 `exists`（不重传）。
