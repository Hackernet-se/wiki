---
title: Cisco pyATS
permalink: /Cisco_pyATS/
---

Cisco pyATS är ett testing framework skrivet i python. Det kan användas
för att ta en snapshot på "state" i nätverket. pyATS <ssh:ar> runt och
samlar in show-kommandon ifrån nätinfrastrukturen.

Setup
-----

Installera

`pip install pyats[full]`

Skapa ett inventory, även kallat testbed.

`pyats create testbed interactive --output testbed1.yml --encode-password`

Diff
----

`pyats learn ospf interface routing pim mcast vrf ntp arp vlan config --testbed-file=aci_ipn.yml --output=before_change`

`**make change to network**`

`pyats learn ospf interface routing pim mcast vrf ntp arp vlan config --testbed-file=aci_ipn.yml --output=after_change`

`pyats diff before_change after_change`

[Category:Cisco](/Category:Cisco "wikilink")