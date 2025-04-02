---
title: Cisco Services
permalink: /Cisco_Services/
---

[Cisco IOS](/Cisco_IOS "wikilink") har stöd för diverse protokoll för
mgmt och filöverföring.

Kontrollera vilka portar som är aktiva: **show control-plane host
open-ports**

Samt vilken service som använder vilken port: **show ip port-map**

HTTP
====

`ip http server`
`ip http secure-server `
`show ip http server all`

Filöverföring med HTTP brukar vara snabbare än tftp och scp.

`copy `[`http://10.0.0.10/ios.bin`](http://10.0.0.10/ios.bin)` flash:`

DNS
===

Server

`ip dns server`
`ip dns spoofing 2.2.2.2`
`ip name-server 8.8.4.4 8.8.8.8 `
`ip domain round-robin`

Verify

`show ip dns primary`
`debug domain`

Hosts

`ip host r1 10.0.0.10`
`show hosts`

NTP
===

NTP är väldigt effektivt för att synkronisera klockan mellan två system,
ett paket i minuten räcker för att synka det till en millisekunds
noggrannhet. I nyare versioner av IOS används NTPv4 (*show ntp
information*) och det finns därmed stöd för IPv6. Det går dock att
ställa NTP-version per interface eller peer. Offset måste vara mindre än
1000 msec för att servern ska anses *sane*. Om det är mycket offset så
kommer synk-processen att ta lång tid.

Packet types

-   Control messages: peer status och set management parameters
-   Update/request messages: time synchronization

<div class="mw-collapsible mw-collapsed" style="width:200px">

Client:

<div class="mw-collapsible-content">

[<File:Cisco_NTP_client.png>](/File:Cisco_NTP_client.png "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:200px">

Server:

<div class="mw-collapsible-content">

[<File:Cisco_NTP_server.png>](/File:Cisco_NTP_server.png "wikilink")

</div>
</div>

`ntp logging`
`debug ntp all`

**Tidszon** (Sverige)

`clock timezone CET 1`
`clock summer-time CEST recurring last sunday march 02:00 last sunday october 03:00`

**Server**

`ntp master `<stratum>`  #8 är default`
`show ntp packets mode server`

**Klient**

`ntp server 10.0.0.10`
`ntp server vrf Mgmt 130.236.254.102`

*OBS det kan ta lång tid innan klient synkar med server första gången.*

**Peer**
Båda enheter kan uppdatera sina klockor mot varandra, som ett
NTP-kluster

`ntp peer 10.0.0.10 [key 20]`

**Verify**
För att veta att NTP fungerar som det ska kan man kolla på reach-fältet.
Det är en 8-bitars buffer där varje lyckat paket representeras av en 1:a
och det som står i reach-fältet är på basen 8 så det man vill se är 377,
annars betyder det att någon av de senaste 8 ntp-paketen inte kommit
fram. När server och klient närmar sig synk och inga paket droppas
kommer poll-intervallet att öka över tid, till max 1024. Det går ej att
ändra routerns NTP poll intervall eftersom det bestäms av en heuristisk
algorithm.

`show ntp status`
`show ntp associations `

Ställ klockan manuellt. Kan göras för att skynda på klocksynkronisering.

`clock set 12:00:00 20 July 2020`

**Access control**
Med ACL, NTP Access control levels:

`ntp access-group ipv4 `<ACL>

**Authentication**
enable authentication, configure a key with a key index, trust the key.

`ntp authenticate`
`ntp authentication-key 20 md5 SECRET`
`ntp trusted-key 20`

`show ntp associations detail  | inc auth`

**Broadcast**
NTP-paket går även att skicka med broadcast eller multicast, detta
händer alltså utan att klienten "beställer" det.

`interface gi2`
` ntp broadcast|multicast`
` ntp broadcast key 20`

Receiver

`int vlan 101`
` ntp broadcast|multicast client`

**Others**
Default-inställningar

`ntp max-associations 100`
`ntp allow mode control 3`
`ntp mindistance 1`
`ntp maxdistance 8`

Enable hardware clock synchronization

`ntp update-calendar`

If my peer or configured master's clock is more than 1,000 seconds
(default) off of my clock, reject the update and syslog.

`ntp panic update`

Distance, 1 är slow convergence, 16 är fast

`ntp maxdistance <1-16>`

Orphan kicks in when we lose sync with our server. The number here is a
stratum number, and must be a number lower than your real upstream NTP
server

`ntp orphan <1-16>`

### NX-OS

NX-OS kör också NTPv4.

`feature ntp`
`ntp logging`

Cisco Fabric Services (CFS) kan användas för att distribuera
NTP-konfigurationen mellan Nexus-switchar. När man gör NTP-konfiguration
så blir NTP låst network-wide (Fabric Lock).

`ntp distribute`

`ntp master`
`ntp server 10.0.1.10`
`ntp source-interface loopback0`

`ntp commit / abort`

Verify

`show ntp status`
`show ntp peers`

Notera att det endast är en [VDC](/Nexus_VDC "wikilink") som synkar
klockan i switchen.

`clock protocol ntp vdc `<vdc-id>

SCP
===

Secure copy protocol på IOS kräver AAA för user authentication och
authorization eftersom copy är ett exec-kommando.

Server

`ip scp server enable`

Push ios to switch

`scp ios.bin admin@10.0.0.10:ios.bin`

Fetch ios from server

`copy scp://10.0.0.10:ios.bin flash:ios.bin`

TFTP
====

Server, dela ut fil med TFTP.

`tftp-server nvram:startup-config alias TEST`

Klient

`ip tftp source-interface loopback0`
`copy `[`tftp://10.0.0.10/TEST`](tftp://10.0.0.10/TEST)` null:`

För att säkerställa interoperability med gamla TFTP-servrar kan man
behöva ställa ner blocksize.

`ip tftp blocksize 1024`

Debug

`debug tftp events`

FTP
===

Server, because of numerous vulnerabilities (bug ID CSCse29244, IOS
crash when transferring files via FTP) Cisco has removed the FTP server
functionality from recent IOS releases.

Klient

`no ip ftp passive`
`ip ftp source-interface Loopback0`
`ip ftp username USER`
`ip ftp password SECRET`

[Category:Cisco](/Category:Cisco "wikilink")