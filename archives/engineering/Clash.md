---
tags:
  - type/lit
  - topic/learning
  - status/archive
source: 《卡片盒笔记法》 by Sönke Ahrens
---

## Text
           PID: 10196 (clash-verge)
           UID: 1000 (mia)
           GID: 1000 (mia)
        Signal: 6 (ABRT)
     Timestamp: Tue 2026-03-10 16:56:43 CST (11s ago)
  Command Line: clash-verge
    Executable: /usr/bin/clash-verge
 Control Group: /user.slice/user-1000.slice/user@1000.service/session.slice/wayland-wm@hyprland.desktop.service
          Unit: user@1000.service
     User Unit: wayland-wm@hyprland.desktop.service
         Slice: user-1000.slice
     Owner UID: 1000 (mia)
       Boot ID: 0ac3bda48d524cbeb01c17dc7ae1eaf8
    Machine ID: 328fe1c4539145148eb3e5b39e3692d7
      Hostname: mia-82ms
       Storage: /var/lib/systemd/coredump/core.clash-verge.1000.0ac3bda48d524cbeb01c17dc7ae1eaf8.10196.1773133003000000.zst (present)
  Size on Disk: 2.2M
       Message: Process 10196 (clash-verge) of user 1000 dumped core.
                
                Stack trace of thread 10267:
                #0  0x00007efca2789a2c n/a (libc.so.6 + 0x98a2c)
                #1  0x00007efca272f1a0 raise (libc.so.6 + 0x3e1a0)
                #2  0x00007efca27165fe abort (libc.so.6 + 0x255fe)
                #3  0x000055ff1c91609a n/a (/usr/bin/clash-verge + 0x1e0d09a)
                #4  0x000055ff1c9245a9 n/a (/usr/bin/clash-verge + 0x1e1b5a9)
                #5  0x000055ff1c901bba n/a (/usr/bin/clash-verge + 0x1df8bba)
                #6  0x000055ff1c901baa n/a (/usr/bin/clash-verge + 0x1df8baa)
                #7  0x000055ff1c925dad n/a (/usr/bin/clash-verge + 0x1e1cdad)
                #8  0x000055ff1c925bca n/a (/usr/bin/clash-verge + 0x1e1cbca)
                #9  0x000055ff1c91f1b9 n/a (/usr/bin/clash-verge + 0x1e161b9)
                #10 0x000055ff1c901bdd n/a (/usr/bin/clash-verge + 0x1df8bdd)
                #11 0x000055ff1c37a100 n/a (/usr/bin/clash-verge + 0x1871100)
                #12 0x000055ff1c379236 n/a (/usr/bin/clash-verge + 0x1870236)
                #13 0x000055ff1bdc30a3 n/a (/usr/bin/clash-verge + 0x12ba0a3)
                #14 0x000055ff1bb5f3e3 n/a (/usr/bin/clash-verge + 0x10563e3)
                #15 0x000055ff1ca7efcb n/a (/usr/bin/clash-verge + 0x1f75fcb)
                #16 0x000055ff1ca7d6de n/a (/usr/bin/clash-verge + 0x1f746de)
                #17 0x000055ff1ca73586 n/a (/usr/bin/clash-verge + 0x1f6a586)
                #18 0x000055ff1ca674c6 n/a (/usr/bin/clash-verge + 0x1f5e4c6)
                #19 0x000055ff1ca68fb3 n/a (/usr/bin/clash-verge + 0x1f5ffb3)
                #20 0x000055ff1c9196df n/a (/usr/bin/clash-verge + 0x1e106df)
                #21 0x00007efca278797a n/a (libc.so.6 + 0x9697a)
                #22 0x00007efca280b2bc n/a (libc.so.6 + 0x11a2bc)
                
                Stack trace of thread 10253:
                #0  0x00007efca280906d syscall (libc.so.6 + 0x11806d)
                #1  0x000055ff1c5fc179 n/a (/usr/bin/clash-verge + 0x1af3179)
                #2  0x000055ff1ca7bb5e n/a (/usr/bin/clash-verge + 0x1f72b5e)
                #3  0x000055ff1ca7ed3b n/a (/usr/bin/clash-verge + 0x1f75d3b)
                #4  0x000055ff1ca7d9df n/a (/usr/bin/clash-verge + 0x1f749df)
                #5  0x000055ff1ca73586 n/a (/usr/bin/clash-verge + 0x1f6a586)
                #6  0x000055ff1ca674c6 n/a (/usr/bin/clash-verge + 0x1f5e4c6)
                #7  0x000055ff1ca68fb3 n/a (/usr/bin/clash-verge + 0x1f5ffb3)
                #8  0x000055ff1c9196df n/a (/usr/bin/clash-verge + 0x1e106df)
                #9  0x00007efca278797a n/a (libc.so.6 + 0x9697a)
                #10 0x00007efca280b2bc n/a (libc.so.6 + 0x11a2bc)
                
                Stack trace of thread 10252:
                #0  0x00007efca280906d syscall (libc.so.6 + 0x11806d)
                #1  0x000055ff1c5fc179 n/a (/usr/bin/clash-verge + 0x1af3179)
                #2  0x000055ff1ca7bb5e n/a (/usr/bin/clash-verge + 0x1f72b5e)
                #3  0x000055ff1ca7ed3b n/a (/usr/bin/clash-verge + 0x1f75d3b)
                #4  0x000055ff1ca7d9df n/a (/usr/bin/clash-verge + 0x1f749df)
                #5  0x000055ff1ca73586 n/a (/usr/bin/clash-verge + 0x1f6a586)
                #6  0x000055ff1ca674c6 n/a (/usr/bin/clash-verge + 0x1f5e4c6)
                #7  0x000055ff1ca68fb3 n/a (/usr/bin/clash-verge + 0x1f5ffb3)
                #8  0x000055ff1c9196df n/a (/usr/bin/clash-verge + 0x1e106df)
                #9  0x00007efca278797a n/a (libc.so.6 + 0x9697a)
                #10 0x00007efca280b2bc n/a (libc.so.6 + 0x11a2bc)
                
                Stack trace of thread 10263:
                #0  0x00007efca280906d syscall (libc.so.6 + 0x11806d)
                #1  0x000055ff1c5fc179 n/a (/usr/bin/clash-verge + 0x1af3179)
                #2  0x000055ff1ca7bb5e n/a (/usr/bin/clash-verge + 0x1f72b5e)
                #3  0x000055ff1ca7ed3b n/a (/usr/bin/clash-verge + 0x1f75d3b)
                #4  0x000055ff1ca7d9df n/a (/usr/bin/clash-verge + 0x1f749df)
                #5  0x000055ff1ca73586 n/a (/usr/bin/clash-verge + 0x1f6a586)
                #6  0x000055ff1ca674c6 n/a (/usr/bin/clash-verge + 0x1f5e4c6)
                #7  0x000055ff1ca68fb3 n/a (/usr/bin/clash-verge + 0x1f5ffb3)
                #8  0x000055ff1c9196df n/a (/usr/bin/clash-verge + 0x1e106df)
                #9  0x00007efca278797a n/a (libc.so.6 + 0x9697a)
                #10 0x00007efca280b2bc n/a (libc.so.6 + 0x11a2bc)
                
                Stack trace of thread 10272:
                #0  0x00007efca280906d syscall (libc.so.6 + 0x11806d)
                #1  0x00007efcaae3480e g_cond_wait_until (libglib-2.0.so.0 + 0x8d80e)
                #2  0x00007efcaadcd1f7 n/a (libglib-2.0.so.0 + 0x261f7)
                #3  0x00007efcaadcd36f g_async_queue_timeout_pop (libglib-2.0.so.0 + 0x2636f)
                #4  0x00007efcaae3e2a0 n/a (libglib-2.0.so.0 + 0x972a0)
                #5  0x00007efcaae3d13c n/a (libglib-2.0.so.0 + 0x9613c)
                #6  0x00007efca278797a n/a (libc.so.6 + 0x9697a)
                #7  0x00007efca280b2bc n/a (libc.so.6 + 0x11a2bc)
                
                Stack trace of thread 10256:
                #0  0x00007efca280906d syscall (libc.so.6 + 0x11806d)
                #1  0x000055ff1c5fc179 n/a (/usr/bin/clash-verge + 0x1af3179)
                #2  0x000055ff1ca7bb5e n/a (/usr/bin/clash-verge + 0x1f72b5e)
                #3  0x000055ff1ca7ed3b n/a (/usr/bin/clash-verge + 0x1f75d3b)
                #4  0x000055ff1ca7d9df n/a (/usr/bin/clash-verge + 0x1f749df)
                #5  0x000055ff1ca73586 n/a (/usr/bin/clash-verge + 0x1f6a586)
                #6  0x000055ff1ca674c6 n/a (/usr/bin/clash-verge + 0x1f5e4c6)
                #7  0x000055ff1ca68fb3 n/a (/usr/bin/clash-verge + 0x1f5ffb3)
                #8  0x000055ff1c9196df n/a (/usr/bin/clash-verge + 0x1e106df)
                #9  0x00007efca278797a n/a (libc.so.6 + 0x9697a)
                #10 0x00007efca280b2bc n/a (libc.so.6 + 0x11a2bc)
                
                Stack trace of thread 10547:
                #0  0x00007efca280906d syscall (libc.so.6 + 0x11806d)
                #1  0x000055ff1c5fc27b n/a (/usr/bin/clash-verge + 0x1af327b)
                #2  0x000055ff1ca67586 n/a (/usr/bin/clash-verge + 0x1f5e586)
                #3  0x000055ff1ca68fb3 n/a (/usr/bin/clash-verge + 0x1f5ffb3)
                #4  0x000055ff1c9196df n/a (/usr/bin/clash-verge + 0x1e106df)
                #5  0x00007efca278797a n/a (libc.so.6 + 0x9697a)
                #6  0x00007efca280b2bc n/a (libc.so.6 + 0x11a2bc)
                
                Stack trace of thread 10270:
                #0  0x00007efca280906d syscall (libc.so.6 + 0x11806d)
                #1  0x00007efcaae33a2e g_cond_wait (libglib-2.0.so.0 + 0x8ca2e)
                #2  0x00007efcaadcd22d n/a (libglib-2.0.so.0 + 0x2622d)
                #3  0x00007efcaae3d607 n/a (libglib-2.0.so.0 + 0x96607)
                #4  0x00007efcaae3d13c n/a (libglib-2.0.so.0 + 0x9613c)
                #5  0x00007efca278797a n/a (libc.so.6 + 0x9697a)
                #6  0x00007efca280b2bc n/a (libc.so.6 + 0x11a2bc)
                
                Stack trace of thread 10269:
                #0  0x00007efca280906d syscall (libc.so.6 + 0x11806d)
                #1  0x00007efcaae33a2e g_cond_wait (libglib-2.0.so.0 + 0x8ca2e)
                #2  0x00007efcaadcd22d n/a (libglib-2.0.so.0 + 0x2622d)
                #3  0x00007efcaadcd29d g_async_queue_pop (libglib-2.0.so.0 + 0x2629d)
                #4  0x00007efca055851c n/a (libpangoft2-1.0.so.0 + 0xc51c)
                #5  0x00007efcaae3d13c n/a (libglib-2.0.so.0 + 0x9613c)
                #6  0x00007efca278797a n/a (libc.so.6 + 0x9697a)
                #7  0x00007efca280b2bc n/a (libc.so.6 + 0x11a2bc)
                
                Stack trace of thread 10266:
                #0  0x00007efca280906d syscall (libc.so.6 + 0x11806d)
                #1  0x000055ff1c5fc179 n/a (/usr/bin/clash-verge + 0x1af3179)
                #2  0x000055ff1ca7bb5e n/a (/usr/bin/clash-verge + 0x1f72b5e)
                #3  0x000055ff1ca7ed3b n/a (/usr/bin/clash-verge + 0x1f75d3b)
                #4  0x000055ff1ca7d9df n/a (/usr/bin/clash-verge + 0x1f749df)
                #5  0x000055ff1ca73586 n/a (/usr/bin/clash-verge + 0x1f6a586)
                #6  0x000055ff1ca674c6 n/a (/usr/bin/clash-verge + 0x1f5e4c6)
                #7  0x000055ff1ca68fb3 n/a (/usr/bin/clash-verge + 0x1f5ffb3)
                #8  0x000055ff1c9196df n/a (/usr/bin/clash-verge + 0x1e106df)
                #9  0x00007efca278797a n/a (libc.so.6 + 0x9697a)
                #10 0x00007efca280b2bc n/a (libc.so.6 + 0x11a2bc)
                
                Stack trace of thread 10540:
                #0  0x00007efca278ff32 n/a (libc.so.6 + 0x9ef32)
                #1  0x00007efca278439c n/a (libc.so.6 + 0x9339c)
                #2  0x00007efca27d4452 clock_nanosleep (libc.so.6 + 0xe3452)
                #3  0x00007efca27e0537 __nanosleep (libc.so.6 + 0xef537)
                #4  0x000055ff1c459f86 n/a (/usr/bin/clash-verge + 0x1950f86)
                #5  0x000055ff1c45baef n/a (/usr/bin/clash-verge + 0x1952aef)
                #6  0x000055ff1c9196df n/a (/usr/bin/clash-verge + 0x1e106df)
                #7  0x00007efca278797a n/a (libc.so.6 + 0x9697a)
                #8  0x00007efca280b2bc n/a (libc.so.6 + 0x11a2bc)
                
                Stack trace of thread 10251:
                #0  0x000055ff1c34fb3f n/a (/usr/bin/clash-verge + 0x1846b3f)
                #1  0x000055ff1c33c50e n/a (/usr/bin/clash-verge + 0x183350e)
                #2  0x000055ff1c3471b8 n/a (/usr/bin/clash-verge + 0x183e1b8)
                #3  0x000055ff1bee1410 n/a (/usr/bin/clash-verge + 0x13d8410)
                #4  0x000055ff1c5f6e4a n/a (/usr/bin/clash-verge + 0x1aede4a)
                #5  0x000055ff1bee09a9 n/a (/usr/bin/clash-verge + 0x13d79a9)
                #6  0x000055ff1b6d96ad n/a (/usr/bin/clash-verge + 0xbd06ad)
                #7  0x000055ff1bdcc0cb n/a (/usr/bin/clash-verge + 0x12c30cb)
                #8  0x000055ff1bbcdf13 n/a (/usr/bin/clash-verge + 0x10c4f13)
                #9  0x000055ff1ca7efcb n/a (/usr/bin/clash-verge + 0x1f75fcb)
                #10 0x000055ff1ca7d6de n/a (/usr/bin/clash-verge + 0x1f746de)
                #11 0x000055ff1ca73586 n/a (/usr/bin/clash-verge + 0x1f6a586)
                #12 0x000055ff1ca674c6 n/a (/usr/bin/clash-verge + 0x1f5e4c6)
                #13 0x000055ff1ca68fb3 n/a (/usr/bin/clash-verge + 0x1f5ffb3)
                #14 0x000055ff1c9196df n/a (/usr/bin/clash-verge + 0x1e106df)
                #15 0x00007efca278797a n/a (libc.so.6 + 0x9697a)
                #16 0x00007efca280b2bc n/a (libc.so.6 + 0x11a2bc)
                
                Stack trace of thread 10254:
                #0  0x00007efca280906d syscall (libc.so.6 + 0x11806d)
                #1  0x000055ff1c5fc179 n/a (/usr/bin/clash-verge + 0x1af3179)
                #2  0x000055ff1ca7bb5e n/a (/usr/bin/clash-verge + 0x1f72b5e)
                #3  0x000055ff1ca7ed3b n/a (/usr/bin/clash-verge + 0x1f75d3b)
                #4  0x000055ff1ca7d9df n/a (/usr/bin/clash-verge + 0x1f749df)
                #5  0x000055ff1ca73586 n/a (/usr/bin/clash-verge + 0x1f6a586)
                #6  0x000055ff1ca674c6 n/a (/usr/bin/clash-verge + 0x1f5e4c6)
                #7  0x000055ff1ca68fb3 n/a (/usr/bin/clash-verge + 0x1f5ffb3)
                #8  0x000055ff1c9196df n/a (/usr/bin/clash-verge + 0x1e106df)
                #9  0x00007efca278797a n/a (libc.so.6 + 0x9697a)
                #10 0x00007efca280b2bc n/a (libc.so.6 + 0x11a2bc)
                
                Stack trace of thread 10551:
                #0  0x00007efca280906d syscall (libc.so.6 + 0x11806d)
                #1  0x000055ff1c42bc16 n/a (/usr/bin/clash-verge + 0x1922c16)
                #2  0x000055ff1c4290ea n/a (/usr/bin/clash-verge + 0x19200ea)
                #3  0x000055ff1c42f8df n/a (/usr/bin/clash-verge + 0x19268df)
                #4  0x000055ff1c9196df n/a (/usr/bin/clash-verge + 0x1e106df)
                #5  0x00007efca278797a n/a (libc.so.6 + 0x9697a)
                #6  0x00007efca280b2bc n/a (libc.so.6 + 0x11a2bc)
                
                Stack trace of thread 10255:
                #0  0x00007efca280906d syscall (libc.so.6 + 0x11806d)
                #1  0x000055ff1c5fc179 n/a (/usr/bin/clash-verge + 0x1af3179)
                #2  0x000055ff1ca7bb5e n/a (/usr/bin/clash-verge + 0x1f72b5e)
                #3  0x000055ff1ca7ed3b n/a (/usr/bin/clash-verge + 0x1f75d3b)
                #4  0x000055ff1ca7d9df n/a (/usr/bin/clash-verge + 0x1f749df)
                #5  0x000055ff1ca73586 n/a (/usr/bin/clash-verge + 0x1f6a586)
                #6  0x000055ff1ca674c6 n/a (/usr/bin/clash-verge + 0x1f5e4c6)
                #7  0x000055ff1ca68fb3 n/a (/usr/bin/clash-verge + 0x1f5ffb3)
                #8  0x000055ff1c9196df n/a (/usr/bin/clash-verge + 0x1e106df)
                #9  0x00007efca278797a n/a (libc.so.6 + 0x9697a)
                #10 0x00007efca280b2bc n/a (libc.so.6 + 0x11a2bc)
                
                Stack trace of thread 10271:
                #0  0x00007efca278ff32 n/a (libc.so.6 + 0x9ef32)
                #1  0x00007efca278439c n/a (libc.so.6 + 0x9339c)
                #2  0x00007efca27843e4 n/a (libc.so.6 + 0x933e4)
                #3  0x00007efca27fe2f6 ppoll (libc.so.6 + 0x10d2f6)
                #4  0x00007efcaae07744 n/a (libglib-2.0.so.0 + 0x60744)
                #5  0x00007efcaae07825 g_main_context_iteration (libglib-2.0.so.0 + 0x60825)
                #6  0x00007efcaae07872 n/a (libglib-2.0.so.0 + 0x60872)
                #7  0x00007efcaae3d13c n/a (libglib-2.0.so.0 + 0x9613c)
                #8  0x00007efca278797a n/a (libc.so.6 + 0x9697a)
                #9  0x00007efca280b2bc n/a (libc.so.6 + 0x11a2bc)
                
                Stack trace of thread 10261:
                #0  0x00007efca280906d syscall (libc.so.6 + 0x11806d)
                #1  0x000055ff1c5fc179 n/a (/usr/bin/clash-verge + 0x1af3179)
                #2  0x000055ff1ca7bb5e n/a (/usr/bin/clash-verge + 0x1f72b5e)
                #3  0x000055ff1ca7ed3b n/a (/usr/bin/clash-verge + 0x1f75d3b)
                #4  0x000055ff1ca7d9df n/a (/usr/bin/clash-verge + 0x1f749df)
                #5  0x000055ff1ca73586 n/a (/usr/bin/clash-verge + 0x1f6a586)
                #6  0x000055ff1ca674c6 n/a (/usr/bin/clash-verge + 0x1f5e4c6)
                #7  0x000055ff1ca68fb3 n/a (/usr/bin/clash-verge + 0x1f5ffb3)
                #8  0x000055ff1c9196df n/a (/usr/bin/clash-verge + 0x1e106df)
                #9  0x00007efca278797a n/a (libc.so.6 + 0x9697a)
                #10 0x00007efca280b2bc n/a (libc.so.6 + 0x11a2bc)
                
                Stack trace of thread 10277:
                #0  0x00007efca278ff32 n/a (libc.so.6 + 0x9ef32)
                #1  0x00007efca278439c n/a (libc.so.6 + 0x9339c)
                #2  0x00007efca27843e4 n/a (libc.so.6 + 0x933e4)
                #3  0x00007efca27fe2f6 ppoll (libc.so.6 + 0x10d2f6)
                #4  0x00007efcaae07744 n/a (libglib-2.0.so.0 + 0x60744)
                #5  0x00007efcaae07825 g_main_context_iteration (libglib-2.0.so.0 + 0x60825)
                #6  0x00007efc940f37be n/a (libdconfsettings.so + 0x77be)
                #7  0x00007efcaae3d13c n/a (libglib-2.0.so.0 + 0x9613c)
                #8  0x00007efca278797a n/a (libc.so.6 + 0x9697a)
                #9  0x00007efca280b2bc n/a (libc.so.6 + 0x11a2bc)
                
                Stack trace of thread 10262:
                #0  0x00007efca280906d syscall (libc.so.6 + 0x11806d)
                #1  0x000055ff1c5fc179 n/a (/usr/bin/clash-verge + 0x1af3179)
                #2  0x000055ff1ca7bb5e n/a (/usr/bin/clash-verge + 0x1f72b5e)
                #3  0x000055ff1ca7ed3b n/a (/usr/bin/clash-verge + 0x1f75d3b)
                #4  0x000055ff1ca7d9df n/a (/usr/bin/clash-verge + 0x1f749df)
                #5  0x000055ff1ca73586 n/a (/usr/bin/clash-verge + 0x1f6a586)
                #6  0x000055ff1ca674c6 n/a (/usr/bin/clash-verge + 0x1f5e4c6)
                #7  0x000055ff1ca68fb3 n/a (/usr/bin/clash-verge + 0x1f5ffb3)
                #8  0x000055ff1c9196df n/a (/usr/bin/clash-verge + 0x1e106df)
                #9  0x00007efca278797a n/a (libc.so.6 + 0x9697a)
                #10 0x00007efca280b2bc n/a (libc.so.6 + 0x11a2bc)
                
                Stack trace of thread 10196:
                #0  0x00007efca27943bb n/a (libc.so.6 + 0xa33bb)
                #1  0x00007efca2796d61 n/a (libc.so.6 + 0xa5d61)
                #2  0x00007efca2796fed n/a (libc.so.6 + 0xa5fed)
                #3  0x00007efcaae0cabb g_malloc (libglib-2.0.so.0 + 0x65abb)
                #4  0x00007efcaae55cc3 n/a (libglib-2.0.so.0 + 0xaecc3)
                #5  0x00007efcaae5131f g_variant_new_string (libglib-2.0.so.0 + 0xaa31f)
                #6  0x00007efca4f3dbd5 g_dbus_message_set_destination (libgio-2.0.so.0 + 0x10ebd5)
                #7  0x00007efca4f3ed4d g_dbus_message_new_method_call (libgio-2.0.so.0 + 0x10fd4d)
                #8  0x00007efca4f42e08 n/a (libgio-2.0.so.0 + 0x113e08)
                #9  0x00007efca4f431f7 g_dbus_connection_call (libgio-2.0.so.0 + 0x1141f7)
                #10 0x00007efca4f50206 n/a (libgio-2.0.so.0 + 0x121206)
                #11 0x00007efca4f5062f n/a (libgio-2.0.so.0 + 0x12162f)
                #12 0x00007efca4ed794c n/a (libgio-2.0.so.0 + 0xa894c)
                #13 0x00007efca4edd3b2 n/a (libgio-2.0.so.0 + 0xae3b2)
                #14 0x00007efca4f428fb n/a (libgio-2.0.so.0 + 0x1138fb)
                #15 0x00007efca4ed794c n/a (libgio-2.0.so.0 + 0xa894c)
                #16 0x00007efca4ed7995 n/a (libgio-2.0.so.0 + 0xa8995)
                #17 0x00007efcaae05f4d n/a (libglib-2.0.so.0 + 0x5ef4d)
                #18 0x00007efcaae07617 n/a (libglib-2.0.so.0 + 0x60617)
                #19 0x00007efcaae07825 g_main_context_iteration (libglib-2.0.so.0 + 0x60825)
                #20 0x00007efca536bd3f gtk_main_iteration_do (libgtk-3.so.0 + 0x36bd3f)
                #21 0x000055ff1b80a10e n/a (/usr/bin/clash-verge + 0xd0110e)
                #22 0x000055ff1bce2900 n/a (/usr/bin/clash-verge + 0x11d9900)
                #23 0x000055ff1c33c413 n/a (/usr/bin/clash-verge + 0x1833413)
                #24 0x000055ff1c33c455 n/a (/usr/bin/clash-verge + 0x1833455)
                #25 0x00007efca27187f9 __libc_start_main (libc.so.6 + 0x277f9)
                #26 0x000055ff1b5b75a5 n/a (/usr/bin/clash-verge + 0xaae5a5)
                
                Stack trace of thread 10264:
                #0  0x00007efca278ff32 n/a (libc.so.6 + 0x9ef32)
                #1  0x00007efca278439c n/a (libc.so.6 + 0x9339c)
                #2  0x00007efca27843e4 n/a (libc.so.6 + 0x933e4)
                #3  0x00007efca280b595 epoll_wait (libc.so.6 + 0x11a595)
                #4  0x000055ff1ca70b37 n/a (/usr/bin/clash-verge + 0x1f67b37)
                #5  0x000055ff1ca76b12 n/a (/usr/bin/clash-verge + 0x1f6db12)
                #6  0x000055ff1ca7ec65 n/a (/usr/bin/clash-verge + 0x1f75c65)
                #7  0x000055ff1ca7d9df n/a (/usr/bin/clash-verge + 0x1f749df)
                #8  0x000055ff1ca73586 n/a (/usr/bin/clash-verge + 0x1f6a586)
                #9  0x000055ff1ca674c6 n/a (/usr/bin/clash-verge + 0x1f5e4c6)
                #10 0x000055ff1ca68fb3 n/a (/usr/bin/clash-verge + 0x1f5ffb3)
                #11 0x000055ff1c9196df n/a (/usr/bin/clash-verge + 0x1e106df)
                #12 0x00007efca278797a n/a (libc.so.6 + 0x9697a)
                #13 0x00007efca280b2bc n/a (libc.so.6 + 0x11a2bc)
                
                Stack trace of thread 10257:
                #0  0x00007efca280906d syscall (libc.so.6 + 0x11806d)
                #1  0x000055ff1c5fc179 n/a (/usr/bin/clash-verge + 0x1af3179)
                #2  0x000055ff1ca7bb5e n/a (/usr/bin/clash-verge + 0x1f72b5e)
                #3  0x000055ff1ca7ed3b n/a (/usr/bin/clash-verge + 0x1f75d3b)
                #4  0x000055ff1ca7d9df n/a (/usr/bin/clash-verge + 0x1f749df)
                #5  0x000055ff1ca73586 n/a (/usr/bin/clash-verge + 0x1f6a586)
                #6  0x000055ff1ca674c6 n/a (/usr/bin/clash-verge + 0x1f5e4c6)
                #7  0x000055ff1ca68fb3 n/a (/usr/bin/clash-verge + 0x1f5ffb3)
                #8  0x000055ff1c9196df n/a (/usr/bin/clash-verge + 0x1e106df)
                #9  0x00007efca278797a n/a (libc.so.6 + 0x9697a)
                #10 0x00007efca280b2bc n/a (libc.so.6 + 0x11a2bc)
                
                Stack trace of thread 10258:
                #0  0x00007efca280906d syscall (libc.so.6 + 0x11806d)
                #1  0x000055ff1c5fc179 n/a (/usr/bin/clash-verge + 0x1af3179)
                #2  0x000055ff1ca7bb5e n/a (/usr/bin/clash-verge + 0x1f72b5e)
                #3  0x000055ff1ca7ed3b n/a (/usr/bin/clash-verge + 0x1f75d3b)
                #4  0x000055ff1ca7d9df n/a (/usr/bin/clash-verge + 0x1f749df)
                #5  0x000055ff1ca73586 n/a (/usr/bin/clash-verge + 0x1f6a586)
                #6  0x000055ff1ca674c6 n/a (/usr/bin/clash-verge + 0x1f5e4c6)
                #7  0x000055ff1ca68fb3 n/a (/usr/bin/clash-verge + 0x1f5ffb3)
                #8  0x000055ff1c9196df n/a (/usr/bin/clash-verge + 0x1e106df)
                #9  0x00007efca278797a n/a (libc.so.6 + 0x9697a)
                #10 0x00007efca280b2bc n/a (libc.so.6 + 0x11a2bc)
                
                Stack trace of thread 10265:
                #0  0x00007efca280906d syscall (libc.so.6 + 0x11806d)
                #1  0x000055ff1c5fc179 n/a (/usr/bin/clash-verge + 0x1af3179)
                #2  0x000055ff1ca7bb5e n/a (/usr/bin/clash-verge + 0x1f72b5e)
                #3  0x000055ff1ca7ed3b n/a (/usr/bin/clash-verge + 0x1f75d3b)
                #4  0x000055ff1ca7d9df n/a (/usr/bin/clash-verge + 0x1f749df)
                #5  0x000055ff1ca73586 n/a (/usr/bin/clash-verge + 0x1f6a586)
                #6  0x000055ff1ca674c6 n/a (/usr/bin/clash-verge + 0x1f5e4c6)
                #7  0x000055ff1ca68fb3 n/a (/usr/bin/clash-verge + 0x1f5ffb3)
                #8  0x000055ff1c9196df n/a (/usr/bin/clash-verge + 0x1e106df)
                #9  0x00007efca278797a n/a (libc.so.6 + 0x9697a)
                #10 0x00007efca280b2bc n/a (libc.so.6 + 0x11a2bc)
                
                Stack trace of thread 10545:
                #0  0x00007efca280906d syscall (libc.so.6 + 0x11806d)
                #1  0x000055ff1b7f0646 n/a (/usr/bin/clash-verge + 0xce7646)
                #2  0x000055ff1b7ca379 n/a (/usr/bin/clash-verge + 0xcc1379)
                #3  0x000055ff1b84e5ff n/a (/usr/bin/clash-verge + 0xd455ff)
                #4  0x000055ff1c9196df n/a (/usr/bin/clash-verge + 0x1e106df)
                #5  0x00007efca278797a n/a (libc.so.6 + 0x9697a)
                #6  0x00007efca280b2bc n/a (libc.so.6 + 0x11a2bc)
                
                Stack trace of thread 10546:
                #0  0x00007efca280b2ad n/a (libc.so.6 + 0x11a2ad)
                ELF object binary architecture: AMD x86-64


