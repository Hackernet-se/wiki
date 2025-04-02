---
title: System storage manager
permalink: /System_storage_manager/
---

System storage manager aka ssm, är ett CLI program som ska vara enkelt
att använda. Det har stöd för bla BTRFS, RAID och krypterade volymer.
SSM använder flera verktyg, bl.a. [Mdadm](/Mdadm "wikilink"),
Cryptsetup, device-mapper och LVM2.

Installera
==========

`yum install system-storage-manager.noarch`
`apt-get install system-storage-manager`

Verify

`sudo ssm list`

Utöka en LVM volume
-------------------

Ta reda på vilken volume du vill utöka:

`ssm list volumes`

För att utöka med 10Gb:

`ssm resize -s+10G /dev/centos/root`

[Category:Tools](/Category:Tools "wikilink")