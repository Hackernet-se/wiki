---
title: Cisco OSPF
permalink: /Cisco_OSPF/
---

Open Shortest Path First (RFC 2328) är ett link-state routingprotokoll
standardiserat av Internet Engineering Task Force (IETF). Link-state
innebär att enheterna känner till alla länkar i topologin och deras
*operational states* och lagrar detta i en LSDB. OSPF konvergerar snabbt
och har bra skalbarhet. Det kommunicerar med multicast som har ttl satt
till 1 alternativt unicast på vissa nätverkstyper. OSPF använder IP
protokoll \#89. Se även [Cisco OSPFv3](/Cisco_OSPFv3 "wikilink") för
IPv6-stöd.

**Type:** Link State

**Algorithm:** Dijkstra

**AD:** 110

**Metric:** Cost (Bandwidth)

**Protocols:** IP

**Packets:** 5

Metric
------

OSPF i IOS använder 100MBit/s som referensbandbredd för att räkna ut
cost på varje länk. Man kan ändra detta till t.ex. 100G.

`router ospf 1`
` auto-cost reference-bandwidth 100000  #Mbits per second`
`show ip ospf interface | i Cost`

Om man stänger av auto-cost får alla länkar samma cost (10) oavsett
bandbredd, så som [IS-IS](/Cisco_IS-IS "wikilink") fungerar.

**Preferens**
Det är viktigt att känna till att olika typer av routes har olika
preferens och detta går före metric för path selection. I vissa fall går
detta att ändra.

1.  intra-area
2.  inter-area
3.  external
4.  nssa-external

Routrar föredrar default N2 routes över E2 routes som injicerats av
typ-7 till typ-5 translator men detta går att ändra.

`router ospf 1`
` compatible rfc1587`

Packets
-------

Alla paket kan vara unicast eller multicast, det avgörs av nätverkstyp.

-   **Hello:** Används för att upptäcka grannar. Innehåller mask,
    timers, flaggor (capabilities), DR/BDR (om det finns) och router-ID
    för grannar.

<div class="mw-collapsible mw-collapsed" style="width:250px">


Exempel:

<div class="mw-collapsible-content">

[<File:Cisco_OSPF_Hello.PNG>](/File:Cisco_OSPF_Hello.PNG "wikilink")

</div>
</div>

-   **Database Description:** Innehåller LSA headers under den initiala
    topologi-synken. Används först för att avgöra master/slave i
    grannskapet, högst router-id blir master.

<div class="mw-collapsible mw-collapsed" style="width:250px">


Exempel:

<div class="mw-collapsible-content">

[<File:Cisco_OSPF_DD.PNG>](/File:Cisco_OSPF_DD.PNG "wikilink")

</div>
</div>

-   **Link-State Request:** Innehåller vilka LSA:er som avsändaren vill
    ha alla detaljer om.

<div class="mw-collapsible mw-collapsed" style="width:250px">


Exempel:

<div class="mw-collapsible-content">

[<File:Cisco_OSPF_Request.PNG>](/File:Cisco_OSPF_Request.PNG "wikilink")

</div>
</div>

-   **Link-State Update:** Innehåller alla typer och detaljer om LSA:er
    och skickas på förfrågan eller vid topologiändring

<div class="mw-collapsible mw-collapsed" style="width:250px">


Exempel:

<div class="mw-collapsible-content">

[<File:Cisco_OSPF_Update.PNG>](/File:Cisco_OSPF_Update.PNG "wikilink")

</div>
</div>

-   **Link-State Acknowledgment:** LSU confirmation.

<div class="mw-collapsible mw-collapsed" style="width:250px">


Exempel:

<div class="mw-collapsible-content">

[<File:Cisco_OSPF_Ack.PNG>](/File:Cisco_OSPF_Ack.PNG "wikilink")

</div>
</div>

Grannskap
---------

OSPF-grannskap har bestämda tillstånd och neighbors måste komma överens
om:

-   Subnät/Mask
-   Area
-   Timers
-   Olika router-ID
-   Flaggor: Stub, NSSA
-   MTU
-   Authentication type
-   Kompatibla nätverkstyper, DR-election eller ej

**Neighbor states**
Kronologisk ordning

-   Down: Initial state. Om det inte kommer in några OSPF-paket under
    Dead interval blir grannen down.
-   Attempt: Gäller endast NBMA och point-to-multipoint nonbroadcast.
-   Init: Ett hello (utan mottagarens router-ID) har tagits emot.
-   2-way: Ett hello med mottagarens router-ID har tagits emot.
-   ExStart: Utbyta tomma DD för att bestämma master/slave.
-   Exchange: Utbyta database description
-   Loading: LSA:er tankas över
-   Full: Allt klart

LSA-typer
---------