---

## Thoughts
PID: 6045 (drkonqi-coredum)

UID: 1000 (mia)

GID: 1000 (mia)

Signal: 11 (SEGV)

Timestamp: Tue 2026-03-10 17:04:36 CST (12s ago)

Command Line: /usr/lib/drkonqi-coredump-launcher

Executable: /usr/lib/drkonqi-coredump-launcher

Control Group: /user.slice/user-1000.slice/user@1000.service/app.slice/drkonqi-coredump-launcher@16-16387-5896_5897-0.service

Unit: user@1000.service

User Unit: drkonqi-coredump-launcher@16-16387-5896_5897-0.service

Slice: user-1000.slice

Owner UID: 1000 (mia)

Boot ID: 4aab6d4c734843a09b7fc142b4839fb8

Machine ID: 328fe1c4539145148eb3e5b39e3692d7

Hostname: mia-82ms

Storage: /var/lib/systemd/coredump/core.drkonqi-coredum.1000.4aab6d4c734843a09b7fc142b4839fb8.6045.1773133476000000.zst (present)

Size on Disk: 723.3K

Message: Process 6045 (drkonqi-coredum) of user 1000 dumped core.

Stack trace of thread 6045:

#0 0x00007f5112be4e53 _ZN8QVariantC2ERK7QString (libQt6Core.so.6 + 0x1e4e53)

