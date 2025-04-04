---
title: Cisco L2VPN
permalink: /Cisco_L2VPN/
---

Provider-provisioned Layer-2 Virtual Private Network. Att sträcka L2 är
aldrig häftigt men man får göra så gott man kan med
[STP](/Cisco_STP "wikilink") alternativt ha routrar direkt på andra
sidan. Se även [Cisco MPLS](/Cisco_MPLS "wikilink").

### Ethernet Virtual Circuit

Att binda en kund eller tjänst till en port eller VLAN var en
begränsande faktor i access-lagret. Därför togs EVC framework fram för
att komma förbi det. Det är en unified software infrastructure för att
konfigurera Ethernet services. Tanken är att låta access circuits mappas
till flera olika typer av Ethernet-tjänster så som L2 point-to-point
local connects, L2 point-to-point xconnects, L2 multipoint-to-multipoint
VPLS och andra tjänster. Man kan genom att välja encapsulation även
vlan-tagga, dubbel-tagga eller skriva om vlan-tag.

`interface GigabitEthernet2`
` no ip address`
` service instance 10 ethernet`
`  encapsulation default`
`  xconnect 19.19.19.19 219 encapsulation mpls`

Verification

`show ethernet service instance summary`
`show ethernet service instance id 10 interface gig2 detail`
`show l2vpn service all `

**BFD**
bfd-template multi-hop MH

` interval min-tx 200 min-rx 200 multiplier 3 `
`bfd map ipv4 1.1.1.0/24 1.1.1.1/32 MH`

`pseudowire-class MPLS-BFD`
` encapsulation mpls`
` monitor peer bfd local interface Loopback0`

VPLS
====

Virtual Private LAN Service (VPLS) är ett sätt att tillhandahålla
Ethernet-baserad multipoint-to-multipoint-kommunikation över IP eller
MPLS. Multipla siter kopplas ihop med hjälp av full mesh pseudowires.
VPLS använder Virtual Forwarding Instance (VFI) för att hosta alla
pseudowires för en tjänst. Den vanligaste bäraren är MPLS och för
control plane (Auto-Discovery/Signaling) kan LDP eller
[BGP](/Cisco_BGP "wikilink") användas. Det finns inbyggd loop prevention
i form av att frames som kommer ifrån en VPLS aldrig får skickas vidare
inom VPLS (split-horizon). En begränsande faktor för VPLS är
minnesmängden på Edge devices eftersom de måste lära sig kundens
MAC-adresser. All MAC Learning är data plane driven. Det fungerar som en
vanlig bridge dvs det är dynamiskt och baserat på source MAC. By default
så age:ar VFI:er ut inaktiva MAC-adresser efter 5 minuter.

Manual VPLS, legacy syntax. Bridge domain används för mac learning samt
att binda ihop Ethernet UNI med LSP. Man kan ej blanda gammal och ny
syntax pga att bridge-domain betyder olika beroende på config context.

`l2 vfi VPLS manual`
` vpn id 100`
` bridge-domain 1`
` neighbor 10.0.0.2 encapsulation mpls`
` neighbor 10.0.0.3 encapsulation mpls`

`interface gi2`
` service instance 10 ethernet`
`  encapsulation default`
`  bridge-domain 1`

Bridge Domain Centric (preferred syntax). Full mesh scaling är ett
administrativt problem oavsett syntax.

`l2vpn vfi context VPLS`
` vpn id 100`
` member 10.0.0.2 encapsulation mpls`
` member 10.0.0.3 encapsulation mpls`
` member 10.0.0.4 encapsulation mpls`

`interface gi2`
` service instance 10 ethernet`
`  encapsulation default`

`bridge-domain 1`
` mac limit maximum addresses 50`
` member gi2 service-instance 10`
` member vfi VPLS `

Verify

`show l2vpn vfi`
`show bridge-domain`
`show l2vpn service all `
`show mpls l2transport vc`
`show mpls forwarding-table | i l2ckt`

Man kan även koppla in L3-interface på sin bridge-domain.

`interface BDI1`
` ip address 172.20.0.10 255.255.255.0`

### BGP Autodiscovery

**LDP** based VPLS med BGP Autodiscovery (RFC 4762). BGP används för att
upptäcka VPLS-endpoints automatiskt för varje VPN och VC-grannar
konfigureras ej maneullt. Varje VPLS får en egen rd och detta går att
använda i kombination med route reflector.

