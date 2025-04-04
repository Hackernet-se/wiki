---
title: Cisco EIGRP
permalink: /Cisco_EIGRP/
---

EIGRP är ett avancerat distance vector routingprotokoll. Det är
utvecklat av Cisco och har varit helt properitärt men är sedan 2013
släppt, dock bara som Informational RFC. EIGRP använder ett eget
IP-protokoll (88) på lager 4, Reliable Transport Protocol. Det finns
flera skillnader som gör EIGRP avsevärt mycket bättre än
legacy-protokollet IGRP. IGRP stödjer inte VLSM, discontiguous networks,
manuell summering eller grannskap. Det kan uppstå routing loopar,
konvergerar långsamt och retransmittar inte tappade paket. IGRP fattar
inte heller 0.0.0.0/0 som en default route. För topologiuträkningar
används DUAL och EIGRP använder både unicast och multicast. Kolla
versioner på EIGRP-komponenter: *show eigrp plugins*

**Type:** Distance Vector

**Algorithm:** DUAL

**AD:** 90, 170

**Protocols:** IP

**Packets:** 7

Packets
-------

EIGRP använder 7 olika typer av RTP-paket för att kommunicera.
EIGRP-paket byggs med TLV:er för att göra det flexibelt. Förutom route
entries innehåller de även fält för DUAL-processen,
multicast-sekvensering och IOS-version.

-   **Hello:** Skickas till multicast 224.0.0.10/FF02::A var 5:e sekund
    för keepalive samt innehåller grundläggande info så som AS, IP-nät,
    K-värden, authentication för att grannskap ska kunna upprättas.

<!-- -->

-   **Acknowledgement:** De flesta typer av paket är viktiga att de
    kommer fram som de ska, därför finns det en Acknowledgement-mekanism
    i EIGRP. Följande pakettyper kommer att besvaras med en Ack: Update,
    Query, Reply, SIA-query och SIA-reply. Pga detta kallas de paketen
    för Reliable Packets. Acknowledgement skickas alltid med unicast och
    om det är ett Hello-paket så är det ett tomt Hello som endast
    innehåller sekvensnumret för Acken. Det går även att skicka med
    sekvensnumret för acken med andra paket, t.ex. om en router både
    behöver skicka en uppdatering och acka ett paket kan det göras i
    samma utskick. Alla paket kan användas för Ack sålänge de är
    unicast.

<!-- -->

-   **Update:** Under den första fasen i ett grannskap när hela
    databasen ska utbytas används unicast. Därefter används multicast,
    förutom på point-to-point och med statiska grannar. Alla Updates
    ackas.

<!-- -->

-   **Query:** Med Query-paket kan en router ta hjälp av sina grannar
    för att hitta bästa routen till en destination. Det skickas default
    ut med multicast på multiaccess-segment. Om en granne inte ackar
    Queryn kommer Queryn att skickas till den med unicast. Det är även
    unicast på point-to-point-länkar eller ifall man har manuellt
    konfigurerade grannar.

<!-- -->

-   **Reply:** Används som svar på Query-paket och innehåller info om
    distance till det som har frågats efter.

<!-- -->

-   **Stuck-in-Active Query:** Om en granne tar lång tid på sig att
    svara på en Reply kan man ta reda på om grannen är död eller jobbar
    på Replyen genom att skicka en SIA-Query. En SIA-Query kommer alltid
    att svaras på omedelbart även om det sker routing-omräkningar.

<!-- -->

-   **Stuck-in-Active Reply:** Ett svar på en SIA-Query kallas SIA-Reply
    och får man tillbaka ett sånt vet man att grannen lever och då
    resettas timern för computation, detta ger grannen lite mer tid. Man
    kan konfigurera hur länge en route kan vara aktiv, default är 3
    minuter:

`timers active-time `<minutes>
`show eigrp protocols | i Active`

Verify

`show ip eigrp traffic`

Default får 50% av interfacebandbredden användas för EIGRP-trafik.

`ip bandwidth-percent eigrp 100 50`

Path Selection
==============

**Computed Distance:** den totala metricen för att nå destination via en
särskild granne, dvs reported distance från granne plus distance till
grannen.

**Feasible Distance:** en "notering" av den lägsta kända computed
distance sedan routens senaste övergång från Active till Passive. FD
behöver med andra ord inte nödvändigtvis vara samma som nuvarande CD. FD
har routrarna koll på lokalt för att säkerställa loopfria vägar, det
skickas aldrig till någon annan.

**Advertised/Reported Distance:** hur långt en granne rapporterar
(metric) att det är till en destination router, dvs grannens bästa väg.

