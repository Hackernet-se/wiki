---
title: Bcache
permalink: /Bcache/
---

Bcache är en Linux kernel block layer cache.

Installation
============

`sudo add-apt-repository ppa:g2p/storage`
`sudo apt-get update && sudo apt-get -y install bcache-tools`

Konfiguration
=============

Först skapar man caching devices, SSDer.

`sudo make-bcache -C /dev/sdc1`

Sedan skapar man backing devices, HDDer.

`sudo make-bcache -B /dev/sdb1`

Registrera samtliga devices. (Endast om inte udev används på systemet)

`sudo echo /dev/sdX1 > /sys/fs/bcache/register`

Skapa filsystem och mounta.

Attach

`ls /sys/fs/bcache`
`echo bcache-UUID > /sys/block/bcache0/bcache/attach`

### Writeback

Default är det read cache (writethrough), för att slå på write cache.

`echo writeback > /sys/block/bcache0/bcache/cache_mode`

[Category:Guider](/Category:Guider "wikilink")