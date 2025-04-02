---
title: Extreme XOS
permalink: /Extreme_XOS/
---

Extreme XOS bygger på linux kärnan och busybox.

Konfiguration
-------------

**Hostnamn**

`configure snmp sysName [hostname]`

**Sommartid/vintertid**

`configure timezone name MET 60 autodst  begins every last sunday march at 2 0 ends every last sunday october at 3 0`

**Mgmt port**

`configure vlan Mgmt ipaddress 192.168.0.1 255.255.255.0`
`configure iproute add default [gw] vr VR-Mgmt`

**Skapa användare**

`create account admin [username] [password]`

**Sätta password på användare**

`configure account [konto] password`

**Enable SSH**

SSH modulen kan man behöva lägga på i efterhand. Man lägger på modulen
på samma sätt som man lägger på ny firmware.

`enable ssh`

**LLDP**

`enable lldp ports all`
`configure lldp ports all advertise port-description`
`configure lldp ports all advertise system-name`
`configure lldp ports all advertise management-address`

Firmware
--------

**Byt mellan primary och secondary image.**

`use image primary/secondary`

### TFTP

**Från VR-Mgmt(mgmt port)**

`download image [ip] firmware/images/exos/[image]`

**Från VR-Default(vanlig port/vlan)**

`download image [ip] firmware/images/exos/[image] vr vr-d`

[Category:Extreme](/Category:Extreme "wikilink")