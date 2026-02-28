---
tags:
  - type/permanent
  - status/evergreen
  - attr/principle
  - topic/learning
  - type/tips
---

## installation
`yay -S virt-manager`
`yay -Syu qemu-full libvirt dnsmasq virt-viewer edk2-ovmf bridge-utils swtpm

`
## Permission
- if your disk is mounted by `fstab`, then the [[virt-manager]] can handle it auto.
- if your disk is mounted on `/run/media/name`, you may config `sudo vim /etc/libvirt/qemu.conf`
	- user -> `user = "your name"`
	- group -> `group = "your group"`

## Add windows virtual machine

[[Tip-Install Windows via Libvirt]]

---
## **Related**：
[[Libvirt]]
[[Tip fix can not open virt-manager]]