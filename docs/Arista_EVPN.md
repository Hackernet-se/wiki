---
title: Arista EVPN
permalink: /Arista_EVPN/
---

Ethernet VPN (RFC 7432) är en modernare variant än
[VPLS](/Cisco_VPLS "wikilink") för att tillhandahålla Ethernet
multipoint services över IP ([VXLAN](/Arista_VXLAN "wikilink")) eller
MPLS (med eller utan [SR](/Arista_SR "wikilink")). BGP EVPN är en ny
adressfamilj som används för att distribuera lokala MAC-adresser och
MAC/IP bindings till VTEP:s. Next-hop i EVPN-uppdateringarna är antingen
egress Label Switch Router eller VXLAN Tunnel Endpoint. EVPN har bl.a.
features för att hålla koll på hostar som flyttar mellan datacenter
(sekvensnummer i annonseringarna) och kan då konvergera snabbt. Ett
EVPN-nätverk kan göra både bridging och routing och har inbyggd support
för multi-tenancy. Protokollet är öppet så det finns interoperability
med andra network vendors, se t.ex. [Cisco](/Cisco_EVPN "wikilink"),
[Cumulus](/Cumulus_EVPN "wikilink") och
[Quagga](/Quagga#EVPN "wikilink") EVPN.

**Route types**
\# Ethernet Auto-Discovery Route

1.  MAC/IP Advertisement Route
2.  Inclusive Multicast Ethernet Tag Route
3.  Ethernet Segment Route
4.  IP Prefix Route

Konfiguration
=============

EVPN kan konfigureras på olika sätt beroende på hur designen ser ut
däremot måste man byta BGP agent ifrån GateD till arBGP.

`service routing protocols model multi-agent`

EOS kan än sålänge inte auto-derivera RD eller RT.

### Underlay

Underlay routing kan göras med IGP, iBGP eller eBGP. Alla VTEP:s måste
kunna nå varandra. Simpelt exempel:

`ip routing`

`interface Loopback0 `
` description VTEP`
` ip address 1.1.1.1/32 `

`router ospf 1`
` redistribute connected`
` network 0.0.0.0/0 area 0.0.0.0`

### Overlay

`interface Vxlan1  `
` vxlan source-interface Loopback0`
` vxlan udp-port 4789 `

`router bgp 65000`
`  no bgp default ipv4-unicast`
`  neighbor 172.16.0.2 remote-as 65000`
`  neighbor 172.16.0.2 send-community extended`
`  !`
`  address-family evpn`
`    neighbor 172.16.0.2 activate`

Verify

`show bgp evpn summary`

#### Bridging

`vlan 100-101`

`interface Vxlan1  `
` vxlan vlan 100 vni 10100`
` vxlan vlan 101 vni 10101`

`router bgp 65000`
` vlan 100`
`   rd 1.1.1.1:100`
`   route-target both 65000:10100`
`   redistribute learned`
` vlan 101`
`   rd 1.1.1.1:101`
`   route-target both 65000:10101`
`   redistribute learned`

Verify

`show bgp evpn route-type mac-ip`

#### L3

Arista implementerar EVPN VXLAN routing i symmetric mode. För att få
fram RMAC samt ha ett interface in mot fabricen (logisk) autoskapar EOS
ett SVI per VRF som har ett L3VNI knytet till sig. Det man måste konfa
är VRF, knyta till L3VNI och få in i BGP.

`vrf definition Tenant1`

`ip routing vrf Tenant1`

`interface Vxlan1`
` vxlan vrf Tenant1 vni 30001`

`router bgp 65000`
` vrf Tenant1`
`   rd 1.1.1.1:1009`
`   route-target import 65000:30001`
`   route-target export 65000:30001`

**Anycast GW**

`ip virtual-router mac-address 0000.1111.2222`

`interface Vlan100`
` vrf forwarding Tenant1`
` ip address virtual 10.0.0.1/24`

'''Skicka lokala IP prefix, route type 5

`router bgp 65000`
` vrf Tenant1`
`  redistribute connected`

Verify

`show bgp evpn route-type ip-prefix ipv4`

[Category:Arista](/Category:Arista "wikilink")