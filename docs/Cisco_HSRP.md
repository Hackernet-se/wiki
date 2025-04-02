---
title: Cisco HSRP
permalink: /Cisco_HSRP/
---

Hot Standby Router Protocol (RFC 2281) är ett standardiserat men
Ciscolicensierat FHRP. HSRP låter två routrar dela på en virtuell IP och
MAC-adress så att andra system kan använda samma IP/MAC och skicka paket
till fast adressen kan vara aktiv på olika enheter. Tanken är att de
inte ens märker när ena routern går ner. Den virtuella IPn måste vara i
samma subnät som interface-IPn. Endast en router är aktiv i taget medans
standby-routern lyssnar efter Hellos som default skickas var 3:e sekund
från den aktiva. Uteblir dessa tar standby-enheten över och blir aktiv.
Den router med högst prioritet blir aktiv, 100 är default för IOS, och
vid lika avgör högsta interface IP-adress. Preempt är inte påslaget
default. Autentisering går att göra med clear-text eller MD5.

HSRP går att använda tillsammans med [NAT](/Cisco_NAT#HSRP "wikilink").
Se även [FHRP](/Cisco_FHRP "wikilink").

### Version

HSRP finns i två versioner som använder olika paketformat. Version 2
använder TLVer och är inte kompatibel med version 1. I version 1 (som är
default) kan man ha standby-grupp 0-255 medans i v2 är detta utökat till
0-4095. Version 2 skickar med en 6-byte identifier field som innehåller
MAC-adressen på avsändaren så man vet vem som är originator. Det skickas
även med timer values i millisekundformat så andra sidan kan synka med.
HSRP version 2 har stöd för IPv6.

| HSRP version | Protocol | Group address           | UDP Port          | Virtual MAC address range |
|--------------|----------|-------------------------|-------------------|---------------------------|
| 1            | IPv4     | 224.0.0.2 (all routers) | 1985              | 00:00:0c:07:ac:XX         |
| 2            | IPv4     | 224.0.0.102 (HSRP)      | 1985              | 00:00:0c:9f:fX:XX         |
| IPv6         | ff02::66 | 2029                    | 00:05:73:a0:0X:XX |                           |

### States

-   Initial: HSRP körs inte.
-   Learn: Routern känner inte till VIP utan väntar på att den aktiva
    enheten ska prata.
-   Listen: Routern känner till VIP men är varken active eller standby.
-   Speak: Routern skickar HSRP hellos och är med i valet för active.
-   Standby: Routern håller koll på hellos från active och är beredd att
    ta över.
-   Active: Routern forwarderar paket som virtuell router.

Packets
-------

**Version 1**

<div class="mw-collapsible mw-collapsed" style="width:250px">

-   Advertise:

<div class="mw-collapsible-content">

[<File:Cisco_HSRP_Advertise.png>‎](/File:Cisco_HSRP_Advertise.png‎ "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:250px">

-   Hello Speak:

<div class="mw-collapsible-content">

[<File:Cisco_HSRP_Speak.png>‎](/File:Cisco_HSRP_Speak.png‎ "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:250px">

-   Hello Standby:

<div class="mw-collapsible-content">

[<File:Cisco_HSRP_Standby.png>‎](/File:Cisco_HSRP_Standby.png‎ "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:250px">

-   Hello Active:

<div class="mw-collapsible-content">

[<File:Cisco_HSRP_Active.png>‎](/File:Cisco_HSRP_Active.png‎ "wikilink")

</div>
</div>

**Version 2**

<div class="mw-collapsible mw-collapsed" style="width:250px">

-   Advertise:

<div class="mw-collapsible-content">

[<File:Cisco_HSRP_v2_Advertise.png>‎](/File:Cisco_HSRP_v2_Advertise.png‎ "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:250px">

-   Hello Speak:

<div class="mw-collapsible-content">

[<File:Cisco_HSRP_v2_Speak.png>‎](/File:Cisco_HSRP_v2_Speak.png‎ "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:250px">

-   Hello Standby:

<div class="mw-collapsible-content">

[<File:Cisco_HSRP_v2_Standby.png>‎](/File:Cisco_HSRP_v2_Standby.png‎ "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:250px">

-   Hello Active:

<div class="mw-collapsible-content">

[<File:Cisco_HSRP_v2_Active.png>‎](/File:Cisco_HSRP_v2_Active.png‎ "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:830px">

För att ta över active-rollen skickas ett Coup message, detta används
vid preemption.

<div class="mw-collapsible-content">

[<File:Cisco_HSRP_v2_Coup.png>‎](/File:Cisco_HSRP_v2_Coup.png‎ "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:830px">

När ett interface shutas på active device skickas det ut ett Resign
message så att standby kan bli active direkt.

<div class="mw-collapsible-content">

[<File:Cisco_HSRP_v2_Resign.png>‎](/File:Cisco_HSRP_v2_Resign.png‎ "wikilink")

</div>
</div>

Konfiguration
=============

`interface [interface]`
` standby version 2`
` standby 1 ip [virtual ip]`
` standby 1 priority <0-255>`
` standby 1 preempt`
` standby 1 timers [hold] [dead]`

**Verify**

`show standby brief`
`show standby`

Initialisation delay. Man kan konfigurera en delay för när HSRP ska
aktiveras efter omboot och interface link up.

` standby delay minimum 30`
` standby delay reload 60`

`show standby delay`

Använd burned in MAC address

`standby use-bia`

Configure sending of ICMP Redirect messages with an HSRP virtual IP
address as the gateway IP address

`standby redirects enable`

`show standby redirect`

Man kan slå på att HSRP ska skicka en gratuitous ARP från aktiva
grupper. Default skickas det en när en grupp blir aktiv, en 2 sekunder
senare och sedan en ytterligare 2 sekunder senare.

`standby arp gratuitous`

Autentisering
-------------

HSRP måste ha en authentication-sträng som skickas i paketen och default
så ligger "cisco" (*standby X authentication cisco*), dvs cisco i
klartext används men det syns inte i konfigen.

Plain text

`standby 1 authentication text SECRET`

MD5

`standby 1 authentication md5 key-string SECRET`
`standby 1 authentication md5 key-chain HSRP-CHAIN`

Tracking
--------

HSRP kan hålla koll på interface för att veta vilken enhet som bör vara
aktiv. Man kan automatiskt sänka HSRP priority när line protocol på
utvalt interface blir down, default decrement är 10.

`standby 1 track Gi0/0 30`
`show standby | i Track`

**IP SLA**
Allt som går att tracka med [IP SLA](/Cisco_Routing#IP_SLA "wikilink")
kan HSRP använda sig av. Man kan även ha flera objekt som man trackar
och med decrement valus styra att flera saker måste vara nere för att
aktiv enhet ska bytas.

`track 100 interface gi0/1 line-protocol`
`standby 1 track 100 decrement 30`

Secondary VIP
-------------

Man kan ha secondary virtual IP address med HSRP. Denna VIP eller info
om den skickas inte i något HSRP-paket, dvs det hålls ingen egen state
för det utan det följer helt enkelt rollen som HSRP-gruppen har.

`interface gi2`
` standby 1 ip 10.0.0.1 secondary`

BFD
---

HSRP [BFD](/Cisco_BFD "wikilink")

Global

`standby bfd all-interfaces`

Per interface

`interface gi2`
` standby bfd`

MHSRP
-----

Multiple HSRP. Man kan ha flera HSRP-grupper på samma interface vilket
möjliggör en variant av lastdelning. För att MHSRP ska kunna lastdela
kan inte alla hostar i subnätet ha samma default gateway utan några
måste använda den ena virtuella IPn och några mot en för en annan
HSRP-grupp, dock fortfarande i samma subnät. På Nexus-plattformen går
det att lösa så att alla enheter är aktiva för samma VIP, se [Anycast
HSRP](/Nexus_FabricPath#Anycast_HSRP "wikilink").

NX-OS
-----

Switch 1

`feature hsrp`

`interface e1/1`
` ip 10.0.0.2/24`
` hsrp bfd`
` hsrp version 2`
` hsrp 1`
`  ip 10.0.0.1`
`  follow master1`

Switch 2

`feature hsrp`

`interface e1/1`
` ip 10.0.0.3/24`
` hsrp bfd`
` hsrp version 2`
` hsrp 1`
`  ip 10.0.0.1`
`  priority 110`
`  name master1`

Det är rekommenderat att köra BFD istället för att ändra HSRP-timers.

För att stödja HSRP under ISSU (In-Service Software Upgrades) så kan man
aktivera förlängda kontrollmeddelanden för HSRP.

`hsrp timers extended-hold`

Man kan låta HSRP lära sig VIP av andra HSRP-noder.

`interface vlan 10`
` hsrp 10`
`  ip`

Med IPv6 kan man auto-konfigurera VIP, då görs EUI-64 på HSRP-gruppens
MAC-adress.

`interface vlan 10`
` hsrp 10 ipv6`
`  ip autoconfig`

[Category:Cisco](/Category:Cisco "wikilink")