**Feasibility Condition:** Om FD är satt till t.ex. 2000 så vet routern
att någongång fanns det en gångbar och loopfri väg till destination med
distance så lågt som 2000. Det betyder att alla grannar som
tillhandahöll denna väg måste ha varit ännu närmare destinationen, dvs
RD måste ha varit lägre än 2000. Alla grannar som hade distance 2000
eller lägre måste ha varit säkra att använda eftersom de aldrig skulle
skicka tillbaka det, varken direkt eller via någon annan. Om RD är
mindre än FD så vet man att det är en loopfri väg. Detta är en
requirement som måste uppfyllas för att en route ska kunna hamna i
routingtabellen.

**Successor:** de bästa routesen och som hamnar i routingtabellen.
Default är detta de med lägst metric och som uppfyller feasibility
condition.

**Feasible Successor:** alternativa (inte de bästa) routes som uppfyller
feasibility condition. EIGRP får använda dessa men gör inte det default.

Kolla CD, FD och RD.

`show ip eigrp topology`

Kolla grannar som inte uppfyller feasibility condition.

`show ip eigrp topology all-links`

### DUAL

När EIGRP tappar en successor kollas det genast i topologitabellen efter
en Feasible Successor. Finns det en blir den successor och det meddelas
till övriga grannar. Detta kallas local computation och går fort samt är
CPU-snålt. Finns det däremot ingen skickas det ut queries till alla
grannar efter alternativa vägar. Routen blir aktiv och detta kallas
diffused computation. Har grannen kännedom om en annan path svarar den
på queryn men om den inte har det får den i sin tur fråga sina grannar,
och så vidare. Om mottagande router inte har några andra grannar att
fråga svarar den direkt med metric satt till inifinty. En route är aktiv
tills alla har svarat. Det bästa sättet att lösa Stuck-in-Active problem
är en strukturerad IP-plan för att kunna summera manuellt så mycket som
möjligt. Ju mer summering ju mindre måste EIGRP jobba vid konvergens.

`show ip eigrp topology active`

Stuck in active?

`debug eigrp packet terse`

Med named mode kan slå graceful restart för stuck-in-active neighbors.

`address-family ipv4 as 100`
` soft-sia`

Metrics
-------

EIGRP använder flera typer av metrics, så kallade *component metrics*.
De klassiska är bandwidth, load, delay, reliability, MTU och hop count.
De första fyra kan användas för att räkna fram composite metric aka cost
eller distance.

**Bandwidth:** är en statisk metric som sätts per interface med
*bandwidth*-kommandot. Sätter man ingen bandwidth manuellt så kollar
routern på vad ethernet har länkat upp i. För att räkna ut
bandwidth-metricen till en destination tar man den lägsta bandwidthen
längst vägen. Man jämför vad grannen har skickat för bandwidth med ens
egen bandwidth till den grannen och använder det lägre värdet till DUAL
samt vidareannonsering. På så sätt känner man till den lägsta
bandbredden längs vägen. Det är inte rekommenderat att påverka path
selection med hjälp av manuell bandwidth-konfiguration i
produktionsmiljö!

`interface gi0/3`
` bandwidth `<kbps>

**Load:** är ett dynamiskt värde som IOS sätter på interface. Eftersom
ingress och egress kan vara olika lastade hålls två skilda värden för
detta. För att räkna på detta till composite metric används högsta
Txload, routern jämför värdet den får in med sin Txload på det
interfacet och väljer det högre värdet. Det triggas ingen uppdatering
ifall load plötsligt skulle ändras. Denna metric används ej default.

`show interface gi0/3 | i load`

**Delay:** är en statisk metric som sätts per interface med
*delay*-kommandot. Detta är inget som dynamiskt ändras, t.ex. utifrån
paketstorlek, utan är en uppskattning av genomsnittlig fördröjning.
Sätter man inte detta manuellt så assignar IOS ett värde på varje
interface. För att räkna ut totalen till en destination så adderar man
värdet man får av sin granne med delayen på interfacet till grannen, dvs
all delay längs vägen adderas ihop. Med klassisk metric kan detta ha
1-167772214 tiotal mikrosekunder. 167772215 är infinite distance och med
detta kan man annonsera ut unreachable network. Det är så man löser
Split Horizon with Poisoned Revered och withdrawing a route, man skickar
det med delay 167772215 tiotal mikrosekunder.

`interface gi0/3`
` delay `<tens of microseconds>
`show interface gi0/3 | i DLY`

OBS Output är i microseconds.

**Reliability:** är ett dynamiskt värde som IOS sätter på interface. 255
är högsta och betyder 100% reliability. Detta skickas med i
EIGRP-paketen och det lägsta värdet är det som gäller till composite
metric, dvs man jämför värdet man får in med det man själv har på det
interfacet. Dock triggas ingen uppdatering ifall reliability plötsligt
skulle ändras. Denna metric används ej default.

