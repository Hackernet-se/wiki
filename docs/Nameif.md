---
title: Nameif
permalink: /Nameif/
---

När Linuxkärnan bootar tilldelas namn till nätverksinterfacen i den
ordning som den finner dem. Detta innebär att två olika versioner av
kärnan kan hitta interfacen i olika ordning. När detta händer kan du
behöva byta all konf för att få igång det igen. Ett sätt att undvika
detta är med udev-regler, ett annat är att namnge interfacen med nameif.

`sudo yum install net-tools`

`sudo nano /etc/mactab`
`# This file relates MAC addresses to interface names.`
`eth0 00:60:97:52:2A:94`
`eth1 00:A0:C9:43:1F:77`

Ta ner interfacen och kör kommandot **nameif** alternativt reboota
maskinen.

[Category:Tools](/Category:Tools "wikilink")