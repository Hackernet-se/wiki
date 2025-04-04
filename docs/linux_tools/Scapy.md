---
title: Scapy
permalink: /Scapy/
---

Scapy är ett kraftfullt och interaktivt paketmanipulationsprogram. Det
kan förfalska och avkoda paket av flera protokoll samt skicka ut dem på
tråd. Det kan hantera de flesta klassiska uppgifter som skanning,
tracerouting, enhetstester, attacker eller nätverksidentifiering. Scapy
är skrivet i Python.
Enligt utvecklaren kan Scapy ersätta hping, 85% av Nmap, arpspoof, arp
-sk, arping, tcpdump, tethereal samt p0f.

**Grunder:**

`Lista protokoll och alternativ`
`ls()`
`Lista inbyggda kommandofunktioner`
`lsc()`
`Visa/sätt konfiguration`
`conf`
`Skicka paket på lager 3`
`send()`
`Skicka paket på lager 2`
`sendp()`

**Användbara exempel:**

`sendp(Ether(src='00:50:56:22:33:e7', dst='00:50:56:cc:aa:af')/IPv6(src='2001::5', dst='2001::10', hlim=64)/ICMPv6EchoRequest(data=''))`

[Category:Tools](/Category:Tools "wikilink")