`l2vpn vfi context VPLS`
` vpn id 100`
` autodiscovery bgp signaling ldp`
`  auto-route-target  #på default`

`router bgp 100`
` address-family l2vpn vpls`
`  neighbor 1.1.1.1 activate`
`  neighbor 1.1.1.1 send-comunity extended`

Verify

`show bgp l2vpn vpls all summary`

**BGP** based VPLS med BGP Autodiscovery (RFC 4761). BGP används för att
upptäcka VPLS-endpoints men också för att signalera labels. Man måste
suppress ldp signaling för att slå på bgp signaling.

`l2vpn vfi context VPLS`
` vpn id 100`
` autodiscovery bgp signaling bgp`
`  ve id 11  #unik per VPLS Edge device `

`router bgp 100`
` address-family l2vpn vpls`
`  neighbor 1.1.1.1 suppress-signaling-protocol ldp`

Verify

`show bgp l2vpn vpls all`

### H-VPLS

VPLS skalar inte superbra eftersom det kräver full-mesh, detta går att
bygga ut med Hierarchical VPLS. Det man gör då är att koppla ihop flera
VPLS och stänga av split horizon vid intersektionerna. Notera att
Split-Horizon endast har effekt på Core Facing pseudowires (mesh
pseudowires) och inte Spoke pseudowires. Trafik ifrån Spoke kan
forwarderas till Core PW och vice versa. Spoke kan även skicka till
annan spoke, dock går den trafiken alltid via core. Trafik tar alltså
sällan den optimala vägen och alla PEs måste lära sig alla MAC-adresser.
För att få redundans ifrån u-PE (spoke) till n-PE (core) kan man använda
Pseudowire Redundancy.

### L2 Tunneling

För CDP, LACP, STP frames etc krävs l2 tunneling protocol. Detta finns
det inte stöd för på alla plattformar, *l2protocol action not
supported*.

`interface gi2`
` service instance 100 ethernet`
`  l2protocol tunnel`

`show ethernet service instance detail | i L2protocol`

EoMPLS/AToM
===========

Ethernet-over-MPLS eller Any Transport over MPLS (RFC 4448). Requires
end-to-end MPLS LSP. Notera att MTU på Access Circuits måste matcha för
att pseudowire ska gå upp. Det finns ingen MAC Learning med EoMPLS.

EoMPLS features

-   Ethernet Port Mode
-   VLAN Mode
-   Inter-AS Mode
-   QinQ Mode
-   QinAny Mode

Port mode använder VC type 5 (Ethernet) och VLAN mode använder VC type 5
men med type 4 (Vlan) som fallback (*show mpls l2transport binding*).

PW logging

`xconnect logging pseudowire status `

PE1

`interface gi2`
` xconnect 2.2.2.2 102 encapsulation mpls`

PE2, VCID måste matcha på båda sidor

`interface gi2`
` xconnect 1.1.1.1 102 encapsulation mpls`

Verify

`show xconnect all`
`show xconnect peer 2.2.2.2 vcid 102`
`show l2vpn service all `
`show mpls l2transport vc 102 detail`
`ping mpls pseudowire 10.0.0.10 102`

Segment 1 är de interface som kunden sitter på, segment 2 är core.

**Pseudowire Redundancy**
Pseudowire redundancy innebär att man sätter upp en backup PW.

`l2vpn xconnect context Redundancy`
` member 1.1.1.1 10 encapsulation mpls group 1 priority 1`
` member 2.2.2.2 10 encapsulation mpls group 1 priority 2`

EVPN-VPWS
---------

`l2vpn evpn`
` replication-type ingress`
` router-id Loopback0`
` mpls label mode per-ce`
`!`
`l2vpn evpn instance 10 vlan-based`
` route-distinguisher 1.1.1.1:10`
` route-target both 10:10`
` no auto-route-target`
`! `
`member evpn-instance 10`
` member GigabitEthernet0/0/1 service-instance 10`
`!`
`interface GigabitEthernet0/0/1`
` no ip address`
` service instance 10 ethernet`
`  encapsulation dot1q 100`
`! `
`router bgp 1`
` address-family l2vpn evpn `
`  neighbor IBGP activate`
`  neighbor IBGP send-community both`

Verify

`show l2vpn evpn evi detail `
`show l2vpn evpn mac `
`show l2vpn l2route evpn mac`

L2TPv3
------