LSUer innehåller link-state advertisements, dessa beskriver länkar och
enheter i nätverket. Det är endast den router som en LSA härstammar
ifrån som får modifiera eller ta bort LSA:n. Andra routrar måste
processa och skicka den omodifierad vidare inom sitt flodding scope, de
får ej droppa den innan maximum lifetime har gått ut. Detta säkerställer
att alla routrar har identiska LSDB men det medför också att man blir
begränsad i var man kan aggregera och filtrera routes. För att ta bort
en LSA snabbt sätts age till 3600 sekunder (maximum lifetime) och den
kommer då att tas bort direkt. En LSA header är vanligtvis 20 bytes.

De vanligaste LSAerna.

-   **Type 1, Router:**
    Alla routrar skapar och floodar en LSA som representerar sig själv.
    Det finns information om vilka interface och grannar som finns i den
    arean. Floodas endast inom origin area. ABR sätter B-biten och ASBR
    sätter E-biten för att informera arean om sin roll.

`show ip ospf database router`
`show ip ospf database router | i Link`

-   **Type 2, Network:**
    Dessa representerar transit subnät och skapas endast om det finns en
    DR på det subnätet, dvs multiaccess-segment. LSID sätts till DRs
    interface IP på subnätet men innehåller också information (RID) om
    alla grannar till DR på det subnätet. Floodas endast inom origin
    area.

`show ip ospf database network`

Note: Typ 1 och 2 räcker för att alla routrar inom arean ska kunna känna
till topologin och köra SPF för att bestämma bästa vägarna.

-   **Type 3, Net Summary:**
    Typ 1 och 2 går ej till andra areor utan istället skapar ABR (router
    med ben i 2 areor) typ 3 LSA:er (en ABR genererar aldrig summary LSA
    om den inte har ett ben i area 0). Det som annonseras är samma men
    den enda infon som skickas med är: subnät, mask och costen för ABR
    att nå dit. Typ 3 LSA:er korsar aldrig areor, istället har ABR en
    intern OSPF-routingtabell som innehåller allt som har kommit i
    backbone-arean och för varje intra- eller inter-area route skapas
    det nya typ 3 LSAer som floodas i nonbackbone-arean. OBS ABR
    accepterar endast typ 3 LSA:er från backbone area, detta för att
    förhindra routingloopar.

`show ip ospf border-routers`
`show ip ospf database summary`

-   **Type 4, ASBR Summary:**
    När en ABR floodar vidare en typ 5 LSA in i sin area vet inte övriga
    routrar i arean hur långt det är till ASBR. Därför skapar den en LSA
    typ 4 som den också floodar. Den innehåller ASBRs RID och ABRs cost
    till ASBR. Typ 4 LSA:er behöver inte finnas i samma area som ASBR
    eftersom där berättar ASBR om sig själv med typ 1 LSA med E-biten
    satt utan dessa behövs i övriga areor.

`show ip ospf database asbr-summary`

-   **Type 5, AS External:**
    När en ASBR skickar in en extern route skapar den en typ 5 LSA som
    innehåller metric och metric type. Det som är intressant för övriga
    routrar att veta är hur långt det är till ASBR och ifall det finns
    flera vägar som är lika används alla. Finns det flera ASBR används
    den som är närmast internt enligt SPF.

`show ip ospf border-routers`
`show ip ospf database external`

Det finns två typer av externa routes, E1 (increment metric) och E2 (do
not increment metric). Detta avgörs beroende på vad ASBR sätter för
flagga på LSAn. Default på Cisco är E2 för redistribution, dock är E1
prefered över E2. Externa routes måste även innehålla en **Forwarding
Address**. Vanligtvis sätts 0.0.0.0, det innebär att det ska skickas
till ASBR själv. Det finns dock situationer när man vill ha något annat
(nonzero) för att undvika suboptimal routing. Denna adress måste kännas
till intra- eller interarea annars installeras inte routen i
routingtabellen.

-   **Type 7, NSSA External:**

Floodas inom egna NSSA-arean, översätts till LSA typ 5 av ABR med högst
RID för att lämna arean OM Propagate-biten är satt till 1. Annars
stannar LSA:n inom arean, detta konfigureras vid redistributionen med
nyckelordet **nssa-only**. Om man vill att trafiken alltid ska gå igenom
translator kan man suppressa forward address, **area 1 nssa translate
type7 suppress-fa**.

`show ip ospf database nssa-external`

**Show**

Se alla LSA:er och RIB.

`show ip ospf database`
`show ip ospf rib`
`show ip ospf topology-info`

Kolla vilka LSA:er en viss nod annonserar ut.

`show ip ospf database adv-router `<RID>

-   **Others:** Typ 6 (MOSPF) och 8 stöds inte på Cisco-routrar och 9-11
    är Opaque.