`show interface gi0/3 | i reliability`

**MTU** skickas med i EIGRP-paketen men används ej på något sätt.

**Hop Count:** används som en säkerhetsmekanism. Går hop count över 100
(default) så är det unreachable vilket gör att oändliga loopar ej
uppstår. Det används ej på något sätt för path selection eller composite
metric.

**Composite metric**
Kolla composite och alla component metrics för ett prefix.

`show ip eigrp topology 10.2.2.0/28 | b Composite`
`     Composite metric is (130816/128256), route is Internal`
`     Vector metric:`
`       Minimum bandwidth is 1000000 Kbit`
`       Total delay is 5010 microseconds`
`       Reliability is 255/255`
`       Load is 1/255`
`       Minimum MTU is 1500`
`       Hop count is 1`

**Wide Metrics**
Det finns Classic metrics och Wide metrics. De gamla metricen fungerar
för hastigheter upp till 1Gbps eftersom då är bandwidth satt till högsta
värdet och delay till det lägsta. Detta leder till att classic metrics
inte kan skilja på t.ex. 1G och 10G. Wide Metrics löser detta och stöds
i Named Mode och om det används är Metric Version = 64bit samt att det
finns en K6.

`show ip protocols | i Metric`

Eftersom wide metrics kan producera metrics som är större än 32-bitar
och RIBen stödjer metrics upp till 32-bitar dividerar man det med 128
innan det hamnar i RIBen samt presenteras av IOS show-kommandon. Detta
går att ändra per adressfamilj.

`address-family ...`
` metric rib-scale 128`

**Throughput:** (bandwidth) fungerar på exakt samma sätt men nu är
referensbandbredden 655.36 Tbps.

**Load:** Samma som classic.

**Latency:** (delay) fungerar på samma sätt men nu används picosekunder
istället för mikrosekunder.

**Reliability:** Samma som classic.

**MTU:** Samma som classic.

**Hop Count:** Samma som classic.

**Extended Metrics:** reserverad för framtida extensions. Finns Jitter,
Energy och Quiescent Energy men de används inte.

**Computation formula**

-   k1 = bandwidth
-   k2 = load
-   k3 = delay
-   k4 = reliability
-   k5 = MTU

Simplified default metric, legacy = 256 \* (10^7/bandwidth + delay/10)
Simplified default metric, wide = 65536 \* (10^7/bandwidth +
delay/1000000)

`show eigrp protocols | i Metric`

Ändra vilka metrics som ska användas för EIGRP-processen

`metric weights 0 1 0 1 0 0`

Konfiguration
=============

Ändrar man AD kommer alla grannskap att droppas och sättas upp på nytt.

`router eigrp 100`
` distance eigrp 90 170`

Logging av neighbor changes är på default

`show ip eigrp events type`

Modernare konfigurationsformat

` eigrp upgrade-cli`

**Router ID**
Alla EIGRP-instanser måste ha ett router id, dock kan flera processer ha
samma 32 bitars nummer (till skillnad från OSPF). Från början användes
RID för att förhindra routingloopar vid multipoint redistribution
eftersom man skickar med sin RID med de externa routes som man
annonserar in i EIGRP och på så sätt identifierar det originating
router. Har alla redistributionsroutrar samma RID blir det ingen loop
eftersom om man får in en route med samma RID som man själv har
discardas den. Numera används det också för intern EIGRP och man kan
alltid se Originating router på alla prefix.

ID väljs enligt följande ordning och interfacen behöver inte vara nåbara
eller ha något med EIGRP att göra utan alla interface jämförs.

1.  router-id kommandot
2.  Högsta IP-adressen på ett no-shut loopback interface
3.  Högsta IP-adressen på ett no-shut interface

ID ändras endast när processen startas om eller router-id-kommandot körs
men alla grannskap resettas vid RID-byte.

`show eigrp protocols | i Router-ID`

Kolla om routes droppas pga duplicate RID

`show eigrp address-family ipv4 events`

Debug

`debug eigrp packets hello`
`debug eigrp fsm`

Adjacency
---------

EIGRP upptäcker grannar dynamiskt och AS, K-values och authentication
måste matcha. Så fort man slår på EIGRP på ett interface börjar det
skickas Hello-paket till multicast 224.0.0.10/FF02::A var 5:e sekund. Så
fort ett Hello har tagits emot sätts grannen i pending state för att man
inte ska acceptera routing-uppdateringar innan man är säker på att det
finns bidirectional connectivity. Om det finns en EIGRP-router på andra
sidan kommer den att svara med ett Hello, sedan skickas en null update
som har satt initialization bit för att signalera att dra igång
initialization process. Då kommer en null update med init bit skickas
tillbaka som även ackar den första. När sedan den andra updaten har
ackats går grannskapet till "Up" och databassynkroniseringen drar igång.
När den är klar kommer endast inkrementella uppdateringar att skickas i
fortsättningen. log-neighbor-changes är påslaget default.

