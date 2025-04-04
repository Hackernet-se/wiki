---
title: Rar2fs
permalink: /Rar2fs/
---

Är ett FUSE fil system som låter dig läsa rar arkiv som om det vore
vanliga filer.

Förberedelser
-------------

`apt-get install libfuse-dev autoconf`

Installera senaste unrarlib. I skrivande stund är 5.3.2 senaste.

`wget `[`ftp://ftp.rarlab.com/rar/unrarsrc-5.3.2.tar.gz`](ftp://ftp.rarlab.com/rar/unrarsrc-5.3.2.tar.gz)` && tar -xvf unrarsrc-5.3.2.tar.gz`
`cd unrar && make lib -f makefile && cp libunrar.so /usr/lib`

Installation
------------

`git clone `[`https://github.com/hasse69/rar2fs`](https://github.com/hasse69/rar2fs)
`cd rar2fs && autoreconf -f -i`
`./configure --with-unrar=../unrar`
`make && make install`

Kommandon
---------

För en lista med kommandon.

`rar2fs -h`

Mounta

`rar2fs -o allow_other /path/to/rararchives /path/to/mount/point`

Unmounta

`fusermount -u /path/to/mount/point`

### Automount

För att kunna automounta krävs det att fuse är installerat:

**Debian/Ubuntu**

`apt-get install fuse`

**RHEL/CentOS**

`yum install fuse`

Lägg till följande i `/etc/fstab`

`rar2fs#/path/till/rar/ /vart/du/vill/mounta/ fuse allow_other,--seek-length=1    0 0`

[Category:Guider](/Category:Guider "wikilink")