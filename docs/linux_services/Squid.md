---
title: Squid
permalink: /Squid/
---

Squid är en high-performance cache proxy som har stöd för HTTP, HTTPS,
FTP mycket annat.

Installation
============

**Ubuntu**

`sudo apt-get install squid`

**CentOS**

`yum -y install squid`

Konfiguration
=============

All konfiguration av squid sker i /etc/squid/squid.conf. Denna guide går
igenom hur man installerar väldigt grundläggande proxy server.

Öppna suid.conf och avkommentera följande rad:

`#http_access allow localnet`

Därefter behöver vi definera vilka nät som ska få använda proxy servern.
Leta efter denna rad:

`#acl localnet src`

avkommentera den och ändra den till:

`acl localnet src `<intern ip range>`/`<subnät mask>

Starta om squid:

`sudo service squid restart`

Nu har vi konfigurerat en väldig basic proxy server som svarar på port
3128 som standard.

[Category:Guider](/Category:Guider "wikilink")