Area types
----------

Att dela upp sitt nätverk i OSPF-areor är grunden för att göra OSPF mer
skalbart eftersom det sparar på SPF-beräkningar. Med dagens CPU:er kan
dock areor bli rätt stora innan det blir nödvändigt att dela upp det.
Förutom vanliga areor finns det flera andra typer av areor.

**Stub**
Alla areor behöver inte känna till alla externa nätverk. Då kan man
reducera overhead genom att ha areor där man endast skickar in LSA typ
3. Dvs det finns ingen ASBR och LSA typ 4 och 5 stoppas vid ABR. Skulle
det komma en LSA 4/5 från någon så ignoreras den. För att hitta ut ur
arean så skickar ABR:er in default route med en LSA typ 3.

`router ospf 1`
` area 1 stub`

*Stub bit is sent in hello packets*

**Totally Stubby**
Totally stubby är samma som stubby fast alla LSA typ 3 blockas också
förutom default routen. Inga LSA typ 3,4,5 gör att LSDB reduceras
ytterligare.
ABR

`area 1 stub no-summary`

Others

`area 1 stub`

**NSSA**
Om man vill effektivisera OSPF samtidigt som man behöver injicera in
routes från något annat protokoll genom någon router i en stubby area så
kommer det inte att funka eftersom LSA 4/5 ignoreras. Då kan man använda
en not-so-stubby area. Då sätter routrarna N-biten i hellos och skapar
ASBR typ 7 LSA:er istället. NSSA är en kompromiss som tillåter att
externa routes kan laddas upp till backbone-arean medans all information
från övriga areor ej behöver tas in i arean. I en NSSA kommer inte
default routen att annonseras default som i övriga stubby areas.

`router ospf 1`
` area 1 nssa`
` area 1 nssa default-information-originate`

**NSSA Totally Stubby**
NSSA Totally Stubby är samma som NSSA fast alla LSA typ 3 blockas också
förutom default routen, samt att default routen injiceras default. Inga
LSA typ 3,4,5. Ett ben i area 0 krävs för detta kommando.

`area 1 nssa no-summary`

**Transit**
Non-backbone areas kan användas för inter-area transit om det finns en
kortare väg igenom dem. Transit är på default men går att stänga av.

`router ospf 1`
` no capability transit`
`show ip ospf | i transit`

Nätverkstyper
-------------

