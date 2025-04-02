---
title: Cisco SNMP
permalink: /Cisco_SNMP/
---

Simple Network Management Protocol är ett protokoll definierat av IETF
som används för att övervaka och hantera nätverk baserade på TCP/IP. En
SNMP-agent är en router eller en switch med information som kan frågas
om med SNMP. Vilken typ av information som hålls av enheten kallas en
MIB (Management Information Base), [SNMP Object
Navigator](http://snmp.cloudapps.cisco.com/Support/SNMP/do/BrowseOID.do).
SNMPv1 does not support 64 bit counters, only 32 bit counters.

Konfiguration
=============

`snmp-server contact Admin`
`snmp-server location Molnet`
`snmp-server community Hackernet`

`show snmp`
`show snmp community`

Maintain ifindex values across reboots. Detta kommando hette tidigare
*snmp-server ifindex persist*. Det går även att göra per interface.

`snmp ifmib ifindex persist`
`show snmp mib ifmib ifindex`

### Access control

Vitlista de som ska få prata SNMP.

`access-list 10 permit 172.16.0.0 0.0.0.255`
`access-list 10 deny any log`

`snmp-server community PUBLIC ro 10`

### Views

Med views kan man begränsa vad som får frågas om, t.ex. endast vissa MIB
subtree. Man kan specificera object name eller OID.
Exempel: alla Cisco-MIBar utom de EIGRP-relaterade.

`snmp-server view CISCO cisco included`
`snmp-server view CISCO ciscoEigrpMIB excluded`

Users och communities går att binda till views.

`snmp-server community PUBLIC view CISCO`

Verify

`show snmp view`

### Traps

SNMP Traps skickas default till UDP 162.

`snmp-server enable traps`
`snmp-server host 10.0.0.10 traps v2c-community/v3-username`
`show snmp host`

Det går att skicka traps vid t.ex. linkup och down på interface.

`snmp-server enable traps snmp linkup linkdown`

Per interface

`int gi2`
` snmp trap link-status permit duplicates`
` snmp trap ip verify drop-rate`

Det går att skicka traps med [Syslog](/Cisco_Logging "wikilink"). Först
skickas det lokalt till en speciell history buffer och sedan replikerar
SNMP agenten det till traps.

`snmp-server enable traps syslog`

SNMPv3
======

Den stora skillnaden med SNMPv3 kontra tidigare varianter är säkerheten.
Med version 3 kan både autentisering och kryptering användas.

-   **noauth:** no auth, no enrypt
-   **auth:** auth, no enrypt
-   **priv:** auth, enrypt

Skapa grupp för version 3. Grupper definierar access rights för users
till MIBar genom att kopplas till MIB views.

`snmp-server group v3GROUP v3 priv`
`show snmp group`

Skapa user, detta sparas ej i runnning conf. SNMPv3 user passwords
hashas utifrån local Engine-ID.

`snmp-server user SNMPUSER v3GROUP v3 auth sha SECRETKEY priv aes 128 SECRETKEY`
`show snmp user`

### NX-OS

NX-OS har inte stöd för SNMPv3 noAuthNoPriv security level.

Privacy, enforces message encryption för alla users.

`snmp-server globalEnforcePriv`

Skapa user

`snmp-server user SNMPUSER network-operator auth sha SECRETKEY priv aes-128 SEVRETKEY`
`show snmp user`

VRF

`snmp-server host 10.1.2.4 use-vrf management`

Traps

`snmp-server host 10.1.2.4 traps version 3 priv SNMPUSER`

Man kan kolla vilka interface som används som source för SNMP-paket.

`show snmp source-interface`

[Category:Cisco](/Category:Cisco "wikilink")