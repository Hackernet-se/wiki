---
title: Cumulus Linux
permalink: /Cumulus_Linux/
---

Cumulus Linux är ett öppet Network OS som man kan köra på white-box
switches. Det är baserat på [Debian](/Debian "wikilink") och man har
tillgång till allt som Debian är kapabelt till. Cumulus står för en
switch daemon, asic drivers och Network Command Line Utility (NCLU) och
kan bootstrapas med ONIE. Routingmotorn i Cumulus Linux är Free Range
Routing (FRR) och allt som FRR stödjer fungerar. Default är
ARP-timeouten 18 minuter. Cumulus-mjukvaran i sig är gratis att använda
men det krävs en licens för att aktivera front-panel interfaces.

### Cumulus VX

Cumulus Linux finns som free virtual appliance att ladda ner från
Cumulus Networks hemsida. Det finns image för [KVM](/KVM "wikilink") och
[VMware](/VMware_ESXi "wikilink"). Se även [EVE-NG](/EVE-NG "wikilink").

### Architecture

[<File:Cumulus_Linux_Architecture.PNG>](/File:Cumulus_Linux_Architecture.PNG "wikilink")

Konfiguration
-------------

Här nedan följer hur man gör grundläggande konfiguration av Cumulus
Linux. Är man osäker på hur något konfas kan man alltid kolla exempel
med hjälp av **net example *<feature>***.

Hostname

`net add hostname Cum01`

Configuration, kan visas i olika format

`net show configuration`
`net show configuration commands`

Commit

`net pending`
`net commit`

`net show commit last `
`net show commit history`

Switch upgrade

`sudo apt-get update && sudo apt-get upgrade`

Mgmt VRF. Notera att services som syslog, ntp etc default ligger i
default-tabellen och måste bindas om ifall de ska nyttja mgmt-vrf:en.

`net add vrf mgmt`

Skapa vlan. Cumulus reserverar default vlan 3000-3999 för internal usage
men det går att ändra.

`net add vlan 100-200`

Access port

`net add interface swp4 bridge access 100`

SVI

`net add vlan 100 ip address 192.168.10.1/24`

Switchport trunk allowed vlan

`net add interface swp3 bridge vids 200,205`

Det spelar inte någon roll vad man väljer att konfigurera först. När man
commitar något switchrelaterat så skapas det en global switch (bridge).

Useful show commands

`net show version`
`net show interface`
`net show bridge vlan`
`net show bridge macs`

Factory reset, detta rensar ej mgmt vrf.

`net del all`

Adding Question Mark Ability to NCLU. Logga ut, logga in för att
ändringen ska läsas in.

`sed -i "s/# ?: complete/ ?: complete/g" /home/cumulus/.inputrc`

### Prescriptive Topology Manager

PTM används för att validera att man har kopplat kablar rätt. Man skapar
en fil med hur det ska vara kopplat, denna distribuerar man sedan till
alla switchar som jämför denna målbild med vilka LLDP-grannskap som
finns. På så sätt kan man upptäcka om något har kopplats fel.

### Zero Touch Provisioning

ZTP görs genom att mgmt-porten (eth0) vid boot ropar efter DHCP option
239. Man pekar ut ett shell script som ska tankas ner och exekveras.
Detta kan vara bash, [python](/Python "wikilink"), perl, ruby vilket ger
flexibilitet.

Exempel:

``` bash
#!/bin/bash

#CUMULUS-AUTOPROVISIONING

apt-get update -y

net add vrf mgmt
net commit

exit 0
```

Ska man aktivera mgmt-vrf bör det göras sist.

Enable ztp on next switch boot.

`sudo ztp -e`

Status & Debugging

`sudo ztp -s`
`sudo systemctl -l status ztp.service`
`sudo ztp -v -r `[`http://192.168.0.50/ztp-script.sh`](http://192.168.0.50/ztp-script.sh)

[Category:Cumulus](/Category:Cumulus "wikilink")