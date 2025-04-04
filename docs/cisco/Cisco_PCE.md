---
title: Cisco PCE
permalink: /Cisco_PCE/
---

Tanken med Path Computation Element är att en enskild entitet har
visibilitet över och håller koll på LSPer i en hel domän oavsett antal
areor och IGPer. Detta gör att man kan få fungerande TE både inter-area
och inter-AS. PCE består av Traffic Engineering Database (TED) och Path
Computation Client (PCC).

SR-PCE är en IOS-XR multi-domain stateful SR Path Computation Element
(PCE) som kan köras både virtuellt och fysiskt (kallas då XR Transport
Controller). XTC kan prata ISIS, OSPF och BGP-LS för att få
topologi-information ifrån flera domäner. SR-PCE är SR-optimerat och kan
updatera SRTE-policys allt eftersom. Man deployar det likt RR. Se även
[Segment Routing](/Cisco_SR "wikilink").

Konfiguration
-------------

BGP-LS på P/PE

`router isis 1`
` distribute link-state`
` address-family ipv4 unicast`

`router bgp 100`
` neighbor 11.11.11.11`
`  remote-as 100`
`  update-source Loopback0`
`  address-family link-state link-state`

`show bgp link-state link-state summary`

XTC

`pce`
` address ipv4 11.11.11.11   #own loopback`

`show pce ipv4 peer`

PCC på P/PE

`segment-routing`
` traffic-eng`
`  maximum-sid-depth 5`
`  pcc`
`   source-address ipv4 1.1.1.1   #own loopback`
`   pce address ipv4 11.11.11.11  #XTC`
`   !`
`   report-all`

`show segment-routing traffic-eng pcc ipv4 peer brief`

Förutom vanlig IGP link metric information kan PCE även lära sig prefix
SID och adjacency SID för alla länkar. Detta gör att PCE kan göra path
computation baserat på IOS-XR's CSPF-algoritmer.

`show pce ipv4 topology summary`

[Category:Cisco](/Category:Cisco "wikilink")