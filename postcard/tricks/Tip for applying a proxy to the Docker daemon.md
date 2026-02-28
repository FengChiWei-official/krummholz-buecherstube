---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
aliases:
  - Tip for applying a proxy to the dockerd
---
yes, what you should handle is **[[docker daemon]]**.

## Symptom
If you found that you used a `Golobal Proxy` and visual NIC, and you Docker cannot login, with `curl -I https://registry-1.docker.io/v2/` can not access , however, browser can.

## Text

### 解决方法：不要依赖 TUN 模式，显式指定“真实 IP”

要让 Docker 100% 稳定地走代理，最稳妥的方法是**在 daemon.json 中使用宿主机的局域网 IP（或 Docker 网桥 IP），而不是 127.0.0.1**，同时开启代理软件的**“允许局域网连接”**。

#### 步骤 1：开启代理软件的“允许局域网连接”

在你的代理软件（Clash, v2rayU 等）设置里，找到 **Allow LAN** (允许来自局域网的连接)，把它打开。

- 原因：我们要让 Docker 通过“外部”IP 访问你的代理，而不是通过内部回环。
    

#### 步骤 2：找到你的“真实 IP”

在终端输入：

codeBash

```
ip addr show docker0
```

找到 inet 后面的那个 IP，通常是 **172.17.0.1**。

- 解释：这是 Docker 自带的网桥网关地址。Docker 守护进程和容器都能无条件访问这个 IP。
    

如果找不到 docker0，也可以用 ip addr 找你的 Wifi 或以太网 IP（例如 192.168.1.5）。

#### 步骤 3：修改 daemon.json

把之前的 127.0.0.1 换成刚才找到的 172.17.0.1。

codeBash

```
sudo vim /etc/docker/daemon.json
```

修改后如下（假设你的代理端口是 7890）：

codeJSON

```
{
  "proxies": {
    "http-proxy": "http://172.17.0.1:7890",
    "https-proxy": "http://172.17.0.1:7890",
    "no-proxy": "localhost,127.0.0.1,::1,127.0.0.0/8,172.17.0.0/16,10.0.0.0/8"
  }
}
```

注意：我在 no-proxy 里加了 172.17.0.0/16 等私有网段，防止 Docker 访问内部容器服务时也傻傻地去走代理。

#### 步骤 4：重启 Docker

codeBash

```
sudo systemctl restart docker
```

#### 步骤 5：验证

codeBash

```
docker login
```
## Thoughts