Interface vars IP-adress träffas av network-kommandot blir
EIGRP-enabled.

`network [ip-address] [wildcard-mask]`

Designate passive interfaces. Passive interfaces stoppar grannskap och
därmed inlärning av routes.

`passive-interface default`
`no passive-interface gi2`
`show ip eigrp interfaces detail`

Det går även att ändra timers per interface. Hold time säger hur länge
en router maximalt ska vänta mellan två EIGRP-paket från en granne.
Kommer inget paket blir grannen unreachable och DUAL informeras. Default
är denna tid tre gånger Hello interval, dvs 15 eller 180 sekunder
beroende på interfacetyp. Hold time ändras dock inte automatiskt ifall
man ändrar Hello time. Notera att detta inte är en inställning som
används lokalt utan ett "advertised value", om man sätter hold time
lägre än hello time kommer grannar att flappa.

`int gi0/0`
` ip hello-interval eigrp 100 `<sekunder>` `
` ip hold-time eigrp 100 `<sekunder>
`show ip eigrp 100 interfaces detail | i time`

Vissa nätverk stödjer inte broadcast eller multicast då måste man
manuellt konfigurera grannar och unicast används. När man konfigurerar
en granne så disableas multicast på det interfacet som används för
unicasten. Det går därför inte att kombinera unicast- och
multicastgrannskap på ett delat segment.

`router eigrp 10`
` neighbor 10.0.1.1 gi0/0 `

**Verify**

`show ip eigrp neighbor`

Outputen innehåller flera tal.

-   H (Handle): lokalt löpnummer för grannar.
-   SRTT (Smooth Round Trip Time): tid det tar att få tillbaka en ACK
    från granne, i millisekunder.
-   RTO (Retransmit Time Out): hur länge eigrp väntar på ack innan ett
    paket i kön skickas om, i millisekunder. Efter 16 omskickade paket
    utan ack blir det RETRY LIMIT EXCEEDED.
-   Q Cnt Num: paket som inte har ackats hamnar i kön. Detta är 0 i ett
    stabilt nätverk.

Om en router skickar en multicast-uppdatering som inte ackas av någon
kommer den att vänta RTO och sedan skicka en sequence TLV som instruerar
den routern att inte lyssna efter multicast-paket mer. Sedan skickar den
allt med unicast till den grannen tills den har ackat ifatt och då
skickas återigen en sequence TLV som säger att den ska lyssna på
multicast igen.

Route hold-timer bestämmer hur länge NSF-routrar som kör EIGRP ska hålla
routes för inaktiva grannar.

`timers graceful-restart purge-time 60`

### Authentication

MD5 authentication måste matcha för grannskap. Med Named mode finns även
stöd för SHA-256.

`interface [interface]`
` ip authentication mode eigrp md5`
` ip authentication key-chain eigrp [ASN] [name-of-chain]`

**Key rotation**
Key chain kan innehålla flera nycklar men endast lägsta aktiva nyckeln
används i EIGRP Hellos, Key ID måste därmed matcha.

`key chain ROTATION`
` key 10`
`  key-string CISCO10`
`  accept-lifetime 00:00:00 Jan 1 1993 00:15:00 Jan 1 2030`
`  send-lifetime 00:00:00 Jan 1 1993 00:05:00 Jan 1 2030`
` key 20`
`  key-string CISCO20`
`  accept-lifetime 00:00:00 Jan 1 2030 infinite`
`  send-lifetime 00:00:00 Jan 1 2030 infinite`

`show key chain`

### Troubleshoot

-   Uncommon subnet: de sitter inte i samma subnät.
-   K value mismatch: måste vara samma på båda sidor.
-   AS mismatch: måste vara samma på båda sidor.
-   Layer 2 issues.
-   Access-list issues.
-   NBMA.
-   Authentication issues.
-   Secondary addresses.

`ping 224.0.0.10`

Subnet mask behöver inte matcha för att grannskap ska bildas men däremot
blir topologitabellen felaktig vilket kan ställa till det
routingmässigt.

Clearing routing process. Behöver göras vid t.ex. byten av K-values.

`clear ip eigrp neighbors`

Unequal-Cost Load Balancing
---------------------------

