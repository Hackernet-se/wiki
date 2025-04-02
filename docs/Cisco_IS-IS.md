---
title: Cisco IS-IS
permalink: /Cisco_IS-IS/
---

Intermediate System-to-Intermediate System är ett link-state routing
protokoll. Det använder Network Service Access Point (NSAP) adressering
för att identifiera routrar, area-tillhörighet och deras grannskap.
IS-IS använder inte något L3-protokoll alls utan det enkapsuleras direkt
i L2 multicast frames, för L1 används 01:80:C2:00:00:14 och för L2
01:80:C2:00:00:15, detta gör det helt L3-protokolloberonde. Grannskap
och adressinformation skrivs med Type-Length-Value (TLV) records, detta
gör det väldigt flexibelt. T.ex. om en ny adressfamilj eller ett nytt
protokoll ska läggas till så handlar det om att definiera nya TLVer som
innehåller adress- och topologiinformation. För lista med TLVer som
IS-IS kan använda se IANAs [TLV
Codepoints](http://www.iana.org/assignments/isis-tlv-codepoints/isis-tlv-codepoints.xhtml).

IS-IS är ett av de tre protokollen i standarden Connectionless Network
Services
([CLNS](https://en.wikipedia.org/wiki/Connectionless-mode_Network_Service)),
de andra två är CLNP och ES-IS. Numera används det vanligare för IP IGP
och är bl.a. en del i klassisk [MPLS Traffic
Engineering](/Cisco_MPLS#Traffic_Engineering "wikilink"). Level 3
routing är routing mellan domäner (AS) och det var tänkt att göras med
protokollet IDRP men numera görs det fördelaktigt med
[BGP](/Cisco_BGP "wikilink"), som kan bära NSAP-adresser.

**Type:** Link State

**Algorithm:** Dijkstra

**AD:** 115

**Protocols:** IP, CLNS

**Packets:** 4

### Terminologi

-   End system: host
-   Intermediate system: router
-   Circuit: interface
-   Domain: autonomous system
-   SNPA: layer 2 address

Packets
-------

**Hello/IIH:** IS-IS Hello används för att upptäcka grannar och
kontrollera att de lever. De skickas default var 10:e sekund och
innehåller en lista på alla grannar man har på segmentet om det är ett
broadcastnäverk. De används också för att välja DIS (Designated IS) där
det behövs. DIS skickar Hellos mer frekvent, hello time delat på 3 så
var 3.33 sekund default. Hold time är Hello-interval x Hello-multiplier.
Varken Hello eller Hold behöver matcha för grannskap. På broadcast
segment används separata Hellos för L1 och L2 medans på point-to-point
interface används gemensamma L1L2 Hellos pga effektivitet. Hello padding
görs default för att ta reda på hur stora frames som kan skickas.

<div class="mw-collapsible mw-collapsed" style="width:450px">

L1 Hello:

<div class="mw-collapsible-content">

[<File:Cisco_ISIS_Hello_L1.png>](/File:Cisco_ISIS_Hello_L1.png "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:450px">

L1L2 Hello:

<div class="mw-collapsible-content">

[<File:Cisco_ISIS_Hello_L1L2.png>](/File:Cisco_ISIS_Hello_L1L2.png "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:450px">

P2P Hello: (finns ingen prio utan istället finns Local Circuit ID)

<div class="mw-collapsible-content">

[<File:Cisco_ISIS_Hello_P2P.png>](/File:Cisco_ISIS_Hello_P2P.png "wikilink")

</div>
</div>

Timers ställs per interface. Default är 10 sekunder och multiplier är 3
för hold time.

`isis hello-interval 10 [level]`
`isis hello-multiplier 3 [level]`

**Link state PDU:** LSPs används för att skicka routing-information till
andra IS. Det finns inte olika LSP-typer som OSPF har olika LSA-typer
utan adjacencies och prefixes skickas med en LSP som innehåller olika
TLVer. En LSPs payload kan därmed variera i storlek. Varje LSP
innehåller ett LSPID som gör det unikt. Det består av System ID (router
that originated the LSP), Pseudonode ID (DIS) och LSP number (fragment
number). För att skilja mellan olika versioner av samma LSP sätts även
ett löpnummer. Det börjar på 1 och varje gång en ändring görs ökas det
med 1.

Om Attached Biten är satt i LSP-headern betyder det att den kommer ifrån
en nod med ben i en annan area eller L2, det finns flera "Attached bits"
men endast default metric används på Cisco IOS. För att en L1L2 ISIS
router ska sätta ATT-biten på sina LSPer måste den vara ansluten till
två olika areor. Den behöver inte själv vara directly attached till en
annan area men arean måste finnas kopplad till L2. Varje LSP har även en
remaining lifetime satt, det börjar på 1200 sekunder och tickar neråt.
Var 900:e sekund så refreshar en IS-IS router sina self-originated LSPer
och skickar ut dem pånytt. Går remaining lifetime ner till 0 på en LSP
tas routing informationen bort från LSDB och routern kommer att flooda
ut endast LSP:ns header med remaining lifetime satt till 0 för att
signalera att man vill ha ny information och på så vis ta reda på om
någon annan känner till mer aktuell information, detta kallas LSP Purge.
LSP headern hålls kvar i LSDB så länge som ZeroAgeLifetime är satt till,
60 sekunder default men kan sparas 20 minuter på Cisco-routrar.

`router isis`
` max-lsp-lifetime 1200`
` lsp-refresh-interval 900`

Eftersom IS-IS paket enkapsuleras direkt i L2-frames måste IS-IS ha en
egen fragmenteringsfunktion för LSPer som är större än MTU. Behöver man
skicka en LSP vars header + TLVer är större än MTU så delar routern upp
det i flera LSPer som innehåller några TLVer var. LSPerna har samma
LSPID men LSP/fragment number ökas per LSP med start från 0.
Fragmentering görs av den router som skapar LSPn, när den sedan har
skickats ut får den inte modifieras eller fragmenteras om. Detta leder
till att MTU på alla interface inom arean måste vara identiskt. Annars
får man manuellt ställa lsp-storlek på alla enheter så det inte
överstiger lägsta MTU.

`lsp-mtu 1400`

<div class="mw-collapsible mw-collapsed" style="width:250px">

Exempel:

<div class="mw-collapsible-content">

[<File:Cisco_ISIS_LSP.png>](/File:Cisco_ISIS_LSP.png "wikilink")

</div>
</div>

**Complete Sequence Numbers PDU:** CSNP används för att synkronisera
LSDB mellan enheter (fungerar ungefär på samma sätt som DD i OSPF). CSNP
innehåller en komplett lista med alla LSPer som routern har och
mottagaren kan jämföra det mot sin egen LSDB. Finns det någon LSP som
mottagaren ej har kan den requesta den och fattas det någon hos
avsändaren floodas den tillbaka. Finns det fler LSPID:n än vad MTU
klarar skickas det flera paket. Varje CSNP specificerar vilka LSPID:n
den innehåller och det börjar på 0000.0000.0000.00-00 och räknar uppåt
(stigande).

På point-to-point-länkar utbyts CSNP vid adjacency buildup och på
broadcast skickas det regelbundet av DIS. Eftersom ack sköts av PSNP på
point-to-point-länkar skickas inga CSNP periodiskt, detta kan man slå på
manuellt med interface-kommandot **isis csnp-interval <nonzero value>**

<div class="mw-collapsible mw-collapsed" style="width:250px">

Exempel:

<div class="mw-collapsible-content">

[<File:Cisco_ISIS_CSNP.png>](/File:Cisco_ISIS_CSNP.png "wikilink")

</div>
</div>

**Partial Sequence Numbers PDU:** PSNP skickas för att requesta eller
acka en LSP (fungerar både som OSPF LSR och LSAck). En PSNP kan requesta
eller acka flera LSPer. På broadcast används dock PSNP endast för
Request eftersom Ack görs av CSNP från DIS.

<div class="mw-collapsible mw-collapsed" style="width:250px">

Exempel:

<div class="mw-collapsible-content">

[<File:Cisco_ISIS_PSNP.png>](/File:Cisco_ISIS_PSNP.png "wikilink")

</div>
</div>

Levels
------

En IS-IS router konfigureras med nivå som anger systemtyp - antingen
Level 1, Level 2 eller Level 1-2. Se en Level 2 router som motsvarande
area 0 (backbone area) i [OSPF](/Cisco_OSPF "wikilink") och Level 1 som
en area som är ”NSSA Totally Stubby ”, d.v.s. det enda som injiceras i
arean är en default route samt att redistribution från andra
routingprotokoll är tillåtet, och en Level 1-2 som en ABR.

IS-IS routrar på level 1 agerar oberoende av level 2 och vice versa. De
upprättar separata grannskap på varje level. T.ex. om det finns två
stycken IS-IS routrar som båda kör L1 och L2 så kommer de att ha två
grannskap med varandra. Det blir bara grannskap om båda är på samma
level, t.ex. L2 + L1L2 = L2-grannskap. De kommer även hålla separata
LSDBer för varje level. Så Link State PDUer som skickas görs det
antingen på L1 eller L2. L1-LSPer beskriver grannskap i L1 och samma
gäller för L2. Det går nästan likna vid separata routing-processer. Att
ändra mellan L1, L2 och L1L2 görs per router.

`router isis 1`
` is-type level-1-2  #Default`

Men det går att ändra per interface för att sluta skicka Hellos för en
specifik level. T.ex. om man själv är L1L2 och vet man att andra sidan
är en L1 only är det onödigt att skicka L2 Hellos.

`interface gi2`
` isis circuit-type {level-1 | level-2 | level-1-2}`

Show

`show isis protocol | i IS-Type`

**Backdoor**
Default använder L1-routrar den närmaste L1L2-routern som gateway of
last resort. Det är inte alltid man vill ha det så, då kan man stänga av
att L1L2-routern sätter attached bit i sina Hellos och övriga routrar
kommer inte att installera en default route till den.

`is-type level-1-2 backdoor `

### NET

Network Entity Title kallas den adress som IS-IS-processer (och därmed
noder) använder, längden kan variera mellan 64 och 160 bitar men det
måste vara jämt antal bytes. Formatet är AFI.DSP.SystemID.NSEL:

-   AFI = 49
-   DSP(Area ID) = 0001
-   SystemID = Räknas fram baserat på Loopback adressen
-   NSEL = 00

### Areas

Eftersom en nod endast har en NSAP-adress tillhör en nod och alla dens
interface samma area (det går att konfigurera upp till 3 NSAP-adresser
men det är endast användbart under splitting/joining/renumbering areor
och det skapas bara en mergead LSDB och SystemID måste vara samma). Två
L1-noder med olika areor upprättar inte grannskap medans L2 inte bryr
sig om area-ID. Både L1 och L2 annonserar sina directly connected IP
networks till sina grannar. Är en nod L1L2 redistribueras alla routes
från L1 till L2 medans åt andra hållet går endast en default route
default. Detta leder till att backbone känner till alla routes.

### Nätverkstyp

Till skillnad från OSPF finns det endast två nätverkstyper, broadcast
och point-to-point. På broadcast-segment har man en pseudonod som alla
formar grannskap med, denna kallas Designated IS och är motsvarigheten
till DR i OSPF. Man låter en enhet stå för LSP för segmentet annars blir
LSDB större och rörigare. Dock är det skillnad på hur flooding fungerar.
Alla uppdaterar alla vilket leder till att det inte behövs någon
"Backup" DIS. DIS floodar periodvis sin databas och finns det då med
någon LSP som en IS inte har fått märker den det och begär att få den av
DIS. Detta leder också till att DIS kan ersättas preemptively vilket
inte OSPF DR kan.

Den som väljs till DIS är den med högst prio (default 64), vid lika är
högsta MAC-adress tie breaker.

`interface gi2`
` isis priority 100`
`show clns interface | i DR`

Metrics
-------

IS-IS använder bandwidth som metric precis som OSPF. Från början fanns
det 4 olika metric-typer men i princip är det endast default (bandwidth)
som används idag. Default så får alla interface en cost av 10 oavsett
bandbredd. Med andra ord så räknar inte routern ut cost på en länk så
som andra routing protokoll gör utan det är upp till administratören att
manuellt ställa metric per interface om man vill. Likt OSPF är det inte
metric som i första hand jämförs vid path selection utan det är typ av
route där L1 \> L2 \> external. Nedan visas det som kallas *narrow
metrics*, det är legacy och är inte default på Cisco-routrar.

`isis metric 1-63`

**Wide metrics** togs fram för att man hade behov av större metrics och
det har 24-bitars längd. Detta är alltid rekommenderat men alla enheter
inom arean måste stödja det. T.ex. krävs det för MPLS traffic
engineering över IS-IS.

`router isis`
` metric-style wide`

Det går även att acceptera båda typerna av metric.

`metric-style transition`

Verify

`R1# show isis protocol | i metrics`
` Generate narrow metrics: none`
` Accept narrow metrics:   none`
` Generate wide metrics:   level-1-2`
` Accept wide metrics:     level-1-2`

Konfiguration
=============

Om man ska köra med flera areor på en enhet måste man ange tag för varje
IS-IS-process. Den första IS-IS instansen som konfigureras blir default
L1L2 och därefter blir instanser L1. Det finns även RFC för
defaultvärden för att underlätta interoperability (RFC 8196).

`router isis [tag]`
` is-type level-1-2`
` log-adjacency-changes`
` net 49.0001.0001.0001.0001.0001.00`

` address-family ipv4 unicast`
` exit`
` address-family ipv6 unicast`
` exit`

Passive interfaces, med passive interface default annonseras allt som är
directly connected i isis men inga grannskap byggs förrens man tar bort
passive på något interface. Det är även med passive interfaces man gör
prefix suppression.

` passive-interface default`
` no passive-interface te0/1/1`

` passive-interface lo0`
` advertise passive-only`

För att skicka en default route i level 2

`default-information originate`

Verify

`show isis`
`show isis database`

**Default konfiguration** när man drar igång IS-IS (kan skilja mellan
IOS-versioner).

`router isis`
` no protocol shutdown`
` max-area-addresses 3`
` no fast-flood`
` adjacency-check`
` no use external-metrics`
` metric 10 level-1`
` metric 10 level-2`
` hello padding`
` no nsf cisco`
` no nsf ietf`
` maximum-paths 4  #Max är 32`
` distance 115 ip`
` no bfd all-interface`
` no bfd check-ctrl-plane-failure`

Vänta med att använda en granne som nyss har bootat.

`set-overload-bit on-startup 180`

**MPLS**
[MPLS](/Cisco_MPLS "wikilink") LDP kan autokonfigureras med hjälp av
IS-IS. Man kan även synka IS-IS mot LDP, dvs låta LDP bli klar innan
länken får en normal (låg) IGP-metric och därmed börjar användas.

`mpls ldp autoconfig`
`mpls ldp sync`

`show isis mpls ldp`

IS-IS kan även användas för [Segment Routing](/Cisco_SR "wikilink") med
MPLS.

Adjacency
---------

Enablea IS-IS på interface. Interface MTU måste matcha för grannskap.
Grannar måste även vara i samma IP subnet för att adjacency ska gå upp,
detta behövdes inte förr men nu är checken på default. Går inte
grannskap upp kan det också bero på duplicate system ID men det säger
loggen tydligt.

`interface te0/1/1`
` ip router isis 1`
` no isis hello padding`
` isis network point-to-point  #effektivisera LSP-hantering`
` no shut`

**Verify**

`show isis hostname`
`show isis neighbors/adjacency`
`show isis topology`
`show clns neighbor`

### Authentication

IS-IS authentication skiljer sig ganska mycket från authentication med
övriga IGP:er. Authentication för Hellos görs fristående från övriga
pakettyper. Authentication görs med en TLV och en LSP får ej modifieras
av någon annan än originator, detta medför att alla inom arean måste ha
samma authentication på sina LSP/CSNP/PSNP men det blir inget krav på
Hellos. Sålänge Hello-paket autentiseras korrekt kommer grannskap att
bli Up men det behöver inte betyda att LSP:er kan utbytas utan då måste
som sagt area/domain password matcha. Authentication kan göras med clear
text eller md5. Använder man en key chain så skickas heller inte key id
med.

Hello-paket görs per interface oavsett level.

`interface gi2`
` isis authentication mode md5`
` isis authentication key-chain `<key-chain-name>

LSP authentication

`router isis 1`
` authentication mode md5`
` authentication key-chain `<key-chain-name>

Redistribution
--------------

Routes som redistribueras in i IS-IS får default metric 0. En viktig
faktor för route leaking i ISIS är U/D-biten i TLV:n för routen. Den
fyller samma funktion som Down-biten i OSPF, den används för att
förhindra loopar. En L1L2-router som via L1 får in routes med U/D-biten
satt kommer inte att skicka in den till L2.

Redistribution into level 2. Redistribution into level 1

`redistribute static ip`
`redistribute static ip level-1`

`show isis ip rib redistribution`

Man kan läcka L2 routes till L1 med hjälp av redistribution.

`redistribute isis 1 ip level-2 into level-1 distribute-list `*`ACL`*

### Summary

När routes går mellan areor eller redistribueras kan man summera (likt
OSPF).

`summary-address 10.1.0.0 255.255.0.0 [level]`

-   level-1: endast routes redistribuerade in i Level 1 summeras.
-   level-1-2: routes redistribuerade in i Level 1 summeras och routes
    från Level 1 routing eller redistribution summeras in i Level 2
    backbone.
-   level-2: routes från Level 1 routing eller redistribution summeras
    in i Level 2 backbone.

IPv6
----

IS-IS är oberoende av L3-protokoll för grannskap och kan bära
information om destinationer för olika adressfamiljer. IPv6 prefix kan
skickas med samma IS-IS-process, i samma LSP:er över samma grannskap som
IPv4 och samma L1/L2-förhållanden gäller då för IPv6. Det man däremot
bör ha koll på är om IPv4 och IPv6 ska använda samma topologi eller ej,
ska man köra single topology krävs en 1:1-korrelation mellan IPv4 och
IPv6 interface (dvs dual stack överallt) och då kommer det endast göras
en SPF-beräkning. Adjacency checken som är på default rejectar Hellos
från grannar som inte kör IPv6. Ska man köra multi topology behöver man
inte ha dual stack överallt, SPF beräknas fristående per protokoll och
man måste använda wide metrics. Det konfigureras under adressfamiljen.
Man kan även köra multi-topology under en transitionsperiod, då
accepterar och genererar man både IS-IS IPv6 och Multi-topology IPv6
TLVs.

Den mesta av konfigurationen görs under adressfamiljen, till skillnad
från IPv4. IS-IS kommer att skicka vidare IPv6-information men ej börja
använda det förens man lagt in *address-family ipv6*.

`router isis 1`
` address-family ipv6 unicast`
`  multi-topology [transition]`
`  maximum-paths 16`
` exit`

Verify

`show ipv6 route isis`
`show isis ipv6 topology  #Multi topology`
`show isis ipv6 rib`

Convergence
-----------

Timers

`lsp-gen-interval 5 50 50`
`prc-interval 5 50 50`
`spf-interval 5 50 50`

**Nonstop Forwarding**
När en router gör en RP switchover måste den nya snabbt få all info om
adjacencies och en synkad LSDB. IS-IS NSF kan möjligöras på två sätt.

-   IETF (RFC 3847): NSF-kapabla enheter skickar IS-IS NSF restart
    requests till grannarna som är NSF-aware. Då förstår de att de inte
    ska starta om grannskapet utan istället initiera en
    LSDB-synkronisering. Grannarna måste ha stöd för NSF IETF.
-   Cisco: Skickar både protocol adjacency och link-state information
    från aktiv RP till standby. Detta är inte beroende av att grannarna
    är NSF-aware.

**BFD**
När IS-IS konfigureras med [BFD](/Cisco_BFD "wikilink") blir det ett
registrerat protokoll till BFD och kan dra nytta av de forwarding path
detection failure messages som BFD tillhandahåller. Det kan antingen
konfigureras under adressfamiljen eller per interface.

`int te0/1/1`
` bfd interval 50 min_rx 50 multiplier 5`
` isis bfd`

IS-IS-klienten kan även utnyttja BFD C-biten för att veta om det är ett
äkta data plane failure eller om det är resultatet av ett control plane
failure t.ex. pga reboot, detta är på default.

`router isis `
` bfd check-control-plane-failure `

**iSPF**
SPF-algoritmen behöver inte köras för alla länkar varje gång det sker en
topologi-förändring. Med incremental SPF körs endast algoritmen för de
delar som har påverkats av förändringen för att spara CPU-cykler. Detta
går att styra individuellt på enheterna med ispf-kommandot. Det kan vara
svårt att veta exakt hur mycket skillnad detta gör men generellt ju
större topologi ju större skillnad. OBS iSPF är inte längre supporterat
i IOS.

`router isis 1`
` ispf level-1-2 10`
`show isis protocol | i Incremental`

**Fast flood**
Man kan välja att LSP:er ska floodas innan SPF-beräkningen påbörjas för
att få snabbare konvergenstid. Detta är ej påslaget default.

`router isis 1`
` fast-flood`

### Loop-Free Alternate Fast Reroute

Med IP LFA FRR kommer IS-IS beräkna loop-fria next-hop routes till
forwarding plane som kan användas om primary path går ner. Detta
beräknas per prefix. LFA är en next-hop route som skickar paketet till
destination utan att loopa tillbaka det. LFA gör ingen signaling utan
lokal router räknar själv.

-   **P:** de noder man kan nå utan att gå igenom länken man vill skydda
-   **Q:** de noder som kan nå destination utan att gå igenom länken man
    vill skydda

Finns det inga PQ får man extenda P space genom att kolla P noder
utifrån dina grannar.

**Remote LFA**
Med IS-IS remote LFA FRR kan man skapa backup paths som är flera hop
bort, dvs man man tunnlar det till en drop off point som sedan skickar
till slutdestination. Det man gör i praktiken är att tunnla till
närmasta PQ. Detta är t.ex. användbart i ringtopologier. IS-IS stödjer
detta endast när också targeted LDP stöds. LFA-beräkningar är begränsade
till interface/länkar som tillhör samma area och level. Finns det
multipla LFAs för en primary path så kommer IS-IS att använda en
tiebreaking rule för att välja en LFA och finns det multipla LFA paths
så kommer prefixen att distribueras jämt mellan dem. Eftersom IS-IS
kollar på prefixen efter att SPF har körts kan best repair path hållas
efter att grannen har kört SPF. När man slår på remote LFA enableas
microloop avoidance med delay 5000 ms. Alla IS-IS interface måste vara
point-to-point.

`router isis 1`
` fast-reroute remote-lfa level-2 mpls-ldp`

`show isis fast-reroute remote-lfa tunnels`

**TI-LFA**
Med Topology Independent LFA får man alltid post-konvergens routen och
den är garanterat loopfri med 100% coverage. Syftet med TI-LFA är att
garantera link protection i symmetric metric networks (t.ex. ringnät),
skydda IP och MPLS-trafik samt undvika congestion och suboptimal routing
genom att undvika high metric links. TI-LFA använder inte targeted LDP
utan det bygger på Segment Routing.

`router isis 1`
` segment-routing mpls`
` ip route priority high tag 1000`
` fast-reroute per-prefix level-2 all`
` fast-reroute ti-lfa level-2`

Verify

`show isis fast-reroute summary`
`show isis fast-reroute interfaces`
`show isis fast-reroute ti-lfa tunnel`
`show ip route repair-paths`

NX-OS
=====

Grundkonfiguration

`feature isis`

`router isis IS`
` net 49.0001.0001.0001.0001.0002.00`
` is-type level-1`
` passive-interface default level-1`
` log-adjacency-changes`

` address-family ipv4 unicast`
` exit`

NX-OS, några defaults

`router isis IS`
` graceful-restart`
` maximum-paths 8`
` max-lsp-lifetime 1200`
` lsp-mtu 1492`
` reference-bandwidth 40 Gbps`

Fast convergence

`spf-interval level-2 5000 50 50`
`lsp-gen-interval level-2 5000 50 50`

Authentication

`authentication-type md5 level-2`
`authentication key-chain `<key-chain-name>` level-2`

Vänta med att använda en granne som nyss har bootat.

`set-overload-bit on-startup 180`

Interface

`int lo0`
` ip router isis IS`

`interface e1/1`
` no switchport`
` ip router isis IS`
` no isis passive-interface level-2`
` no isis hello-padding`
` isis network point-to-point`
` isis authentication-type md5 level-2`
` isis authentication key-chain `<key-chain-name>` level-2`

Genom att använda network type p2p effektiviserar man LSP-hanteringen.
Det går även att använda kommandot "medium p2p" för att uppnå detta.

[BFD](/Cisco_BFD#NX-OS "wikilink")

`feature bfd`
`interface e1/1`
` bfd interval 50 min_rx 50 multiplier 3`
` no bfd echo`
` isis bfd`

IOS-XR
======

IOS-XR IS-IS kör default i Multi Topology mode.

`router isis 1`
` set-overload-bit on-startup 180`
` is-type level-2-only`
` net 49.0000.0000.0011.00`
` nsr`
` nsf cisco`
` log adjacency changes`
` lsp-refresh-interval 65000`
` max-lsp-lifetime 65535`
` lsp-password keychain ISIS-KEY`
` address-family ipv4 unicast`
`  metric-style wide`
`  advertise passive-only`
` !`
` address-family ipv6 unicast`
`  metric-style wide`
`  advertise passive-only`
` !`
` interface Loopback0`
`  passive`
`  address-family ipv4 unicast`
`  !`
`  address-family ipv6 unicast`
` !`
` interface TenGigE0/0/0/10`
`  point-to-point`
`  hello-password keychain ISIS-KEY`
`  address-family ipv4 unicast`
`   fast-reroute per-prefix`
`   fast-reroute per-prefix ti-lfa`
`   metric 100`

**LFA**
router isis 1

` interface GigabitEthernet0/0/0/0`
`  address-family ipv4 unicast`
`   fast-reroute per-prefix`
`   fast-reroute per-prefix ti-lfa`
`  address-family ipv6 unicast`
`   fast-reroute per-prefix`
`   fast-reroute per-prefix ti-lfa`

IOS-XR har även per-link LFA men det finns egentligen inget use case för
det längre. Default märker ISIS /32-prefix som Medium priority och allt
annat som Low priority.

`show isis fast-reroute summary`
`show cef fast-reroute`

**Prefix Prioritization**

`router isis 1`
` address-family ipv4 unicast`
`  spf prefix-priority level 2 high tag 100`
` !`
` interface Loopback0`
`  address-family ipv4 unicast`
`   tag 100`

När man konfigurerar några prefix med high priority så får alla andra
prefix (inklusive /32) low priority.

**SRLG**

`srlg`
` interface GigabitEthernet0/0/0/1`
`  8 value 10`
` ! `
` interface GigabitEthernet0/0/0/2`
`  8 value 10`
`!`
`router isis 1`
` address-family ipv4 unicast`
`  fast-reroute per-prefix tiebreaker srlg-disjoint index 40`
`  fast-reroute per-prefix tiebreaker lowest-backup-metric index 50`

[Category:Cisco](/Category:Cisco "wikilink")