Det finns olika typer av nätverk och pga hur OSPF fungerar måste man
konfigurera det lite olika beroende på typ. T.ex. DR/BDR election hålls
endast på broadcast och NBMA. Om frame relay används måste DR och BDR ha
PVC till alla andra routrar annars får inte alla uppdateringar. På
multiaccess och point-to-point (ethernet) används default nätverkstypen
BROADCAST. Beroende på nätverkstyp behövs **neighbor**-kommandot
användas eller ej, regel är non-broadcast needs neighbors.
Point-to-multipoint interface annonseras som /32:or av effektivitetsskäl
och lämpar sig väl om man kör OSPF över
[Cisco_L2VPN\#VPLS](/Cisco_L2VPN#VPLS "wikilink").

`show ip ospf interface | i protocol|Network Type`

Ändra nätverkstyp på ett interface. Det behöver tekniskt sett inte vara
samma på båda sidor sålänge det som behövs matchar, t.ex. timers.

`interface gi0/0`
` ip ospf network ?`

Loopback annonseras default som stub endpoint (/32), detta ändras med
nätverkstyp point-to-point.

`interface lo0`
` ip ospf network point-to-point`

### Designated Router

OSPF optimerar flooding-processen på multiaccess-länkar genom att
använda *designated routers* och *backup designated routers*. Annars
hade varenda router på ett sådant segment behövt upprätta fulla
grannskap med alla andra. Med en DR räcker det med att alla utbyter LSDB
endast med den, detta resulterar i mindre trafik. Varje router har fullt
grannskap med DR och BDR, 2-way med övriga. DR har två syften, det är
också så att det är DRs som skapar typ 2 LSAn som representerar
multiaccess-segmentet, annars hade det behövts för varje grannskap och
det hade inte blivit någon vacker LSDB.

Behöver en DR skicka ut en LSU gör den det till 224.0.0.5 som alla
DROther lyssnar på. Behöver en DROther skicka en uppdatering gör den det
till 224.0.0.6 som DR och BDR lyssnar på (det är av denna anledning det
behövs en BDR). Alla enheter som får en LSU ackar den med en unicast
LSAck till avsändaren, med undantag om LSUn kom från sig själv. I
nätverkssegment utan DR används 224.0.0.5 för allt.

DR election görs mellan 2-way och ExStart i och med att Hellos
innehåller DR/BDR om det finns. Om det kommer in en Hello med DR satt
till 0.0.0.0 betyder det att det inte finns någon DR än, t.ex. efter ett
outage. Då väntar routern en liten stund för att ge andra en chans att
komma upp. Detta kallas OSPF wait time och är ställt till samma som Dead
time på det interfacet. Under wait time lyssnar routern in RID och
prioritet från sina grannar. Val av DR/BDR görs först efter wait time är
över. Election görs lokalt på routern utifrån de värden som kommit in.
Dock slutar det alltid med att alla har samma.

Finns det en DR RID i ett Hello som kommer in så har någon annat gjort
valet och man kan direkt hoppa till election, dvs skippa resten av wait
time. Det som görs då är att man fyller den roll som ej är fylld, t.ex.
BDR genom att ta den högsta prioriteten och högsta router id som man
känner till. Detta gör att det inte finns någon preemption. Däremot kan
det tillfälligt existera routrar som är klara med election och som har
kommit fram till olika slutsatser. Då hålls election igen och man byter
DR och BDR till de med högst prio/id när man upptäckte krocken. Om man
kör samma prio på alla och stöter på att det inte högsta RID som är DR
är det för att den med lägre RID har kommit upp först. Det finns som
sagt ingen preemption.

Alla routrar med OSPF priority 1-255 är med i election, 1 är default och
sätter man 0 ignoreras DR/BDR election på den enheten som därmed aldrig
kan bli DR. Det är viktigt att DR kan nå alla andra vilket inte är
fallet i en hub-and-spoke-topologi där en spoke är DR, se även [Cisco
DMVPN](/Cisco_DMVPN "wikilink").

`interface gi0/0`
` ip ospf priority 50`

Även om det inte upptäcks några grannar på ett interface där DR election
vanligtvis hålls så kommer OSPF ändå hålla valet med sig själv som
vinnare, det väntas alltså inte på grannskap först. Om det däremot
endast finns en OSPF-router på ett segment så kallas detta stub network
och ingen LSA typ 2 kommer att genereras för det är onödigt utan då blir
nätverksadressen och subnätmasken en LSA typ 1 som floodas.

Konfiguration
=============

Routrar måste ha ett OSPF-id för att kunna skicka meddelanden, på
Ciscoenheter väljs ID enligt följande ordning:

1.  router-id kommandot
2.  Högsta IP-adressen på ett no-shut loopback interface (som ej är
    assignat någon annan OSPF-process)
3.  Högsta IP-adressen på ett no-shut interface (som ej är assignat
    någon annan OSPF-process)

Interfacen behöver inte vara nåbara eller ha något med OSPF att göra
utan alla interface jämförs. ID ändras endast när processen startas om.

router-id for this OSPF process (in IPv4 address format)

`router ospf 1`
` router-id 1.1.1.1`

**Administrative Distance**

`router ospf 1`
` distance ospf intra-area 110 inter-area 110 external 110`
`show ip protocols | i Distance`

Advertise a maximum metric so that other routers do not prefer the
router as an intermediate hop for 60 seconds.

`max-metric router-lsa on-startup 60`

**MTU mismatch**

`ip ospf mtu-ignore`

**Allmänna rekommendationer**

-   Set your maximum LSA settings to keep from killing weak boxes
    (**max-lsa**)
-   Baseline your network so you know how many LSAs normally float
    around
-   Configure LSA warnings to alert of problems
-   Crash each type of box on your network in a lab environment so you
    know what it will do under stress.

**MPLS**
Om man kör OSPF kan man autoenablea LDP på alla OSPF-interface. Se även
[Cisco MPLS](/Cisco_MPLS "wikilink") och [Segment
Routing](/Cisco_SR "wikilink").

`router ospf 1`
` mpls ldp autoconfig `
`show ip ospf mpls ldp interface`

**IP unnumbered**
Man kan köra IP unnumbered med OSPF och det finns ett network statement
som matchar IP-adressen på primär-interfacet så kommer båda interfacen
att användas av OSPF i den valda arean. När man använder unnumbered
kommer routern att ignorera source IP address i hello-paketen vilket
annars fungerar som en check så att inte vilket paket som helst
accepteras utan det ska komma från det subnät som det mottagande
interfacet sitter i. Man kan ha loopback och fysiska interface i olika
areor, dock kommer man att annonsera samma prefix i fler än en area.

`interface gi0/1`
` ip unnumbered Loopback0`
` ip ospf network point-to-point`
` ip ospf 1 area 1`

Adjacency
---------

Logga ändringar i neighbor state, detta är på default.

`router ospf 1`
` log-adjacency-changes`
`show ip ospf events`

Styr grannskap/uppdateringar med passive-interface

`passive-interface default`
`no passive-interface [interface]`
`show ip ospf interface | i Ethernet|Passive`

**Unicast**
Specificera granne manuellt, detta måste göras på NBMA och
point-to-multipoint nonbroadcast. Det räcker att göra detta på ena sidan
för att grannskap ska bildas men best practice är att köra detta på båda
sidor.

`router ospf 1`
` neighbor 10.0.0.2`

Per neighbor cost/metric

`neighbor 10.0.0.5 cost 1000`

Man kan sätta prioritet på sina grannar om man kör unicast. Default är
detta 0 men om man har flera neighbor statements och någon har icke-noll
så kommer routern att först skicka Hellos till denna. Endast när DR/BDR
election är klart så börjar det skickas Hellos till de övriga grannarna.
Detta är en mekanism som ökar chansen att DR och BDR blir de routrar man
vill. OBS detta har inget med vinnare av DR/BDR att göra.

`router ospf 1`
` neighbor 10.0.0.5 priority <0-255>`

**Verify**

`show ip ospf neighbor`
`show ip ospf interface brief`
`show ip ospf neighbor detail | i interface`
`ping 224.0.0.5`

Clearing routing process

`clear ip ospf process`
`debug ip ospf adj`

**GTSM**
TTL Security Check kan konfigureras per process eller per interface och
gäller både unicast och multicast. Dessa kommandon har ingen inverkan på
virtual links eller sham links utan det görs med *area virtual-link
ttl-security* och *area sham-link ttl-security*.

`router ospf 1`
` ttl-security all-interfaces`
`interface gi2`
` ip ospf ttl-security `

**Graceful restart**
En router kan starta om OSPF-grannskap och ändå fortsätta forwarda paket
som vanligt med hjälp av Graceful OSPF Restart (RFC 3623). Cisco har
även en egen variant av detta som kallas NSF (Non Stop Forwarding) men
IOS har stöd för båda varianterna. Den som restartar skickar grace-LSA
och hamnar i *restart mode* och directly connected grannar måste stödja
*helper mode* för att detta ska lira. Helpers måste ignorera att det
uteblir Hellos under antydd period och låtsas som att grannskapet är
uppe och DR är densamme. Överskrids tidsgränsen rivs adjacency direkt.
NSF-aware (helper support) finns på de flesta enheter och är på default,
*nsf ietf/cisco helper* medans NSF-capable finns på high-end
plattformar. GR/NSF utnyttjar att modernare enheter sköter data plane
och control plane i olika hårdvara.

`router ospf 1`
` nsf ietf`
` nsf cisco`

`show ip ospf nsf`

NSR är en intern mekanism som låter standby RP ta över etablerade
sessioner vid en switchover.

` nsr`
`show ip ospf nsr`

**Graceful shutdown**
Droppa adjacencies, flusha LSA:er och skicka ut Hello med tom neighbor
list för att trigga att grannens adjacency går direkt till Init state,
kanske inte så graceful men det heter så ändå.

`router ospf 1`
` shutdown`

Per interface

`int gi2`
` ip ospf shutdown`

### Authentication

Klassisk OSPF authentication är none/null, clear-text eller MD5. Default
är none och man slår på det per interface eller per area. Man kan ha
multipla nycklar per interface, då skickas det multipla OSPF paket
parallellt vilket gör att grannskap ej går ner under key rotation. Detta
pågår tills båda sidor har samma nyckel som senast konfigurerad, dvs key
ID måste matcha men det spelar ingen roll för vilken som är att föredra
utan det är youngest key. Det går även att köra authentication på
virtual links, se det stycket.

Enable clear-text authentication on area 0

`router ospf 1`
` area 0 authentication`
`interface gi0/1`
` ip ospf authentication-key [password]`

Enable MD5 authentication on area 0.

`router ospf 1`
` area 0 authentication message-digest`
`interface gi0/1`
` ip ospf message-digest-key 10 md5 [password]`

Enable MD5 authentication on an interface

`interface gi0/1`
` ip ospf authentication message-digest`
` ip ospf message-digest-key 10 md5 [password]`

Verify

` show ip ospf interface | i Ethernet|authentication`

**Extended cryptographic authentication** (RFC 5709) finns i modernare
implementationer av OSPF och har stöd för key-chains och SHA-HMAC.
Nyckel med högst id används ifall det finns flera nycklar som är aktiva.
Cryptographic algorithm + key bildar SA.

`key chain HACKER`
` key 1`
`  key-string SECRET`
`  cryptographic-algorithm hmac-sha-512`

Per interface, det finns inget area-kommando som slår på key-chain auth
på alla interface som vid klassisk konfiguration.

`int gi2`
` ip ospf authentication key-chain HACKER`

### Multiarea Adjacency

Med OSPFv2 Multiarea Adjacency kan man konfigurera en länk för optimal
routing i flera areor. Varje multiarea interface annonseras som en
point-to-point unnumbered link och fungerar som en logisk konstruktion
över det primära interfacet. Det upprättas grannskap med multiarea
interface på andra sidan och detta är oberoende av neighbor state på det
primära interfacet. Alla OSPF-parametrar (t.ex. autentisering) ärvs från
det primära. Det går endast att konfigurera multiarea adjacency på
interface som har två OSPF speakers, så på ethernet måste det
konfigureras som network point-to-point.

`interface gi2`
` ip address 10.0.0.1 255.255.255.0`
` ip ospf 1 area 0 `
` ip ospf network point-to-point `
` ip ospf multi-area 2`

`show ip ospf 2 multi-area`

Default Routing
---------------

Kräver gateway of last resort.

`default-information originate`

Om man inte har någon gateway of last resort kan man ändå annonsera ut
en default route.

`default-information originate always`

**NSSA**
En NSSA ABR genererar inte en default route by default (om den inte
konfas som totally stubby) eftersom man inte vet om gateway of last
resort ska vara i en annan area eller externt (type 7). En NSSA ASBR
måste ha en default route i routingtabellen för att kunna skicka ut en
default route. En NSSA ABR behöver inte det:

`area 1 nssa default-information-originate`

**Conditional**
Med hjälp av en route map kan man annonsera en default route när ett
visst kriterie är uppfyllt.

`default-information originate route-map TRACK_PREFIX`

Summarization
-------------

OSPF-routrar inom samma area måste ha identiska LSDB efter att flooding
är färdigt vilket gör att summering endast tillåts vid ABR eller ASBR.
Med hjälp av **not-advertise** i slutet av kommandona kan man styra om
summeringen ska fungera som filtrering, då varken de mer specifika
prefixen eller aggregeringen annonseras.

**ABR**

`router ospf 1`
` area 10 range 10.10.0.0 255.255.252.0`

Area 10 säger var summeringen kommer ifrån så denna aggregering skickas
till alla andra areor. Cost för summeringen tas från den component route
med lägst metric om man inte anger något specifikt.

**ASBR**

`router ospf 1`
` summary-address 10.10.0.0 255.255.252.0`

Konfigureras vid redistributionspunkt och summeringar ärver attribut
från component routes.

**Discard**
Default installeras det en discard route när man summerar för att
förhindra att det forwarderas trafik som man inte har någon specifik
route för.

`no discard-route external|internal`

Convergence
-----------

Tuning protocol parameters per interface.

`ip ospf hello-interval `*`seconds`*
`ip ospf dead-interval `*`seconds`*
`ip ospf retransmission-interval `*`seconds`*
`ip ospf transmit-delay `*`seconds`*

Fast Hellos, dead-interval minimal = 1 sek.

`ip ospf dead-interval minimal hello-multiplier 3`

Timers: LSA & SPF

`router ospf 1`
` timers throttle spf 100 1000 10000`
` timers pacing flood 50`
` timers pacing retransmission 75`
` timers throttle lsa all 10 4000 6000`
` timers lsa arrival 2000`
`show ip ospf | i msec`

Med Group Pacing kan LSA:er "samåka" i refresh-paket.

**SPF Prefix Priority**
Man kan välja vilka prefix som SPF-algoritm ska köra först. Man skapar
en route-map som matchar på route-type, prefix-list eller route-tag.

`route-map PREFIX-PRIORITY permit 10`
` match tag 100`

`router ospf 1`
` prefix-priority high route-map PREFIX-PRIORITY`

Verify

`show ip ospf rib detail`

**iSPF**
SPF-algoritmen behöver inte köras för alla länkar varje gång det sker en
topologi-förändring. Med incremental SPF körs endast algoritmen för de
delar som har påverkats av förändringen för att spara CPU-cykler. Detta
går att styra individuellt på enheterna med *ispf*-kommandot. Det kan
vara svårt att veta exakt hur mycket skillnad detta gör men generellt ju
större topologi ju större skillnad. OBS iSPF är inte längre supporterat
i IOS.

`router ospf 1`
` ispf`
`show ip ospf | i Incremental`

**BFD**
Se även [BFD](/Cisco_BFD "wikilink").

`router ospf 1`
` bfd all-interfaces`

Disable per interface

`int gig2`
` ip ospf bfd disable`

### LSDB Optimization

**Prefix Suppression**
För att få Loopback till Loopback-konnektivitet mellan alla routrar med
minimal belastning på routingtabellen kan man skippa att ha med
OSPF-länknäten i RIB. Alla noder bör stödja detta.

Global

`router ospf 1`
` prefix-suppression`

Per interface

`interface gi2`
` ip ospf prefix-suppression`

Verify

`show ip ospf interface | i Ethernet|Prefix-suppression`

**Flooding Reduction**
OSPF flood reduction stoppar det normala floodandet av LSAer genom att
sätta DoNotAge (DNA) biten vilket gör att de inte behöver refreshas med
jämna mellanrum.

`interface Gi2`
` ip ospf flood-reduction`

### LFA

Eftersom OSPF-databasen är identisk på alla routrar i samma area har man
modifierat SPF så att man lokalt kan köra SPF-algoritmen men med en
granne som rot. Detta gör att man kan hitta alternativa loopfria vägar
även i komplexa topologier. Man kan specificera flera kriterier för
vilka alternate path som ska väljas, t.ex. använd ej de som använder
samma interface, next-hop eller SRLG. Man måste använda
[MPLS](/Cisco_MPLS "wikilink") för att kunna dra nytta av Loop-Free
Alternate Fast Reroute och IOS supporterar endast per-link LFA. The high
priority enables FRR for /32 prefixes only, the low priority enables FRR
for all prefixes. The fast-reroute keep-all-paths option keeps all
information in the table, including paths that were not chosen. When an
area is specified, external routes are not a candidate for FRR. This is
because they do not belong to an area.

Single Hop LFA / IP FRR.

`router ospf 1`
` fast-reroute per-prefix enable prefix-priority low`
` fast-reroute per-prefix enable area 0 prefix-priority high`
` fast-reroute keep-all-paths`

`show ip ospf fast-reroute`
`show ip ospf fast-reroute prefix-summary`
`show ip route repair-paths`

Med hjälp av Remote LFA Tunnel kan man tunnla trafik loopfritt (i nästan
alla topologier) till routrar flera hop bort utifrån lokala beräkningar.
Detta stöds endast i default VRF:en och kräver MPLS.

`mpls ldp explicit-null`
`mpls ldp discovery targeted-hello accept`
`router ospf 1`
` fast-reroute per-prefix remote-lfa tunnel mpls-ldp `

`show ip ospf fast-reroute remote-lfa tunnels`

Interface options:
Om ett interface inte ska kunna användas för backup paths.

`ip ospf fast-reroute per-prefix candidate disable`

Primary routes som pekar på detta interface kommer inte att bli
skyddade.

`ip ospf fast-reroute per-prefix protection disable`

Filtering
---------

Non-local filtering för OSPF kan endast göras på ABR och ASBR.

**Intra-area**
Filtering påverkar inte LSDB eller flooding utan endast det som hamnar i
RIB. Det går att göra med en distribute-list dock bör alla routrar vara
konfade likadant annars kan det bli blackholing.

`access-list 1 deny 172.16.3.1`
`access-list 1 permit any`
`router ospf 1`
` distribute-list 1 in`

Alternativt

`summary-address 10.0.0.0 255.255.255.0 not-advertise`

Administrative Distance, filtrering kan göras på Advertising Router.

`access-list 10 permit 10.0.0.0 0.0.0.255`
`router ospf 1`
` distance 255 `<RID>` 0.0.0.0 10`

LSA Type-3 Filtering

`area 1 range 10.0.0.0 255.255.255.0 not-advertise`

**Inter-area**

`ip prefix-list PFXLIST seq 5 deny 10.10.0.0/24`
`ip prefix-list PFXLIST seq 10 permit 0.0.0.0/0 le 32`

`router ospf 1`
` area 1 filter-list prefix PFXLIST out|in`

out betyder att det som lämnar area 1 filtreras, in betyder filtrering
av det som skickas in i area 1.

**Database Filtering**
Man kan stoppa OSPF-processen från att skicka LSA:er. Detta fungerar på
network type point-to-multipoint och görs per interface alternativt
neighbor. Det bör endast användas där all flooding är unnecessary, t.ex.
NBMA subnets där det finns många routrar.

`interface gi2`
` ip ospf database-filter all out`

**Route-Map**
Med en route-map kan man matcha på interface, ip-adress, ip next-hop, ip
route-source, metric, tagging och route-type. Eftersom det är en
distribute-list påverkar detta endast lokala routingtabellen.

`access-list 1 permit `<prefix>
`access-list 2 permit `<RID>

`route-map DENY_R2 deny 10`
` match ip address 1`
` match ip next-hop 2`

`route-map DENY_R2 permit 20`

`router ospf 1`
` distribute-list route-map DENY_R2 in`

Virtual Link
------------

OSPF kräver att alla areor är anslutna till area 0. I vissa scenarior
kan det vara svårlöst och då kan man använda sig av virtual links för
att tunnla OSPF-paket över en annan nonbackbone-area. ABR:n som ej har
en direktanslutning till area 0 kan på så sätt få en full kopia av
LSDB:n i area 0. Det har inget med data plane att göra utan endast OSPF
control plane. En virtual link syns i LSDB som en unnumbered
point-to-point länk och LSU:er som skickas har DoNotAge-biten satt.
Arean som tunneln går över blir en transit area och den måste vara en
vanlig area, dvs ingen stub eller nssa. Detta pga av att data plane går
därigenom som vanlig routad trafik så den arean måste känna till allt,
intra-, inter- och external routes. VL fungerar som en demand circuit
därför bör man ta ner och upp interfacet vid konfigurationsändringar.
Interface MTU skickas ej med i DBD-paket över en VL. Virtual link är
rekommenderat som backup- eller temporär anslutning. Man kan även
använda VL för att koppla ihop area 0 om den finns på flera ställen.

**R1** ABR mellan area 0 och 1

`router ospf 1`
` network 10.0.1.0 0.0.0.255 area 1`
` network 1.1.1.0 0.0.0.255 area 0`
` area 1 virtual-link 3.3.3.3  #Router-ID`

**R3** ABR mellan area 1 och 2

`router ospf 1`
` network 10.0.1.0 0.0.0.255 area 1`
` network 10.0.2.0 0.0.0.255 area 2`
` network 3.3.3.0 0.0.0.255 area 2`
` area 1 virtual-link 1.1.1.1  #Router-ID`

**Verify**

`show ip ospf virtual-links`
`show ip ospf border-routers`

**Authentication**

`area 2 virtual-link 2.2.2.2 authentication message-digest message-digest-key 10 md5 CISCO`

Redistribution
--------------

Default seed metric: 1 för BGP, 20 för övrigt.

`default-metric 20`

Med OSPF behövs ordet subnets annars redistribueras endast classful
networks. I nyare IOSer kan "subnets" auto-konfas i vissa lägen, man får
kolla konfigurationen.

`redistribute maximum-prefix 100`

**NSSA**
En NSSA-redistribution kan man styra om den ska nå endast NSSA-arean
eller får göras om och skickas vidare till andra areor. Routrar som är
med i flera areor gör detta automatiskt.

`redistribute isis nssa-only`

**Static**

`redistribute static`

Notera att default route inte kan redistribueras med *redistribute
static*, inte ens om en route-map används utan **default-information
originate** bör användas.

**[RIP](/Cisco_RIP "wikilink")**

`router ospf 1`
` redistribute rip subnets`

**[EIGRP](/Cisco_EIGRP "wikilink")**

`router ospf 1`
` redistribute eigrp 1 subnets tag 90`

**[BGP](/Cisco_BGP "wikilink"),** seed metric för bgp är 1. När man
redistribuerar prefix från BGP så sätts senaste AS i pathen som route
tag i LSA:n.

`router ospf 1`
` redistribute bgp 100 subnets`

NX-OS
-----

Här följer [Nexus](/Cisco_Nexus "wikilink")-specifik syntax. Några
grundläggande skillnader mot IOS är att referensbandbredden för cost
default är 40Gbps, Loopback0 väljs som Router-ID oavsett IP, det finns
inget network-kommando, loopbacks är passive default och man kan konfa
flera VRF:er under samma OSPF-process.

`feature ospf`

`router ospf 1`
` log-adjacency-changes`
` bfd`

`interface loopback0`
` ip router ospf 1`

`interface Ethernet1/1`
` ip router ospf 1`

Maintenance mode

`router ospf 1`
` isolate`

Verify and troubleshoot

`show run ospf`
`show ip ospf neighbors`
`show ip ospf 1 event-history rib `
`show ip ospf 1 event-history redistribution`

IOS-XR
------

En skillnad emot IOS är att External LSA:er installeras i RIB även fast
forwarding address inte är lärd av ospf.

Här följer [IOS-XR](/Cisco_IOS-XR "wikilink")-specifik syntax.

`router ospf 1`
` log adjacency changes detail`
` router-id 100.0.0.10`
` bfd minimum-interval 100`
` bfd fast-detect`
` bfd multiplier 3`
` mpls ldp sync`
` mpls ldp auto-config`
` max-lsa 12000`
` security ttl`
` auto-cost reference-bandwidth 1000000`
` max-metric router-lsa on-startup 30`
` max-metric router-lsa on-proc-restart 10`
` area 0`
`  authentication message-digest`
`  message-digest-key 1 md5 encrypted 12411A1A0D13271D030A791111`
`  fast-reroute per-prefix remote-lfa tunnel mpls-ldp`
`  !`
`  interface Loopback0`
`   passive enable`
`  !`
`  interface HundredGigE0/0/0/0`
`   network point-to-point`
`   flood-reduction enable`

Verify

`show run router ospf`
`show ospf`
`show ospf neighbor`
`show ospf interface brief`
`show ospf database`

[Category:Cisco](/Category:Cisco "wikilink")