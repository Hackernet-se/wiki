---
title: Cisco BGP
permalink: /Cisco_BGP/
---

Border Gateway Protocol (RFC 4271) är ett path vector routing protokoll.
Det kommunicerar på TCP port 179 så routing måste vara på plats, man kan
nästan se det som ett L4-protokoll. TCP tillhandahåller acknowledgement,
retransmission, sequencing och update fragmentation. BGP kan få många
vägar till samma destination. Bästa vägen väljs utifrån en ökänd
[algoritm](http://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/13753-25.html).
Den bästa pathen markeras valid/best och blir en kandidat till
routingtabellen. Om next hop inte är reachable så blir aldrig en route
best. Se även [BGP Multicast](/Cisco_Multicast#BGP "wikilink") och
[ExaBGP](/ExaBGP "wikilink").

**Type:** Path Vector

**AD:** 20, 200

**Protocols:** IP

**Packets:** 5

### Pakettyper

**OPEN**: Första paketet som skickas av varje sida används för att
upprätta grannskap, innehåller grundläggande parametrar och
capabilities.

<div class="mw-collapsible mw-collapsed" style="width:250px">

Exempel:

<div class="mw-collapsible-content">

[<File:Cisco_BGP_Open.PNG>](/File:Cisco_BGP_Open.PNG "wikilink")

</div>
</div>

**UPDATE**: En update innehåller routinginformation. Varje NLRI skickas
endast en gång.

<div class="mw-collapsible mw-collapsed" style="width:250px">

Exempel:

<div class="mw-collapsible-content">

[<File:Cisco_BGP_Update.PNG>](/File:Cisco_BGP_Update.PNG "wikilink")

</div>
</div>

**NOTIFICATION**: Errormeddelanden, kan skickas för att starta om ett
grannskap. För alla error codes se [IANAs
lista](http://www.iana.org/assignments/bgp-parameters/bgp-parameters.xhtml)

<div class="mw-collapsible mw-collapsed" style="width:250px">

Exempel:

<div class="mw-collapsible-content">

[<File:Cisco_BGP_Notification.PNG>](/File:Cisco_BGP_Notification.PNG "wikilink")

</div>
</div>

**KEEPALIVE**: Skickas regelbundet för att säkerställa att grannen
lever. Peers måste komma överens om holdtime för keepalives, default är
holdtime 180 sek och då skickas keepalives var 60 sek.

<div class="mw-collapsible mw-collapsed" style="width:250px">

Exempel:

<div class="mw-collapsible-content">

[<File:Cisco_BGP_Keepalive.PNG>](/File:Cisco_BGP_Keepalive.PNG "wikilink")

</div>
</div>

**ROUTE REFRESH**: (RFC 2918) Båda sidor måste stödja denna capability.

<div class="mw-collapsible mw-collapsed" style="width:250px">

Exempel:

<div class="mw-collapsible-content">

[<File:Cisco_BGP_RouteRefresh.PNG>](/File:Cisco_BGP_RouteRefresh.PNG "wikilink")

</div>
</div>

BGP table
---------

Källor till BGP table:

-   Network command
-   BGP updates
-   Redistribution

Show BGP table

`show ip bgp`
`show bgp `<AFI>` unicast update-sources `

Path Selection
--------------

Till skillnad från IGPer används inte enbart metric för att avgöra
vilken som är bästa routen, istället används ett gäng Path Attributes
för att komma fram till vad som ska annonseras vidare och installeras i
routingtabellen. Dock sker ingen path selection för ogiltiga routes utan
de ignoreras direkt (no valid next-hop, not synchronized, AS-looped).
Kolla inkomna PA som inte stöds: *show ip bgp path-attribute
discard\|unknown*

**Well Known** ska stödjas av alla BGP-implementationer

| Mandatory | Discretionary    |
|-----------|------------------|
| AS Path   | Local Preference |
| Next Hop  | Atomic Aggregate |
| Origin    |                  |

Allt som är Mandatory måste alltid skickas med i varje uppdatering, det
är ej ett krav för Discretionary.

**Optional**

| Transitive | Non transitive |
|------------|----------------|
| Aggregator | MED            |
| Community  | Originator     |
|            | Cluster ID     |

Transitive betyder att PA ska forwarderas till andra även om routern
själv inte har stöd för just det PA. Nontransitive PA ska tas bort från
uppdateringar som lämnar det egna AS.

**Path Selection Summary**

| Attribute       | Description                            | Preferens |
|-----------------|----------------------------------------|-----------|
| Weight          | Administrativ                          | Högsta    |
| LOCAL_PREF     | Skickas mellan peers inom AS           | Högsta    |
| Self-originated | Prefer paths originated locally        |           |
| AS_PATH        | Minimize AS hops                       | Kortast   |
| ORIGIN          | Prefer IGP-learned routes over unknown | IGP       |
| MED             | Used externally to enter an AS         | Lägsta    |
| External        | Prefer eBGP routes over iBGP (AD)      | eBGP      |
| IGP Cost        | Consider IGP metric to NEXT_HOP       | Lägsta    |
| eBGP Peering    | Favor more stable routes               | Äldsta    |
| Router ID       | Sista tie breaker                      | Lägsta    |

**Best path selection**
Det finns många sätt att ändra BGPs beteende med avseende på path
selection.

Stänga av att oldest path kan ge best route. Compare router-id for
identical EBGP paths

`bgp bestpath compare-routerid`

Stänga av att AS path length kollas. OBS detta är ett dolt kommando.

`bgp bestpath as-path ignore`

Ignore cost IGP metric in bestpath selection

`bgp bestpath igp-metric ignore`

Ignore cost communities in bestpath selection

`bgp bestpath cost-community ignore`

Allow comparing MED from different neighbors

`bgp always-compare-med`

Treat missing MED as the least preferred one

`bgp bestpath med missing-as-worst`

Compare MED among confederation paths

`bgp bestpath med confed`

Pick the best-MED path among paths advertised from the neighboring AS

`bgp deterministic-med`

### Multipath

**Maximum Paths**
Flera paths kan hamna i routingtabellen men endast best path kan
annonseras vidare (om inte add-path används). Default är EN path till
skillnad från andra routingprotokoll. Default måste allt upp till IGP
Cost vara lika för att maximum paths ska spela någon roll. Inte alla
topologier stödjer multipath. **bgp bestpath as-path multipath-relax**
används för att möjliggöra ECMP genom olika AS, detta är ett dolt
kommando.

`router bgp 100`
` maximum-paths 4        #eBGP`
` maximum-paths ibgp 4   #iBGP`
` maximum-paths eibgp 4  #MPLS`

**Additional Paths**
Med iBGP kan man använda add-paths. Syftet är att tillhandahålla en
backup route för snabbare konvergering. Det är en capability som skickas
med i open message per adressfamilj. Add-paths lägger på ett unikt Path
ID på varje prefix för att det ska kunna gå att skilja på dem. För att
det ska funka måste next-hop på backup path skilja sig från det på
primary path.

Det går att konfigurera per adressfamilj eller per neighbor.

`router bgp 100`
` bgp additional-paths select all`
` neighbor 1.1.1.1 additional-paths send receive`
` neighbor 1.1.1.1 advertise additional-paths all`

`show ip route repair-paths`

Man kan välja additional paths och skicka vidare dem utan att installera
det i RIB/FIB lokalt.

`bgp additional-paths install`

**Diverse Path**
Diverse-Path säger åt en BGP-router att medvetet beräkna en 2nd-best
path som har en annan next hop som den första pathen. Diverse-Path var
en workaround innan Add-Path var supporterat. Det görs endast på route
reflector. Diverse-Path är ej supporterat i IOS-XR.

`router bgp 1`
` address-family vpnv4 unicast`
`  maximum-paths 2`
`  bgp bestpath igp-metric ignore`
`  bgp additional-paths select backup`
`  bgp additional-paths install`
`  neighbor IBGP advertise diverse-path backup`

Konfiguration
=============

För att byta från NLRI-format till AFI-format i konfigurationen

`bgp upgrade-cli `

Administrative Distance: eBGP, iBGP, local. Det går ändra distance per
granne också med distance-kommandot och en acl.

`distance bgp 20 200 200`

Synchronization is disabled by default in Cisco IOS post 12.2(8)T.
Synchronization bör vara avstängt annars medföljer vissa begränsningar.
T.ex. måste routes finnas i IGP innan det kan propagera vidare med BGP
och OSPF RID måste vara samma som BGP RID om sync är på.

`no synchronization`

IPv4 aktiveras default i BGP på IOS men det går att stänga av.

`no bgp default ipv4-unicast`

Neighbor
--------

För att kunna utbyta routinginformation måste grannskap upprättas, detta
görs med en TCP-anslutning som det skickas BGP-meddelanden över. eBGP
har TTL satt till 1 på alla BGP-paket som skickas ut, detta går att
ändra med *ebgp-multihop*. iBGP har inga sådana begränsningar utan
skickar med TTL 255. eBGP byter även next-hop på den NLRI som kommer in,
dock inte om next-hop finns i samma subnät som en själv. eBGP kan inte
initiera peering med hjälp av en default route.

**States**
BGP har en finite state machine vilket betyder att grannskap kan befinna
sig i olika tillstånd.
**TCP**
Idle State: ConnectRetry timer 120 sekunder
Active State: BGP speaker försöker nå peer med TCP
Connect State: TCP session established
**BGP**
OpenSent State: BGP version, AS number, hold time, BGP ID. Börja skicka
keepalives
OpenConfirm State: Response recieved
Established State: Skicka uppdateringar. Neighbor up
Om ett grannskap är iBGP eller eBGP avgörs med remote-as som antingen är
samma AS som en själv eller ett annat. Default accepteras all NLRI från
eBGP-grannar, så fungerar ej IOS XR.

`router bgp 65000`
` neighbor 1.1.1.1 remote-as 65001`
` neighbor 1.1.1.1 description Other side`
` neighbor fe80::a00:27ff:fe80:7008%GigabitEthernet1 remote-as 65001`

When configuring iBGP always use loopbacks (advertised by your IGP) for
peering.

`neighbor 1.1.1.1 update-source Loopback0`

md5 authentication görs med tcp option 19

`neighbor 1.1.1.1 password SECRET`
`show ip bgp neighbors 1.1.1.1 | i state|Flags`

Man kan konfigurera intervallet mellan uppdateringar till grannar där 0
är annonsera direkt. Default är 0 sek för iBGP, 0 sek för eBGP i en VRF
och 30 sek för eBGP-sessioner i default-vrfen.

`neighbor 1.1.1.1 advertise-interval `<interval>

Verify

`show ip bgp neighbor`
`show ip bgp summary`
`show tcp brief`

Debug

`debug ip bgp events`

### Peer Group

För att förenkla konfen kan man gruppera flera grannar som ska ha
likadan konfiguration i så kallade peer groups. Det blir även lite
effektivare processing eftersom identiska Updates skickas till alla
peers i gruppen. Man kan ju ha olika out policy per grannskap och då
funkar inte identiska Updates till alla men IOS löser detta automatiskt
genom att skapa fler update groups dynamiskt.

`neighbor GROUP01 peer-group`
`neighbor GROUP01 remote-as 100 [alternate-as 50000]`
`neighbor GROUP01 update-source Loopback0`
`neighbor 1.1.1.1 peer-group GROUP01`
`neighbor 2.2.2.2 peer-group GROUP01`

Verify

`show ip bgp peer-group`
`show ip bgp update-group`
`show ip bgp replication`

Eftersom peers kan svara segt (av någon anledning) finns det en dynamisk
funktion för att splita peer-grupper och lägga dessa i slow-update
groups. When “permanent” is not configured, the “slow peer” will be
moved to its regular original update group, after it becomes regular
peer (converges).

` bgp slow-peer split-update-group dynamic`
`show ip bgp neighbors slow`

**Templates**
Det går även att skapa policy och session templates. Detta går tyvärr ej
att kombinera med bgp listen range eftersom den kopplas till en peer
group.

`template peer-session RR`
` remote-as 101`
` password SECRET`
` update-source Loopback0`
`exit-peer-session`

`template peer-policy RR`
` route-reflector-client`
` send-community both`
` additional-paths send receive`
`exit-peer-policy`

`neighbor 1.1.1.1 inherit peer-session RR`
`neighbor 1.1.1.2 inherit peer-session RR`

`address-family vpnv4`
` neighbor 1.1.1.1 activate`
` neighbor 1.1.1.1 inherit peer-policy RR`

Verify

`show ip bgp template peer-session`
`show ip bgp template peer-policy`

### Dynamic Peering

Det får ej finnas några statiska neighbor statements när man använder
listen range.

`router bgp 100`
` bgp listen range 10.1.123.0/24 peer-group AS_200`
` bgp listen limit 15`
` neighbor AS_200 peer-group`
` neighbor AS_200 remote-as 200`

` address-family ipv4`
`  neighbor AS_200 activate`
`  neighbor AS_200 send-community both`

### Route Refresh vs Soft Reconfiguration

Både Route Refresh och Soft Reconfiguration tillåter en router att ändra
sin routing policy utan att starta om grannskapet (Hard reset). Soft
reset skickar route-refresh message för att begära att all NLRI skickas
igen medans Soft Reconfiguration lagrar all NLRI som kommer in från
grannen i en separat tabell (adj-ribs-in) för att kunna köra om policyn
lokalt när man clearar. Blir minne korrupt över tiden kan det dock
ställa till problem. Soft Reconfiguration använder mer minne medans
Route Refresh använder lite mer bandbredd. Route Refresh är
rekommenderat nuförtiden tack vare att bandbredd sällan är ett problem
samt att de flesta enheter har stöd för det. Vill man spara minne men
ändå ha tillgång till Adj-RIB-In får man använda BMP (se BMP-stycket).

`show ip bgp neighbors 1.1.1.1 | s Neighbor capabilities`
`Neighbor capabilities:`
`   Route refresh: advertised and received(new)`

Route Refresh är en capability som finns i olika varianter och skickas i
open message. Det IOS-XE kallar "new" decodar wireshark som "Cisco". En
BGP-peer kan annonsera flera varianter.

[<File:Cisco_BGP_Route_Refresh_Capability.PNG>](/File:Cisco_BGP_Route_Refresh_Capability.PNG "wikilink")

Om en router inte har stöd för Route Refresh får Soft Reconfiguration
användas. Då måste man slå på det på grannskapet.

`neighbor 1.1.1.1 soft-reconfiguration inbound`
`show bgp ipv4 unicast neighbors 1.1.1.1 policy`

Alternativt använd soft reconfiguration som fallback om andra sidan inte
stödjer route refresh.

`bgp soft-reconfig-backup`

Kolla adj-ribs-in (alla prefix raw):

`show ip bgp neighbors 1.1.1.1 received-routes`

Oavsett om reset eller reconfiguration används så kör man
clear-kommandot för att göra det.

`clear ip bgp 1.1.1.1 soft [in]`
`clear ip bgp * soft`

**eBGP Multihop**
Ska man upprätta eBGP-grannskap om neighbor-IP ej är directly connected,
t.ex. mellan loopbacks, behöver man öka TTLn på paketen som skickas ut.

`neighbor 1.1.1.1 ebgp-multihop 3`

Alternativt godta TTL 1 genom att stänga av checken som kollar om
grannen sitter på ett directly connected network genom att kolla
routingtabellen. Grannen kan dock max vara ett hop bort för TTL är 1 med
detta alternativ.

`neighbor 1.1.1.1 disable-connected-check`

**TTL Security**
GTSM (RFC 3682) används för att skydda mot spoof attacks. Med GTSM (utan
angiven "hops") lyssnar man bara på TCP/BGP-paket med ett TTL-fält på
minst 254, det betyder att paketet inte kan ha routats och därmed inte
kan komma ifrån någon på internet utan endast från närliggande granne,
dvs den man peerar med. Notera att TTL security och eBGP multihop är
mutually exclusive. Detta gäller endast för eBGP peers.

`neighbor 2.2.2.2 ttl-security hops 10`
`show ip bgp neighbors 2.2.2.2 | i TTL|hop`

T.ex. "hops 10" betyder att endast BGP-paket med TTL 245 eller högre kan
accepteras.

**PMTUD**
Förr i världen sattes max data segment på BGPs TCP-session till 536
bytes men nu finns PMTUD default.

`bgp transport path-mtu-discovery`
`show ip bgp neighbor | i Data|MTU|transport|MSS`

Turn off per neighbor

`neighbor $PEER transport path-mtu-discovery disable`

**Multi Session TCP**
Multi Session TCP Transport per AF togs fram för att stödja Multi
Topology Routing. Multisession capability utbyts i OPEN message och
indikerar att multisession BGP stöds.

`neighbor 1.1.1.1 transport multi-session`
`show tcp brief`

**Passive Peer**
Kan t.ex. behövas om grannskap går igenom en brandvägg. Default är
såklart active.

`bgp neighbor transport connection-mode active/passive`

**GRE**
Det går även att upprätta BGP-grannskap över
[GRE](/Cisco_GRE "wikilink")-tunnlar. Det är dock viktigt att se till
att next hop blir rätt.

### Next Hop

Ändra så att annonserade uppdateringar har den egna IP-adressen (peer
address) istället för det som står i uppdateringen från den granne man
har lärt sig prefixet av.

`neighbor 10.0.0.10 next-hop-self`

Alternativt

`neighbor 10.0.0.10 route-map OUT`
`route-map OUT permit 10 `
` set ip next-hop self | peer-address`

Route Reflector Server ändrar inte next-hop när prefix skickas vidare
till RR-klienter oavsett om man har konfigurerat next-hop-self eller en
route-map. Sätt next-hop-self oavsett om det är reflected routes.

`neighbor 10.0.0.10 next-hop-self `**`all`**

Det finns situationer då man kör eBGP men vill att next-hop ej ska
ändras, t.ex. vid Inter-AS MPLS Option C.

`neighbor 10.0.0.10 next-hop-unchanged`

### 4 byte ASN

Från början användes 2 bytes för ASN vilket ger 65535 stycken men det
räcker inte. Nyare routrar skickar AS_PATH som innehåller 4 bytes ASN
men det blir inte bakåtkompatibelt så därför har det i RFC 5396 skapats
nya optional transitive path attributes: AS4_PATH, AS4_AGGREGATOR och
extended communities som kan användas för att bära den korrekta
informationen igenom gamla enheter. 4 byte ASN en capability som listas
i OPEN message. Ska en ny router i ett AS högre än 65535 prata med en
gammal router som inte har stöd för 4 byte ASN kan den ändå ta upp
grannskapet men använder då det reserverade ASN 23456 som kallas
AS_TRANS. Alla 4 byte ASN kommer att skickas som AS4_PATH medans i
AS_PATH kommer de att bytas ut mot detta 23456 så att ändå path length
stämmer. Om detta kommer till en ny router vid ett senare tillfälle kan
den sätta ihop den korrekta as-pathen.

Man kan konfigurera hur man vill att ASN ska presenteras i outputen från
show-kommandon.

`bgp asnotation dot`

### Diverse

När BGP startar väntas en specificerad tidsperiod för att grannarna ska
etablera sig själva innan de första uppdateringarna skickas. När
perioden är slut räknas best path för varje prefix och detta annonseras.
Detta förbättrar konvergeringstiden eftersom om det skickades
uppdateringar direkt och det strax efter kom ny information och en annan
best path hade det behövts skickas igen. Update-delay används för att
konfigurera just denna tidsperiod, default är 120 sekunder.

`bgp update-delay `<seconds>

Update-delay kan användas i kombination med graceful restart. Detta är
en capability som förhandlas mellan NSF-capable och NSF-aware peers i
OPEN message när grannskap sätts upp. En router som är NSF-capable kan
göra stateful switchover. BGP graceful restart är på default när IOS
stödjer det. Defaultvärden som används om inget annat anges är
restart-time: 120 sekunder och stalepath-time: 360 sekunder.

`bgp graceful-restart`
`bgp graceful-restart extended`

**Backdoor**
Eftersom eBGP har AD 20 är det preferred över IGPs. Om man kör IGP
mellan AS och vill att det i första hand ska styra trafiken kan man
manipulera BGP. Det man kan göra är att själv annonsera ut de prefix som
de andra AS har. iBGP har AD 200 och blir således inte preferred. Dock
blir då next-hop fel och det är där BGP Backdoor feature kommer in. Med
backdoor annonseras inte några prefix till eBGP-grannar om man själv
inte har det i sitt AS men AD lokalt blir fortfarande 200.

`network 10.0.0.0 mask 255.0.0.0 backdoor`

Går även manuellt att sätta högre distance på prefix från grannar.

**DMZ Link över eBGP**
Use DMZ Link Bandwidth as weight for BGP multipaths on single-hop EBGP
peers. Bandwidth skickas med i uppdateringar som extended community och
kan användas för lastdelning av trafiken.

`router bgp 100`
` maximum-path 4`
` bgp dmzlink-bw`
` neighbor 2.2.2.2 dmzlink-bw`

`show ip bgp `<prefix>` | i DMZ`

För att verifiera får man också kolla traffic share.

IOS-XR
neighbor 1.1.1.1

` dmz-link-bandwidth`
` ebgp-send-extcommunity-dmz`
` ebgp-recv-extcommunity-dmz`

För att köra multipath över olika AS.

`bgp bestpath as-path multipath-relax`
`bgp bestpath as-path ignore`

Have route-map set commands take priority over BGP commands such as
next-hop unchanged.

`bgp route-map priority`

Default annonseras routes som ej hamnar i RIB (RIB-failure) vidare till
andra, ändra detta:

`bgp suppress-inactive`
`show ip bgp rib-failure`

Path Manipulation
-----------------

**Outbound from AS:**

-   Weight
-   Local preference
-   Communities (mer skalbart än LOCAL_PREF)

**Inbound to AS:**

-   AS-prepend
-   MED

### MED

Multi-exit discriminator är ett konfigurerbart värde som kan användas
för att välja var trafik komma in till sitt AS. Eftersom det är ett
nontransitive attribute skickas det inom AS men lämnar ej. Det jämförs
bara om flera olika paths kommer från samma AS, detta kan ändras med bgp
*always-compare-med*.

`route-map MED_50 permit 10`
` set metric 50`
`neighbor 1.1.1.1 route-map MED_50 out`

4,294,967,295 är max metric och räknas som infinity.

### Local Preference

Local Preference är ett konfigurerbart värde som används för att välja
var trafik ska lämna det egna AS. Det skickas med NLRI till iBGP-grannar
men ej eBGP. När en uppdateringar kommer från en eBGP-peer sätts default
preference (100) på prefixet innan det annonseras vidare till iBGP.

`bgp default local-preference 100`

Eller stäng av det

`no bgp default local-preference`

Högst preference vinner

`route-map LOCALPREF permit 10`
` set local-preference 500`
`neighbor 1.1.1.1 route-map LOCALPREF in`

### AS-prepend

För att ändra var man vill att trafik ska komma in till det egna AS kan
man manipulera AS_PATH genom att lägga på sitt AS flera gånger för att
göra pathen längre.

`route-map PREPEND permit 10`
` set as-path prepend 100 100 100`
`neighbor 1.1.1.1 route-map PREPEND out`

### Weight

Cisco proprietary och finns endast inom routern själv.

`route-map WEIGHT permit 10`
` match ip address prefix-list HEAVY`
` set weight 2000`
`neighbor 1.1.1.1 route-map WEIGHT in`

Default weight per neighbor

`neighbor 1.1.1.1 weight <0-65535>`

### Community

Community Path Attribute är 32-bitars nummer som används för att tagga
prefix. Då kan man använda taggen för att matcha på och sedan manipulera
path eller filtrera. Routrar kan kolla efter taggen och sedan fatta
routingbeslut. Detta PA bärs med i annonseringarna och kan därmed
användas av enheter som befinner sig flera AS bort. Eftersom det är ett
optional transitive PA så behöver inte ens routrarna emellan förstå det.
Till exempel kan man konfigurera att prefix med en viss community ska få
en viss LOCAL_PREF och man kan på så sätt styra trafiken.

Både heltal och AA:NN accepteras i konfiguration och show-kommandon men
outputen från show route-map går att ändra. Detta är best practice.

`ip bgp-community new-format`

Verify

`show ip bgp community ?`

Så står det antingen aa:nn eller 1-4294967295 beroende på format

För att Community ska funka måste det skickas i uppdateringarna,
standard och extended

`neighbor [ip-address] send-community both`

Skicka community

`route-map SETCOMMUNITY permit 10`
` match ip address prefix-list COMMUNITY`
` set community 5`

Alternativt flera med eller utan additive beroende på om att lägga till
community istället för att ersätta är önskvärt.

` set community 5 10 15`
` set community 5 10 15 additive`

Man kan även ta bort community.

` set community none`

Delete anything starting with 300

`ip community-list expanded REGEXP permit 300:[0-9]+_`
`route-map DELETE permit 10`
` set comm-list REGEXP delete`

Ta emot community

`ip community-list 6 permit 5`
`route-map CHANGEPREF permit 10`
` match community 6`
` set local-preference 250`

Vill man matcha med regex måste man använda en extended community list.
Community Internet (0:0) kan användas i community lists och betyder
match any.

`ip community-list 101 permit `<regex>

Show

`show ip bgp community`

Några kända communities, *set community ?*

-   Internet: 0:0
-   no-export: Annonsera inte utanför eget AS
-   no-advertise: Annonsera inte till någon
-   gshut: graceful shutdown
-   local-as (NO_EXPORT_SUBCONFED): Annonsera inte utanför eget
    confederation sub-AS

`show ip bgp community no-advertise no-export local-AS`

**Graceful BGP session shutdown**
GRACEFUL_SHUTDOWN är en well-known community som används i samband med
BGP Graceful Shutdown feature. Man skickar ut communityn till de grannar
som man vill ska sluta använda länkarna till den router som man t.ex.
ska ha underhåll på. För att vara compliant med denna community måste
man ha en ingress policy som säger "match community gshut -\> make path
least prefered". IOS XE har en inbyggd macro för detta community-utskick
och man anger hur många sekunder det tar innan man bryter grannskapet.

Exempel:

`neighbor 10.0.1.1 shutdown graceful 30`

Då skickas det ut UPDATE + ROUTE REFRESH som har community value
0xFFFF0000. 30 sekunder senare skickas det NOTIFICATION med admin
shutdown. Då hamnar även "neighbor 10.0.1.1 shutdown" i running conf.

Man kan även skicka med en egen community eller local pref (funkar
såklart inte på ebgp).

`neighbor 10.0.1.1 shutdown graceful 30 community 100 local-preference 150`

Det går även att aktivera community-utskicket + admin shutdown för alla
grannskap samtidigt. Oavsett om man använder peer-groups eller inte så
hamnar shutdown på alla enskilda neighbors. Det finns ingen macro för
unactivate utan "neighbor shutdown" får man ta bort själv efteråt.

`bgp graceful-shutdown all neighbors activate`

### AS Manipulation

Man kan konfigurera sig själv att skicka ett helt annat ASN i OPEN
message än vad man egentligen har så att man ser ut som ett annat AS för
externa partar, detta görs med *local-as*. Man kan även välja om detta
"fake" AS ska läggas på eller ej på det som tas emot beroende på hur ens
AS är uppdelat, dvs anledningen till att man ens kör local-as. Man kan
också ställa in att det enda som andra sidan ser är fake AS,
*replace-as*. Under en övergångsperiod kan man acceptera två AS och
grannen kan då peera med valfritt, *dual-as*.

`neighbor 1.1.1.1 local-as 601 no-prepend [replace-as] [dual-as]`

Kan användas för att dölja ASN, Override matching AS-number while
sending update, dvs det är en egress feature.

`neighbor 1.1.1.1 as-override`

Acceptera as-path som innehåller det egna ASN, kan behövas i vissa fall
där ens AS är uppdelat. Default får ens AS förekomma 3 gånger i
AS_PATH.

`neighbor 1.1.1.1 allowas-in `

Ta bort private AS number från utgående uppdateringar, detta AS måste
finnas i början av AS path för att detta ska funka.

`neighbor 1.1.1.1 remove-private-as [all]`

**Attribute-map**
Attribute map kan användas för att manipulera AS och/eller attributes
från AS-sets.

`set origin egp 22`

Filtering
---------

BGP kan filtrera AS, NLRI och PA i alla inkommande och utgående
uppdateringar antingen per granne eller per peer group. För att en
filterändring ska gå igenom krävs clear-kommandot.

**Maximum prefixes**

`neighbor 1.1.1.1 maximum-prefix 1000 `

Only give warning message when limit is exceeded

`neighbor 1.1.1.1 maximum-prefix 1000 warning-only`
`show ip bgp neighbors 1.1.1.1 | i Maximum|Threshold`

### AS

Regular Expressions

-   .\* = Any
-   ^$ = Local AS
-   _200$ = Originated in AS 200
-   _200_ = Transited AS 200
-   ^200_ = Learned from 200
-   \[0-9\]+ = Any AS

AS-path ACL

`ip as-path access-list 100 deny _120$`
`ip as-path access-list 100 permit .*`
`neighbor 1.1.1.1 filter-list 100 in`

Maximum number of ASes in the AS-PATH attribute

`bgp maxas-limit <1-254>`

### Network

Distribute-list, standard ACL

`access-list 1 permit 10.10.10.0 0.0.0.255 `
`neighbor 1.1.1.1 distribute-list 1 in`

Extended ACL tolkas av BGP som:

`access-list 100 permit ip `<subnet>` `<wildcard for subnet>` `<mask>` `<wildcard for mask>
`neighbor 1.1.1.1 distribute-list 100 in`

Prefix-list, det rekommenderade sättet.

`ip prefix-list ACCEPT seq 10 permit 10.10.10.0/24 le 24`
`neighbor 1.1.1.1 prefix-list ACCEPT in`

Verify

`show ip bgp prefix-list ACCEPT`

**ORF**
Outbound route filtering kan användas för att berätta för sina neighbors
vilka prefix man tillåter in så de dynamiskt kan sätta samma
prefix-lista som outbound prefix filter och inte ens behöver skicka
något annat. Båda sidor måste stödja ORF för att det ska kunna användas.

`neighbor 1.1.1.1 prefix-list ALLOW in `
`neighbor 1.1.1.1 capability orf prefix-list both`

`show ip bgp neighbors 1.1.1.1 | s Outbound`
`show ip bgp neighbors 1.1.1.1 received prefix-filter`
`clear ip bgp 1.1.1.1 soft in prefix-filter`

### RT

Filtrera inkommande routes genom att vitlista specifikt route-target

`ip extcommunity-list standard FILTER-AS400-VPNV4-IN permit rt 1337:10`
`route-map FILTER-AS400-VPNV4-IN permit 10`
` match extcommunity FILTER-AS400-VPNV4-IN`

`address-family vpnv4`
` neighbor 172.16.99.2 route-map FILTER-AS400-IN in`

Verify

`show ip extcommunity-list`
`show bgp vpnv4 unicast all extcommunity-list FILTER-AS400-VPNV4-IN`

Convergence
-----------

BGP är inte designat för att vara det snabbaste protokollet, detta för
att kunna fungera i stor skala men det finns flera tekniker för att
sänka konvergeringstid (recovery). Även om routes tas bort från
routingtabellen snabbt så väntar BGP-processen på att TCP-sessionen ska
timea ut eller hold-down ska gå ut innan konvergeringsprocessen börjar.
Hold-down timer är default 3 minuter. Det är också så att BGP inte
skickar uppdateringar direkt till grannar utan det sker periodvis
baserat på peering-typ, 0 sekunder för iBGP-grannar och 30 sekunder för
eBGP. BGP verifierar next-hop reachability med hjälp av IGP, detta görs
var 60:e sekund. Allt detta leder till att BGP kan ta väldigt lång tid
på sig att konvergera.

Timers

`timers bgp `<keepalive>` `<holdtime>` `<minimum hold time from neighbor>
`timers bgp 10 30 20`

I IOS-XE verkar *keepalive* vara verkningslöst, det är holdtime delat
med tre som blir aktivt.

**Next Hop Tracking**
NHT is an on-by-default feature that notifies BGP to a change in routing
for BGP prefix next-hops. This is important because previously this only
happened as part of the BGP Scanner process, which runs every 60 seconds
by default. The bgp nexthop trigger delay defines how long for the NHT
process to delay updating BGP. This timer is here to prevent BGP from
being beaten up by a flapping IGP route. At default value 5 seconds, the
BGP process can't get bogged down from unnecessary updates.

`bgp nexthop trigger enable`
`bgp nexthop trigger delay 5`

**Scan interval**
Hur ofta IGP ska scannas efter uppdateringar, default är 60 sekunder.
OBS *bgp scan-time configuration less than 15 seconds can cause high cpu
usage by BGP Scanner.*

`router bgp 100`
` bgp scan-time <5-60>`
`show ip bgp summary | i scan`

Kolla VRF:er om det finns nya routes att annonsera med MP-BGP.

` address-family vpnv4 unicast`
`  bgp scan-time <5-60>`
`show bgp vpnv4 unicast all summary | i scan`

Man kan reducera konvergenstiden när BGP paths förändras genom att
konfigurera policyn för vad som ska dra nytta av BGP Event-Based VPN
Import feature.

`address-family ipv4 vrf Cust_A`
` import path selection all`

**eBGP neighbor loss detection**
BGP-grannskap rivs direkt när länken mellan går ner vilket leder till
att BGP-routsen flushas direkt och det sökes efter alternativ. Detta är
default i IOS sedan länge.

`bgp fast-external-fallover  #Global`
`ip bgp fast-external-fallover  #Per interface`

**iBGP neighbor loss detection**
Så fort en grannens IP-address försvinner från routingtabellen (på grund
av IGP) så tas grannskapet ner och konvergering kan börja direkt. Ingen
hold-down eller delay i deaktivering av BGP-session används. Är IGPn det
minsta långsam på att hitta en alternativ route till grannen så hinner
grannskapet tas ner. Det går även att använda detta för eBGP t.ex. om
man peerar med loopbacks och det fungerar på samma sätt.

`neighbor 1.1.1.1 fall-over`

#### BFD

Se även [Cisco BFD](/Cisco_BFD "wikilink").

`neighbor 1.1.1.1 fall-over bfd`
`show bfd neighbor`

The C-Bit is set by the BFD process itself, and isn't something you can
toggle. However, you can tell your BFD process whether to ignore the
setting or not. The default is to ignore.

`neighbor 2.2.2.2 fall-over bfd check-control-plane-failure`

### PIC

Prefix Independent Convergence är en CEF/FIB-feature framtagen för att
snabba upp data-plane recovery när man har FIB med väldigt många routes
och next-hop blir unreachable men det finns en annan gångbar next-hop.
Traditionellt byggdes FIB med Prefix -\> Interface/Next-Hop. Ändras
next-hop måste FIB:en uppdateras för varenda prefix vilket kan ta lång
tid ifall det finns många. Med PIC Core lägger man in en pointer
emellan, Prefix -\> Pointer -\> Interface/Next-Hop. Ändras next-hop
behöver endast en pointer pekas om, alla prefix kan fortfarande peka mot
samma pointer. BGP FRR precomputes en näst bästa väg i BGP och ger den
till RIB som en backup/alternate path och CEF programmerar det i line
cardsen. BGP PIC feature supporterar prefix för IPv4, IPv6, VPNv4 och
VPNv6. Kör man BGP Multipath så finns support för PIC. Har man route
reflector endast i control plane behöver man inte slå på PIC eftersom
det handlar om data plane recovery.

**PIC Core**
Hierarchical FIB, local only mechanism.

`bgp additional-paths install`

`cef table output-chain build favor convergence-speed`

Stänga av PIC

`cef table output-chain build favor memory-utilization  `

**PIC Edge**
Eftersom PIC Edge precomputes en alternate path försvinner poängen med
CEF recursion så därför kommer det att disableas för prefix med /32-mask
eller som är directly connected när man slår på BGP PIC. *bgp recursion
host* enableas för VPNv4 och VPNv6 address families och disableas för
IPv4 och IPv6 address families.

`bgp additional-path install`
`bgp recursion host`
`bgp advertise-best-external`

**IOS-XR**
route-policy PIC-EDGE

` set path-selection backup 1 advertise`
`end-policy`

`router bgp 1`
` address-family vpnv4 unicast`
`  additional-paths selection route-policy PIC-EDGE`

Default route
-------------

Send default route, görs per adressfamilj och måste finnas i
routingtabellen.

`network 0.0.0.0`

eller använd **default-information originate** (det kräver också
redistribution)

Skicka default route villkorslöst, görs per neighbor. Detta går förbi
output filtering och kräver inte gateway of last resort i RIB.

`neighbor 1.1.1.1 default-originate`

Summarization
-------------

Auto-Summary är avstängt default och bör vara det. Om det är påslaget
påverkar det network och redistribution.

-   network-kommando: classful and more specific
-   redistribution: only classful

För att skicka summerade routes används aggregate-address och en null
route installeras automatiskt. Inget annonseras om inte det inte finns
någon component route i BGP-tabellen. Om component routes har olika
AS_SEQ så kan inte de slås samman utan då kommer aggregeringen att
skickas med AS_SEQ null. aggregate-address skickas med PA: Atomic
Aggregate.

`aggregate-address 10.0.0.0 255.0.0.0 [summary-only] [as-set]`

summary-only = suppress detailed routes. AS-set innebär att alla ASN
från de mer specifika prefixen ska sättas ihop och inkluderas i
summeringen, ett set räknas som ett AS hopp och används för loop
prevention. Övrig information från de mer specifika prefixen slås också
ihop och en del information då vara överlappade. Man kan manipulera
detta själv genom att välja ut enskilda prefix som ska utgöra källan för
de attribut som aggregeringen ska ha. Detta görs med route-map som
konfigureras efter as-set, **advertise-map ADVERTISE_MAP**.

Alternativt

`ip route 10.0.0.0 255.0.0.0 null 0`
`router bgp 100`
` network 10.0.0.0 255.0.0.0`

**Suppress-map**
Med aggregate-address skickas en summary och de mer specifika prefixen.
Detta går att styra med en suppress-map som fungerar som en svartlista.

`ip prefix-list DONT-SUPPRESS-THIS permit 10.0.2.0/24`
`route-map SUPPRESS deny 10`
` match ip address prefix-list DONT-SUPPRESS-THIS`
`route-map SUPPRESS permit 20`

`router bgp 100`
` aggregate-address 10.0.0.0 255.255.0.0 suppress-map SUPPRESS`

**Unsuppress-map**
Används om man vill skicka mer specifika prefix till en granne trots att
man använder summary-only, fungerar som en vitlista.

`ip prefix-list UNSUPPRESS-THIS permit 10.0.2.0/24`
`route-map UNSUPPRESS permit 10`
` match ip address prefix-list UNSUPPRESS-THIS`

`router bgp 100`
` aggregate-address 10.0.0.0 255.255.0.0 summary-only `
` neighbor 1.1.1.1 unsuppress-map UNSUPPRESS`

Multiprotocol BGP
-----------------

För att kunna skicka NLRI om annat än IPv4, t.ex. VPN routes för olika
VRF:er, behövs fler path attributes. MP-BGP (RFC 4760) är ett extension
till BGP som ger två nya optional nontransitive attributes.
Multiprotocol Reachable NLRI (MP_REACH_NLRI) annonserar MP-routes och
Multiprotocol Unreachable NLRI (MP_UNREACH_NLRI) drar tillbaka
MP-routes. Dessa innehåller AFI, Next-hop och NLRI. NLRI står för lägga
till eller ta bort routes och next-hop. MP-BGP listas som capability i
Open-paketen och körs för det mesta inom samma AS. Se även [Cisco
MPLS](/Cisco_MPLS "wikilink").

<div class="mw-collapsible mw-collapsed" style="width:270px">

Exempel:

<div class="mw-collapsible-content">

[<File:Cisco_BGP_MP.png>](/File:Cisco_BGP_MP.png "wikilink")

</div>
</div>

IPv4 unicast aktiveras så fort man konfigurerar MP-BGP.

`router bgp 100`
` no bgp default ipv4-unicast`
` address-family vpnv4`
`  neighbor 1.1.1.1 activate`
`  neighbor 1.1.1.1 send-community extended`
` exit-address-family`

BGP send-community slås på automatiskt när man aktiverar en granne för
det är ett måste för att MP-BGP ska fungera.

Se routes som skickas från en VRF (adj-ribs-out)

`show ip bgp vrf Name neighbors 10.10.10.10 advertised-routes `
`clear ip bgp 10.10.10.10 vrf Name`

Route Reflector
---------------

Routes lärda av iBGP skickas ej vidare till iBGP-grannar per default. En
route reflector (RFC 1966) bryter denna regel så full mesh
iBGP-grannskap behövs ej och iBGP blir mer skalbart. Dock skickar en RR
endast vidare routes som anses "best" i den egna BGP-tabellen, detta
håller nere antalet annonserade routes. Den enda gången en RR inte
skickar vidare NLRI när det ska till en icke-klient då NLRI är mottagen
från en icke-klient, dvs vanlig iBGP. För att hålla nätverket loopfritt
används Path Attribute, RR sätter CLUSTER_LIST och det innehåller egna
cluster-id som skickas med Updates. Innehåller en mottagen update det
egna cluster-id så kommer prefixet discardas. ORIGINATOR_ID, RID på
iBGP-routern som först annonserade prefixet, skickas även med. Ser en
router ett prefix med sitt egna RID som ORIGINATOR_ID kommer inte
prefixet att annonseras vidare. För high availability och resiliency
används fördelaktigt ett eller flera RR-kluster.

**Utmaningar**
På grund av att RR endast annonserar vidare en path blir det reduced
path diversity och om inte klienterna får additional path visibility i
förväg kan RR introducera högre konvergeringstid samt att man tappar
multi-pathing. Detta går att lösa med Additional Paths. Eftersom RR kör
best path utifrån sitt eget perspektiv (IGP cost) kan det även leda till
sub-optimal routing. Om man kör IP forwarding istället för label
forwarding kan även forwarding loopar skapas i vissa scenarier på grund
av RR-placering. Som generell regel kan man säga att BGP-sessionerna
inte ska avvika för mycket ifrån forwarding topology. Detta gäller
alltså inte när man använder mpls vpn för all data plane, då spelar
placering i princip ingen roll.

Man måste också bestämma om det ska vara vanlig iBGP eller
route-reflector-client till andra kluster och det beror på vilken
redundansdesign man valt. Kör man non-client finns det vissa
failure-situationer som kan leda till traffic black holes. Väljer man
client kommer man att få in uppdateringar med det man själv annonserar
ut dvs feedback loop. Detta är inga problem med små BGP-tabeller men kan
ställa till det med stora.

RR-server

`router bgp 65000`
` neighbor 1.1.1.1 remote-as 65000`
` neighbor 1.1.1.1 update-source lo0`
` neighbor 1.1.1.1 route-reflector-client`

Kluster konfigureras på RR-server, sätt samma cluster-id på de RR som
ska ingå i klustret. Man kan ha flera kluster.

`router bgp 65000`
` bgp cluster-id 5`

RR-klienter känner inte till RR-konceptet så de konfigureras som vanlig
iBGP.

`router bgp 65000`
` neighbor 2.2.2.2 remote-as 65000`
` neighbor 2.2.2.2 update-source lo0`

Verify

`show ip bgp update-group`

Det är inte alltid RR finns i forwarding path, då kan man använda
"Selective RIB Download" för att spara lokala resurser. All NLRI finns i
BGP-tabellen som vanligt för best-path och annonsering men det behöver
ju aldrig läggas in entries i RIB/FIB. En table-map är en route-map för
BGP-tabellen istället för per grannskap.

`table-map BORD filter`

Confederations
--------------

BGP confederations (RFC 5065) delar upp ett AS i flera sub-AS. Routrar
inom samma sub-AS är confederation iBGP-grannar medans mellan sub-AS är
confederation eBGP-grannar. iBGP fungerar precis likadant, dvs routes
lärda från iBGP annonseras ej vidare till iBGP-grannar och det behövs
således full mesh grannskap alternativt en route reflector inom varje
sub-AS. För att undvika loopar används path attributet AS_PATH.
Istället för de vanliga AS_SEQ och AS_SET används AS_CONFED_SEQ och
AS_CONFED_SET. Confed-AS räknas som ett AS vid path selection. Finns
en grannes sub-AS redan med i AS_CONFED_SEQ så kommer prefixet inte
att annonseras till den. När det gäller confederation eBGP används TTL 1
precis som med vanlig eBGP däremot ändras inte NEXT_HOP default mellan
sub-AS. Om ett prefix ska annonseras ut från en confederation tas
confederation ASN bort från AS_PATH så utsidan ser endast ett AS.

`router bgp 65000`
` bgp confederation identifier 123`

För att routern ska veta att det är ett confederation eBGP-grannskap och
inte ett vanligt ange *bgp confederation peers*. Detta behövs inte på
routrar som ej har confederation eBGP-grannskap.

`router bgp 65000`
` bgp confederation peers 65001`
` neighbor 10.0.0.20 remote-as 65001`

Redistribution
--------------

Man måste vara försiktig när man redistribuerar mellan IGP och BGP
eftersom BGP klarar så mycket fler routes än någon IGP. Default så
redistribueras endast eBGP till andra protokoll pga att iBGP inte har
någon egen loop prevention mekanism. Man kan ändra detta men det bör man
inte göra.

`bgp redistribute internal`

**OSPF**
Only internal OSPF routes will be redistributed into BGP by default.

`redistribute ospf 1 `
`redistribute ospf 1 route-map SET-ORIGIN  # betyder allt i rib dvs externals följer med`

Dampening
---------

Förutom att använda route aggregation för att minska risken att CPU går
i taket på alla enheter när något flappar kan dampening användas.

`route-map DAMPENING permit 10`
` set dampening 5 1900 2000 10`

5=half-life, 1900=reuse-limit, 2000=suppress-limit, 10
max-suppress-limit

`router bgp 100`
` bgp dampening route-map DAMPENING`

Route flap

`show ip bgp flap-statistics`
`show ip bgp dampening parameters`

Conditional Route Injection
---------------------------

The ability to insert more specific prefixes into BGP without having
them in the IP routing table. Routemap which specifies prefixes to
inject and routemap which specifies exist condition (Det går även köra
med non-exist om man vill vända på det)

`ip prefix-list INJECT-THIS permit 110.0.1.0/24`
`ip prefix-list INJECT-THIS permit 110.0.2.0/24`
`ip prefix-list AGGREGATE permit 110.0.0.0/8`
`ip prefix-list SOURCE permit 1.1.1.1/32`

`route-map INJECT`
` set ip address prefix-list INJECT-THIS`

`route-map EXIST`
` match ip address prefix-list AGGREGATE`
` match ip route-source prefix-list SOURCE`

`router bgp 100`
` bgp inject-map INJECT exist-map EXIST`

The less-specific prefix MUST come from a BGP neighbor. No insertion of
more-specific prefixes of a locally-originated prefix.

Verify

`show ip bgp injected-paths`
`show ip bgp neighbors 1.1.1.1 | i status`

### Conditional Advertisement

Conditional advertisement tillåter att man per neighbor endast
annonserar utvalda prefix om vissa prefix existerar/inte existerar i den
lokala BGP-tabellen, som kollas av BGP scanner/NHT.

`route-map ADVERTISE_MAP permit 10`
` match as-path 1`

`ip prefix-list PREFIX permit 10.0.10.0/24`

`route-map NON_EXIST_MAP permit 10`
` match ip address prefix-list PREFIX`

`router bgp 100`
` neighbor 1.1.1.1 advertise-map ADVERTISE_MAP non-exist-map NON_EXIST_MAP`

Flowspec
--------

BGP flow specification är en feature som man kan använda för att
propagera filter- och policy-funktionalitet till sina BGP-noder. Det kan
användas för att mitigera DDoS-attacker. Med flowspec går det att
filtrera mycket mer granulärt än med Remote Trigger Blackhole (RTBH).
Man har även fler möjligheter för vad man vill göra med attacken, t.ex.
drop eller police, next-hop eller VRF redirect, DSCP Markings. Flowspec
implementeras som en adressfamilj. IOS XE har stöd för flowspec client
function men som flowspec controller behövs något annat. Controllern som
t.ex. kan lyssna på ett DDoS-detekteringssystem skickar ut flowspec NLRI
till klienterna, detta säger vad som ska göras med vilken trafik. Ju
fler och ju mer avancerade regler man skjuter ut ju mer TCAM går åt.

Det finns flera mjukvaror som kan agera controller, t.ex.
[IOS-XR](/Cisco_IOS-XR "wikilink"), GoBGP eller
[ExaBGP](/ExaBGP "wikilink").

IOS XE

`flowspec`
` address-family ipv4`
`  local-install interface-all`

`router bgp 100`
` address-family ipv4 flowspec`
`  neighbor 10.1.1.1 activate`

Verify

`show flowspec summary `
`show bgp ipv4 flowspec `

BMP
---

The BGP Monitoring Protocol (BMP) feature supports functionality to
monitor Border Gateway Protocol (BGP) neighbors. Det kan t.ex. användas
för BGP Looking glass och/eller advanced route analytics. Det kan även
underlätta vid route-policy troubleshooting. BMP devices (routers)
skickar BMP messages till en BMP collector/daemon, t.ex.
[OpenBMP](https://github.com/OpenBMP/openbmp).

`router bgp 65000`
` neighbor 30.1.1.1 bmp-activate server 1`
` bmp server 1`
`  address 10.0.0.10 port-number 8000`
`  activate`

Verify

`show ip bgp bmp server 1`
`show ip bgp bmp server summary`

RPKI
----

"Resource Public Key Infrastructure allows IP address holders to specify
which Autonomous Systems (AS’s) are authorized to originate their IP
address prefixes." RPKI ökar dock komplexitet. Konfigurera RPKI
Cache-server, RPKI Prefix Validation, BGP Prefix Validation och RPKI
Bestpath Computation.

**IOS**

`router bgp 100`
` bgp rpki server tcp 10.0.10.10 port 1333 refresh 600`

Slå av Validation of BGP Prefixes men ladda ner RPKI Information.

`bgp bestpath prefix-validate disable`

Tillåt Invalid Prefixes som Best Path.

`bgp bestpath prefix-validate allow-invalid`

Announce RPKI information mha Extended Community

`neighbor 1.1.1.1 announce rpki state`

Verify

`show ip bgp rpki servers`
`show ip bgp rpki table`
`clear ip bgp rpki server`

**IOS-XR**
Fr.o.m. XR 6.5.1 är origin-as validation disabled by default.

`router bgp 1`
` rpki server 10.0.0.10`
`  transport tcp port 3323`
`  refresh-time 600`
`!`
`bgp bestpath origin-as use validity`
`bgp bestpath origin-as allow invalid`
`address-family ipv4 unicast`
` bgp origin-as validation signal ibgp`

Verify

`show bgp rpki summary`

Route Server
------------

BGP route server är feature designad för internet exchange (IX)
operators som ger ett alternativ till full eBGP mesh peering inne på
IXP. Det tillhandahåller route reflection med support för unik policy
per service provider. Route server ger transparens för AS-path, MED och
next-hop så SPs som peerar med varandra fortfarande kan göra det som
directly connected men IX route server medlar denna peering. Detta är
osynligt utanför IX. Route server leder till mindre konfiguration samt
CPU/minnesanvändning på varje border router.

`router bgp 1337`
` neighbor 10.0.0.1 remote-as 100`
` neighbor 10.0.0.2 remote-as 200`

` address-family ipv4 unicast`
`  neighbor 10.0.0.1 activate`
`  neighbor 10.0.0.1 route-server-client`
`  neighbor 10.0.0.2 activate`
`  neighbor 10.0.0.2 route-server-client`

`show ip bgp ipv4 unicast route-server all summary`

Default så nekar en router uppdateringar från en eBGP-peer som inte har
det egna ASN i början av as-path. Detta gör att en route servers
beteende inte är okej så denna check måste stängas av på alla border
router.

`router bgp 100`
` no bgp enforce-first-as`
` neighbor 10.0.0.137 remote-as 1337`

[Category:Cisco](/Category:Cisco "wikilink")