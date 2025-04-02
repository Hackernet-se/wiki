---
title: Dnstracer
permalink: /Dnstracer/
---

Dnstracer är som traceroute fast för dnsuppslag.

Installation
============

Debian/Ubuntu

`apt-get install dnstracer`

Växlar
======

-   -c
    -   Stäng av lokal cache.
-   -C
    -   Sätt på negative cache.
-   -o
    -   Visa ett mer lätt läst resultat.
-   -q
    -   Ändra query-class, default är A. Eller nån av följande a, aaaa,
        a6, soa, cname, hinfo, mx, ns, txt och ptr.
-   -r
    -   Antal dns försök, default 3.
-   -s
    -   Vilken DNS server som ska användas, ifall ingen anges så används
        systemets DNS server. Om en punkt skrivs så kommer den använda
        A.ROOT-SERVERS.NET.
-   -v
    -   Verbose output på vad som skickats och tagits emot.
-   -4
    -   Använd bara IPv4 servrar.
-   -S
    -   Ändra vilken source adress som används.

Exempel
=======

`dnstracer -o4s . hackernet.se`

[Category:Tools](/Category:Tools "wikilink")