Att det är möjligt med unequal-cost LB i EIGRP är pga att det finns
feasible successors. De har inte bästa vägen till destination men de är
garanterat loopfria. Variance multiplicerat med lowest metric blir
gränsen för hur dålig metricen får vara för att pathen ändå ska kunna
användas för load-sharing. Dvs variance säger hur många gånger sämre en
path får vara för att användas. För att ta reda på andelen trafik som
går över en viss länk måste man räkna högsta installerade metricen delat
med metricen på alla paths som används för närvarande och skriva ihop
dem för att få respektive andel.

`router eigrp 100`
` variance `<multiplier>
` maximum-paths 4  #Max är 32`
` traffic-share balanced`

Default är variance 1 och det betyder equal-cost load balancing. Det går
även begränsa antalet parallella paths som används. Använd
*traffic-share balanced* (som är default) annars blir det equal-cost LB
ändå.

`show ip protocols | i Maximum`

Verifiera per IP

`show ip route 90.0.0.1 | i share`

Summarization
=============

Man kan manuellt aggregera routes var som helst eftersom EIGRP är ett
distance vector routingprotokoll (*auto-summary* är avstängt default
sedan IOS 15 och bör aldrig användas). När en summary route annonseras
ut måste den finnas i routingtabellen för att undvika att det
forwarderas trafik för destinationer i summeringen som det inte finns
någon mer specifik route för så det skapas automatiskt en null route med
AD 5. Denna distance går att ändra i named mode med summary-metric under
topology base men sätt ej 255 då kommer inget att annonseras ut om inte
samma route kommer ifrån någon annan källa. Detta går därmed att nyttja
som conditional advertisment. För metric till summary route väljs den
lägsta metricen bland component routsen som ingår i summaryn. Försvinner
den component routen måste alla gås igenom igen för att välja en ny och
skicka ut, detta kan vara CPU-intensivt ifall det finns många component
routes. För att undvika detta kan man ställa en fast metric på varje
summary, detta görs under topology base med summary-metric också.

Summarization med EIGRP innebär en gräns för Queries eftersom en granne
till en router som summerar inte känner till de mer specifika näten och
när en router får in en Query för ett nät som inte finns i
topologitabellen så skickas det direkt tillbaka en Reply med
unreachable. Detta gör att en Query aldrig floodas vidare vilket leder
till att load och konvergeringstid minskar. En Query modifieras inte
heller någonstans.

Eftersom det är ett distance vector routingprotokoll görs summary per
interface. *Classic mode*

`interface gi2`
` ip summary-address eigrp 100 192.168.0.0 255.255.0.0`

**Leak-map**

`access-list 1 permit 192.168.2.0 0.0.0.0`
`route-map LEAK permit 10`
` match ip address 1`
`int gi2`
` ip summary-address eigrp 100 192.168.0.0 255.255.0.0 leak-map LEAK`

Finns det ingen route-map än som heter LEAK kommer endast summeringen
att annonseras.

Verify

`show ip protocols | s Summ`
`show ip route eigrp | i Null`

**Poisoned Floating Summarization**

`router eigrp 100`
` summary-metric 10.1.0.0/23 distance 255`

### Default route

Annonsera en default route ut på ett interface, inget annat kommer att
skickas på detta interface.

`interface gi2`
` ip summary-address eigrp 100 0.0.0.0 0.0.0.0`

Acceptera default routing information, detta är på default.

`default-information allowed`

Acceptera endast default route från specifik källa

`access-list 6 permit 10.0.0.0`
`router eigrp 100`
` default-information in 6`

Skicka ej default route

`no default-information allowed out`

Legacy

`router eigrp 100`
` network 10.0.0.0`
` ip default-network 10.0.0.0`

Convergence
===========

Optimization & Scalability. Detecting, notifying, calculating and
installing new routes.

### Stub Routing

Stub routing är designat för att göra EIGRP mer skalbart och stabilt.
Det används vanligtvis i hub-and-spoke topologier och konfigureras
endast på spokes. Då kommer spoke att lägga till en ny TLV i
Hello-paketen som säger stub router status. Det gör att spoken aldrig
kommer att annonsera ut något som den lär sig av någon EIGRP-granne för
att inte kunna riskera att bli Feasible Successor för något nätverk. Det
enda den annonserar ut är det man specificerar. I och med att grannarna
till en stub känner till att den är en stub router kommer de aldrig att
skicka EIGRP-Queries. Men en stub router skickar ut Queries som vanligt.
Det kan dock komma in Queries ändå, t.ex. en gammal IOS-enhet som inte
känner till stub kommer fortfarande skicka Queries eller om alla routrar
på ett segment är stub kommer det att skickas Queries som om ingen var
stub. När en Query kommer in behandlas den som vanligt om det som Queryn
handlar om faller inom det som är tillåtet för stub routern. Gör det
inte det så kommer det ändå att besvaras men med infinite metric oavsett
om routern känner till nätverket eller ej. Har man ett mixat segment
kommer EIGRP endast att skicka Queries till icke-stubs antingen genom
att unicasta till icke-stubs eller så kommer Conditional Receive mode
användas, det beror på antalet icke-stubs på segmentet.

