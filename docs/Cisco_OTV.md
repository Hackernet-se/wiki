---
title: Cisco OTV
permalink: /Cisco_OTV/
---

Overlay Transport Virtualization är en tunnlingsteknik för att sträcka
L2-domäner över ett L3-nät med hjälp av enkapsulering. Det är routing
baserat på mac-adress och för control plane används IP-enkapsulerad
[IS-IS](/Cisco_IS-IS "wikilink"). OTV lär sig MAC-IP par genom MAC
address learning på internal interface, IGMP snooping och OTV control
plane (IS-IS) updates. Alla MAC-adresser sparas i OTV Routing
Information Base (ORIB) med VLAN ID och associerad remote IP.

Det finns inbyggd felisolering tack vare att broadcast och unknown
unicast droppas vid edge istället för att floodas över tunneln. ARP
optimeras också genom att Edge Devices kan svara på ARP-frågor för
enheter som finns på andra sidan, detta genom att lyssna på ARP-trafik
på den lokala siten och cachea den. OTV går även att kombinera med en
krypterad transport, t.ex. [GET VPN](/Cisco_IPsec#GET_VPN "wikilink").
IPsec kan då terminera i samma box som OTV och det funkar både ihop med
OTV unicast och multicast mode.

### Termer

**Edge Device:** Gränsenhet mellan lanet och utsidan, där
OTV-enkapsulering görs.

**Authoritative Edge Device:** Enhet som är aktiv på siten. Endast en i
taget, vlan lastdelas.

**Join Interface:** L3-interface som ska kunna nå andra OTV-siters join
interface.

**Internal Interface:** L2-interface som når de VLAN som ska sträckas.

**Overlay Network:** Det logiska nätverk där L2-trafiken går över
Transport Network. Inga BPDUer går över detta nät.

**Transport Network:** Det nätverk som kopplar ihop de olika siterna,
kan vara WAN/internet eller en blandning. Ska finnas rum för 42 extra
bytes MTU.

Neighbors
---------

Innan trafik kan forwarderas måste det upprättas grannskap. För detta
krävs Source Specific multicast-stöd av nätverket emellan (om
transportnätverket inte stödjer multicast så kan en unicast-funktion i
OTV som heter Adjacency Server användas). Edge devices skickar IGMP
membership report och sedan OTV-enkapsulerade hello packets. Alla edge
devices ska bilda adjacency. Neighbors delar MAC-adress reachability med
varandra genom att skicka uppdateringar med multicast.

### Fast Convergence

-   VLAN AED synchronization
-   Site ID and proactive advertisments
-   Prepopulation
-   BFD and route tracking
-   Graceful insertion
-   Graceful shutdown
-   Prioritized processing of LSPs

Om man använder multihoming, dvs flera edge devices per site är det
starkt rekommenderat att slå på spanning-tree på OTV-routrarna. Genom
att göra det kan de skicka ut topology change notification (TCN) när de
märker att AED failar och rollen ska flyttas. Detta får switcharna att
reducera sin aging timer till 15 sekunder vilket skyndar på
konvergensen.

OTV-noder sparar remote unicast MAC addresses i sin ORIB även för
non-AED vlan, detta för att snabba upp konvergens vid AED failover.

Konfiguration
=============

Notera att "OTV cannot be configured when MPLS features are enabled on
the router".

site bridge-domain är samma sak som site-vlan.

`otv site bridge-domain 100`
`otv site-identifier 0000.0000.0101`

`otv isis Overlay1`
` log-adjacency-changes`

Overlay-interface

`interface Overlay1`
` no ip address`
` otv join-interface GigabitEthernet3`
` otv use-adjacency-server 10.0.0.10 unicast-only`

` service instance 200 ethernet`
`  description Test-vlan`
`  encapsulation dot1q 200`
`  bridge-domain 200`

Verify

`show otv site`
`show otv adjacency`
`show otv overlay 1`

Internal interface

`interface GigabitEthernet4`
` description Internal-interface`
` no ip address`
` negotiation auto`
` service instance 100 ethernet`
`  encapsulation dot1q 100`
`  bridge-domain 100`

` service instance 200 ethernet`
`  description Test-vlan`
`  encapsulation dot1q 2`
`  rewrite ingress tag translate 1-to-1 dot1q 200 symmetric  #VLAN translation 2 <-> 200`
`  bridge-domain 200`

Det går även att ta in det otaggat.

`interface GigabitEthernet2`
` service instance 201 ethernet`
`  encapsulation untagged`
`  bridge-domain 201`

Verify

`show otv route`
`show otv vlan`
`show otv arp-nd-cache`

AED håller även koll på multicast senders på den lokala siten. Show OTV
multicast routing table for overlays.

`show otv mroute`

Default skickas alla paketen över overlay med DF-biten satt. För att
tillåta fragmentation of IP packets över overlays måste man slå på det.
OBS alla edge devices i overlayen bör supportera reassembly in hardware.

`otv fragmentation join-interface port-channel 1`

### Enkapsulering

I nya versioner av hårdvara/mjukvara kan man välja vilken enkapsulering
man ska använda, default används
[GRE](/Cisco_GRE "wikilink")/[MPLS](/Cisco_MPLS "wikilink") men nu kan
man även använda [UDP/VXLAN](/Cisco_VXLAN "wikilink"). Väljer man den
VXLAN blir det overhead 50 Bytes per paket.

`otv encapsulation-format ip gre | udp`

### FHRP

Om man har en design där båda sidor har FHRP active router måste
FHRP-paket filtreras så de ej korsar OTVn.

`interface Overlay1`
` otv filter-fhrp`

Native-stöd även för NX-OS är planerat, lösning sålänge är att man
använder VLAN-ACL i kombination med OTV MAC route filter och
arp-inspection filter (feature dhcp).

Nexus
=====

OTV är kompatibelt med ett IPv4 transport network.

`feature otv`

VLAN

`vlan 1000`
` name OTV-SITE-VLAN`
`vlan 2000`
` name OTV-TEST1`
`vlan 2001`
` name OTV-TEST2`
`exit`

`no ip dhcp relay`
`no ipv6 dhcp relay`

**Join interface**
Alla core och core facing L3 interface ska ha stöd för jumbo frames
eftersom OTV sätter DF-biten i IP-headern på alla control och data plane
packets. Vill man ha bättre load-balancing i sitt core (depolarization)
kan man konfa flera IP-adresser (secondary) på sina join-interface, då
kommer OTV att hasha och kunna använda alla IP-adresser som source på
OTV-enkapsulerade paket. Transportnätverket måste supportera ASM eller
PIM-Bidir men slå ej på PIM på join interfacet. Exempel, för SSM.

`interface po1`
` no ip redirects`
` ip igmp version 3`
` no shut`

**Site VLAN**

`otv site-vlan 1000`
`otv site-identifier 0x2`

`otv-isis default `
` vpn Overlay1`

`interface vlan1000`
` no ip redi`
` no ipv6 redi`
` ip add 10.1.1.1/30`
` no shut`

**Overlay**
The site VLAN must not be extended into the OTV.

`int Overlay1`
` otv join-interface po1`
` otv control-group 239.4.4.1`
` otv data-group 232.8.8.0/26`
` otv extended-vlan 2000`
` otv extended-vlan add 2001`
` no shut`

**BFD**
Man kan köra [BFD](/Cisco_BFD "wikilink") över site-vlan:et för att
snabbt upptäcka forwarderingsproblem inom siten.

`interface vlan1000`
` no ip redirects`
` ip address 10.1.1.1/30`

`otv site-vlan 1000`
` otv isis bfd`

`otv-isis default`
` track-adjacency-nexthop`

Verify

`show otv isis track-adjacency-nexthop`
`show bfd neighbors`

**Static flood**
Undantag för unknown unicast (t.ex. silent hosts). Broadcast går ej.

`otv flood mac 0011.2233.4455 vlan 160`

`otv flood mac FF:FF:FF:FF:FF:FF vlan 160`
*`The`` ``flood`` ``mac`` ``can`` ``not`` ``be`` ``a`` ``broadcast`` ``mac.`*

**VLAN Mapping**
Man kan skriva om VLAN ID:n på frames som gör över tunneln. Detta är
inte supporterat på Cisco M3- och F3-moduler men man kan då använda
per-port vlan-översättning (switchport vlan mapping).

`interface overlay 5`
` otv vlan mapping 10,14-16 to 20-21,25,28`
` otv extended-vlan 10,14-16`

Show

`show otv vlan-mapping`

### Loopback Join Interface

Med NX-OS 8 kan man använda ett loopback som join interface, detta gör
att man kan ha multipla routade upplänkar till sitt multicast core.
Upplänkar och loopback ska köra PIM för att detta ska funka. Unicast
(Adjacency Server) stöds inte med denna typ av join interface.

`feature pim`

`interface loopback1`
` ip address 10.10.10.2/32`
` ip router ospf 100 area 0.0.0.0`
` ip pim sparse-mode`

`interface Overlay1`
` otv join-interface loopback1`

### PVLAN

I nyare releaser av NX-OS kan man sträcka [Private
VLAN](/Cisco_VLAN#Private_VLAN "wikilink") över OTV och därmed behålla
segmenteringen.

`feature pvlan`

`vlan 100`
`   private-vlan primary`
`   private-vlan association 101-103`
`vlan 101`
`   private-vlan community`
`vlan 102`
`   private-vlan community`
`vlan 103`
`   private-vlan isolated`

`interface overlay 1`
`   otv extend-vlan 100`

Show

`show otv vlan private-vlan`

[Category:Cisco](/Category:Cisco "wikilink")