---
title: Cisco STP
permalink: /Cisco_STP/
---

Spanning Tree Protocol blockar portar på switchar så att det på L2
skapas en logisk trädtopologi och på så sätt hålls ethernetsegment
loopfria. Enheter som använder STP skickar BPDU-meddelanden mellan
varandra för att utbyta information. De skickas till
01:80:C2:00:00:00/01:00:0C:CC:CC:CD. Den BPDU som är superior har
företräde och övriga kan ignoreras. För att avgöra vilken som är bäst
jämförs följande värden i skriven ordning: Root Bridge ID, Root Path
Cost, Sender Bridge ID, Sender Port ID, Receiver Port ID (RPID följer ej
med i BPDUn utan switchen själv vet ju detta). Det första värdet där det
skiljer sig avgör och lägst vinner. BPDUer skickas ej på non-designated
portar eftersom de inte är superior och därmed onödiga att skicka.
Varenda port på varenda switch i STP sparar superior BPDUn på det
segmentet. Non-designated portar sparar BPDU från andra sidan och
Designated portar sparar sin egen BPDU.

Se även [Cisco MST](/Cisco_MST "wikilink").

STP
===

STP (IEEE 802.1D) använder BPDUer med Version 0. Kommer det inte in
någon BPDU innan MaxAge (minus MessageAge) har gått ut måste STP räkna
om. Rotbryggan avgör dessa timers. Root Path Cost skickas med i varje
Hello och genom att addera det med costen på interfacet där Hellon kom
in vet switchen hur långt det är till rotbryggan.

<div class="mw-collapsible mw-collapsed" style="width:210px">

**BPDU**

<div class="mw-collapsible-content">

[<File:Cisco_STP_BPDU.png>](/File:Cisco_STP_BPDU.png "wikilink")

</div>
</div>

**Process**
STP-processen börjar med att alla switchar ser sig själva som root och
skickar ut Hellos. Sedan görs följande val:

1.  Root Bridge: Lowest BID = Priority + MAC (Den ursprungliga
    STP-varianten hade ej med VLAN ID)
2.  Root Port: Av alla BPDUer på alla portar vilken är superior. Dvs
    bästa vägen bandbreddsmässigt till rotbryggan, en per nonroot
    switch.
3.  Designated Port: Superior BPDU på ett segment
4.  Non Designated: Övriga

På rotbryggan finns det ingen root port utan alla är designated.
STP-processen slutar aldrig utan varje BDPU som kommer in ska jämföras.

PVST-processen skiljer sig lite grann:

-   Root Bridge: Lowest BID (Priority + **VLANID** + MAC)

**Topology Change**
Det finns en slags BPDU i 802.1D som heter TCN (Topology Change
Notification), den används för att informera övriga om en förändring.
Detta skickas om: det kommer in en TCN BPDU på en designated port, en
port går från Learning till Forwarding eller Blocking, en switch blir
rotbrygga. Kom ihåg att vanliga BPDUer som inte är superior ignoreras
därför måste en TCN skickas till root (görs genom root port) som sedan
kan skicka ut det till alla. En TCN skickas med varje Hello tills en TCA
(Acknowledgement) fås som svar, sedan gör nästa switch samma sak till
det når root. Rotbryggan sätter nu TC-biten i sina utgående BPDUer som
instruerar övriga att förkorta Aging Time till ForwardDelay för att
påskynda konvergens.

**Timers**
Det finns flera olika typer av timers som skickas med i BPDUerna.
MessageAge är en uppskattning på hur länge sedan BPDUn lämnade
rotbryggan (med detta satt till 0). Övriga switchar brukar plussa på 1
innan de skickar det vidare. MaxAge, HelloTime och ForwardDelay är
värden satta på rotbryggan, har andra switchar andra värden
konfigurerade spelar det ingen roll för det är rotbryggan som bestämmer.
Hellos skickas default var 2 sekund.

`spanning-tree vlan 1-4094 hello-time 2`
`spanning-tree vlan 1-4094 forward-time 15`
`spanning-tree vlan 1-4094 max-age 20`