Fördelar med Stub är att man undviker suboptimal routing i hub-and-spoke
topologier, routrar med dålig bandbredd blir aldrig transit router och
antalet Queries reduceras vilket leder till snabbare konvergens och
mindre SIA. Defualt för stub är (CONNECTED SUMMARY ) och grannskap
resettas vid omkonfiguration.

`router eigrp 100`
` eigrp stub ?`
`    connected   `
`    receive-only `
`    redistributed `
`    static  `
`    summary `

Undantag läggs med en leak-map. Man får hålla koll på
route-aggregeringar när man kör stub för de mer specifika routsen
annonseras default.

` router eigrp 100`
`  eigrp stub leak-map `*`NAME`*

Verify

`show ip protocols | i EIGRP|Stub`
`show eigrp address-family ipv4 100 neighbors detail | i Stub`
`show ip eigrp neighbors detail`

### Fast Reroute

EIGRP använder DUAL för att räkna fram successors och feasible
successors där successor används som primary path och feasible
successors som repair paths eller LFAs. EIGRP har alltid haft backup
paths för snabb konvergens men det LFA FRR ger är en möjlighet att styra
vilka backup paths som ska användas, detta kan göras per primary path
per prefix. Man kan t.ex. sätta regler för att inte använda LFAs där
outgoing interface, linecard eller SRLG är samma. EIGRP använder alltid
prefix-based LFAs.

*Named mode only*

`address-family ipv4 unicast autonomous-system 100`
` topology base`
`  fast-reroute per-prefix all`

ECMP använder alla equal cost paths men för att kontrollera vilka LFAs
som används kan man stänga av load-sharing och istället låta FRR använda
tie-breaking rules.

` fast-reroute load-sharing disable`
` fast-reroute tie-break linecard-disjoint 2`

Verify

`show ip eigrp topology frr `

### BFD

Se [BFD](/Cisco_BFD "wikilink")

`router eigrp 100`
` bfd interface gi2   #Enable BFD on specific interface`
` bfd all-interfaces  #Enable BFD on all interfaces`

Filtering
=========

Med EIGRP går det att filtrera routes på många olika sätt. T.ex. kan
router-id användas för att filtrera bort routes från en viss granne. När
man applyar en distribute-list under EIGRP-processen skickas en ROUTE
FILTER CHANGED och grannskapet resettas för att topologitabellen ska
synkas om.

### Prefix-Lists

`ip prefix-list FILTER seq 5 deny 172.16.10.0/24`
`ip prefix-list FILTER seq 10 permit 0.0.0.0/0 le 32`
`router eigrp 100`
` distribute-list prefix FILTER in`

Det går även använda prefix-listor för att filtrera på neighbor
(gateway).

### ACL

Standard

`access-list 3 deny 30.0.0.0`
`access-list 3 permit any`
`router eigrp 100`
` distribute-list 3 in gi0/0`

Extended

`access-list 103 deny ip host 10.0.0.10 host 172.20.1.0`
`access-list 103 deny ip host `<next-hop>` host `<prefix>
`access-list 103 permit ip any any`
`router eigrp 100`
` distribute-list 103 in gi0/0`

### Administrative Distance

Per prefix filtering med AD (255 = UNKNOWN)

`access-list 7 permit 20.0.0.0`
`router eigrp 100`
` distance 255 0.0.0.0 255.255.255.255 7`

*Träffar alla grannar*

AD för internal routes går att ändra per prefix men ej external.

### Route Map

Med route-maps kan man matcha på metrics, tags och acler.

`route-map RM deny 10`
` match tag 4`
`route-map RM permit 20`
`router eigrp 100`
` distribute-list route-map RM in`

### Prefix Limit

Per process

`maximum-prefix 1000`

Max antal prefix från granne.

`neighbor 10.0.1.1 maximum-prefix 100`

**Övrigt**
Ändra hop-count limit. Prefix med högre hop-count kommer att filtreras
ut.

`metric maximum-hops 2`

Med Offset Lists kan man addera metric (Delay) när routes kommer in
eller skickas ut. Det fungerar med EIGRP men är inte rekommenderat pga
komplexiteten hos EIGRPs metric, det finns andra enklare sätt att
manipulera routes.

Redistribution
==============

För redistribution måste man sätta en seed metric eftersom default är
infinity. Man kan sätta samma router-id på två EIGRP-routrar för att
blockera ut externa routes vid redistribution för att undvika loopar.

`router eigrp 100`
` default-metric 1000000 10 255 1 1500`

**Static**
Med static och connected behövs ingen seed metric.

