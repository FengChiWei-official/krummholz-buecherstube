---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---

## Text
## 配置 Docker 使用 Clash 代理

### 前提条件

首先确认：
```
# Clash 是否在运行？
curl -x http://127.0.0.1:7890 https://www.google.com -I
# 如果有响应说明代理正常（7890 是 Clash 默认端口，根据你的配置改）
```
### 方案 A：配置 Docker Daemon（推荐）

创建 Docker systemd 服务目录：
```
mkdir -p /etc/systemd/system/docker.service.d
```

创建代理配置文件：
```
cat > /etc/systemd/system/docker.service.d/http-proxy.conf << 'EOF'
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:7890"
Environment="HTTPS_PROXY=http://127.0.0.1:7890"
Environment="NO_PROXY=localhost,127.0.0.1"
EOF
```

重新加载并重启 Docker：
```
systemctl daemon-reload
systemctl restart docker

# 验证配置
systemctl show --property=Environment docker
```

---

## Thoughts