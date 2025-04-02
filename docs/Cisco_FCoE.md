---
title: Cisco FCoE
permalink: /Cisco_FCoE/
---

Fibre Channel over Ethernet är en teknik för att enkapsulera Fibre
Channel frames över lossless Ethernet. FCoE fungerar som vanlig FC men
FC0 och FC1 görs av ethernet istället. Se även [Cisco
FC](/Cisco_FC "wikilink"). Genom att konsolidera nätverk och storage
behövs inte lika mycket kablage i datacentret. Servrar som ska nyttja
FCoE behöver converged network adapters dvs de har fysiska
ethernet-portar men de innehåller funktionsmässigt både HBA och NIC.
FCoE har en dedikerad Ethertype, 0x8906, och fungerar med 802.1Q taggar.
Fibre Channel är ett stängt point-to-point medium medans Ethernet är
öppet multi-access medium. Trots detta kan ethernet (med hjälp av vissa
enhancements) användas för att bära FC. Fibre Channel traffic kräver
lossless transport. FCoE har en egen EtherType (0x8906).

**Termer**
\* End Node (E-Node): de noder som har CNA.

-   FCF: Fibre Channel Forwarder är en switch som förstår både FC och
    FCoE.

**Overview**
[<File:Cisco-FCoE-CNA.png>](/File:Cisco-FCoE-CNA.png "wikilink")

**Data Center Bridging**
Ett DCB-nätverk tillhandahåller I/O consolidation. Det betyder att SAN-
och LAN-trafik går i samma nätverk. DCB kallas även DCE eller CEE.
Switcharna måste supportera CoS-based traffic differentiation. Fibre
Channel är känsligt för packet drops och är beroende av att paketen
kommer fram i samma ordning som de skickades. I ett DCB-nätverk används
virtuella länkar (VLs) för att differentiera trafik-klasser. VLs är en
extension av CoS vilket gör att trafik i en klass inte påverkar trafik i
en annan. Det finns 8 CoS värden. DCBX är på default på Nexus-switchar.

**Priority Flow Control**
PFC (IEEE 802.1bb) är ett subprotokoll till DCB. Det är en mekanism som
förhindrar frame loss pga congestion. Det är likt 802.3x Flow Control
(pause frames) men det jobbar på en per CoS basis. När en buffer
threshold överstigs pga congestion så skickas en pause frame till andra
sidan för att den ska sluta skicka frames med ett visst CoS-värde på den
länken under en viss tid. När sedan trafik går ner under ett visst
gränsvärde så skickas en resume frame för att dra igång dataflödet på
länken igen. PFC kommunicerar genom att skicka frames till well-known
multicast address 01:80:C2:00:00:01.

Det första som händer när länken mellan FCoE-switch och CNA kommer upp
är att DCBX (Data Centre Bridging capabilities eXchange protocol)
berättar för CNA hur den ska vara konfad med avseende på PFC & ETS
(enhanced transmission selection). ETS jobbar med priority groups som
man kan assigna bandbredd till. DCBX transporteras on the wire av LLDP.
När DCBX är klart kan FIP ta vid.

**FCoE Initiation Protocol**
FIP är en väsentlig del i FCoE. Det används för att upptäcka och
initiera FCoE-kapabla enheter som är kopplade till ethernetnätverket.
FIP har hand om vlan och FCF discovery samt FLOGI och Fabric Discovery.
Det är FIP som sätter upp virtuella FC-länkar. På varje FCoE Ethernet
port på FCF skapas en virtuell FC-port (vfc). Varje virtuell FC-länk
identifieras av FCoE VLAN ID samt MAC-adresserna i varje ände på länken.
Under FIP så får alltså CNA reda på vilken mac-adress man ska prata med
på FCF. Det betyder också att varje FC-paket måste vara taggat med det
vlan som vsanet är mappat med, detta vlan kan ej användas till något
annat än FCoE. Notera dock att FIP använder native vlan först men gör en
vlan discovery så man får en lista av FCoE-vlan.

FIP bygger även länkar FCF till FCF för multihop FCoE samt håller koll
på länkar mha periodiska maintenance messages. E-Nodes använder olika
MAC-adresser för FIP och FCoE. FIP sourcas med burned in address medans
FCoE sourcas med den MAC-adress som fabricen tillhandahållit, Fabric
Provided MAC Address. FPMA utgörs av FCoE MAC address prefix (24 bitar)
plus FC_ID (24 bitar). För att rymma den maximala FC-framen är qos
class-fcoe definierad med MTU 2240 bytes. FIP har en dedikerad Ethertype
(0x8914). Protokollet finns i två versioner (CIN-DCBX & CEE-DCBX) och
Nexus har stöd för båda.

