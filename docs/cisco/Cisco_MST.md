---
title: Cisco MST
permalink: /Cisco_MST/
---

Multiple Spanning Tree Protocol, IEEE 802.1s, använder algoritm Rapid ST
och konvergerar snabbt. Man kan konfigurera så många topologier som man
vill ha. Alla VLAN som inte specificeras i någon instans hamnar i
instans 0 som default. Pathcost method behöver inte konfigureras utan
operational value är alltid long till skillnad från andra STP-varianter.
Se [Cisco STP](/Cisco_STP "wikilink"). MST-konfiguration går även att
distribuera med hjälp av [VTPv3](/Cisco_VTP#VTPv3 "wikilink").

### MST BPDU

MST använder en BPDU för att skicka information om alla instanser.

<div class="mw-collapsible mw-collapsed" style="width:190px">

Exempel

<div class="mw-collapsible-content">

[<File:Cisco_MST_BPDU.png>](/File:Cisco_MST_BPDU.png "wikilink")

</div>
</div>

**Topology change**
Den enda gång en topologiändring anses hända är när en non-edge port går
från non-forwarding till forwarding. Den nya portan kan ha en bättre väg
för MAC-adresserna och CAM-tabellen måste uppdateras. Går en port från
forwarding till non-forwarding spelar det ingen roll för då är de
MAC-adresserna unreachable, dyker de upp någon annanstans är det för att
någon annan port har gått från non-forwarding till forwarding och då är
det en topologiändring iallafall. Med MST floodas BPDUer med TC-biten
satt till alla non-edge designated ports och root port förutom porten
där ändringen kom in på. Även så flushas alla MAC-adresser på den
porten. För att MST ska kunna tillhandahålla snabb konvergens måste alla
inter-switchlänkar måste vara p2p och alla portar mot end systems måste
vara edge ports annars kommer prestandan att degraderas.

Region Interoperability
-----------------------

MST instance 0 kallas Internal Spanning Tree (IST) och det är den som
används för att interagera med andra MST-regioner och STP-protokoll. Det
gör att MST-regionen ser ut som en enda stor switch för utsidan.
STP-domäner kan kopplas ihop på flera ställen vilket kan leda till
loopar därför skapar MST en Common Spanning Tree (CST) som innehåller
alla inter region links. Andra STP-protokoll vet ej att de deltar i en
CST. Detta kan sedan kopplas ihop med varje IST för att skapa Common and
Internal Spanning Tree (CIST) som omfattar hela topologin som därmed
hållas loopfri. Eftersom varje region har en egen rotbrygga kan det
finnas flera CIST Regional Root Switches men det kan endast finnas en
CIST Root. Den med bäst Bridge ID av alla switchar i alla regioner blir
CIST. Alla andra regionala root väljs utifrån lägst cost till CIST och
inte BID.

[650px](/File:Cisco_MST_Regions.jpg "wikilink")

Konfiguration
=============

Följande element måste vara identiska på alla switchar inom samma MST
region:

-   region name
-   revision number
-   instances

`spanning-tree extend system-id`
`spanning-tree mode mst`
`spanning-tree mst configuration`
` name Site1`
` revision 1`
` instance 1 vlan 1-2000`
` instance 2 vlan 2001-4094`
` show current`

Root, priority 0 är det absolut lägsta medans root primary sätter prio
till 24k förutsatt att det ger root-rollen, detta ändras inte dynamiskt.

`spanning-tree mst 1 root primary`
`spanning-tree mst 2 priority 0`
`spanning-tree mst 0 root primary diameter 7 hello-time 2`

Port Cost & Priority

`interface Gi0/1`
` spanning-tree mst 1 cost 50`
` spanning-tree mst 1 port-priority 128`

**Verify**

`show spanning-tree mst`
`show spanning-tree mst interface`

`spanning-tree logging `
`test spanning-tree diameter 3`
`test spanning-tree get configuration mst`

Mappa alla secondary vlan till samma MST-instans som deras primary VLAN
befinner sig i, se även [Private
VLAN](/Cisco_VLAN#Private_VLAN "wikilink").

`spanning-tree mst configuration`
` private-vlan synchronize`

MST började implementeras av tillverkarna innan standarden var helt
spikad vilket man bör tänka på om man kör gamla enheter. Dock säger
standarden att pre-standard MST-grannar måste kunna upptäckas
automatiskt av kompabilitetsskäl. I normalfallet märker man ingenting
men om grannen är tyst, t.ex. en root port, kan man slå på det per
interface.

`interface gi0/7`
` spanning-tree mst pre-standard`

`show spanning-tree mst configuration digest`

Nexus
-----

Grundkonf för [NX-OS](/Cisco_Nexus "wikilink").

`spanning-tree mode mst`
`spanning-tree mst configuration`
` name DC1`
` revision 1`
` exit`

`spanning-tree mst 0 priority 32768`
`spanning-tree pathcost method long`
`spanning-tree port type edge default`
`spanning-tree port type edge bpduguard default`
`spanning-tree port type edge bpdufilter default`
`spanning-tree loopguard default`

Extensions
==========

Det finns många tillägg till spanning-tree som kan öka stabilitet och
säkerhet. Dessa agerar fristående från varandra förutom att de går att
konfigurera ihop. Detta är tillägg för protokoll som kör Rapid ST.

`show spanning-tree summary`

### PortFast

När en vanlig port aktiveras så initierar RSTP sin synk-process för
snabb konvergens. Om andra sidan t.ex. är en server så kommer den inte
att köra STP och inget sync response kommer att skickas tillbaka. Detta
gör att RSTP måste falla tillbaka till legacy STP-regler och vänta på
att forward delay ska gå ut innan länken blir i forwarding state. Med
PortFast definierar man edge ports, dessa går direkt till forwarding när
de kommer upp och inget topology change event genereras. En edge port
skickar ut BDPUer men förväntar sig inga tillbaks. Om det kommer in en
BPDU slutar porten vara edge port och återgår till normal tills
interfacet går down/up. Används för anslutningar ut till servrar och
andra end hosts. Ibland är PortFast ett måste pga att
[DHCP](/Cisco_DHCP "wikilink") hinner timea ut innan porten blivit
forwarding.

Globalt, aktiveras på alla portar i operational state: access

`spanning-tree portfast default`

Per interface, on/off

`spanning-tree portfast`
`spanning-tree portfast disable`

Verify

`show spanning-tree interface gi0/10 portfast`

Vill man ha portfast på en trunk måste man ställa det per interface

`spanning-tree portfast trunk`

Kör aldrig portfast mot andra switchar! MST och RSTP har tekniker för
att vara snabba ändå.

### BPDU Guard

BPDU Guard är en säkerhetsmekanism som sätter interface i error disable
om det kommer en BPDU. *%PM-4-ERR_DISABLE: bpduguard error detected on
Po2, putting Gi0/8 in err-disable state*

Globalt, skyddar alla PortFast-portar

`spanning-tree bpduguard default`

Per interface, on/off

`spanning-tree bpduguard enable`
`spanning-tree bpduguard disable`

Auto recovery

`errdisable recovery cause bpduguard `

### Root Guard

Skydda så att ingen annan än den enhet man själv har konfigurerat kan
bli root genom att ignorera superior BPDUer som kommer in på portar med
Root Guard påslaget. Om det kommer in en superior BPDU så hamnar porten
i root-inconsistent blocking state och frames varken forwardas eller tas
emot. Porten går automatiskt tillbaka när dessa BPDUer slutar att komma
in. *%SPANTREE-2-ROOTGUARD_BLOCK: Root guard blocking port
GigabitEthernet0/8 on VLAN0002.*

Per interface

`spanning-tree guard root`

### BPDU Filter

En edge port skickar BPDUer som vanligt enligt Hello-interval men om det
inte finns något som talar STP på andra sidan är detta onödigt. Med BPDU
filter påslaget slutar switchen att skicka BPDUer efter 10 obesvarade
(det skickas även en BDPU direkt vid link up så 11 totalt). Porten är
dock beredd på att behandla BPDUer och BDPU-filter inaktiveras ifall det
kommer in en BPDU vilket gör att detta är ett någorlunda mindre osäkert
sätt att terminera sin STP-domän på.

Globalt, gäller alla PortFast-portar

`spanning-tree portfast bpdufilter default`

Man kan också hårdställa BPDU-filter per interface om man t.ex. ska
splita ett nätverk i olika STP-domäner. Inga BPDUer kommer att skickas
eller behandlas.

Per interface, hard on/off

`spanning-tree bpdufilter enable`
`spanning-tree bpdufilter disable`

### Loop Guard

Unidirectional links kan ställa till det för en L2-domän. Med Loop Guard
stoppar man den vanliga STP-konvergeringen för root och alternate
portar. Eftersom det ska komma in BPDUer på vissa portar är det inte
normalt att det plötsligt inte gör det längre utan att länken har gått
ner. Loop Guard förhindrar dessa portar från att bli designated utan de
hamnar istället i loop-inconsistent blocking state. När det kommer
BPDUer igen återgår portarna till normalt tillstånd. Loop Guard fungerar
endast på point-to-point länkar. *%SPANTREE-2-LOOPGUARD_BLOCK: Loop
guard blocking port GigabitEthernet0/8 on VLAN0002.*

Globalt, skyddar alla root- och alternate-portar

`spanning-tree loopguard default`

Per interface

`spanning-tree guard loop`

### Bridge Assurance

Bridge Assurance är en utökning till Loop Guard och det fungerar med
RSTP och MST. Slår man på det så skickar båda sidor alltid BPDUer
oavsett port state och BPDUerna används som en Hello-mekanism för att se
om grannen lever. BPDU agerar alltså keepalive message och skickas
per-vlan eller per-instans beroende på STP mode. Kommer det inte in
någon BPDU hamnar porten i BA-inconsistent blocking state tills BPDU
åter mottages. Båda sidor av länken måste alltså slå igång Bridge
Assurance. Detta skyddar mot unidirectional links eftersom de error
disableas men även vid loopar orsakade av switchar som slutat prata STP
men ändå forwarderar frames. BA prunear också onödiga VLAN på
trunklänkar. Detta är en [Nexus](/Cisco_Nexus "wikilink")-feature men
finns även i nyare versioner av IOS.

Global

`spanning-tree bridge assurance`

Per interface

`spanning-tree portfast network `

### PVST Simulation

MST kan samköras med Rapid PVST+ utan någon speciell konfiguration.
Detta är en feature på [Nexus](/Cisco_Nexus "wikilink")-switchar och
nyare IOS och det slåss på när man konfigurerar MST. Man kan stänga av
PVST simulation globalt eller per port, det som händer då är att en port
som får in en Rapid PVST+ BPDU hamnar i blocking state tills det slutar
komma BPDUer. Rotbryggan för alla VLAN måste finnas på samma sida,
antingen i MST eller i PVST+. Om man inte uppfyller detta kommer porten
att hamna i PVST simulation-inconsistent state dvs forwarding stängs av.

`interface Gi0/2`
` spanning-tree mst simulate pvst`

### Others

Dispute mechanism innebär att role och state hos porten som skickar en
BPDU skickas med i BPDUn så andra sidan vet att den inte pratat med en
designated port på en designated port. Då hamnar porten i discarding
state. Detta är påslaget default och behöver inte konfigureras. Fungerar
dock inte med de äldsta varianterna av STP.

**UDLD**
Se [Cisco UDLD](/Cisco_UDLD "wikilink")

[Category:Cisco](/Category:Cisco "wikilink")