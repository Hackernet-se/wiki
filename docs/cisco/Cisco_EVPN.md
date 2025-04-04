---
title: Cisco EVPN
permalink: /Cisco_EVPN/
---

Ethernet VPN (RFC 8365) är en modernare variant än
[VPLS](/Cisco_VPLS "wikilink") för att tillhandahålla Ethernet
multipoint services över IP ([VXLAN](/Cisco_VXLAN "wikilink")) eller
[MPLS](/Cisco_MPLS "wikilink") (RFC 7432) utan att behöva en central
controller. EVPN är en adressfamilj i [BGP](/Cisco_BGP "wikilink") som
används för peer discovery och för att distribuera lokala MAC-adresser
och MAC/IP bindings till andra tunnel endpoints. Man använder både L2
och L3 forwarding information och det fungerar ihop med externa
IP-prefix. Next-hop i EVPN-uppdateringarna är antingen egress Label
Switch Router eller VXLAN Tunnel Endpoint. EVPN skalar bra och har bl.a.
features för att hålla koll på hostar som flyttar mellan datacenter
(sekvensnummer-community i annonseringarna) och kan då konvergera
snabbt. Ett EVPN-nätverk kan göra både bridging och routing och har
inbyggd support för multi-tenancy (VPN). [DHCP
Snooping](/Cisco_DHCP#Snooping "wikilink") supporteras inte på VXLAN
VLAN.

EVPN är ett öppet protokoll så det finns interoperability med andra
network vendors, se t.ex. [Arista](/Arista_EVPN "wikilink"),
[Cumulus](/Cumulus_EVPN "wikilink") och
[Quagga](/Quagga#EVPN "wikilink") EVPN.

**Route types**
\# Ethernet Auto-Discovery Route

1.  MAC/IP Advertisement Route
2.  Inclusive Multicast Ethernet Tag Route
3.  Ethernet Segment Route
4.  IP Prefix Route

**Type 5 Routes format**
{\| class="wikitable" \| **Encapsulation:** \| **MPLS** \| **VXLAN** \|-
\| RT-5 Route: \| IP Prefix \| IP Prefix \|- \| RD: \| L3 RD \| L3 RD
\|- \| IP Length: \| prefix length \| prefix length \|- \| IP Address:
\| IP \| IP \|- \| Label: \| BGP MPLS Label \| L3VNI \|- \| Ext
Communities: \| RT for IP-VRF \| RT for IP-VRF, Tunnel Type VxLAN,
Router MAC \|- \|}

Underlay
========

Underlay routing kan göras med IGP, iBGP eller eBGP. Alla VTEP:s måste
kunna nå varandra med jumbo frames. Alla hårdvaruplattformar har inte
stöd för Head-end Replication (aka Ingress Replication) för att lösa
tenant BUM så t.ex. med Nexus 5k måste man även köra PIM Bidir i
underlay. Notera att IGP-annonsering av NVE loopback address efter boot
default kommer att suppressas under 300 sekunder för att overlay ska
hinna konvergera. Detta går att ställa in under interface nve 1.

Simpelt NX-OS exempel

`feature ospf`

`interface loopback0`
` description VTEP`
` ip address 1.1.1.1/32`
` ip router ospf 1 area 0`

`interface Ethernet1/1`
` description Uplink`
` no switchport`
` medium p2p`
` mtu 9216`
` ip address 10.0.2.2/30`
` no shutdown`
` ip router ospf 1 area 0`

Det går även köra upplänkarna IP unnumbered.

Overlay
=======

EVPN-peering för DC VXLAN-overlay kan göras både med iBGP och eBGP, det
är designen som avgör.

Konfig för leafs oavsett iBGP eller eBGP overlay.

`feature bgp`
`feature vn-segment-vlan-based`
`feature nv overlay`
`nv overlay evpn`

`interface nve1`
` no shutdown`
` host-reachability protocol bgp`
` source-interface loopback0`

### IBGP

Den simplaste EVPN fabricen är IBGP overlay med IGP underlay.

`router bgp 65000`
` address-family l2vpn evpn`
` neighbor 2.2.2.2`
`  remote-as 65000`
`  update-source loopback0`
`  address-family l2vpn evpn`
`    send-community`
`    send-community extended`

**Route Reflector**
Precis som med övriga adressfamiljer kan man med hjälp av route
reflector öka skalbarhet och förenkla konfigurationen. Spine-switchar
kan t.ex. stå för denna roll i en IBGP EVPN setup.

`router bgp 65000`
` address-family l2vpn evpn`
` neighbor 1.1.1.0/24`
`   remote-as 65000`
`   update-source loopback0`
`   address-family l2vpn evpn`
`     send-community extended`
`     route-reflector-client`

### EBGP

Om man bygger sin fabric med EBGP EVPN så måste next-hop-unchanged
konfas på spines peeringar mot leaf. Om man kör med autoderiverade RTs
måste man skriva om dem innan de når leaf samt att spine switches inte
har någon VRF-konfig så man måste slå på retain route-target.

`route-map NH-Unchanged permit 10`
` set ip next-hop unchanged`

`router bgp 65000 `
`  address-family l2vpn evpn`
`    retain route-target all`
`  neighbor 1.1.1.0/24`
`    remote-as 65001  `
`    address-family l2vpn evpn`
`      route-map NH-Unchanged out`
`      rewrite-evpn-rt-asn`

**All leaf same ASN**
Spine

`router bgp 65000`
` neighbor 1.1.1.1 remote-as 65001`
`  address-family l2vpn evpn`
`   disable-peer-as-check`

Leaf

`router bgp 65001`
` neighbor 2.2.2.2 remote-as 65000`
`  address-family l2vpn evpn`
`   allowas-in`

### Verify Overlay

`show nve int nve1`
`show nve peers detail`
`show bgp l2vpn evpn summary`
`show nve internal platform interface nve 1 detail `

Bridging
--------

På varje leaf switch mappas local VLAN till ett VNI (VLAN-based mode).

`vlan 100`
` vn-segment 10100`
`vlan 101`
` vn-segment 10101`

<div class="mw-collapsible mw-collapsed" style="width:310px">

VLAN modes:

<div class="mw-collapsible-content">

[<File:Cisco-EVPN-VLAN-mode.PNG>](/File:Cisco-EVPN-VLAN-mode.PNG "wikilink")

</div>
</div>

HER mha EVPN route typ 3

`interface nve1`
` member vni 10100`
`   ingress-replication protocol bgp`
` member vni 10101`
`   ingress-replication protocol bgp`

RD och RT för bridging. RT-import/export görs automatiskt utifrån ASN
och VNI.

`evpn `
` vni 10100 l2 `
`  rd auto `
`  route-target import auto `
`  route-target export auto`
`  exit`
` vni 10101 l2 `
`  rd auto `
`  route-target import auto `
`  route-target export auto`
`  exit`

Verify

`show nve vni`
`show nve peers data-plane detail`
`show l2route evpn mac-ip all`
`show forwarding nve l3 peers`
`show mac address-table`
`show system internal l2fwder mac     #Nexus 9000v`

### vPC

Om man kör [vPC](/Nexus_vPC "wikilink") får man sätta upp sina
VTEP-interface (loopback) med dubbla IP-adresser där secondary IP
address används för all VXLAN-trafik. Secondary ska vara samma på både
vPC-peers och det är så dom presenterar sig själva som en enda VTEP till
remote NVE peers. CFS dubbelkollar att man har gjort rätt. Sista
oktetten i loopbacks primära IP-adress används för att generera RMAC när
man kör vPC. Varje vPC-peer har separata BGP-sessioner till spine. I
övrigt måste de ha identisk konfiguration när det gäller VLAN, VNI och
NVE (*show vpc consistency-parameters vni*).

`interface loopback0`
` ip address 100.0.0.11/32`
` ip address 100.0.0.100/32 secondary`

vPC Domain best practice när man kör EVPN.

`vpc domain 1`
` peer-switch`
` peer-keepalive destination 10.0.0.2 source 10.0.0.1`
` peer-gateway`
` ipv6 nd synchronize`
` ip arp synchronize`

**vPC Fabric Peering**
I nyare NX-OS på N9k behövs ingen fysisk peer-link längre utan man kan
köra CFSoIP över fabricen, detta sparar portar och kallas vPC Fabric
Peering. Data plane traffic görs över en VXLAN-tunnel. Man berättar för
switchen vilka som är fabric-länkar och dessa trackas då.

`hardware access-list tcam region in-flow-redirect 512`
`vpc domain 1`
` peer-keepalive destination 10.0.0.2 source 10.0.0.1`
` virtual peer-link destination 10.0.10.2 source 10.0.10.1/32 `
` peer-switch`
` peer-gateway`
` ip arp synchronize`
` ipv6 nd synchronize`

Verify

`show vpc`
`show vpc fabric-ports`
`show vpc virtual-peerlink vlan consistency`

**advertise-pip**
Default annonseras alla Layer-3 routes med secondary IP address (VIP) på
VTEP. Prefix routes och leaf switch generated routes synkas ej mellan
vPC leaf switches. Om t.ex. vPC-switch och dennes peer har asymmetric
external Layer-3 connections och vissa routes endast är nåbara via den
ena eller om man ska agera [DHCP Relay](/Cisco_DHCP#Relay "wikilink") åt
tenants så kan traffic blackholing uppstå med default beteendet. Man kan
därför konfa att route type 5 routes ska annonseras med primary IP
address så det blir next-hop för fabricen.

`router bgp 65000`
` address-family l2vpn evpn`
`  advertise-pip`

**Backup routing**
Om den ena vPC-peeren tappar sina upplänkar till spine och man inte har
någon backup routing så uppstår traffic blackholing. Detta kan man
motverka genom att bygga en backup-väg över peer-linken till den andra
peeren.

`vlan 99`

`interface vlan99`
` ip address 10.99.99.1/30`
` ip router ospf 1 area 0.0.0.0`
` ip pim sparse-mode`

Nexus 5600

`vpc nve peer-link-vlan 99`

### BD-oriented mode

I VLAN-based mode är VNI-to-VLAN mapping switch wide men om man lägger
in bridge domains emellan så kan man uppnå att VNI-to-VLAN mapping
endast är port wide. Dvs man kan använda samma 802.1Q tag på flera
portar men de är mappade till olika VNI:er. Konfen ser lite annorlunda
ut men både bridging och routing funkar.

Nexus 7k

`feature vni`
`feature-set fabric`
`feature fabric forwarding`

`vni 10000`

`system bridge-domain 100`
`bridge-domain 100`
` member vni 10000`

`encapsulation profile vni Tenant1-101`
` dot1q 101 vni 10000`

`interface e2/1`
` no switchport`
` service instance 1 vni`
`  no shutdown`
`  encapsulation profile Tenant1-101 default`

`interface Bdi 100`
` vrf member Tenant1`
` ip address 10.0.0.1/24`

Routing
-------

NX-OS gör endast symmetric vxlan routing, dvs EVPN-routes har både L2VNI
och L3VNI. Man anger NVE overlay VLAN:s. Dessa ska ej användas som
vanliga VLAN.

`system vlan nve-overlay id 3001-3200`

RT-import och export görs automatiskt utifrån ASN och VNI.

`vrf context Tenant1`
` vni 30001`
` rd auto`
` address-family ipv4 unicast`
`  route-target both auto`
`  route-target both auto evpn`

Varje tenant VRF behöver ett VRF overlay VLAN och ett SVI för VXLAN
routing.

`interface nve1`
` member vni 30001 associate-vrf`

`vlan 3001`
` vn-segment 30001`

`interface Vlan3001`
`  no shutdown`
`  mtu 9216`
`  vrf member Tenant1`
`  ip forward`
`  ipv6 forward`

Verify

`show nve vrf`
`show nve internal bgp rnh database vni 30001`

Exempel, tenant routing table

`routing-context vrf Tenant1`
`show ip route`

`10.1.0.10/32, ubest/mbest: 1/0`
`   *via 100.64.0.11%default, [200/0], 00:02:44, bgp-65000, internal, tag 65000 (evpn) segid: 30001 `
`    tunnelid: 0xa000003 encap: VXLAN`

Troubleshooting

`show troubleshoot l3 ipv4 10.0.0.10 src-ip 10.0.0.20 vrf Tenant1`

#### Anycast GW

Om man slår på anycast gateway feature för ett VNI så måste det enableas
på alla VTEP:s där VNI finns.

`fabric forwarding anycast-gateway-mac 0000.1111.2222`

`interface Vlan100`
` vrf member Tenant1`
` ip address 10.0.0.1/24`
` fabric forwarding mode anycast-gateway`
` no shut`

#### ARP Suppression

Man kan låta en lokal ARP-proxy hantera requests för att suppressa ARP
flooding över VXLAN så mycket som möjligt. Notera att ARP Suppression
inte jobbar med något IPv6-relaterat.

`interface nve1`
` member vni 10100`
`  suppress-arp`
` member vni 10101`
`  suppress-arp`

`show ip arp suppression-cache detail`

OBS på vissa plattformar måste man karva TCAM för att kunna konfigurera
arp-suppression. Här är ett exempel för [Nexus
9000v](/Cisco_Nexus#Nexus_9000v "wikilink").

`show run all | inc "hardware access-list tcam region"`

`hardware access-list tcam region span 0`
`hardware access-list tcam region racl 512`
`copy run start`
`reload`

`hardware access-list tcam region arp-ether 256 double-wide`
`copy run start`
`reload`

#### External Connectivity

Prefix-based routing (Type-5 Routes) används primärt för destinations
utanför DC. IP-VRF till IP-VRF görs enligt interface-less model dvs
routsen har en RMAC attached.

`router bgp 65000`
`  address-family l2vpn evpn`
`   maximum-paths ibgp 4`

`  vrf Tenant1`
`   address-family ipv4 unicast`
`     advertise l2vpn evpn`
`     redistribute direct route-map ALLOW-ALL`

Verify

`show bgp ip unicast vrf Tenant1`

Exempel på släppa ut en tenant (10.0.0.0/24) ifrån evpn-vxlan-fabricen.
Vanlig OSPF pratas mellan border leaf och external device. På border
leaf:

`router ospf 100`
`  vrf Tenant1`
`    redistribute bgp 65000 route-map ALLOW-ANY`

`router bgp 65000`
`  vrf Tenant1`
`    address-family ipv4 unicast`
`      advertise l2vpn evpn`
`      redistribute ospf 100 route-map ALLOW-ANY`
`      aggregate-address 10.0.0.0/24`

DHCP Relay
----------

VXLAN EVPN har stöd för DHCP relay-funktionalitet. I en
multi-tenant-lösning används tre suboptions av [Option
82](/Cisco_DHCP#Option_82 "wikilink").

-   Sub-option 151 - Virtual Subnet Selection
-   Sub-option 11 - Server ID Override
-   Sub-option 5 - Link Selection

`feature dhcp`

`service dhcp`
`ip dhcp relay`
`ip dhcp relay information option`
`ip dhcp relay information option vpn`
`ipv6 dhcp relay`

Om DHCP-server är nåbar i default-VRFen.

`interface Vlan1001`
` description Tenant facing SVI`
` ip dhcp relay address 100.0.1.10 use-vrf default`

Om DHCP-server finns i tenant-VRF måste man skapa ett unikt
tenant-loopback per VTEP eftersom det måste vara en unik IP-adress som
source för de relayade DHCP-paketen för att servern ska kunna svara till
rätt relay agent.

`interface loopback11`
` vrf member Tenant1`
` ip address 11.11.11.11/32`

`interface Vlan1001`
` description Tenant facing SVI`
` ip dhcp relay address 100.0.1.10 `
` ip dhcp relay source-interface loopback11`

Multicast
---------

EVPN kan lösa IPv4 routed multicast för tenants (TRM). Man kör MVPN
ovanpå vxlan-fabricen för att förhindra onödig multicast-forwardering,
samma som i MPLS-nät fast utan [PIM](/Cisco_PIM "wikilink"). Man
använder ngMVPN, det behövs ingen RP och designated router är
distribuerad (Anchor DR). Inga PIM- eller IGMP-paket skickas alltså över
fabricen utan BGP gör jobbet. PIM ASM och PIM SSM funkar i overlay men
inte PIM BiDir. Man har en multicastgrupp i underlay per vrf (coret
måste vara multicast-baserat). L2 only mode finns också när man t.ex.
inte har någon VRF. Med TRM så är inte advertise-pip och advertise
virtual-rmac supporterat.

`feature ngmvpn`
`ip igmp snooping vxlan`
`advertise evpn multicast`
`ip multicast overlay-spt-only`

Tenant

`interface loopback 300`
` vrf member Tenant-TRM`
` ip address 1.1.1.1/32`
` ip pim sparse-mode`

`vrf context Tenant-TRM`
` vni 30000`
` ip pim rp-address 1.1.1.1 group-list 224.0.0.0/4`
` ip pim ssm range 232.0.0.0/8`
` address-family ipv4 unicast`
`  route-target both auto`
`  route-target both auto mvpn`
`  route-target both auto evpn`

IP 1.1.1.1 ska finnas på alla VTEPs samt att "ip pim sparse-mode" ska
läggas på tenants L3SVI:er.

Verify

`show fabric multicast vrf all`
`show fabric multicast globals`

VXLAN EVPN Multi-Site
=====================

Man kan bygga en multisite lösning genom att upprätta eBGP-sessioner
mellan så kallade border gateways och låta dem skriva om next-hop i
EVPN-uppdateringarna, dvs reoriginera EVPN-routes. VTEPs ser endast
neighbors och border gateways i sin egen fabric. Alla externa routes har
border gateway som next-hop och BGW gör data plane decapsulation och
re-encapsulation. Det går alltså att sträcka L2 mellan siter men man får
åtminstone protection och enforcement points i form av BGWs och
storm-control. BGW-rollen går även att kombinera med vanlig VRF-Lite,
t.ex. om det kommer in back-to-back VRF kopplingar för tenants.

Varje sites border gateways sätts upp som anycast (virtual IP), för
lastdelning och redundans, och BGWs pratar VIP till VIP med varandra
mellan siterna. Utöver VIP har varje BGW en PIP (man använder primary
VTEP IP), den används för L2 BUM. Mellan siter är det endast ingress
replication för BUM-transport men inom siterna kan det vara PIM ASM
eller ingress replication. Det behöver heller inte matcha mellan
siterna. BGWs blir BUM-DF per L2VNI, på så sätt distribueras trafiken.
Election process görs och DF synkas med hjälp av Route Type 4 (Ethernet
segment route) mellan BGWs inom siten. BGW har flera inbyggda split
horizon regler för att kunna flooda till alla samtidigt som loopar
undviks. Det finns även pseudo-BGW, dvs leaf utan spine. Då har man
ingen internal site vtep neighbor. Det är t.ex. användbart vid
migreringar in i en EVPN/VXLAN fabric.

`evpn multisite border-gateway `<id>

`interface loopback 100`
` description Anycast BGW IP`

`interface nve 1`
` source-interface loopback 0`
` host-reachability protocol bgp`
` multisite border-gateway interface loopback 100`
` `
` member vni 200    #Every L2VNI that needs stretch`
`  multisite ingress-replication`


`interface ethernet1/1`
` description DCI`
` evpn multisite dci-tracking`
` `
`interface ethernet1/2`
` description Spine`
` evpn multisite fabric-tracking`

`router bgp 65000`
`  address-family l2vpn evpn`
`  neighbor 10.0.0.2`
`   remote-as 65001`
`   peer-type fabric-external`
`   address-family l2vpn evpn`
`     rewrite-evpn-rt-asn`

Tracking är mandatory annars reorigineras inga EVPN routes, det görs
endast om det finns DCI/fabric links som är uppe. Man konfar heller inte
next-hop-self, detta händer av sig själv eftersom EVPN fungerar så
default.

`show nve multisite`
`show nve ethernet-segment`
`show nve multisite dci-links`
`show nve multisite fabric-links`

För "show nve ethernet-segment" notera att L3VNI alltid står som aktiv
på alla BGWs eftersom designated-forwarder election inte görs för dem.

**Storm-control**

`evpn storm-control broadcast level 10`

Overlay Stitching
-----------------

Man kan binda ihop overlays med hjälp av EVPN, t.ex. VXLAN \<-\> MPLS
VPN.

**IOS-XE**

`vrf definition Tenant1`
` rd 125:101`
` `
` address-family ipv4`
`  route-target export 65000:30001`
`  route-target import 65000:30001`
`  route-target export 65000:30001 stitching`
`  route-target import 65000:30001 stitching`
` exit-address-family`

`bridge-domain 3001`
` member vni 30001`

`interface BDI3001 `
` vrf forwarding Tenant1`
` ip address 169.254.0.1 255.255.255.0`
` encapsulation dot1Q 3001`
` no shut`

`interface nve1`
` no ip address`
` no shutdown`
` source-interface Loopback0`
` host-reachability protocol bgp`
` member vni 30001 vrf Tenant1`

`router bgp 65000`
` bgp log-neighbor-changes`
` no bgp default ipv4-unicast`
` no bgp default route-target filter`
` neighbor 10.0.0.11 remote-as 65000`
` neighbor 10.0.0.11 update-source Loopback0`
` neighbor 10.0.0.250 remote-as 65000`
` neighbor 10.0.0.250 update-source Loopback0`

` address-family vpnv4`
`  import l2vpn evpn re-originate `
`  neighbor 10.0.0.250 activate`
`  neighbor 10.0.0.250 send-community extended`
` exit-address-family`

` address-family l2vpn evpn`
`  import vpnv4 unicast re-originate`
`  neighbor 10.0.0.11 activate`
`  neighbor 10.0.0.11 send-community both`
` exit-address-family`

Detta autoskapas på ASR.

`interface Tunnel0`
` ip unnumbered Loopback0`
` no ip redirects`
` ip mtu 9216`
` tunnel source 10.0.0.25`
` tunnel mode udp multipoint`
` tunnel src-port 4789`

**NXOS**

`vrf context Tenant1`
`  vni 30001`
`  rd auto`
`  address-family ipv4 unicast`
`     route-target both auto`
`     route-target both auto evpn `

`router bgp 65000`
`  neighbor 10.2.2.2 remote-as 65000`
`    address-family vpnv4 unicast`
`      import l2vpn evpn reoriginate`
`  neighbor 10.10.10.201 remote-as 65000`
`    address-family l2vpn evpn`
`      import vpn unicast reoriginate`

IOS-XR
======

MPLS Data Plane

### Multihoming

Man har en label för unicast och en multicast label för BUM. Label
allocation görs per BD. Det finns också en label som används för
split-horizon. För unicast är det all active men för BUM så finns det en
DF. Route type 4 används för DF election, detta görs lastdelat
udda/jämna EVI-ID. Både RD och RT autogenereras.

**Leaf**

`interface TenGigE0/0/0/1`
` description "Link to Host"`
` bundle id 1 mode active`
` load-interval 30`
`!`
`interface Bundle-Ether 1`
` lacp system mac 1101.1111.1111`
` load-interval 30`
`!`
`evpn`
` evi 100`
`  advertise-mac   <- enable RT 2 mac-only`
` !`
` interface Bundle-Ether 1`
`  ethernet-segment`
`   identifier type 0 11.11.11.11.11.11.11.11.11`
`   bgp route-target 1111.1111.1111`
`  !`
` !`
` l2vpn`
`  bridge group Cust1`
`   bridge-domain 100`
`    interface BE1`
`    evi 100`
` !`
`!`
`router bgp 1`
` address-family l2vpn evpn`
` !`
` neighbor-group RR`
`  address-family l2vpn evpn`

Verify

`show evpn ethernet-segment detail `
`show evpn evi`
`show evpn evi mac`

**Bring down AC**
För att undvika traffic blackholing när man tappar upplänkar kan man
ange att AC ska stängas när noden är isolerad.

`evpn`
` group 1`
`  core interface `<uplink1>
`  core interface `<uplink2>
` !`
` core-isolation-group 1`

**Single-Active Multihoming**

`evpn`
` interface Bundle-Ether 1`
`  ethernet-segment`
`   load-balancing-mode single-active`

### Routing

`cef adjacency route override rib`
`!`
`interface BVI100`
` host-routing    <- enable RT 2 mac+IP`
` vrf Cust1`
` ipv4 address 10.0.0.1 255.255.255.0`
` mac-address 0000.0000.0111`
`!`
`router bgp 1`
` address-family vpnv4 unicast`
` !`
` vrf Cust1`
`  rd auto`
`  address-family ipv4 unicast`
`   additional-path receive`
`   maximum-paths ibgp 2`
`   redistribute connected`

**VPN Stitching**
EVPN\<-\>VPNv4/6 interconnect

`route-policy rt2-filter`
` if destination in (0.0.0.0/0 ge 32) then`
`  drop`
` else`
`  pass`
` endif`
`end-policy`
`!`
`router bgp 1`
` address-family l2vpn evpn`
`  import stitching-rt re-origiante`
`  advertise vpnv4 unicast re-originated stitching-rt`
` !`
` address-family vpnv4 unicast`
`  import re-originate stitching-rt`
`  route-policy rt2-filter out`
`  advertise vpnv4 unicast re-originated`

[Category:Cisco](/Category:Cisco "wikilink")