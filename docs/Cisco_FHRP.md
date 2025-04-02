---
title: Cisco FHRP
permalink: /Cisco_FHRP/
---

First Hop Redundancy Protocol används för att skydda
gateway-tillgängligheten genom att låta flera enheter agera backup för
varandra. Se även [Cisco HSRP](/Cisco_HSRP "wikilink").

VRRP
====

Virtual Router Redundancy Protocol (RFC 3768) är ett öppet FHRP. Det
fungerar väldigt likt HSRP men med några skillnader. Preemption är
påslaget default till skillnad från HSRP, båda protokollen kan dock ha
det på eller av. VRRP använder den inbyggda trackingfunktionen i IOS.
Source-IP för VRRP-paket är interface IP, destination-IP är 224.0.0.18
och protokoll är 112. Hellos skickas default varje sekund. Man kan till
skillnad från HSRP ha samma virtual ip som interface ip. Konfigurerar
man det ändras VRRP-prio till 255 på den enheten som har samma IP som
VIP. Backupenheter har 100 som default.

MAC-adress: 00:00:5E:00:01:XX

**VRRPv3**
För att stödja IPv6 togs VRRPv3 (RFC 5798) fram. Det är inkompatibelt
med VRRPv2 men har stöd för både IPv4 och IPv6. Det har även stöd för
mer fintrimmade timers. Dessa anges i millisekunder och default hello
interval är 1000ms. Timer learning är också enabled default. Transport
görs med IP protocol 112 och skickas till multicast address 224.0.0.18
och FF02:0:0:0:0:0:0:12. I v2 görs preemption till den med högst
interface IP om två noder har samma prio, så funkar inte v3 utan det är
endast högst prio som ändra rollerna.

Slå på VRRPv3 och Virtual Router Redundancy Service (VRRS) globalt. När
man växlar till VRRPv3 stängs VRRPv2 av.

`fhrp version vrrp v3`

### Konfiguration

Konfiguration görs per interface. VRRP tillåter inte virtual router
group 0 och har därmed aldrig en tom grupp.

`interface gi0`
` vrrp 1 description HA-gateway`
` vrrp 1 priority <1-254>`
` vrrp 1 timers advertise [msec] interval`

Timers måste matcha och man kan låta VRRP-gruppen lära sig advertisement
interval från master virtual router.

` vrrp 1 timers learn`

Preempt delay

`vrrp delay minimum 30`
`vrrp delay reload 60`

Autentisering

`vrrp 1 authentication cisco`

**Verify**

`show vrrp brief`
`show vrrp interface gi0`
`show vrrp all`

GLBP
====

Gateway Load Balancing Protocol är ett Ciscoproperitärt protokoll. Det
togs fram för att kunna ha alla noder aktiva samtidigt. Default
lastdelas det och varje AVF används i round-robin. GLBP Forwarder
preemption är på default med en delay på 30 sekunder. Om en AVF blir
unreachable så kommer AVG att redirecta trafiken genom att besvara
requests för den gamla MAC-adressen med nya AVF:er. Source-IP för
GLBP-paket är interface IP, destination-IP är 224.0.0.102 och transport
är UDP port 3222. Använd GLBP load balancing method host-dependent när
varje host alltid ska använda samma router och använd weighted när man
vill ha unequal load balancing, t.ex. om routrarna har olika
forwarderingskapacitet.

`interface gi2`
` glbp 1 ip 10.0.0.10`
` glbp 1 priority 150`
` glbp 1 preempt`
` glbp 1 weighting 50`
` glbp 1 load-balancing weighted`

**Verify**

`show glbp brief`

**Authentication**
En router ignorerar alla GLBP-meddelanden som har fel autentisering.

Plain-text

`glbp 1 authentication text secret`

MD5

`glbp 1 authentication md5 key-string GLBP-Key`

**Stateful NAT**
Om GLBP används i kombination med
[SNAT](/Cisco_NAT#Stateful_NAT "wikilink") måste load-balancing vara
satt till host-dependent.

[Category:Cisco](/Category:Cisco "wikilink")