**Interface states**
När nätverket konvergerar kan portar byta mellan Blocking och Forwarding
men detta kan inte göras direkt utan att riskera tillfälliga loopar.
Därför går interfacen igenom olika tillstånd. Längden på transitory
statesen avgörs av ForwardDelay, 15 sek default.

| State      | Forwards data frames | Learns source MACs of received frames | Stable                                   |
|------------|----------------------|---------------------------------------|------------------------------------------|
| Blocking   | No                   | No                                    | Stable (show spanning-tree blockedports) |
| Listening  | No                   | No                                    | Transitory                               |
| Learning   | No                   | Yes                                   | Transitory                               |
| Forwarding | Yes                  | Yes                                   | Stable                                   |
| Disabled   | No                   | No                                    | Stable                                   |

Rapid ST
========

Rapid Spanning Tree Protocol (802.1w) och RPVST+ (Cisco) förbättrar
konvergens avsevärt, under 1 sekund i bra byggda nät. Man har
introducerat att länkar är point-to-point för att kunna ha bättre
mekanismer för recovery (konvergenstid). Det finns också *shared links*
men det bör alltid vara p2p nuförtiden om inget är half duplex.

Man använder 2 nya porttyper.

-   **Alternate Port:** prospekt till root port. Går root port ner kan
    denna ta över snabbt.
-   **Backup Port:** prospekt till designated port. Finns om switchen
    har flera portar i samma segment.

**BPDU**
I RSTP finns endast en sorts BDPU (Version 2) som används för allt. Man
har uppdaterat flag fields och skillnad från tidigare finns nu Proposal
bit, Port role bits, Learning bit, Forwarding bit och Agreement bit.
Alla switchar originerar sina egna BPDUer oavsett BPDUn på root porten
vilket leder till att de är mer pålitliga som Hello-mekanism. Om det
slutar komma BPDU väntar en switch 3x Hello interval sedan blir BPDUn på
den porten age out. MessageAge används nu endast för hop count och är
det samma eller högre än MaxAge discardas BPDUn.

Med STP ignoreras inferior BPDUer men i RSTP accepteras de direkt och
switchen utvärderar sin roll och state på interfacet som vanligt. Detta
leder till att switchen snabbt kan agera ifall den som brukade skicka
superior BDPUer har disruption till root bridge. Kanske finns det en ny
root bridge eller så har costen till root ökat den vägen, hursom ska det
ageras på direkt.

**Proposal/Agreement Process**
När man lägger till en länk i topologin kan en tillfällig switching-loop
uppstå eftersom en switch då kan välja den tillagda länken som ny root
port och övriga switchar inte känner till det direkt. För att skydda mot
detta har RSTP en Proposal/Agreement-mekanism på p2p-länkar (vilket alla
länkar bör vara). Eftersom man inte kan styra andra switchar måste det
loop-skyddas lokalt när man byter root port. Genom att sätta alla
(inklusive gamla root) non-edge designated portar i discarding state
innan den nya root port blir forwarding förhindrar man en loop. Dock
stängs länkar och det tar lite tid att återställa så genom att ha ett
signaling scheme mellan enheterna som används för att försäkra sig om
att det är safe att sätta designated portar i forwarding kan man uppnå
snabb konvergens, detta kallas Proposal/Agreement. Proposal står för de
portar som vill bli forwarding och Agreement står för tillåtelse att
göra så. När en ny p2p-länk kommer upp mellan två switchar blir port
state Designated Discarding på non-edge portar. När porten blir Learning
skickas BPDUer med Proposal-biten satt.

**Topology Change**
Till skillnad från 802.1D är den enda gång en topologiändring anses
hända när en non-edge port går från non-forwarding till forwarding. Den
nya portan kan ha en bättre väg för MAC-adresserna och CAM-tabellen
måste uppdateras. Går en port från forwarding till non-forwarding spelar
det ingen roll för då är de MAC-adresserna unreachable, dyker de upp
någon annanstans är det för någon annan port har gått från
non-forwarding till forwarding och då är det en topologiändring
iallafall. I 802.1D skickades en TCN upstream, i RSTP floodas BPDUer med
TC-biten satt till alla non-edge designated ports och root port utom
porten där ändringen kom in på. Samt flusha alla MAC-adresser på den
porten.

