---
title: Cisco IOS-XR
permalink: /Cisco_IOS-XR/
---

IOS XR är Ciscos OS framtaget för de större enheterna (främst mot
service provider) tex CRS serien, 12000 serien och ASR9000 serien.

XR bygger på en micro-kernel arkitektur och är framtaget för att att
utöka tillgängligheten på enheter t.ex. genom att ha redundant hårdvara
(linjekort, cpu), felhantering som t.ex. skyddat minnesutrymme och med
möjlighet att starta om specifika processer (kan ske per automatik). XR
använder liknande modell som tex. Cisco Nexus där med distribuerad
modell där man kan aktivera de delar man önskar tex. multicast eller
MPLS.

IOS XR är likt Juniper's [JunOS](/Juniper_JunOS "wikilink") uppdelat i
två lägen, admin-läge och "operations"-läge och XR har ett inbyggt
system för hantera användare och grupper. Även i XR behöver man använda
commit precis som i JunOS.

**Security**
IOS-XR har ICMP redirects disabled by default samt att
directed-broadcast packets droppas. Cisco har mycket dokumentation kring
security, [Service Provider
Security](https://www.cisco.com/c/en/us/about/security-center/service-provider-infrastructure-security.html)

Konfigurationshantering
-----------------------

Till skillnad från IOS så ändras inget innan man kör commit. Kommandon
kopplat till konfigurationshantering.

Visa ändringar som kommer att installeras vid commit:

`show configuration`
`alias config diff show commit changes diff`

Visa hur hela konfiguration kommer se ut efter commit:

`show configuration merge`

Göra commit med en märkning av konfigurationen:

`commit label add-loopback1337`

Visa misslyckad commit tex. om något i konfiguration saknas eller är
inkompatiblet (detta meddelas vid en vanlig commit)

`show configuration failed`

Lista historiska förändringar:

`show configuration history`

Backa konfiguration till specifik konfiguration:

`rollback configuration to add-loopback1337`

Backa konfiguration till senaste konfiguration:

`rollback configuration last 1`

Är man inte helt säker på sin commit kan man köra commit confirmed, då
måste man aktivt skriva commit confirm annars görs automatiskt en
rollback.

`commit confirmed`
`commit confirm `

Export configuration on commit.

`configuration commit auto-save filename `[`tftp://10.0.0.11/router1`](tftp://10.0.0.11/router1)

Man kan använda regex-baserad replace av konfiguration, t.ex. om man ska
döpa om en policy eller acl.

`replace pattern 'POLICYMAP-WRONG_NAME' with 'POLICYMAP-RIGHT_NAME'`

Run silently without the user being prompted for yes/no.

`service cli interactive disable`
`copy running-config disk0:test_config.txt`

Default listas interface i bokstavsordning, detta går att ändra.

`configuration display interface slot-order`

To prevent the re-application of the commands which are already present
in the running configuration.

`service cli commit-optimized enable`

**Konfigurationslås**
Vid konfigurering kan konfigurationsläget göras exklusivt:

`configure exclusive`

Visa låst konfiguration:

`show configuration lock`

Visa vem som låst konfigurationen:

`show configuration sessions`

Admin
-----

Gå till admin läge, här kan man styra användares behörigheter, ändra
config-register, installera funktioner etc. Kommandon för admin-läget
kan alltid köras genom tex "admin show running-config"

`admin`

Visa konfiguration (enbat för Admin läge)

`(admin)#show running-config`

Skapa användare

`admin`
`conf t`
`username juan`
` group root-system`
` secret cisco`

#### Fördefinierade grupper

-   root-system: Fullständig access

<!-- -->

-   netadmin: Möjliggör konfiguration av tex OSPF eller EIGRP

<!-- -->

-   sysadmin: Möjliggör systemändringar tex dump av konfig eller tex.
    konfiguration av NTP

<!-- -->

-   operator: Kan titta i konfigurationen men je göra förändringar

<!-- -->

-   cisco-support: För Cisco TAC support

#### Egna grupper

I XR kan man skapa egna grupper för specifika ändamål

`taskgroup BGP`
` task execute bgp`
` task read bgp`
` task write bgp`

`taskgroup ISIS`
` task execute isis`
` task read isis`
` task write isis`

`taskgroup BGPISISTasks`
` inherit taskgroup BGP`
` inherit taskgroup ISIS`

`usergroup BGPISISAdmins`
`taskgroup BGPISISTasks`

`username juan_bgp`
` group BGPISISAdmins`
` secret cisco`

Grundkonfiguration
------------------

`hostname XR-01`
`!`
`ipv4 netmask-format bit-count`
`!`
`line console`
` exec-timeout 30 0`
`!`
`line default`
` exec-timeout 30 0`
` access-class ingress ACL-MGMT-ACCESS`
` transport input ssh`

**SSH**

`crypto key generate rsa general-keys`
`How many bits in the modulus [1024]: `<enter>
`ssh server v2`
`ssh server logging`
`line default transport input ssh`

SSH Package behövs.

`show install active | include k9`

**Logging**

`logging on`
` logging buffered 200000`
` logging 10.0.10.12`

Skicka godtyckligt loggmeddelande

`logmsg HEJ`

**NTP**

`clock timezone CET Europe/Stockholm`

`ntp`
` server 79.136.86.176`
` update-calendar`

**Tidszon**

`clock timezone CET 1`
`clock summer-time CEST recurring last sunday march 02:00 last sunday october 03:00`

**SNMP**
För att spara lite CPU-cykler kan man slå på statsd caching. Detta är
generellt rekommenderat.

`snmp-server ifmib stats cache`

**pyIOSXR**
Enable XML agent

`xml agent tty iteration off`

**CDP**
CDP är default avstängt globalt och per inteface i XR. För att slå på
CDP på XR måste det slås på globalt och per interface:

`cdp`
` interface GigabitEthernet0/0/0/0`
`  cdp`

**MTU**
MTU i IOS-XR räknas lite annorlunda kontra IOS eftersom L2 headern är
inkluderad. Default har IOS och IOS-XR dock samma MTU på
Ethernet-interface (L3: 1500B) men ska man köra jumbo frames och vill
matcha är IOS-XR = IOS + 14, exempel:

IOS

`mtu 9216`

IOS-XR

`mtu 9230`

Plattform
---------

`top`
`show redundancy `
`show platform`
`show install active summary`
`show install committed summary`
`show fpd package`

Upgrade

`fpd auto-upgrade enable`

`sysadmin-vm:0_RSP0# show install health`
`install add source harddisk: asr9k-mini-x64-6.5.3.iso`

### CoPP

Control Plane Policing (CoPP) skyddar kontrollplanet för att säkerställa
stabilitet, nåbarhet och paketleverans. CoPP i IOS-XR implementeras med
hjälp av Local Packet Transport Services. LPTS är ett koncept med
reflexsiva ACL:er, punt policers och en slags intern FIB. Detta skydd är
på default med fördefinierade värden. Cisco rekommenderar att dessa
lämnas default initialt för att eventuellt modifieras vid ett senare
tillfälle utifrån behov. IOS-XR kan även hantera viss trafik direkt i
linjekorten för att avlasta CPU, t.ex. BFD, Netflow och ARP kommer LPTS
instruera lokal CPU att hantera istället för RSP CPU.

`show lpts bindings brief`

**MPP**
Management Plane Protection är på default men alla TCP- och UDP-portar
kan accessas ifrån alla interface. Detta går att strypa ner för både
inband och OoB.

`control-plane`
` management-plane`
`  out-of-band`
`   interface MgmtEth0/0/CPU0/0`
`    allow SSH peer`
`     address ipv4 10.0.0.0/24`

### RPL

När man editerar en existerande policy och commitar kommer det
automatiskt att skickas BGP REFRESH, förutsatt att granne har denna
capability. Det görs också en full table refresh eftersom förändringen
kanske innebär att prefix som inte tidigare importerades nu ska
importeras. Man behöver alltså inte göra någon soft reset som med IOS.
Detta går att stänga av.

`bgp auto-policy-soft-reset disable`

Troubleshooting - dry run

`show bgp route-policy `<ROUTE-POLICY-NAME>

Kolla hur lång tid olika route-policy entries tar för en viss peering

`debug pcl profile detail`
`!clear bgp peering`
`show pcl protocol bgp speaker-0 neighbor-in-dflt `<neighbor>` policy profile`

HSRP
----

`interface GigabitEthernet 0/0/0/0`
` ip address 10.32.0.3 255.255.255.0`
`router hsrp`
` interface GigabitEthernet 0/0/0/0`
` hsrp 1 ipv4 10.32.0.1`
` hsrp 1 priority 95`
` hsrp 1 preempt`
` hsrp 1 track GigabitEthernet 0/0/0/1`

VRRP
----

`interface GigabitEthernet 0/0/0/0`
` ip address 10.32.25.3 255.255.255.0`
`router vrrp`
` interface GigabitEthernet 0/0/0/0`
`  address-family ipv4`
`   vrrp 1`
`    address 10.32.25.1`
`    priority 95`
`    track interface GigabitEthernet 0/0/0/0 10`

VRF
---

Nedan exempel används ihop med MPLS och BGP.

`vrf 1337`
` address-family ipv4 unicast`
`  import route-target`
`   1337:10`
`  export route-target`
`   1337:10`

`router bgp 1337`
` vrf 1337`
`  rd 1337:10`
`  address-family ipv4 unicast`
`   redistribute static`

Protip: I XR när man kör "show run vrf xx" ser man bara det som finns
konfigurerat under "vrf xx", inte tex det som rör vrf under bgp
konfigurationen. För att se allt i konfugrationen som rör en specifik
vrf kan följande kommando användas:

`show run formal | i vrf 10`

**CEF**
show cef ipv6 exact-route 2001::2:2 2001::1:1 protocol icmp
ingress-interface GigabitEthernet0/0/0/0.101

[Category:Cisco](/Category:Cisco "wikilink")