`redistribute static`

**[RIP](/Cisco_RIP "wikilink")**

`redistribute rip metric 1500 100 255 1 1500`

**[OSPF](/Cisco_OSPF "wikilink")**

`redistribute ospf 1`

Route flapping kan upptäckas genom att kolla events, 500 lines hålls i
minnet.

`show ip eigrp events`

Route-tag notation dotted decimal

`eigrp default-route-tag  #internal only`
`show route-tag list`

**Wide metrics**
När man kör named mode måste man tänka på vilken metric man sätter när
man redistribuerar. Följande exempel kommer inte att fungera eftersom
named mode använder wide metrics och då kommer denna redistribution
resultera i infinity metric och inget kommer att annonseras i EIGRP,
utan man måste sätta något mer realistiskt.

`redistribute ospf 1 metric 1 1 1 1 1`

EIGRPv6
=======

Det finns några skillnader mot klassiska IPv4-EIGRP värda att notera.
Man måste no shuta EIGRP-processen för att den ska starta. Default route
kan endast annonseras med hjälp summarization eller redistribution.
Unequal-cost load balancing stöds för närvarande inte med IPv6 EIGRP pga
[CEF](/Cisco_CEF "wikilink")-begränsningar. Defualt så sätter routern
alltid sig själv som next-hop, även när routes annonseras ut på samma
interface som de kom in på, detta går att stänga av med *no ipv6
next-hop-self eigrp*.

`ipv6 unicast-routing`
`ipv6 router eigrp 1`
` eigrp router-id 2.2.2.2`
` maximum-paths 16  #Max är 32`
` no shutdown`

Per interface

`interface gi2 `
` no ip address  `
` ipv6 address 2001::2/64  `
` ipv6 eigrp 1`

` ipv6 authentication mode eigrp 1 md5`
` ipv6 authentication key-chain eigrp 1 EIGRPV6`
` ipv6 summary-address eigrp 1 2001::/64 leak-map LEAKS`

*leak-map för IPv6 summary är en relativt ny feature*

Verify, finns både gammal och ny syntax för show-kommandona.

`show ipv6 route eigrp`
`show ipv6 eigrp interfaces`
`show ipv6 eigrp 100 interfaces detail | i Hello|Split|Authentication`

`show eigrp address-family ipv6 neighbors`
`show eigrp address-family ipv6 topology`

Named mode
==========

Om IOS stödjer Named Mode är det rekommenderat att använda det (IOS
fr.o.m. 15.0(1)M). Detta ändrar inte på något sätt hur EIGRP fungerar
(förutom wide metrics!) utan är endast ett annat mer konsekvent sätt att
konfigurera det på. Man kan på samma router ha Classic och Named
EIGRP-instanser samtidigt. Alla kommandon läggs nu under *router eigrp
<namn>*, även sånt som förut låg på interfacen t.ex. timers,
summarization och Split Horizon. Lägger man EIGRP-konfiguration på
interfacen kommer den att ignoreras. EIGRP använder automatiskt wide
metrics om andra sidan också kör named mode.

Konfigurationen är uppdelad i tre sektioner.

**Address Family section**

`router eigrp HACKER`
` address-family ipv4 unicast autonomous-system 100`
`  eigrp router-id 1.1.1.1`
`  network 10.0.0.0 0.0.0.255`

` address-family ipv4 unicast vrf EXAMPLE autonomous-system 101`
`  eigrp router-id 1.1.20.1`
`  network 10.0.20.0 0.0.0.255`

OBS med *address-family ipv6 unicast* så enableas alla ipv6-interface
för EIGRP automatiskt.

**Per-AF-interface section**

` af-interface default`
`  passive-interface`
`  bfd`
` exit-af-interface`
` !`
` af-interface Gi3`
`  no passive-interface`
`  authentication mode hmac-sha-256 SECRET_KEY`
`  summary-address 10.10.0.0/24`
` exit-af-interface`

**Per-AF-topology section**
Base är det som finns om man inte slår på Multi Topology Routing.

` topology base`
`  redistribute connected`
`  distance eigrp 90 170`
` exit-af-topology`

Automagically convert classic EIGRP configuration into Named EIGRP
configuration.

`eigrp upgrade-cli`

Show commands har också ny syntax

`show eigrp address-family ipv4 ?`

Man kan också tagga routes. För att ändra format finns den globala
inställningen: **route-tag notation dotted-decimal**

`eigrp default-route-tag 1.2.3.4`

### Add-Path

