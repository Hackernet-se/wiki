---
title: Emby Server
permalink: /Emby_Server/
---

[Category:Guider](/Category:Guider "wikilink")
[Category:Sparco](/Category:Sparco "wikilink") Emby är en opensource
media server. Emby fungerar lite som Netflix fast man måste själv stå
för filmerna.

[`http://emby.media/`](http://emby.media/)

Installation
------------

**Debian Jessie**

`wget -qO - `[`http://download.opensuse.org/repositories/home:emby/Debian_8.0/Release.key`](http://download.opensuse.org/repositories/home:emby/Debian_8.0/Release.key)` | sudo apt-key add -`
`sudo sh -c "echo 'deb `[`http://download.opensuse.org/repositories/home:/emby/Debian_8.0/`](http://download.opensuse.org/repositories/home:/emby/Debian_8.0/)` /' >> /etc/apt/sources.list.d/emby-server.list"`
`sudo apt-get update`
`sudo apt-get install mono-runtime mediainfo libsqlite3-dev imagemagick-6.q8 libmagickwand-6.q8-2 libmagickcore-6.q8-2`
`sudo apt-get install emby-server`

Ett fel som jag fick under installationen som dom håller på att fixa är
att `/usr/lib/emby-server/emby-server.sh` hade permissions fel. Det
löstes med detta kommandot,

`chmod +x /usr/lib/emby-server/emby-server.sh`

Starta emby-server

`service emby-server start`

Surfa in på webinterfacet och följ wizarden.

[`http://`](http://)<IP>`:8096`

Tips'n'Trix
-----------

Emby kan inte spela upp filmer som ligger i rar arkiv. Använd därför
[rar2fs](/rar2fs "wikilink").