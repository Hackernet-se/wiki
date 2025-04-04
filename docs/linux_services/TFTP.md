---
title: TFTP
permalink: /TFTP/
---

TFTP är ett väldigt simpelt protokoll som används för att överföra
filer. Det används ofta för att PXE-boota maskiner eller överföra
image-filer till t.ex. switchar. TFTP bygger på
server/klient-arkitekturen.

Server
======

Förbered ett rot-directory.

`sudo mkdir /tftproot`
`sudo chmod -R 1770 /tftproot `
`sudo chown -R root:tftp /tftproot`

Det finns olika TFTP-mjukvaror som fungerar som server.

tftpd
-----

Trivial file transfer protocol server.

atftpd
------

Advanced TFTP server.

tftpd-hpa
---------

HPA's tftp server.

`sudo apt-get -y install tftpd-hpa`
`sudo mv /etc/default/tftpd-hpa /etc/default/tftpd-hpa.old`

`sudo dd of=/etc/default/tftpd-hpa << EOF`
`TFTP_USERNAME="tftp" `
`TFTP_DIRECTORY="/tftproot" `
`TFTP_ADDRESS=":69"`
`TFTP_OPTIONS="--secure --create --listen --verbose"`
`EOF`

`sudo service tftpd-hpa restart`

Felsökning
==========

`ss -tulpn | grep 69`

[Category:Guider](/Category:Guider "wikilink")