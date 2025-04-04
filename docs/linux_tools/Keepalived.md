---
title: Keepalived
permalink: /Keepalived/
---

[BFD](/BFD "wikilink") [vrrp](/vrrp "wikilink") [lvs](/lvs "wikilink")

misc_dynamic
-------------

Misc_dynamic på en misc_check låter dig sätta vikten mot din
realserver dynamiskt baserat på exitkoden från ditt script.

Exitkod 0 är success (oförändrad vikt)

Exitkod 1 är failure (realserver tas ur poolen)

Exitkod 2 och högre sätts som vikt-2, exitkod 252 t.ex. kommer ge dig en
vikt på 250.

<https://www.keepalived.org/>

[Category:Tools](/Category:Tools "wikilink")