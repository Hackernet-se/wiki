---
title: Cisco Routing
permalink: /Cisco_Routing/
---

För dynamiska routingprotokoll se: [BGP](/Cisco_BGP "wikilink"),
[OSPF](/Cisco_OSPF "wikilink"), [EIGRP](/Cisco_EIGRP "wikilink"),
[IS-IS](/Cisco_IS-IS "wikilink") och [RIP](/Cisco_RIP "wikilink"). Se
även: [Cisco PfR](/Cisco_PfR "wikilink") och [Cisco
PE-CE](/Cisco_PE-CE "wikilink").

### RIB

Kolla routingprocesser som kan populera RIB.

`show ip protocol summary`

IOS har en inbyggd funktion för att profilera RIBen dvs kolla hur mycket
som ändras i den över tid.

`ip route profile`
`show ip route profile`

Med debug kan man se det mesta som rör routingtabellen. Bör ej användas
i produktionsmiljöer.

`debug ip routing ?`

Static Routes
-------------

Man kan konfigurera statiska routes med både forwarding address och
outgoing interface. Däremot installeras inga recursive static routes
default i RIB, detta ändras med **ip route static
install-routes-recurse-via-nexthop**.

-   **Next-hop IP:** routen är giltig sålänge det finns en route för
    next-hop value.
-   **Outgoing interface:** routen är giltig sålänge som interfacet är
    UP/UP.
-   **Both next-hop value and outgoing interface:** routen är giltig
    sålänge som next-hop value är reachable över det specificerade
    interfacet.

`ip route 0.0.0.0 0.0.0.0 Gi0 10.10.3.4`

**Floating**

`ip route 172.16.10.0 255.255.255.0 10.10.20.2 `**`210`**

Verify

`show ip static route`

**VRF,** default tillåts static routes att peka på interface i andra
VRF:er.

`ip route static inter-vrf`

IPv6
====

EUI-64

`interface Gi0`
` ipv6 address 2001:2:3:4::/64 eui-64`

**ULA**
Unique Local Address (RFC 4193) är motsvarigheten till IPv4 RFC 1918.
Adressblocket är FC00::/7.

**Router Advertisments**

`interface gi2`
` ipv6 nd ra lifetime 1800`
` ipv6 nd ra interval 200`

Man kan annonsera prefix med ND RA men hostar får ej använda det för
auto-config.

`ipv6 nd prefix 2000::/64 14400 no auto-config`

OBS RA har AD 1 vilket kan därmed trumfa routingprotokoll.

Verify

`show ipv6 interface gi2 prefix`

VRF
===

Man kan se VRF:er som virtuella routrar fast med delat management.
VRF:er utan [MPLS](/Cisco_MPLS "wikilink") kallas VRF Lite.

`show vrf`
`show cef vrf`

Konfiguration

`vrf upgrade-cli multi-af-mode common-policies`
`show vrf detail | i CLI`

Kolla vilka interface som tillhör vilken vrf.

`show ip vrf interfaces`

Man kan i EXEC mode hoppa mellan vrf:er och kommandon som *show ip
route* visar då den aktuella RIB:en.

`routing-context vrf Cust-A`

**Import/Export**
Det går att styra vad och vilken community som ska sättas på det som ska
importeras och exporteras med hjälp av route-maps.

`ip prefix-list Cust-A_DENY seq 5 permit 172.20.0.0/24`

`route-map Cust-A_EXPORT deny 10`
` match ip address prefix-list Cust-A_DENY`
`route-map Cust-A_EXPORT permit 20`

`ip vrf Cust-A`
` export map Cust-A_EXPORT`

**VRF Selection**
Man kan styra på IP vilken VRF som paket ska hamna i men detta är varken
skalbart eller smidigt.

`vrf selection source 172.16.1.0 255.255.255.0 vrf VRF1`
`vrf selection source 0.0.0.0 0.0.0.0 vrf VRF2`

`interface gi2`
` ip vrf select source`
` ip vrf receive VRF1`
` ip vrf receive VRF2`

IP SLA
======

IP SLA låter en enhet mäta och hålla koll på response time, latency,
jitter, packet loss eller bara connectivity mot en punkt utifrån
konfigurerbara tröskelvärden. Enheten kan sedan låta andra processer
tracka detta och fatta routingbeslut utifrån det. T.ex. om primär WAN
gateway går ner slå automatiskt över till sekundär gateway. IP SLA kan
också använda MD5-autentisering, detta konfigureras med **ip sla
key-chain**.

`ip sla 1`
` icmp-echo 100.0.0.20 source-interface GigabitEthernet1`
` threshold 2000`
` timeout 2000`
` frequency 5`
`ip sla schedule 1 life forever start-time now`

Verify

`show ip sla 1`
`show ip sla configuration `
`show ip sla statistics`

### Tracking

