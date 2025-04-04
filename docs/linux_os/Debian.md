---
title: Debian
permalink: /Debian/
---

[Category:Distar](/Category:Distar "wikilink") Debian är en dist som är
inriktad på stabilitet.

First 5 minutes
===============

Debian server installeras med rootkontot som enda kontot. Gör följande
för att öka säkerheten. Logga in som root:

### User

`adduser trevor`
`apt-get update && apt-get install sudo`
`usermod -a -G sudo trevor`
`sed -i -r 's/PermitRootLogin yes/PermitRootLogin no/g' /etc/ssh/sshd_config`
`systemctl restart ssh`

### Hostname

`echo "hostname" > /etc/hostname`
`hostname -F /etc/hostname`

### Tidszon

`dpkg-reconfigure tzdata`

Pakethanterare
==============

[Apt](/Apt "wikilink")

Goodies
=======

Debian Goodies är en uppsättning verktyg som är bra att känna till.

`apt-get install debian-goodies`

När man installerar ett nytt paket kan det hända att program som redan
körs använder filer som blivit uppgraderade. För att ta reda på detta:

`checkrestart`
`checkrestart -v`

Vilket installerat paket tar mest plats:

`dpigs`

Felsök varför något slutat fungera vid uppdatering

`which-pkg-broke `*`packagename`*