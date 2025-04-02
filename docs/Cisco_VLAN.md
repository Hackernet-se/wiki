---
title: Cisco VLAN
permalink: /Cisco_VLAN/
---

Virtual LAN är alla broadcastdomäner som är partitionerade och isolerade
på lager 2 i ett nätverk. Vill man managera VLAN på många Cisco-switchar
centralt kan man använda [VTP](/Cisco_VTP "wikilink"). Det kan maximalt
finnas 4094 VLAN, för att skala förbi det se [Cisco
VXLAN](/Cisco_VXLAN "wikilink").

**Standard:** 1-1005 (1002-1005 är reserverade)

**Extended:** 1006-4094

VLAN
----

Stäng ett VLAN lokalt i switchen och suspenda det i VTP.

`vlan 20`
` shutdown`
` state suspend`

Show

`show vlan brief`
`show vlan internal usage`

**Layer 2 Traceroute**
Man kan tracea mac-adresser i ett vlan. OBS
[CDP](/Cisco_IOS#CDP "wikilink") är ett prereq för detta annars blir det
*Unable to send a l2trace request*. Max hops är 10.

`traceroute mac 0050.5600.0001 0000.aabb.ccdd vlan 20`

Det går även att ta reda på vilken väg en frame tar utifrån IP-adresser.
ARP används för IP-to-MAC resolution och båda adresserna måste finnas i
samma subnät.

**Voice**

`interface GigabitEthernet0/1`
` switchport mode access`
` switchport access vlan 20`
` switchport voice vlan 30`

Alternativt konfigurera en trunk som tillåter voice-vlanet. Så fort man
använder kommandot *switchport voice vlan* enableas portfast.

**Database mode**
Är gammalt och stöds inte längre på alla switchar.

`vlan database`
` vlan 20 name Old-school`
`apply`

Trunking
========

IEEE 802.1q är standarden för att supportera VLAN över ethernet.

Vitlista VLAN

`switchport trunk allowed vlan 1-5,8`
`show interface trunk`

Se till att native VLAN matchar på trunkar, både CDP och DTP kan
upptäcka mismatch.

`switchport trunk native vlan 20`

Man kan tagga alla frames på en trunk.

`vlan dot1q tag native`
`show vlan dot1q tag native`

DTP
---

Dynamic Trunking Protocol är ett Cisco-properitärt protokoll som används
av switchar för att förhandla med andra sidan om ett interface ska vara
trunk eller ej samt ISL eller 802.1q. DTP advertisements skickas med
destination mac 01:00:0C:CC:CC:CC var 30:e sekund och innehåller VTP
domain name så det måste matcha för att DTP ska kunna förhandla upp
trunk (ena sidan kan ha vtp domain NULL så funkar det också). DTP är
påslaget default och skickas både som vanlig ethernet men också
ISL-enkapsulerat. DTP är inte supporterat på någon Nexus-plattform.

<div class="mw-collapsible mw-collapsed" style="width:250px">

DTP frame:

<div class="mw-collapsible-content">

[<File:Cisco_DTP.png>](/File:Cisco_DTP.png "wikilink")

</div>
</div>

`show dtp`

Port Modes, vissa switchmodeller har desirable som default (3560) och
vissa har auto (2960)

-   **dynamic desirable:** switchen kommer aktivt att försöka förhandla
    trunk genom att generera DTP frames.
-   **dynamic auto:** switchen lyssnar och accepterar DTP frames men
    skickar inga själv.

Stänga av DTP. OBS porten måste vara konfad som något för att kunna
använda nonegotiate, annars blir det *Conflict between 'nonegotiate' and
'dynamic' status.*

`switchport mode trunk / access`
`switchport nonegotiate`

Verify

`show dtp interface`
`show interfaces switchport | i Name|Negotiation`

Private VLAN
============

Vanligtvis kan allt i ett VLAN nå övrigt i samma VLAN obehindrat men det
kan finnas situationer när man vill begränsa konnektivitet inom en
broadcastdomän. För att lösa det togs protected ports fram, det konfas
per interface med *switchport protected*. Om en port var protected kunde
den endast nå portar som inte var protected i det VLANet, dvs två
protected portar kan aldrig prata med varandra. Detta funkade lokalt
inom switchen men ej mellan switchar och var därför inte så praktiskt i
miljöer med fler än en switch. För att lösa det implementerades Private
VLAN (RFC 5517). Detta används vanligtvis hos service providers som vill
segmentera kunder från varandra men bara använda ett IP-nät. PVLAN är en
mekanism som delar upp ett VLAN (primary) i secondary VLANs. Secondary
VLAN finns i två varianter, isolated och community. Secondary VLAN måste
tillhöra exakt ett primary VLAN. Det kan finnas flera community men
isolated får det bara finnas ett av per primary.

Inom en PVLAN-domän finns det tre separata porttyper. Varje porttyp har
sin egen unika uppsättning regler som reglerar en ansluten enhets
förmåga att kommunicera med andra anslutna enheter inom samma private
VLAN.
\* **Isolated port:** En isolated port kan inte prata med någon annan
port i private VLAN-domänen med undantag för promiscuous ports.

-   **Community port:** En community port är en del av en grupp med
    portar. Portar i en community kan ha L2 kommunikation med varandra
    och kan även prata med en promiscuous port.

<!-- -->

-   **Promiscuous port:** En promiscuous port kan prata med alla andra
    typer av portar och tillhör primary VLANet.

Private VLAN fungerar över trunklänkar och därmed mellan switchar.
Kommer en frame från ett secondary VLAN och ska skickas över en
trunklänk så taggas den med sitt VLAN ID. Kommer det en frame på en
promiscuous port så taggas den med primary VLAN. Dvs om en frame ska
från en isolated port på en switch till en promiscuous port på en annan
och sedan tillbaka kommer den ha olika VLAN-taggar på dit och
tillbakavägen, såkallad assymetrisk VLAN-taggning. Det sker aldrig någon
dubbeltaggning men switcharna måste ändå ha stöd för private VLAN och
vara konfade likadant (PVLAN-mässigt) annars vet inte switcharna hur
VLANen är associerade med varandra.

Det finns undantag till detta beteende t.ex. om man har en
router-on-stick så vet inte den vad PVLAN är. Då kan man använda
*promiscuous PVLAN trunk* och på den skickas det aldrig ut något som är
taggat med ett secondary VLAN utan allt skrivs om till primary VLAN ID.
Det finns även *isolated PVLAN trunk*, det fungerar tvärtom, då skickas
det alltid ut taggat som ett secondary vlan. Det är användbart om man
ska koppla ihop PVLAN med en switch som inte har stöd för det utan
endast kan köra protected ports.

Det är möjligt för två isolerade hostar att kommunicera om **ip
local-proxy-arp** är konfigurerat på gateway. Det fungerar som proxy ARP
fast inom subnätet. Funktionerna DHCP Snooping, ARP Inspection och
Source Guard på primary VLANet enablear det även på secondary VLANs.

### Konfiguration

`vtp mode transparent`

Alternativt kan [VTP](/Cisco_VTP "wikilink") version 3 användas.

VLAN

`vlan 101`
` private-vlan isolated`
`vlan 102`
` private-vlan community`
`vlan 100`
` private-vlan primary`
` private-vlan assoc 101,102`

Access Ports

`interface g0/1`
` description Gateway`
` switchport mode private-vlan promiscuous`
` switchport private-vlan mapping 100 101-102`

`interface g0/2`
` description Isolated`
` switchport mode private-vlan host`
` switchport private-vlan host-association 100 101`

`interface g0/3`
` description Community`
` switchport mode private-vlan host`
` switchport private-vlan host-association 100 102`

Other switch

`interface g0/4`
` switchport mode trunk`

Promiscuous PVLAN Trunk Port

`interface g0/5`
` switchport private-vlan trunk allowed vlan 100-103`
` switchport private-vlan mapping trunk 103 130-135`
` switchport mode private-vlan trunk promiscuous`

Notera att primary vlan ska vara med i allowed vlan list. Om man har
t.ex. en [ASA](/Cisco_ASA "wikilink") kan man köra med en vanlig
switchport mode trunk om man vill för ASA har native stöd för PVLAN.

SVI

`interface Vlan100`
` ip address 10.0.0.1 255.255.255.0`
` private-vlan mapping 101,102`

Verify

`show vlan private-vlan`
`show interfaces vlan100 private-vlan mapping`
`ping 255.255.255.255`

Q-in-Q
======

Med IEEE 802.1Q tunneling kan man bygga en simpel L2 VPN genom att
dubbeltagga Ethernet-frames.

prereq

`system mtu 1504`
`reload`
`show system mtu`

Port

`switchport mode dot1q-tunnel`
`l2protocol-tunnel cdp`

Verify

`show dot1q-tunnel`

Dubbeltaggning på router

`int gi2`
` mtu 1504`
`int gi2.10`
` encapsulation dot1q 10 second-dot1q 100,101`

Bridging
========

Med bridging kan man ändra en routers beteende att bli mer likt hur en
switch fungerar. För IOS-XE se längre ner.

**Transparent**
Routern blir precis som en L2-switch, dvs ingen IP routing och
[STP](/Cisco_STP "wikilink") används för loop prevention.

`no ip routing`
`bridge 1 protocol vlan-bridge`

`interface gi0`
` bridge-group 1`
`interface gi1`
` bridge-group 1`

Verify

`show bridge`

**CRB**
Transparent bridging har en stor nackdel, en router kan inte både routa
paket och brygga interface, därför finns Concurrent Routing and Bridging
som tillåter både routing och bridging samtidigt. Dock inte på samma
interface-grupper.

`bridge crb`
`ip routing`

`bridge 1 protocol vlan-bridge`

`interface gi0`
` bridge-group 1`
`interface gi1`
` bridge-group 1`

Verify

`show bridge`

**IRB**
En nackdel med CRB är att det inte går att koppla ihop en routed domain
med en bridged domain inom samma enhet, därför finns Integrated Routing
and Bridging. Då skapas Bridge Group Virtual Interface (BVI) som
fungerar som SVI på L3-switchar.

Prereqs & Configuration

`bridge irb`
`ip routing`

`bridge 1 route ip `
`bridge 1 protocol vlan-bridge`

`interface gi0`
` bridge-group 1`
`interface gi1`
` bridge-group 1`
`interface bvi1`
` ip address 10.0.0.10 255.255.255.0`

Verify

`show bridge`

**Fallback Bridging**
Fallback Bridging används för att brygga icke-routebara protokoll mellan
SVIer och routade interface. Ett protokoll kan routas medans det andra
bryggas, t.ex. IPv4 kan routas medans IPv6 bryggas.

`bridge 1 protocol vlan-bridge`

`interface Gi0/2`
` no switchport`
` ip address 10.0.2.10 255.255.255.0`
` bridge-group 1`

`interface Vlan10`
` ip address 10.0.10.10 255.255.255.0`
` bridge-group 1`

**IOS-XE**
På IOS-XE görs bridging med bridge domains och Ethernet flow points
(EFP).

`interface gi0/0/1`
` service instance 1 ethernet`
`  encapsulation untagged`
`  bridge-domain 1`

`interface gi0/0/2`
` service instance 1 ethernet`
`  encapsulation untagged`
`  bridge-domain 1`
`  l2protocol peer stp`
`  mac limit maximum addresses 50`

`interface bdi1`
` ip address 10.0.0.10 255.255.255.0`

Verify

`show bridge-domain`

[Category:Cisco](/Category:Cisco "wikilink")