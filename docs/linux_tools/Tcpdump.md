---
title: Tcpdump
permalink: /Tcpdump/
---

Tcpdump är ett verktyg för att se vilka paket som går via ett interface
och göra lite grundläggande felsökning.

Installation
============

Debian/Ubuntu

`apt-get install tcpdump`

Vanliga Växlar
==============

-   -i
    -   Val av interface att lyssna på
-   -T
    -   Paket typ t.ex. carp, snmp eller radios
-   -n
    -   Gör ingen reverse lookup på IP
-   -c
    -   Antal paket innan klar (standard är undef)

Uttryck
=======

tcpdump visar alla paket som matchar det angivna uttrycket och använder
samma syntax som [pcap-filter](/pcap-filter "wikilink")

Exempel
=======

-   tcpdump -i eth0 port 67 or port 68
    -   Lyssnar efter DHCP paket på eth0
-   tcpdump -i eth0 src 10.20.30.40
    -   Lyssnar efter paket med 10.20.30.40 som source address
-   tcpdump -i eth0 host 10.20.30.40
    -   Lyssnar efter paket som innehåller 10.20.30.40

[Category:Tools](/Category:Tools "wikilink")