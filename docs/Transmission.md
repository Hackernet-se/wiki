---
title: Transmission
permalink: /Transmission/
---

[Category:Guider](/Category:Guider "wikilink")
[Category:Sparco](/Category:Sparco "wikilink") Transmission är en liten
men väldigt kraftfull torrent client för linux.

Installation
------------

`apt-get update && apt-get install transmission transmission-daemon`

Konfiguration
-------------

Körs enklast via webinterface eller remote GUI

### Webinterface

För att aktivera webinterfacet och även RPC.

Öppna `/etc/transmission-daemon/settings.json`och ändra till
`"rpc-enabled":true`

Webinterfacet nås sedan på
[`http://IP:9091/transmission/web/`](http://IP:9091/transmission/web/)

### Transmission Remote GUI

Cross platform front end GUI till transmission, gör det enkelt att lägga
till torrents från din vanliga dator. Finns att tanka hem på
<http://sourceforge.net/projects/transgui/>

För att det ska fungera så måste du ha `"rpc-enabled":true` i config
filen.

RPC path är samma som ditt webinterface fast du ersätter
`/transmission/web` med `/transmission/rpc` istället.

Tips n Trix
-----------

**3th Party tools**

[Flexget](/Flexget "wikilink"), RSS feed downloader. Väldigt användbart
för serier.

[Couchpotato](/Couchpotato "wikilink"), Program som laddar hem filmer åt
dig med hjälp av transmission.

**Script done.**

Kör ett script varje gång en torrent blir klar.

Lägg till

`"script-torrent-done-enabled": true,`
`"script-torrent-done-filename": "/vart/finns/scriptet.sh",`

i din conf fil `/etc/transmission-daemon/settings.json`