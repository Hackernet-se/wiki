---
title: OS X
permalink: /OS_X/
---

OS X heter operativsystemet som körs på Apple Mac datorer. OS X bygger
på UNIX i botten.

Tips'N'Trix
-----------

### Homebrew

Homebrew är en paket hanterare som liknar apt och som OS X inte har. Mer
info finns på deras [hemsida](http://brew.sh/).

### Byt MAC adress

För att sätta en egen mac adress:

`sudo ifconfig en0 ether aa:bb:cc:dd:ee:ff`

För att sätta en random mac adress:

`openssl rand -hex 6 | sed 's/`..`/\1:/g; s/.$//' | xargs sudo ifconfig en0 ether`

Ändringen är inte permanent utan försvinner vid omstart.

[Category:Distar](/Category:Distar "wikilink")