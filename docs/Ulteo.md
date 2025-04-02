---
title: Ulteo
permalink: /Ulteo/
---

[Category:Guider](/Category:Guider "wikilink") Ulteo Open Virtual
Desktop är en FOSS-plattform för virtuella skrivbord. Ulteo kan använda
både java och html5, webbläsare och native client.

Rekommenderat operativsystem: Debian 7

Installation
------------

Följande instruktioner gäller för en uppsättning där Session manager och
Application server körs på samma maskin. (Mer läsning om
Ulteo-arkitekturen:
<http://archive.ulteo.com/ovd/4.0/docs/Architecture.html>)

Referensguide:
<http://archive.ulteo.com/ovd/4.0/docs/Support_Debian_Wheezy.html>

`su -`
`echo "deb `[`http://archive.ulteo.com/ovd/4.0/debian`](http://archive.ulteo.com/ovd/4.0/debian)` wheezy main" > /etc/apt/sources.list.d/ulteo_ovd.list && apt-get update && apt-get -y --force-yes install ulteo-keyring && apt-get update`
`apt-get -y install mysql-server`

Välj rootlösenord

`mysql -u root -p -e 'create database ovd'`
`apt-get -y install ulteo-ovd-session-manager ulteo-ovd-administration-console`

Konfiguration
-------------

Gå sedan in på:följande och konfigurera databasen med root och pw som
sattes tidigare.

[`http://`](http://)<IP>`/ovd/admin`

Fortsätt sedan i cli:t

`apt-get -y install ulteo-ovd-subsystem && apt-get -y install ulteo-ovd-web-client`

Man skiljer på dessa för att den med säkerhet ska ta en komponent i
taget.

Resten av uppsättningen görs i det grafiska gärnssnittet. Gå in på:
"unregistered servers" och välj att registrera localhost. Sätt sedan
servern i "production"

Skapa sedan din första user för att sedan välja den användaren i
"publication wizard". Skapa en user-grupp och en application-grupp.

Ulteo är nu klart att användas.

[`http://`](http://)<IP>`/ovd`

Terminator
----------

Vad vore en linuxmaskin utan terminalemulator. Det följer inte med någon
default utan man får manuellt lägga till det. Här följer instruktioner
för hur man lägger till terminator.

`chroot /opt/ulteo`
`apt-get update`
`apt-get install terminator`

Sedan kan man välja att publicera terminator som en applikation i
webguit.