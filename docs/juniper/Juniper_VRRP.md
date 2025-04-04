---
title: Juniper VRRP
permalink: /Juniper_VRRP/
---

Virtual Router Redundancy Protocol (RFC 3768) är ett öppet FHRP. Det
fungerar väldigt likt [HSRP](/Cisco_HSRP "wikilink") men med några
skillnader. Source-IP för VRRP-paket är interface IP, destination-IP är
224.0.0.18 och protokoll är 112. Hellos skickas default varje sekund.
Man kan till skillnad från HSRP ha samma virtual ip som interface ip.
Konfigurerar man det ändras VRRP-prio till 255 på den enheten som har
samma IP som VIP. Backupenheter har 100 som default.

En virtual router måste använda följande mac adress 00:00:5E:00:01:XX.
Där XX är Virtual Router IDentifier(VRID), som skiljer sig på alla
virtual routers i nätverket.

Konfiguration
=============

VRRP konfigurerar man på interfacet. Interfacet kan vara en ae, irb
eller fysiskt interface.

Basic
-----

`{master:0}[edit interfaces irb unit 10]`
`root@R1# show`
`family inet {`
`    address 192.168.1.2/24 {`
`        vrrp-group 10 {`
`            virtual-address 192.168.1.1;`
`            priority 250;`
`        }`
`    }`
`}`

Autentisering
-------------

För att säkra upp VRRP kan man använda sig av autentisering. Lösenordet
kommer inte sparas i klartext.

`set interfaces `<interface>` unit `<no>` family inet address `<ip>` vrrp-group `<no>` authentication-type simple`
`set interfaces `<interface>` unit `<no>` family inet address `<ip>` vrrp-group `<no>` authentication-key hackernet`

Verify
------

`show vrrp`
`show vrrp interface `**`interface-name`**

[Category:Juniper](/Category:Juniper "wikilink")