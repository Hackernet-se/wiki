---
title: Cisco SPAN
permalink: /Cisco_SPAN/
---

Switch Port Analyzer är Ciscos namn på att spegla trafik, antingen
mellan portar på samma switch eller till en remote switch. Alla typer av
portar kan speglas. SPAN består av source (portar eller
[VLAN](/Cisco_VLAN "wikilink")) och destination port/ar. Med RSPAN
fungerar source på samma sätt men destination port finns på en annan
switch så det skickas i ett RSPAN VLAN till den andra switchen. ERSPAN
(Encapsulated Remote SPAN) är samma som RSPAN men att det kapslas in med
[GRE](/Cisco_GRE "wikilink") så att det kan routas till en annan switch.
Man kan även ha Wireshark som endpoint för GRE-tunneln. Man kan välja om
rx, tx eller att både och ska speglas, default är all rx och tx med
undantag vissa control plane frames (t.ex. CDP, BPDU, VTP, DTP, PAgP).
SPAN ligger före trafikmodifikation för receive, t.ex.
[VACL](/Cisco_Security#VACL "wikilink"), [QoS](/Cisco_QoS "wikilink")
och ingress policing. För tx ligger det efter så med andra ord SPAN
händer längst ut. På vissa low-end switchar måste man låna en asic från
en oanvänd port för att switchen ska kunna spegla trafik.

**Begränsningar**

-   All konfigurationen på en port inaktiveras när den blir konfad som
    destination port för SPAN. Inklusive
    [EtherChannel](/Cisco_EtherChannel "wikilink").
-   Destination port har inte stöd för
    [802.1x](/Cisco_Security#802.1x "wikilink"), [Private
    VLAN](/Cisco_VLAN#Private_VLAN "wikilink"),
    [CDP](/Cisco_IOS#CDP "wikilink"), [STP](/Cisco_STP "wikilink"),
    [VTP](/Cisco_VTP "wikilink"), [DTP](/Cisco_VLAN#DTP "wikilink"),
    etc.
-   Som source går det ej att mixa portar och VLAN.
-   Destinationporten är best effort, dvs överflöd slängs.
-   Endast en SPAN-session kan skicka trafik till en destination port.

SPAN
====

`monitor session 1 source interface fa0/2 rx`
`monitor session 1 source interface fa0/3 both`
`monitor session 1 destination interface fa0/10 encapsulation replicate`

Encapsulation replicate gör att exakt alla frames speglas.

`monitor session 1 filter vlan 2 - 5`

Speglar man en trunkport kan man filtrera så att endast vissa VLAN
speglas.

**Verify**

`show monitor session 1`
`show platform software monitor session 1`

**NX-OS**
Destination

`interface Ethernet1/1`
` description MONITOR-SESSION-1`
` switchport`
` switchport monitor`
` no shutdown`

Monitor session

`monitor session 1`
` description SPAN-to-SERVER`
` source vlan 10-20 both`
` rate-limit auto`
` destination interface Ethernet1/1`
` no shut`

RSPAN
=====

Skapa RSPAN VLAN på alla switchar. RSPAN vlan stänger av mac learning
och allt som kommer in floodas till alla portar som är konfigurerade som
destination.

`vlan 999`
` name RSPAN`
` remote span`
` exit`

Source

`monitor session 1 source interface fa0/3 both`
`monitor session 1 destination remote vlan 999`

Switch 2

`monitor session 1 source remote vlan 999`
`monitor session 1 destination interface gi0/8`

**Verify**

`show monitor session 1`
`show vlan remote-span`

ERSPAN
======

ERSPAN finns i två versioner. I version 1 (type II) används en ERSPAN
header innan GRE-enkapsuleringen. Den innehåller metadata om sessions id
och speglade VLAN. I version 2 (type III) är headern större vilket ger
mer flexibilitet, t.ex. finns det även plats för info om performance och
latency analysis. PTP timestamp information används för att räkna ut
packet latency över edge, aggregate och core switches. De skiljs åt med
hjälp av GRE Protocol Type value, 0x88BE och 0x22EB.

Source

`monitor session 1 type erspan-source`
`source interface gi0/1 both`
`no shut`
`destination`
` erspan-id 101`
` ip address 10.0.0.20`
` origin ip address 172.20.0.10`

Destination

`monitor session 1 type erspan-destination`
`destination interface gi0/2 `
`no shut`
`source`
` erspan-id 101`
` ip address 10.0.0.20`

Verify

`show monitor session 1`
`show capability feature monitor erspan-source`
`show capability feature monitor erspan-destination`

**NX-OS**

`monitor erspan origin ip-address 10.1.2.1`
`monitor session 1 type erspan-source`
` description ERSPAN direct to Sniffer PC`
` erspan-id 32                              # required, # between 1-1023`
` vrf default                               # required`
` destination ip 10.1.2.3                   # IP address of Sniffer PC`
` source interface port-channel1 both       # Port(s) to be sniffed`
` filter vlan 3900                          # limit VLAN(s) (optional)`
` no shut                                   # enable`

Verify

`show monitor session all`

Embedded Packet Capture
=======================

På vissa enheter går det att göra en lokal packet capture. Man kan fånga
paket i båda riktningen på ett interface samt begränsa så att inte allt
fångas. Man kan såklart ha en permit ip any any acl men något slags
filter måste konfigureras. Detta är IOS-XE syntax.

`ip access-list extended CAPTURE`
` permit udp host 172.17.0.13 host 172.16.0.14 eq 53`
` permit udp host 172.16.0.14 host 172.17.0.13 eq 53`

`monitor capture 1 access-list CAPTURE interface g0/0 both`

Start / Stop / Clean up

`monitor capture 1 start`
`monitor capture 1 stop`
`no monitor capture 1`

Show

`show mon cap 1 buffer brief`
`show mon cap 1 parameter`

Ethanalyzer
===========

Ethanalyzer är ett protocol analyzer-verktyg för
[NX-OS](/Cisco_Nexus "wikilink"). Det är en CLI-variant av Wireshark med
stöd för filter.

-   capture-filter: tcpdump capture filter syntax
-   display-filter: wireshark display filter syntax

Exempel: titta på trafik till och från supervisor på mgmt-interface.

`ethanalyzer local interface mgmt`
`ethanalyzer local interface mgmt capture-filter "host 10.0.0.10" limit-captured-frames 50 write bootflash:CAP_MGMT.pcap`

Man kan inte se trafik som går i hårdvaran (ASIC) men man kan använda en
ACL med log option som workaround.

`ip access-list ACL-CAP`
` permit tcp 10.0.0.3/32 10.0.0.10/32 eq 5000 log`
` permit ip any any`
`interface e1/1`
` ip access-group ACL-CAP in`

`ethanalyzer local interface inband capture-filter “tcp port 5000”`

En annan mer kraftfull workaround man kan göra är att spegla trafik från
ASIC (cloud scale) till CPU och sedan använda ethanalyzer.

`monitor session 1`
` source interface e1/15`
` destination interface sup-eth 0`
` no shut`

`ethanalyzer local interface inband mirror limit-captured-frames 50`

RITE
====

På routrar heter SPANs motsvarighet Router IP Traffic Export och man
anger en mac-adress man vill skicka paketen till, det skulle t.ex. kunna
vara en IDS. Man kan matcha det man vill ska skickas mot en acl och man
kan sampla.

`ip traffic-export profile IDS`
` interface Gi0/0`
` mac-address 0123.0005.abcd`
` incoming sample one-in-every 5`
`interface Gi0/2`
` ip traffic-export apply IDS`

Show

`show ip traffic-export`

[Category:Cisco](/Category:Cisco "wikilink")