Fr.o.m. IOS 15.3(2)T har EIGRP stöd för tillägget Add-Path som låter en
router skicka ut uppdateringar som innehåller flera equal-cost vägar
till samma destination. Detta är användbart i
[DMVPN](/Cisco_DMVPN "wikilink")-setuper där flera branch offices är
dual homed. För att kunna skicka ut multipla routes måste de finnas i
routingtabellen samt att Split Horizon är avstängt på multipoint
tunnel-interfacet mot alla spokes.

Detta går bara att konfigurera i named mode och sätts per interface.

`af-interface Tunnel0`
` no split-horizon `
` no next-hop-self`
` add-paths <1-4>`
`exit-af-interface`

`topology base`
` variance 1`
` maximum-paths 4 `
`exit-af-topology`

Maximum-paths måste vara satt till samma eller högre än add-paths annars
kommer det inte att finnas fler equal-cost routes i routingtabellen.
Next-hop-self måste deaktiveras annars kommer alla routes som annonseras
ha samma next-hop. Detta är inte kompatibelt med Unequal Cost LB utan
variance måste vara satt till 1. Spokes behöver inte konfigurera
någonting annat än maximum-paths.

`no-ecmp-mode`

Är rekommenderat om huben använder flera tunnel-interface för att nå
spokes.

### IPv6 VRF-Lite

EIGRP IPv6 [VRF-Lite](/Cisco_Routing#VRF "wikilink") är endast
tillgängligt med Named configurations.

`vrf definition VRF1`
` rd 100:1`
` address-family ipv6`
` exit`

`router eigrp MULTI`
` address-family ipv6 vrf VRF1 autonomous-system 200`

Over the ToP
============

EIGRP Over the ToP (OTP) gör att man kan skapa multipoint overlay VPN:er
över vanlig L3/L3 VPN. Nyckeln är att
[LISP](/Cisco_LISP "wikilink")-enkapsulering (UDP port 4343) används men
EIGRP används för control plane istället för LISPs vanliga mapping
service. Man uppnår en del liknande funktionalitet som med
[DMVPN](/Cisco_DMVPN "wikilink") men det fungerar inte på samma sätt. Om
man kör OTP över MPLS VPN behöver man inte köra någon dynamisk routing
med Provider däremot måste alla CE kunna nå varandra. OTP-trafik kan
krypteras med [GET VPN](/Cisco_IPsec#GET_VPN "wikilink"). Eftersom
grannskap måste konfigureras manuellt blir det omständigt när miljön
växer lite. Detta har lett till att man tagit fram Route Reflector även
för EIGRP, som ger samma funktionalitet som i BGP.

Man konfigurerar ip, max-hops och lisp-id.

`neighbor 1.1.1.1 Gi2 remote 10 lisp-encap 1 `

Verify and show OTP learned routes

`show interface lisp 1`
`show ip route eigrp | i LISP`

Route Reflector har en listen feature (likt BGP) som kan använda sig av
en ACL för att begränsa vilka som får ansluta. På route reflector bör
även split-horizon och next-hop-self stängas av.

`remote-neighbors source gigabitethernet 0/1 unicast-listen lisp-encap allow-list `*`ACL`*

### VRF Support

Man kan även köra OTP i default vrf:en och låta EIGRP bära info om flera
vrf:er. Man binder dem till ett Topology ID. Detta fungerar även på RR.
Alla grannskap etableras i en enskild EIGRP-process. En process hanterar
multipla, separata grannskap i olika vrf:er på lan-sidan samtidigt som
det har grannskap på wan-sidan med OTP peers. Mottagande peer väljer
routes till de olika topologierna som finns lokalt och routes för andra
topologier droppas. LISP Id (LISP Instance ID) mappas till VRF och TID.
Eftersom LISP bär paket för olika vrf:er på olika virtuella
LISP-interface måste LISP ID per vrf vara unikt men samma på alla CE
devices där vrf:en finns.

`router eigrp AF`
` address-family ipv4 autonomous-system 10`
`  topology vrf vrf1 tid 10 lisp-instance-id 122`

`  topology vrf vrf2 tid 11 lisp-instance-id 123`

NX-OS
=====

Här följer Nexus-specifik syntax. Några grundläggande skillnader mot IOS
är att det saknas stöd för UCMP och unicast neighbors. Default väljer
NX-OS Lo0 som Router-ID. Har man ingen manuellt satt RID och konfar Lo0
så kommer EIGRP direkt att byta till Lo0 och processen startas om.

`feature eigrp`

`router eigrp 1`
` log-adjacency-changes`
` autonomous-system 100`
` bfd`

`interface loopback0`
` ip router eigrp 1`

`interface Ethernet1/1`
` ip router eigrp 1`
` ipv6 router eigrp 1`

Maintenance mode

`router eigrp 1`
` isolate`

Verify

`show run eigrp`
`show ip eigrp neighbors`

[Category:Cisco](/Category:Cisco "wikilink")