Layer 2 Tunneling Protocol (RFC 3931, RFC 4719) kräver
[CEF](/Cisco_CEF "wikilink") och IP-konnektivitet end-to-end. Det är
endast point-to-point. IP protocol: 115.

`pseudowire-class L2TP-PWCLASS`
` encapsulation l2tpv3`
` ip local interface Loopback0`

`interface gi2`
` xconnect 2.2.2.2 102 pw-class L2TP-PWCLASS`

Verify

`show l2tp session all`
`show l2tun tunnel all`

Default kopieras inte DF bit som finns i paketen som kommer in ifrån CE
när L2TPv3 IP header adderas. Man kan ändra det i pw-klassen.

`pseudowire-class L2TP-PWCLASS`
` ip pmtu`

Inter-AS Option B
-----------------

PE

`mpls ldp discovery targeted-hello accept`

`l2vpn`
` pseudowire routing `
`  terminating-pe tie-breaker`

`l2vpn vfi context vfiA`
` vpn id 111`
` autodiscovery bgp signaling ldp`
` vpls-id 111:111`
` rd 111:111`
` route-target 111:111`

ASBR

`mpls ldp discovery targeted-hello accept`

`l2vpn`
` pseudowire routing`

`router bgp 1`
` no bgp default route-target filter`
` address-family l2vpn vpls`
`  neighbor `<ibgp>` activate`
`  neighbor `<ibgp>` send-community extended`
`  neighbor `<ibgp>` next-hop-self`
`  neighbor `<ebgp>` activate`
`  neighbor `<ebgp>` send-community extended`

`interface GigabitEthernet1`
` description ASBR-to-ASBR`
` mpls ip`
` mpls ldp discovery transport-address interface`

IOS-XR
======

IOS-XR implementerar ett strukturerat CLI för EFP och EVC konfiguration.

-   **l2transport**: identifierar subinterface, fysisk port eller bundle
    som en EFP.
-   **encapsulation**: används för att matcha på VLAN tag
-   **rewrite**: används för att specificera rewrite av VLAN tag.

Exempel:

`interface Bundle-Ether1.20 l2transport`
` encapsulation dot1q 20`
` rewrite ingress tag pop 1 symmetric`
` mtu 9022`

**Loggning**

`l2vpn`
` logging`
`  bridge-domain`
`  pseudowire`
`  vfi`

**Static VPLS**

`l2vpn`
` bridge group PROD`
`  bridge-domain 101`
`   mtu 9000`
`   interface Bundle-Ether1.101`
`   !`
`   vfi 101`
`    neighbor 10.0.10.15 pw-id 101`
`    neighbor 10.0.10.16 pw-id 101`

Verify

`show l2vpn bridge-domain brief`

**Static P2P**
EoMPLS tillhandahåller en tunnlingsmekanism för Ethernet-trafik över ett
MPLS-enabled L3 core. Man enkapsulerar Ethernet PDUs i MPLS-paket.
Notera att MTU på Access Circuits måste matcha för att pseudowire ska gå
upp.

"VC Type 5" = Port Based

`interface GigabitEthernet0/0/0/1`
` l2transport`
` no cdp`
`!`
`l2vpn`
` !`
` xconnect group GROUP1`
`  p2p TO_XR2`
`   interface GigabitEthernet0/0/0/1`
`   neighbor ipv4 2.2.2.2 pw-id 100`

"VC-Type 4" = VLAN based pseudowire

`l2vpn`
` pw-class VLAN`
`  encapsulation mpls`
`   no transport-mode`
`   transport-mode vlan`

Verify

`show l2vpn forwarding neighbor 2.2.2.2 pw-id 100 detail location 0/0/CPU0`

### Control Word

Normalt sett kollar PE i packet header för att avgöra om det är ett
IPv4- eller IPv6-paket och kollar sedan source/destination tuples för
att avgöra eventuell load sharing. Med L2VPN så kommer headern att vara
en Ethernet-header istället för IP-header. Om MAC-adressen händelsevis
börjar på 0x4 eller 0x6 så kommer routern tro att det är ett IP-paket
och fatta beslut på fel grunder. Genom att lägga till ett kontrollord så
kan routern titta på det för att avgöra om det är ett IP-paket eller ej
och därmed finns det ingen risk att load sharing blir fel. Control-Word
spelar en viktig roll för ECMP och det är rekommenderat att man slår på
det.

`l2vpn`
` pw-class CONTROL`
`  encapsulation mpls`
`   control-word`

[Category:Cisco](/Category:Cisco "wikilink")