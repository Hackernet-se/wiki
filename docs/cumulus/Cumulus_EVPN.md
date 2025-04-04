---
title: Cumulus EVPN
permalink: /Cumulus_EVPN/
---

Ethernet VPN (RFC 7432) är en modernare variant än
[VPLS](/Cisco_VPLS "wikilink") för att tillhandahålla Ethernet
multipoint services över IP (VXLAN) eller MPLS utan att behöva en
central controller. EVPN är en adressfamilj i BGP som används för peer
discovery och för att distribuera lokala MAC-adresser och MAC/IP
bindings till andra tunnel endpoints. Man använder både L2 och L3
forwarding information och det fungerar ihop med externa IP-prefix.
Next-hop i EVPN-uppdateringarna är antingen egress Label Switch Router
eller VXLAN Tunnel Endpoint. EVPN skalar bra och har bl.a. features för
att hålla koll på hostar som flyttar mellan datacenter
(sekvensnummer-community i annonseringarna) och kan då konvergera
snabbt. Ett EVPN-nätverk kan göra både bridging och routing och har
inbyggd support för multi-tenancy (VPN).

Protokollet är öppet så det finns interoperability med andra network
vendors, se t.ex. [Arista](/Arista_EVPN "wikilink"),
[Cisco](/Cisco_EVPN "wikilink") och [Quagga](/Quagga#EVPN "wikilink")
EVPN.

Konfiguration
=============

EVPN kan konfigureras på olika sätt beroende på hur designen ser ut.
Denna artikel har fokus på VXLAN för data plane encapsulation.

### Underlay

Underlay routing kan göras med IGP, iBGP eller eBGP. Alla VTEP:s måste
kunna nå varandra. Simpelt exempel:

`net add loopback lo ip address 1.1.1.1/32`
`net add ospf redistribute connected`
`net add ospf network 0.0.0.0/0 area 0`

### Overlay

EVPN-peering kan göras både med iBGP och eBGP, det är designen som
avgör. Om man kör eBGP mellan leaf och spine får inte spine ändra
next-hop i EVPN-uppdateringarna. Man kan välja att alla lokala VNI:er
ska annonseras med BGP.

`net add bgp autonomous-system 65000`
`net add bgp neighbor 172.16.0.2 remote-as 65000`
`net add bgp neighbor 172.16.0.2 update-source lo`
`net add bgp l2vpn evpn neighbor 172.16.0.2 activate`
`net add bgp l2vpn evpn advertise-all-vni`

EBGP EVPN

`net add bgp bestpath as-path multipath-relax`

Show

`net show bgp evpn summary`

#### Bridging

På varje leaf switch mappas local VLAN till ett VNI (VLAN-based mode).
Man bör disablea data plane MAC learning eftersom EVPN tar hand om att
utbyta mac-adresser mellan VTEP:s. VNI membership utbyts mellan VTEP:s
med hjälp av EVPN type-3. RD/RT-derivering samt import och export görs
automatiskt.

`net add vlan 100`

`net add vxlan VNI100 vxlan id 10100`
`net add vxlan VNI100 vxlan local-tunnelip 1.1.1.1`
`net add vxlan VNI100 bridge access 100`
`net add vxlan VNI100 bridge learning off`
`net add vxlan VNI100 mtu 9216`

Show

`net show evpn vni`
`net show bridge macs`

#### L3

Cumulus kan göra både symmetric och asymmetric VXLAN-routing och har
stöd för L3 multi-tenancy. För asymmetric mode behövs ingen mer konf än
att man per tenant skapar ett anycast SVI på alla leaf. För symmetric
mode routing behöver BGP en 1-till-1 mappning mellan L3VNI och
tenant-VRF, detta måste vara samma överallt. Man installerar
mac-adresser för remote VTEP:s samt genererar RMAC lokalt med ett
"dummy"-SVI per switch. RT-import och export görs automatiskt utifrån
ASN och VNI.

Distributed symmetric routing

`net add vrf Tenant1`

`net add vxlan VNI30001 vxlan id 30001`
`net add vxlan VNI30001 bridge access 2301`
`net add vxlan VNI30001 vxlan local-tunnelip 1.1.1.1`
`net add vxlan VNI30001 bridge learning off`
`net add vxlan VNI30001 bridge arp-nd-suppress on`
`net add bridge bridge ports VNI30001`

`net add vlan 2301 vrf Tenant1`
`net add vrf Tenant1 vni 30001`

Show

`net show evpn vni`
`net show evpn rmac vni all`

**Anycast GW**

`net add vlan 100 ip address-virtual 00:00:11:11:22:22 10.0.0.1/24`
`net add vlan 100 vrf Tenant1`

**ARP/ND Suppression**
Man kan låta en lokal ARP-proxy hantera requests för att suppressa ARP
flooding över VXLAN så mycket som möjligt. MAC+IP address advertisement
behövs för ARP suppression.

`net add vxlan VNI100 bridge arp-nd-suppress on`

Show

`net show evpn arp-cache vni all`

**Type-5 Routes**
Prefix-based routing används primärt för destinations utanför DC.
EVPN-routes har L3-VNI och RMAC enligt symmetric routing model.

`net add bgp vrf Tenant1 autonomous-system 65000`
`net add bgp vrf Tenant1 l2vpn evpn advertise ipv4 unicast`

### MLAG

Cumulus har stöd för dual-attached hosts i VXLAN active-active mode. Det
krävs ingen speciell konfiguration för detta mer än att alla VNI:er
måste konfas identiskt och att peerlinken tillhör bridge. MAC
synchronization görs inte med EVPN utan med MLAG.

`interface lo`
` address 1.1.1.1/32`
` clagd-vxlan-anycast-ip 1.1.1.100`

Denna anycast-adress sätts som next-hop i de EVPN-uppdaterignar som
skickas ut så den adressen måste annonseras i underlay.

[Category:Cumulus](/Category:Cumulus "wikilink")