För att RSTP/RPVST+ ska kunna tillhandahålla snabb konvergens måste alla
switchar köra RSTP eller RPVST+, alla inter-switchlänkar måste vara p2p
och alla portar mot end systems måste vara edge ports. Annars kommer
prestandan att degraderas.

**Interface states**
Med RSTP har man gått från 5 interface states till 3.

| Administrative State | STP        | RSTP       |
|----------------------|------------|------------|
| Enabled              | Blocking   | Discarding |
| Enabled              | Listening  | Discarding |
| Enabled              | Learning   | Learning   |
| Enabled              | Forwarding | Forwarding |
| Disabled             | Disabled   | Discarding |

Discarding lyssnar och skickar (beroende på roll) fortfarande BPDUer och
övrig control plane traffic till och från switchen. Forwarding och
Discarding är stable state medans Learning är transitory.

Konfiguration
=============

Bridge ID med VLAN, detta är default och går ej att ta bort på nyare
switchar för det konsumerar fler MAC-adresser. Kolla den lokala
MAC-adressen som används till Bridge ID: **show version \| i bia\|Base**

`spanning-tree extend system-id`
`spanning-tree mode rapid-pvst`
`show spanning-tree`

**Cost**
802.1D-1998, 1G = 4

`spanning-tree pathcost method short`

802.1D-2004, 1G = 20000

`spanning-tree pathcost method long`
`show spanning-tree pathcost method`

**Root Bridge**
Konfigurera root brygga. Priority 0 är det absolut lägsta medans root
primary sätter prio till 24k förutsatt att det ger root-rollen, detta
ändras inte dynamiskt.

`spanning-tree priority 0`
`spanning-tree root primary`

Verify

`show spanning-tree root`

Default-värden

`default spanning-tree vlan 1-4094 priority`

**Portar**
Root Port och Designated Port

`interface range gi0/7`
` spanning-tree cost 1000`
` spanning-tree port-priority 128`

Restart the protocol migration process

`clear spanning-tree detected-protocols`

**Troubleshoot**

`test spanning-tree diameter 3`
`test spanning-tree get configuration vlan`
`debug spanning-tree events`
`debug spanning-tree backbone fast`
`debug spanning-tree pvst+`

Legacy Extensions
-----------------

Det finns många tillägg till Spanning-tree som bör användas, de hjälper
till att öka stabilitet, säkerhet och kompabilitet. Se även [MST
Extensions](/Cisco_MST#Extensions "wikilink").

**UplinkFast**
Cisco-proprietary teknik som låter en alternate port gå direkt till
forwarding om root port går ner. För att försäkra sig att en switch med
uplinkfast inte blir en transit switch sätts bridge priority automatiskt
till 49152 och port costen blir 3000. Detta kan därför inte användas på
en switch som har sin STP prio modifierad. När överslag görs så skickas
dummy frames till mac 01:00:0c:cc:cc:cc från alla adresser i cam
tabellen för att snabba upp konvergens i övriga nätet. Uplinkfast på
default och konfigureras globalt.

`spanning-tree uplinkfast`
`show spanning-tree uplinkfast`

**BackboneFast**
Cisco-proprietary teknik som används för att snabba upp konvergens vid
indirect link failure genom att låta MaxAge timer gå ut direkt. Om någon
annan plötsligt hävdar sig vara root kanske den tappat sin uplink till
root och då kan man timea ut den tidigare BPDU:n man fått från den
enheten för att snabba upp konvergens. RLQ skickas också till root för
att dubbelkollla att man sjäv inte tappat root. RSTP och MST har detta
inbyggt men bör i övrigt användas på alla enheter, så förhoppningsvis
inga...

`spanning-tree backbonefast`
`show spanning-tree backbonefast`

[Category:Cisco](/Category:Cisco "wikilink")