#1 0x00007f5111f430cd n/a (libQt6Gui.so.6 + 0x5430cd)

#2 0x00007f5111ee216d n/a (libQt6Gui.so.6 + 0x4e216d)

#3 0x00007f5111eecd40 _ZN21QTextDocumentFragment8fromHtmlERK7QStringPK13QTextDocument (libQt6Gui.so.6 + 0x4ecd40)

#4 0x00007f511334d5a2 n/a (libKF6Notifications.so.6 + 0x255a2)

#5 0x00007f511334e03f n/a (libKF6Notifications.so.6 + 0x2603f)

#6 0x00007f51133498fc n/a (libKF6Notifications.so.6 + 0x218fc)

#7 0x00007f5112bd8f0f n/a (libQt6Core.so.6 + 0x1d8f0f)

#8 0x00007f51123dc021 n/a (libQt6DBus.so.6 + 0x8e021)

#9 0x00007f5112bc6474 _ZN7QObject5eventEP6QEvent (libQt6Core.so.6 + 0x1c6474)

#10 0x00007f5112b6bef0 _ZN16QCoreApplication15notifyInternal2EP7QObjectP6QEvent (libQt6Core.so.6 + 0x16bef0)

#11 0x00007f5112b6c320 _ZN23QCoreApplicationPrivate16sendPostedEventsEP7QObjectiP11QThreadData (libQt6Core.so.6 + 0x16c320)

