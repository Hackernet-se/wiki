---
title: Cisco Wireless
permalink: /Cisco_Wireless/
---

WLC Discovery
-------------

1.  Broadcast
2.  DNS
3.  DHCP option 43
4.  Hardcoded
5.  Previous WLC

IP helper
---------

`ip forward-protocol udp 5246`
`ip helper [WLC-IP]`

AP Join Troubleshooting
-----------------------

1.  Layer 3 connectivity (ping)
2.  AP Policy
3.  Controller time in relation to AP cert
4.  regulatory domain
5.  license limit
6.  AP model not supported on WLC version
7.  Mesh APs - AP Auth
8.  no AP Manager

Tips N Trix
-----------

Om accesspunkt inte kopplar upp sig via DHCP eller dns så måste man
hårdkoda WLCn då det är en bugg i den firmwaren som skickas med men
uppgraderas när den får kontakt med WLC

`"Capwap AP controller IP address x.x.x.x" Där x.x.x.x är IP adressen på din WLC`

Om du har en MESH ap så måste du lägga till en exception i WLCn för den
skall koppla upp sig. Tex 1532E

`Security->AAA->AP policys där under lägger du in macadressen på APn sen får man gå in på den under Monitor-> Detail all APs-> sen den valda APn och byta från Bridge mode till Local så fungerar den som en vanlig `
`accesspunkt igen. Där under kan du också byta namn på den.`

Om du vill Byta aktiv WLC i ett HA cluster använder du kommandot:

`Redundancy force-switchover`

Lägg till radius server (webgui)

`Logga in på WLC sen Security->AAA->Radius->Authentication där fyller du i IP adressen till din radius server samt den PREshared key du använder dig av.`

Se hur redundansen ser ut på enheten

`show redundancy summary`

[Category:Cisco](/Category:Cisco "wikilink")