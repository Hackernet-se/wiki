---
title: IPMI
permalink: /IPMI/
---

[Category:Tools](/Category:Tools "wikilink") Intelligent Platform
Management Interface är ett system som tillhandahåller management och
övervakningsfunktioner av en server oberoende av CPU, BIOS eller
operativsystem. IPMI används av systemadministratörer för out-of-band,
t.ex. för att consolea till en server. Det finns olika implementationer
av IPMI, t.ex. HPs kallas iLO och Dells kallas iDRAC.

Installation

`yum install OpenIPMI OpenIPMI-tools`

Ipmitool
--------

Ipmitool är ett verktyg som kan användas för att konfigurera IPMI på de
flesta linuxsystem inklusive [ESXi](/VMware_ESXi "wikilink"). Antingen
kan man kompilera det själv eller ladda ner färdig binär. Logga in på
server med SSH:

`wget `[`http://harsbo.se/filer/ipmitool`](http://harsbo.se/filer/ipmitool)
`chmod +x ipmitool`

För att lista kommandoalternativ kör kommandot utan parametrar.

Skapa användare

`./ipmitool user set name 2 admin`
`./ipmitool user set password 2 `<some passwd>
`./ipmitool user priv 2 4 1`
`./ipmitool channel setaccess 1 2 callin=on ipmi=on link=on privilege=4`
`./ipmitool user list `
`./ipmitool user enable 2`

IPconfig

`./ipmitool lan set 1 ipsrc static`
`./ipmitool lan set 1 ipaddr 10.0.0.45`
`./ipmitool lan set 1 defgw ipaddr 10.0.0.1`
`./ipmitool lan set 1 netmask 255.255.255.0`
`./ipmitool lan set 1 vlan id 5`
`./ipmitool lan print`