#12 0x00007f5112e51e78 n/a (libQt6Core.so.6 + 0x451e78)

#13 0x00007f5111106f4d n/a (libglib-2.0.so.0 + 0x5ef4d)

#14 0x00007f5111108617 n/a (libglib-2.0.so.0 + 0x60617)

#15 0x00007f5111108825 g_main_context_iteration (libglib-2.0.so.0 + 0x60825)

#16 0x00007f5112e4fcb2 _ZN20QEventDispatcherGlib13processEventsE6QFlagsIN10QEventLoop17ProcessEventsFlagEE (libQt6Core.so.6 + 0x44fcb2)

#17 0x00007f5112b76cf6 _ZN10QEventLoop4execE6QFlagsINS_17ProcessEventsFlagEE (libQt6Core.so.6 + 0x176cf6)

#18 0x00007f5112b709f1 _ZN16QCoreApplication4execEv (libQt6Core.so.6 + 0x1709f1)

#19 0x000055a4e457472b n/a (/usr/lib/drkonqi-coredump-launcher + 0xa72b)

#20 0x000055a4e457190a n/a (/usr/lib/drkonqi-coredump-launcher + 0x790a)

#21 0x00007f51124366c1 n/a (libc.so.6 + 0x276c1)

#22 0x00007f51124367f9 __libc_start_main (libc.so.6 + 0x277f9)

