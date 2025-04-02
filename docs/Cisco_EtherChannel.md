---
title: Cisco EtherChannel
permalink: /Cisco_EtherChannel/
---

EtherChannel bundlar individuella Ethernet-länkar till en logisk länk.
Linkaggregering motverkar två problem som medföljer en ensam kabel,
bandbreddsbegränsning och brist på feltolerans. EtherChannel
tillhandahåller lastdelning per frame och adderar bandbredd för de
aktiva interfacen, t.ex. med tre aktiva 100 mbps members blir
interface-bandbredden 300 mbps. För [STP](/Cisco_STP "wikilink") är en
etherchannel en länk och BPDUer skickas på en av member ports. För en
etherchannel måste alla interface ha samma speed, duplex och STP port
cost. Är det en VLAN-trunk måste också native och allowed
[VLAN](/Cisco_VLAN "wikilink") vara samma. För access port-channel måste
access-vlan vara samma.

Se även [vPC](/Nexus_vPC "wikilink")

Konfiguration
-------------

Static

`interface range gi0/1 - 2`
` channel-group 1 mode on`
`interface port-channel 1`
` switchport mode trunk`

Verify

`show etherchannel summary`

### L3

Det är viktigt att man konfigurerar L3 etherchannel i rätt ordning. När
*channel-group*-kommandot exekveras tas attributen från member
interfacen till port-channel-interfacet. Det betyder att *no switchport*
måste slås först annars blir port-channel-interfacet en switchport och
detta går inte ändra i efterhand.

`interface range gi0/1 - 2`
` `**`no`` ``switchport`**
` channel-group 1 mode [mode]`
`interface port-channel 1`
` `**`no`` ``switchport`**
` ip address [ip address] [subnet mask]`

### Load-balancing

Global inställning. EtherChannel tillhandahåller lastdelning per frame.

`port-channel load-balance [method]`
`show etherchannel load-balance`

Kolla vilket interface en viss frame skickas på.

`test etherchannel load-balance interface port-channel 1 ip `<Source-IP>` `<Destination-IP>
*`Would`` ``select`` ``Gi1/0/4`` ``of`` ``Po1`*

### Misconfiguration Guard

Misconfiguration guard är en feldetekteringsmekanism som jobbar lokalt
per switch. Duplex och speed måste överensstämma på alla portar samt att
alla BPDUer som kommer in har samma source MAC-adress. Detta är en
global inställning som automatically error-disables alla portar som är
felkopplade.

`spanning-tree etherchannel guard misconfig`
`show spanning-tree summary | i EtherChannel`

LACP
----

Link Aggregation Control Protocol (802.3ad) är ett IEEE
kontrollprotokoll för etherchannels. En EtherChannel bildas endast om
man lyckas förhandla med andra sidan. Fördeler med en mekanism som
håller koll på länkarna är att failover görs automatiskt och
kabel/konfigurationsmisstag löper mindre risk att ställa till oönskat
beteende i nätverket. Destination mac adress för LACP-frames är
01:80:c2:00:00:02. När LACP ska upptäcka andra sidan initialt skickas
LACPDU varje sekund. Sedan ändras det beroende på keepalive mode, slow
(30 sek interval) är default. Att ändra görs per interface, **lacp rate
fast**, men alla switchmodeller stödjer inte fast rate (1 sek interval).

<div class="mw-collapsible mw-collapsed" style="width:310px">

LACPDU

<div class="mw-collapsible-content">

[<File:Cisco_LACP.png>](/File:Cisco_LACP.png "wikilink")

</div>
</div>

### Konfiguration

För att initiera LACP används nyckelordet active. Det finns också
passive mode = speak when spoken to.

`interface range gi0/1 - 2`
` channel-group 1 mode active`

Enable LACP auto on interface.

` channel-group auto`

Maximalt kan 16 interface konfigureras i en EtherChannel men endast 8
kan vara aktiva samtidigt. Vilka länkar som ska vara aktiva bestäms av
den switch med lägst LACP ID som utgörs av MAC-adress och prioritet. Den
använder de portar med lägst prio i första hand, detta är lokala värden.

`lacp system-mac 0011.2233.4455`
`lacp system-priority 32768`

`interface gi0/2`
` lacp port-priority 0`

Verify

`show etherchannel protocol`
`show lacp ?`
`show lacp neighbor`

#### PAgP

Port Aggregation Protocol är ett Ciscoproperitärt protokoll för samma
funktionalitet som LACP. Det använder destination mac 01:00:0C:CC:CC:CC.
Kommandot per interface är istället: **channel-group 1 mode
auto/desirable**

Link State Tracking
-------------------

Man kan konfigurera portar mot servrar att disablas om uplink går ner.
Detta är användbart om man har multihomed servers för då märker de att
de ska sluta använda sitt primära NIC.

`link state track 1`

`int range gi0/1 - 2`
` switchport trunk encapsulation dot1q`
` switchport mode trunk`
` channel-group 1 mode active`
` link state group 1 upstream`

`int po1`
` description Uplink`
` switchport trunk encapsulation dot1q`
` switchport mode trunk`
` link state group 1 upstream`

`int gi0/10`
` description Server`
` switchport mode access`
` switchport access vlan 10`
` link state group 1 downstream`

Verify

`show link state group detail`

Flex Links
----------

Tekniskt sett inte etherchannel men kan användas istället för det i
vissa situationer. Det som händer när primären går ner är att alla
dynamiska MAC entries flyttas till backupinterfacet och det hamnar i
forwarding state. Inga BPDUer inblandade. Bör användas tillsammans med
[UDLD](/Cisco_UDLD "wikilink").

`interface po2`
` switchport backup int gi0/5`
` switchport backup int gi0/5 preemption mode forced`
` switchport backup int gi0/5 preemption delay 10`

Verify

`show interface po2 switchport backup`

Antingen står det Backup Standby eller Backup Up beroende på status på
port-channeln.

[Category:Cisco](/Category:Cisco "wikilink")