---
title: Arista BGP
permalink: /Arista_BGP/
---

Se även [Cisco BGP](/Cisco_BGP "wikilink")

Konfiguration
=============

`router bgp 65001`
`  neighbor 20.20.20.20 remote-as 65001`
`  neighbor 20.20.20.20 description vEOS20`
`  neighbor 20.20.20.20 password 7 gqWjIYItRuw=`
`  neighbor 20.20.20.20 maximum-routes 12000`
`  network 210.210.210.0/24`

**ECMP**

`router bgp 65001`
` maximum-paths 4 ecmp 4`

**Show**

`show ip bgp summary`
`show ip bgp neighbor`

**Reset**

`clear ip bgp *`
`clear ip bgp `

<address>

soft

### BGP-LU

BGP kan annonsera unicast routes med en associated mpls label (RFC
3107). Det kan t.ex. användas för att tunnela genom andra provider
backbones och på så sätt binda ihop multipla IGP-instancer över
stitchade LSP paths. BGP-LU advertisements påverkar endast edge/border
routers och inte P routers.

`router bgp 65001`
` neighbor 2.2.2.2 remote-as 65001`
` neighbor 2.2.2.2 update-source Loopback0`
` neighbor 2.2.2.2 maximum-routes 12000`

` address-family ipv4 labeled-unicast`
`  neighbor 2.2.2.2 activate`

Verify

`show ip bgp labeled-unicast`

[Category:Arista](/Category:Arista "wikilink")