#23 0x000055a4e4571fa5 n/a (/usr/lib/drkonqi-coredump-launcher + 0x7fa5)

Stack trace of thread 6072:

#0 0x00007f51124adf32 n/a (libc.so.6 + 0x9ef32)

#1 0x00007f51124a239c n/a (libc.so.6 + 0x9339c)

#2 0x00007f51124a23e4 n/a (libc.so.6 + 0x933e4)

#3 0x00007f511251c2f6 ppoll (libc.so.6 + 0x10d2f6)

#4 0x00007f5111108744 n/a (libglib-2.0.so.0 + 0x60744)

#5 0x00007f5111108825 g_main_context_iteration (libglib-2.0.so.0 + 0x60825)

#6 0x00007f5112e4fcb2 _ZN20QEventDispatcherGlib13processEventsE6QFlagsIN10QEventLoop17ProcessEventsFlagEE (libQt6Core.so.6 + 0x44fcb2)

#7 0x00007f5112b76cf6 _ZN10QEventLoop4execE6QFlagsINS_17ProcessEventsFlagEE (libQt6Core.so.6 + 0x176cf6)

#8 0x00007f5112c9277e _ZN7QThread4execEv (libQt6Core.so.6 + 0x29277e)

#9 0x00007f511238507e n/a (libQt6DBus.so.6 + 0x3707e)

#10 0x00007f5112d31c7a n/a (libQt6Core.so.6 + 0x331c7a)

#11 0x00007f51124a597a n/a (libc.so.6 + 0x9697a)

#12 0x00007f51125292bc n/a (libc.so.6 + 0x11a2bc)

ELF object binary architecture: AMD x86-64