### Konfiguration

Nedan följer FCoE-specifik konfiguration, för övrig konfiguration se
[Cisco FC](/Cisco_FC#Konfiguration "wikilink"). Eftersom FCoE och FIP
använder ett taggat FCoE-vlan så måste ethernetport på FCF mot servrar
vara vlan-trunk.

**QoS**
Kontrollera att QoS är konfat med minst en no-drop klass. Default
används CoS 3 för FCoE.

`show policy-map system type network-qos`

**VSAN**
Default mappas vsan till vlan med samma ID.

`vsan database`
` vsan 100`

`vlan 100`
` fcoe vsan 100`

**F-port**

`interface 1/15`
` switchport mode trunk`
` switchport trunk allowed vlan 1,100-105`
` spanning-tree port type edge trunk`

`interface vfc 315`
` bind interface e1/15`
` switchport mode f`

**Verify**

`show flogi database`
`show fcns database`
`show vlan fcoe`
`show fcoe database`
`show topology vsan 100`

**PFC**
interface ethernet 1/15

` priority-flow-control mode auto`

`show interface priority-flow-control`
`show qos dcbxp interface`

auto betyder att no-drop CoS values ska annonseras och förhandlas med
hjälp av DCBXP. En successful negotiation slår på PFC på no-drop CoS.
Medans om det t.ex. är en mismatch i capabilities så kommer inte
förhandlingen att lyckas och PFC förblir avstängt.

**FC-Map**
Man kan identifiera FC-fabricen mha MAC-adresser eftersom detta används
till FPMA. FC-Map är en isoleringsteknik. Frames som inte har detta
prefix discardas, dvs alla switchar i fabrien måste ha samma FC-map.
Default value är 0E.FC.00.

`fcoe fcmap 0xefc10`

**Fabric Priority**
Nexus 5000 annonserar sin prioritet, den används av CNA:er för att
bestämma vilken som är den bästa switchen att ansluta till.

`fcoe fcf-priority 128`

#### Multihop FCoE

Precis som det finns virtuella F-portar finns det även virtuella
E-portar.

`interface vfc 15`
` bind interface ethernet 1/15`
` switchport mode e`
` no shut`

`interface ethernet 1/15`
` switchport mode trunk`
` no shut`

#### Enhanced vPC

Man kan kombinera FCoE med [Enhanced vPC](/Nexus_vPC "wikilink") men man
måste separera A- och B-sidan. Detta kan man göra genom att konfa
FEX:arna att pinna FCoE-trafik till endast den ena parent. Först bygger
man vPC och sedan FCoE på det. FCoE-vlan får ej traversera vPC
peer-linken men detta sköts default. Host facing vfc-interfaces binds
till fysiska ethernetport och inte port-channel interface.

Nexus1

`fex 101`
` fcoe `

`interface vfc 10`
` bind interface ethernet101/1/1`
` no shutdown`

Nexus2

`fex 102`
` fcoe`

`interface vfc 10`
` bind interface ethernet102/1/1`
` no shutdown`

Show

`show fex detail | i FCoE`
`show system internal dcbx info interface ethernet 101/1/1`

#### Nexus 7k

FCoE görs med hjälp av Storage VDC.

`license fcoe module 2`

`system qos`
` service-policy type network-qos default-nq-7e-4q8q-policy`

`vdc SAN type storage`
` allocate interface e2/1-8`
` allocate fcoe-vlan-range 100-101`

iSCSI
-----

iSCSI har egentligen inte mycket med switchar att göra men man bör göra
det lossless.

`class-map type qos match-all class-iscsi`
` match protocol iscsi`
` match cos 6`

`policy-map type qos qos_fcoe_and_iscsi`
` class class-iscsi`
`  set qos-group 2`
` class class-fcoe`
`  set qos-group 1`

`policy-map type network-qos network_fcoe_and_iscsi`
` class type network-qos class-iscsi`
`  mtu 9216`
`  pause no-drop`
` class type network-qos class-fcoe`
`  mtu 2158`
`  pause no-drop`
` class type network-qos class-default`
`  mtu 9216`

`system qos`
` service-policy type queuing input fcoe-default-in-policy`
` service-policy type queuing output fcoe-default-out-policy`
` service-policy type qos input qos_fcoe_and_iscsi`
` service-policy type network-qos network_fcoe_and_iscsi`

[Category:Cisco](/Category:Cisco "wikilink")