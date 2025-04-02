---
title: Arista VXLAN
permalink: /Arista_VXLAN/
---

Virtual Extensible LAN (VXLAN) är en network virtualization technology.
VXLAN bridging tillhandahåller layer 2 konnektivitet för end systems
över en routad infrastruktur. För att koppla ihop end systems i olika
subnät krävs antingen centralized routing eller VXLAN routing. Det
senare kan göras både symmetriskt och asymmetriskt, dvs om samma VNI
används i båda trafikriktninger eller ej. Default för enkapsulerade
paket mellan VTEP:ar används UDP port 4789. Däremot kan control plane
göras på olika sätt, se nedan. Aristas VXLAN går att kombinera med
[MLAG](/Arista_MLAG "wikilink"). Se även [Cisco
VXLAN](/Cisco_VXLAN "wikilink").

Konfiguration
=============

Initial setup. VTEP-IP måste vara nåbar från alla andra VTEP:ar.

`interface Loopback0`
` description VTEP`
` ip address 10.0.0.10/32`

`interface Vxlan1`
` vxlan source-interface Loopback0`
` vxlan udp-port 4789`

Skapa vlan och mappa med VNI.

`vlan 100`

`interface Vxlan1`
` vxlan vlan 100 vni 10100`

Verify

`show interface vxlan 1`
`show vxlan address-table`

Flood and Learn
---------------

Med denna setup görs MAC learning med hjälp av flooding.
Multidestinationstrafik (BUM) hanteras med Head-End Replication i
underlay. Man måste konfa IP-adresser till alla VTEP:ar på alla VTEP:ar.
Man kan även ange den lokala vtep-ip:n i flood-listan, den kommer att
accepteras i konfen men ignoreras i praktiken. Flood and Learn är
simpelt men inte det mest skalbara alternativet.

`interface Vxlan1`
` vxlan vlan 100 flood vtep 10.0.0.11 10.0.0.12`

Verify

`show vxlan flood vtep`

CVX
---

CloudVision eXchange (CVX) kan automatiskt synkronisera VTEP:arna och
deras state samt nödvändiga HER flood-lists. CVX synkroniserar alla
MAC-adresser så fort en switch lärt sig dem på någon lokal port, dvs
leafs publicerar sin mac table till CVX. Man kan sätta upp ett
HA-kluster för resiliency. Det finns även stöd för third-party VTEP:s.

Leaf

`interface vxlan1`
` vxlan source-interface Loopback0`
` vxlan udp-port 4789`
` vxlan control-service`

`management cvx`
` source-interface lo0`
` server host 10.0.0.100`
` no shut`

Standalone CVX VXLAN service on EOS

`interface Loopback0`
` ip address 10.0.0.100/32`

`config`
` cvx`
`  no shutdown`
`  service vxlan`
`   no shutdown`

Verify

`show cvx `
`show cvx connections`
`show vxlan controller status`
`show vxlan controller address-table received`

EVPN
----

Se [Arista EVPN](/Arista_EVPN "wikilink").

Multitenancy routing
====================

Anycast gateway

`hardware tcam profile vxlan-routing`

`vrf definition Tenant1`
` rd 100:1`

`ip routing vrf Tenant1`
`ip route vrf Tenant1 0.0.0.0/0 10.0.0.1`

`interface Vlan100`
` vrf forwarding Tenant1`
` ip address virtual 10.0.0.10/24`

`interface Vlan101`
` vrf forwarding Tenant1`
` ip address virtual 10.0.101.1/24`

NSX
===

Arista-switchar kan agera VTEP:s för
[VMware](/VMware_vCenter "wikilink") NSX. Ta certet och importera i NSX
Manager.

`show hsc certificate`
`show hsc status`

[Category:Arista](/Category:Arista "wikilink")