---
title: Arista OSPF
permalink: /Arista_OSPF/
---

Open Shortest Path First. Se även [Cisco OSPF](/Cisco_OSPF "wikilink")

Konfiguration
-------------

`router ospf [process-id]`

router-id for this OSPF process (in IP address format)

`router-id [OSPF router-id] `

`log-adjacency-changes`

Enable routing on an IP network

`network [network-number] [wildcard-mask] area [area-id]`

Suppress routing updates on an interface

`passive-interface [interface]`

`default-information originate`

`interface [interface]`
`ip ospf priority [number]`
`exit`

ABR Summarization

`router ospf 1`
`area 10 range 10.10.0.0 255.255.252.0`
`exit`

ASBR Summarization

`router ospf 1`
`summary-address 10.10.0.0 255.255.252.0`
`exit`

`router ospf 1`
`auto-cost reference-bandwidth 1000`
`exit`

Troubleshoot
------------

`show ip ospf neighbor`
`ping 224.0.0.5`
`show ip ospf interface brief`

[Category:Arista](/Category:Arista "wikilink")