För att andra processer ska kunna utnyttja IP SLA binder man IP
SLA-objekten via tracking-processen. Tracking kan göras med
[CDP](/Cisco_IOS#CDP "wikilink") och IP SLA och polling interval går att
konfigurera globalt med **track timer**. Tracking kan t.ex. användas av
[HSRP](/Cisco_HSRP#Tracking "wikilink").

Object Tracking

-   Interface IP or line-protocol: Track either the line-protocol
    (up/down) or the presence of an IP address.
-   IP route: Track a route present in the routing table.
-   IP SLA: Track an IP SLA object.

Man kan även använda en lista för att kombinera flera track objects
baserat på vikt/procent eller boolean AND/OR.

`track 10 ip sla 1 state`
`ip route 0.0.0.0 0.0.0.0 10.10.10.2 track 10`

Verify

`show ip route track-table`
`show track timers`
`show track brief`
`show track resolution`
`debug track`

PBR
===

Policy routing låter routern forwardera trafik baserat på konfigurerbara
kriterier utan att använda routingtabellen. Om trafik inte träffas av
någon entry i route-map används routingtabellen som vanligt. Vill man ha
drop-beteende med PBR kan man använda **set interface Null0**.

PBR prioriterar set-kommandona i följande ordning:

1.  Next-hop
2.  Next-hop recursive
3.  Interface
4.  Default next-hop
5.  Default interface

Konfigurationsexempel

`access-list 1 permit 192.168.1.10 `
`access-list 2 permit 192.168.1.20`

`route-map TEST permit 10 `
` match ip address 1 `
` set ip next-hop 10.10.10.2`
`route-map TEST permit 20 `
` match ip address 2 `
` set ip next-hop 10.10.10.60`

`interface Gi0/0 `
` ip policy route-map TEST `

`show ip policy`

**Recursive**
PBR Recursive Next Hop feature låter route-maps konfigureras med
next-hops som inte är directly reachable via något interface. Dessa
installeras då i routingtabellen och gör att man kan dra nytta av CEF
load sharing. Om next-hop IP inte är möjlig att resolva så går paketen
på default routen. Med IPv6 fungerar det men stödjer ej load sharing.

`set ip next-hop recursive 10.10.10.2`

**Default**
Det går ändra endast default next-hop (eller interface) för det som
matchas av en route-map. Då kommer routingtabellen kollas som vanligt
förutom att gateway of last resort inte kommer att användas.

`route-map TEST permit 10 `
` match ip address 1`
` set ip default next-hop 10.0.0.10`

**VRF**
Man kan med hjälp av en route-map ta in viss trafik i en annan vrf än
det som interfacet tillhör. De kommandon som sätter vrf-tillhörighet har
företräde över de andra *set interface, next-hop* etc.

`route-map VRF permit 10`
` match ip address 10`
` set ip vrf `<name>

**Continue**
Vanligtvis är en route-map first match only men vill man ändra det kan
man använda **continue** för att hoppa vidare till nästa entry.

`route-map TEST permit 10 `
` set metric 150`
` continue`
`route-map TEST permit 20 `
` match ip address 1`
` set ip next-hop 10.10.10.2`

OBS funkar inte med redistribution.

### Local Policy Routing

LPR påverkar trafik genererad av routern själv och konfigureras globalt.

`ip local policy route-map ROUTE-MAP`
`show ip local policy`

### Reliable PBR

IP SLA och Enhanced Object Tracking

`route-map POLICY_ROUTING permit 10`
` set ip next-hop verify-availability 100.0.1.5 1 track 1`

CDP, reachability verifieras genom att kolla att det finns någon
[CDP](/Cisco_IOS#CDP "wikilink")-granne som har 100.0.1.5. Detta går
också att använda ihop med *set ip default next-hop*. Alla kommandon som
ändrar routing programmeras i hårdvara utom *set ip next-hop verify
availability* eftersom CDP-info ej finns i linecards.

`route-map POLICY_ROUTING permit 20`
` set ip next-hop 100.0.1.5`
` set ip next-hop verify-availability`

Others
======

**On-demand routing**
ODR är ett slags simpelt routingprotokoll som har administrative
distance 160. Det använder CDP som bärare för uppdateringarna så
fungerande CDP är ett prereq. ODR har stöd för det grundläggande som
filtrering, redistribution, timers och passiva interface. Inga ändra
routingprotokoll bör köras.

`router odr`
` network 0.0.0.0`

Verify

`show ip protocols`
`show ip route odr`

**Backup Interface**
Det primära interfacet bör vara ett point-to-point interface annars kan
inte up/down status avgöras. Backup interfacet får ej vara ett
subinterface eftersom dess state avgörs av main interfacet.

`interface gi2`
` backup interface gi4`
` backup delay 3 60 `

Verify

`show backup`

**IRDP**
En router kan hitta en gateway router med hjälp av ICMP Router Discovery
Protocol. IRDP skickar ut ICMP Router Advertisement (ICMP type 9
packets) på subnätet för att informera om att det finns en potentiell
gateway. Detta funkar endast om IP routing och proxy ARP är avslaget på
enheterna som tar emot ICMP RA.

`ip subnet-zero`
`show ip irdp`

**IP Event Dampening**

`interface gi2`
` dampening 30`
`show dampening`

[Category:Cisco](/Category:Cisco "wikilink")