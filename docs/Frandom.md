---
title: Frandom
permalink: /Frandom/
---

Trött på att urandom är flaskar.

`wget `[`http://billauer.co.il/download/frandom-1.1.tar.gz`](http://billauer.co.il/download/frandom-1.1.tar.gz)
`tar xzf frandom-1.1.tar.gz`
`cd frandom-1.1`
`make`
`` install -m 644 frandom.ko /lib/modules/`uname -r`/kernel/drivers/char/ ``
`depmod -a`
`modprobe frandom`

[Category:Tools](/Category:Tools "wikilink")