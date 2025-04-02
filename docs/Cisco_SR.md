---
title: Cisco SR
permalink: /Cisco_SR/
---

Segment Routing (SR) är ett flexibelt och skalbart sätt att göra source
routing, det är inget routingprotokoll utan ett koncept. Den första
noden väljer path och kodar det i packet header genom en ordnad lista av
"segment". Det går att använda MPLS data plane (labels) eller IPv6 data
plane (header extensions), denna artikel fokuserar på
[MPLS](/Cisco_MPLS "wikilink"). Segment Routing integrerar med dom
multi-service capabilities som finns med MPLS, inklusive L3VPN,
[VPWS](/Cisco_L2VPN#EoMPLS.2FAToM "wikilink"),
[VPLS](/Cisco_L2VPN#VPLS "wikilink") och [EVPN](/Cisco_EVPN "wikilink").

Segment representerar subpaths som en router kan kombinera för att få
fram en komplett route till destination. Varje segment har en identifier
(Segment Identifier) som distribueras genom nätverket med hjälp av
extensions till IGP (IS-IS/OSPF). Segment routing tillåter därmed att
man väljer hela pathen från ingress port till egress port utan att
förlita sig på t.ex. IGP shortest path table. Det är samtidigt simplare
än de flesta andra typer av traffic engineering. SR gör även ECMP till
skillnad från [RSVP-TE](/Cisco_MPLS#Traffic_Engineering "wikilink"). För
att tunea en path så används lokal TE policy alternativt BGP-LU, man
annonserar en unicast route med en associerad MPLS label. SR kräver
inget label distribution protocol så det behövs t.ex. ingen
synkronisering mellan routingprotokoll och LDP.

-   **Prefix SID** - Ett segment ID som innehåller IP-prefix, detta
    måste vara globally unique. Prefix SID konfas manuellt ur
    SRGB-rangen. Kallas även Node SID.
-   **Adjacency SID** - Ett segment ID som innehåller en routers
    adjacency till en granne, dvs det är länken mellan två routrar.
    Eftersom adjacency SID är relativ till en specifik router så är den
    locally unique och endast giltig på den nod som allokerade den.

Man kan använda både Prefix SID och Adjacency SID för att beskriva en
path. Om ett interface går ner kommer Adj-SID att finnas kvar i 30
minuter och kallas då för zombie label.

Det går även att stitcha IGP-domäner genom att konfigurera multipla
IGP-instanser på loopback på domain border nodes. Man anger samma prefix
SID under flera IGP-instanser och därmed blir prefix och prefix SID
nåbara i flera domäner.

Konfiguration
=============

IOS
---

Segment Routing Global Block (SRGB) och Segment Routing Local Block
(SRLB) är de label ranges som är reserverad för segment routing. Default
value för SRGB är 16000 till 23999, det är rekommenderat att använda
default SRGB range (utom vid multi vendor).

`show mpls label range`
`show ip ospf segment-routing global-block`

Associera SID values med lokala prefix, detta prefix måste även
annonseras i IGP.

`interface Loopback0`
` ip address 2.2.2.2 255.255.255.255`

`segment-routing mpls`
` connected-prefix-sid-map`
`  address-family ipv4`
`   2.2.2.2/32 index 2`

Sedan går man in under IGP och slår på segment-routing, detta enablear
MPLS på alla IGP-interface och lägger in MPLS labels för forwarding. För
övrig konfiguration se [IS-IS](/Cisco_IS-IS#Konfiguration "wikilink")
och [OSPF](/Cisco_OSPF#Konfiguration "wikilink").

`router ospf 1`
` segment-routing mpls`

Verify

`show segment-routing mpls state`
`show mpls forwarding-table`
`show ip ospf segment-routing local-prefix`
`show ip ospf segment-routing sid-database`

Kolla Adjacency SID

`show ip ospf neighbor detail | i Neighbor|SR`

**Node SID Redistribution**
router ospf 1

` segment-routing mpls`
` distribute link-state`

### BGP-SR

Man kan även göra segment routing med hjälp av BGP-SR, då används
BGP-LU. Se även [Cisco BGP](/Cisco_BGP "wikilink").

`router bgp 1`
` neighbor 10.1.1.2 remote-as 2`
` !`
` address-family ipv4`
`  redistribute connected`
`  segment-routing mpls`
`  neighbor 10.1.1.2 activate`
`  neighbor 10.1.1.2 send-label`
` exit-address-family`

IOS-XR
------

Segment Routing med MPLS Data Plane. SR funkar även med Multi-topology.

`router isis 1`
` address-family ipv4 unicast`
`  segment-routing mpls`
` !`
` interface Loopback0`
`  address-family ipv4 unicast`
`   prefix-sid absolute 16001`

Verify

`show isis segment-routing label table`
`show isis route sr-only`
`show mpls label table summary`

Detta gäller vid imposition

`segment-routing mpls`
` set-attributes`
`  address-family ipv4`
`   sr-label-preferred`

**PHP**
PHP går att stänga av per prefix SID.

`router isis 1`
` interface Loopback0`
`  address-family ipv4 unicast`
`   prefix-sid index 1 explicit-null`

**Microloop Protection**

`microloop avoidance segment-routing`

**Anycast SID**
Vill man använda en prefix SID för anycast måste man stänga av att den
annonseras som en nod i LSDB.

`router isis 1`
` interface Loopback0`
`  address-family ipv4 unicast`
`   prefix-sid index 1 n-flag-clear`

**OAM**
ping sr-mpls 4.4.4.4/32

`traceroute sr-mpls 3.3.3.3/32 verbose`

**BGP Peer Adjacency SID**
Man kan även skapa Adj-SID för eBGP-grannar, t.ex. på inter-AS-länkar.
Man forwarderar där det finns en BGP-granne, detta kan användas för
Egress Peering Engineering applications.

`router bgp 1`
` neighbor 10.1.1.2`
`  remote-as 2`
`  egress-engineering`
`  address-family ipv4 unicast`

### LDP

SR kan samköras med LDP men ska man koppla ihop ett LDP-nät med SR-nät
måste man sätta upp mapping servers. Alla destinationer måste ha ett
prefix SID. Om en nod inte kan annonsera det själv (t.ex. en LDP-only
nod) så gör mapping servern det på dennes vägnar. Alla Segment Routing
routers behöver också vara mapping clients. Mapping server behöver ej
finnas i data path.

Mapping server

`router isis 1`
` address-family ipv4 unicast`
`  segment-routing prefix-sid-map advertise-local`
`! `
`segment-routing`
` mapping-server `
`  prefix-sid-map`
`   address-family ipv4`
`    1.1.1.1/32 1001 range 8`

Range 8 betyder prefix 1.1.1.1/32 - 1.1.1.8/32 med start label 17001
vilket gör det lätt att se vilka labels som kommer ifrån mapping server.

Mapping client

`router isis 1`
` address-family ipv4 unicast`
`  segment-routing prefix-sid-map receive`

Verify

`show isis segment-routing prefix-sid-map active-policy detail`

SR vs LDP preference

`router isis 1`
` address-family ipv4 unicast`
`  segment-routing mpls sr-prefer`

NX-OS
-----

Se även [NX-OS MPLS](/Cisco_MPLS#NX-OS "wikilink").

`install feature-set mpls`
`feature-set mpls`
`feature mpls segment-routing`

`segment-routing mpls`

`router bgp 65000`
` address-family ipv4 unicast`
`   network 2.2.2.2/32 route-map assign_label`
`   allocate-label all`
` neighbor 10.1.1.2 remote-as 65000`
`     address-family ipv4 labeled-unicast`
`        send-community extended`

SR-TE
=====

SR-TE kallas SR Policy. Med SR-TE behöver inte längre nätet hålla något
state per-flow eller per-applikation utan man följer bara det
forwarding-instruktioner som finns i paketet. Man nyttjar även bandbredd
bättre eftersom man kan dra nytta av ECMP där det finns. Eftersom man
låter en extern källa räkna på required paths genom nätverket lättar man
lasten för övriga routrar.

För att styra en path så används lokal TE policy alternativt BGP-LU, man
annonserar en unicast route med en associerad MPLS labelstack. Se
exempel med [ExaBGP](/ExaBGP#Segment_Routing "wikilink").

`segment-routing`
` traffic-eng`
`  segment-list SIDLIST1`
`   index 10 address ipv4 1.1.1.3`
`   index 20 mpls label 24006`
`   index 30 mpls label 16008`
`  !`
`   policy POLICY1`
`    binding-sid mpls 15000`
`    color 10 end-point ipv4 1.1.1.10`
`    candidate-paths`
`     preference 100`
`      explicit segment-list SIDLIST1`

Verify

`show segment-routing traffic-eng policy`
`show segment-routing traffic-eng forwarding policy `

[Category:Cisco](/Category:Cisco "wikilink")