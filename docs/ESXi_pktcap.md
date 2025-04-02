---
title: ESXi pktcap
permalink: /ESXi_pktcap/
---

pktcap-uw är efterföljare till tcpdump-uw och innehåller några nya
funktioner. Det används för paketanalys och ingår default sedan 5.5. Man
kan fånga trafik från vmk-interface, vmnicar och fysiska nicar.

Användning
==========

Lista interface

`esxcli network nic list`
`esxcli network ip interface list`

Fysisk NIC

`pktcap-uw --uplink vmnic0`

Spara capture till fil med -o

`pktcap-uw --vmk vmk0 -o vmk0.pcap`

Specifik IP

`pktcap-uw --vmk vmk0 --ip x.x.x.x`

Specifik port

`pktcap-uw --vmk vmk0 --tcpport 443`

Använd esxtop för att ta reda på en virtuell maskins vswitch Port ID

`esxtop  #press n`
`pktcap-uw --switchport 33554439`

[Category:VMware](/Category:VMware "wikilink")