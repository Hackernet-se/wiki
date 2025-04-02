---
title: Cisco PIM
permalink: /Cisco_PIM/
---

För att routrar ska kunna veta vilka andra routrar som har
multicast-källor och mottagare används något protokoll (control plane),
DVMRP, MOSPF eller PIM. De berättar vilka nät som är med i olika
multicastgrupper. För loop prevention används RPF och inga paket
forwarderas utan att klara denna check. Det som skiljer Protocol
Independent Multicast från DVMRP och MOSPF är att det inte är något
routingprotokoll utan ett signaleringsprotokoll, dvs det distribuerar
ingen routinginformation. PIM använder unicast RIB:en för RPF-checken
medans de andra protokollen bygger sina egna tabeller och kör RPF mot.
Med IPv6 körs PIM default på alla interface när man slår igång ipv6
multicast-routing.

Se även [Cisco Multicast](/Cisco_Multicast "wikilink"). Man kan även
använda PIM över [GRE](/Cisco_GRE "wikilink")-tunnlar.

### Neighbor

PIMv2 formar adjacencies och använder 224.0.0.13 neighbor discovery
(Hellos) och updates. PIMv2 Hellos skickas default var 30:e sekund på
interface konfigurerade för PIM. Hello innehåller holdtime som brukar
vara 3 ggr Hello time. Det äldre PIMv1 använde inte Hellos utan skickade
Queries till 224.0.0.2.

**Paket**

-   PIM Hello
-   PIM Join
-   PIM Prune
-   PIM Assert
-   PIM Graft
-   PIM Register

Konfiguration
-------------

Global enable. På vissa enheter är kommandot *ip multicast-routing
distributed*

`ip multicast-routing`
`show ip multicast`

**Default konfiguration** (detta kan skilja mellan IOS-version)

Globalt

`ip pim dm-fallback`
`ip pim autorp`
`ip pim bidir-offer-interval 100 msec`
`ip pim bidir-offer-limit 3`
`ip pim v1-rp-reachability`
`ip pim log-neighbor-changes`

Per interface

`ip pim join-prune-interval 60`
`ip pim dr-priority 1`
`ip pim query-interval 30`

Gå med i grupp manuellt

`ip igmp join-group 224.10.0.10`

Verify

`show ip mroute`
`show ip mroute active`
`show ip mroute count`
`show ip pim interface`
`show ip pim neighbor`
`show ip rpf x.x.x.x `

**Limiting**
Global multicast mroute limit

`ip multicast limit cost `<ACL>` `<cost>

Maximum number of multicast routes, default är 2147483647.

`ip multicast route-limit 100`

Multicast boundary feature tillåter att man begränsar multicast både
control plane och data plane per interface. Med standard acl filtreras
grupp och med extended både grupp och källa. Detta filtrerar också
Auto-RP announcements. Att begränsa multicast kan även göras med TTL
scoping.

`ip multicast boundary [ACL]`

**NBMA**
Det finns inbyggd loop prevention för multicast i form av split horizon.
I vissa topologier (t.ex. [DMVPN](/Cisco_DMVPN "wikilink")) måste
multicast-paket skickas ut på samma interface som det kom in på för att
det ska fungera och det går att konfigurera per interface. PIM NBMA mode
gör att PIM håller reda på OIL som interface + NBMA-adress, istället för
bara interface. Detta är inte kompatibelt med PIM-DM.

`ip pim nbma-mode`

**Multipath**
Att slå på ECMP Multicast Load Splitting gör att Joins till RP kommer
att skickas på fler än ett interface och man måste använda en hash
annars kommer RPF-check att faila.

`ip multicast multipath`
`ip multicast multipath s-g-hash`

Dense Mode
==========

Dense mode utgår ifrån att alla subnät har någon som vill ta emot
multicast-trafik därför kommer paketen att forwarderas ut på alla
interface som är konfigurerade för multicast utom det som det kom in på.
Alla routrar gör samma sak och alla subnät får strömmen, detta träd
kallas *source-based distribution tree* eller *shortest-path tree*. Det
finns dock möjlighet för routrar att begära att inte få paket för vissa
multicast-grupper om man inte har någon router downstream som är aktiv i
gruppen samt ej heller någon enhet på ett directly connected interface
som är med i gruppen. Då skickas ett Prune message upstream för att
berätta detta. Prune har timeout 3 minuter, sedan återgår interfacet
till forwarding. För att förhindra pendlandet mellan Pruned och
Forwarding kom PIMv2 med en feature som kallas *State refresh*. Om
downstream fortfarande inte vill vara med i multicastströmmen kan den
skicka ett State refresh upstream för att nollställa Prune timer, detta
skickas var 60:e sekund. Behöver en router plötsligt lyssna på en
multicastgrupp (för att den fått in IGMP Join) kan den "unprune" genom
att skicka ett Graft message upstream som gäller så fort det kommer fram
vilket sänker konvergeringstiden. Det ackas med Graft Ack. För Dense
mode kan olika multicast-routingprotokoll användas. PIM Dense mode
skalar inte superbra pga excessive flooding.

`interface gi2`
` ip pim dense-mode`

Verify

`show ip pim interface`
`show ip mroute`

Sparse Mode
===========

Det är inte säkert att alla nät har någon mottagare av multicast, därför
finns Sparse mode (RFC 4601) som inte använder lika mycket
nätverksresurser som Dense mode. Den stora skillnaden är deras
default-beteende. Med IPv6 finns endast Sparse mode. Default är att inte
skicka vidare paket downstream om man inte fått ett Join meddelande som
begär paket för en viss multicast-grupp. Detta händer när det har kommit
in ett IGMP Join message på ett directly connected interface eller en
annan router downstream har begärt trafik för gruppen. Multicast
forwardas sålänge det kommer Join-meddelanden. Vem som ska ha vad hålls
koll på av en Rendezvous Point som alla måste känna till. I små nät görs
detta manuellt och i större nät kan detta göras automatiskt.

När en Source host skickar multicast-trafik första gången kommer routern
som tar emot det att enkapsulera paketet i ett PIM Register och skicka
det med unicast till RP. Känner inte RP till någon downstream som begärt
denna ström kommer den att svara med ett Register-Stop meddelande och
den första routern ska inte forwarda denna multicast-ström.
Register-Suppression timer startar då och router väntar 1 minut minus 5
sekunder sedan frågar den RP igen men denna gång utan det enkapsulerade
mc-paketet utan Null-Register biten är satt istället. Däremot om RP
känner till någon som vill ha multicast-strömmen kommer den att
dekapsulera paketet och forwarda det. På så sätt fungerar multicast
tills registration process är klar. När en PIM-SM router längs vägen får
in ett PIM Join sätts interfacet i forwarding för den multicastgruppen.
För att multicast ska fortsätta forwardas måste routrar forsätta skicka
PIM Joins annars blir gruppen pruned. En router fortsätter med detta om
den själv får in Joins eller någon host på ett directly connected
interface svarar på IGMP Queries. Prune timer är default 3 minuter.

Med sparse mode används shared trees som betecknas (\*,G). RP kommer att
gå med både i (\*,G) men också (S,G) där S är source för strömmen. Finns
det flera källor till strömmen kommer det först att gå till RP för att
sedan forwardas ut shared distribution tree / root-path tree. Det finns
även möjlighet för en PIM-SM router att bygga SPT direkt med källan.
Ifall man har närmre till källan är det onödigt att all trafik ska gå
igenom RP först. Då kan routern faktiskt meddela RP med ett Prune
message att multicast-strömmen inte behöver skickas till den längre.
Ciscoroutrar gör detta byte direkt efter första paketet, detta går att
ändra med **ip pim spt-threshold infinity**.

På alla enheter (static RP):

`ip multicast-routing`
`ip pim rp-address 10.0.0.10 [override]`

`interface gi2`
` ip pim sparse-mode`
`interface gi3`
` ip pim sparse-mode`

På Rendezvous Point utöver det ovan. En router vet om att den är RP om
den har ett interface med den konfigurerade rp-adressen. Man måste kör
PIM på det interface man annonserar som RP.

`interface lo0`
` ip address 10.0.0.10 255.255.255.0`
` ip pim sparse-mode`

För att förhindra att oönskade RPs och grupper blir aktiva i ens nät kan
man skydda sig med filter. Man skriver standard-acler som listar de
grupper som är tillåtna, till exempel tillåt endast join och prune
messages från RP 10.0.0.10 som har med grupp 224.4.4.4 att göra. Det
räcker att konfigurera detta på RP men det bör göras överallt.

`ip access-list standard ALLOWED_GROUPS`
` permit 224.4.4.4`

`ip pim accept-rp 10.0.0.10 ALLOWED_GROUPS`

Verify

`show ip mroute`
`show ip pim rp mapping`
`show derived-config interface tunnel0`

På RP skapas två stycken tunnel interface, ett för att enkapsulera PIM
Register messages och ett för att dekapsulera.

`show ip pim tunnel`

### Sparse Dense Mode

PIM Sparse-Dense mode är en hybrid av Sparse och Dense mode operations.
En “sparse” multicast-grupp är en som har RP definierat. När man kör *ip
pim sparse-dense-mode* på ett interface så kommer det att forwardera
trafik både för sparse och dense multicast groups ut på det interfacet.

`interface gi2`
` ip pim sparse-dense-mode`

Stänga av dense mode fallback.

` no ip pim dm-fallback`

Auto-RP
-------

I Sparse mode måste alla multicast-routrar känna till RP, i större nät
blir detta mödosamt att konfigurera. Det finns två mekanismer för att
upptäcka RP automatiskt, Auto-RP och BSR (se nästa stycke). Auto-RP är
ett Ciscoproperitärt protokoll som använder 224.0.1.39 och 224.0.1.40
för kommunikation, dvs multicast som routas. Enheter som kör Auto-RP och
vill vara RP (candidates) skickar först ut RP-Announce till 224.0.1.39
med sig själv satt som RP. Det skickas ut var 60:e sekund och det
innehåller vilka multicast-grupper man är RP för. Detta leder till att
olika routrar kan vara RP för olika grupper vilket ger lastdelning.
Sedan måste någon vara mapping agent (vanligtvis samma enhet) som lär
sig alla RPs och vilka grupper de är med i för att kunna sprida
informationen. Genom att gå med i 224.0.1.39 får man all info från RPs.
Alla Cisco-enheter som är konfigurerade för Auto-RP och Sparse mode går
med i 224.0.1.40. Mapping agent skickar sedan ut RP-Discovery
innehållandes RP-mappningar till 224.0.1.40 port 496 och alla kan lära
sig var RP finns. Finns det flera cRPs för samma grupp väljs den som
annonserar longest match annars blir det den med högst RP-IP. Finns det
flera mapping agents så kommer de att höra varandra och de som inte har
högst IP slutar då skicka discoveries. Anledningen till att man behöver
mapping agents överhuvudtaget är för att annars skulle det kunna uppstå
situationer där olika routrar har valt olika RPs för samma grupp.

Eftersom Auto-RP kommunicerar med multicast och sparse mode inte
forwardar multicast utan RP så får man antingen köra sparse-dense-mode
alternativt köra en inbyggd IOS feature som gör undantag för 224.0.1.39
och 224.0.1.40, detta kallas Auto-RP Listener och konfigureras globalt.

`ip pim autorp listener`

Candidate RP

`ip access-list standard GROUPS`
` permit 224.0.0.0 7.255.255.255`

`ip pim send-rp-announce Loopback0 scope 10 group-list GROUPS`

Multicast mapping agent

`ip pim send-rp-discovery Loopback0 scope 10`

Filtrera announcements från RPs, görs på MA med standard-acler.

`ip pim rp-announce-filter rp-list `<access-list>` group-list `<access-list>

Verify

`show ip pim autorp`
`show ip pim rp mapping`

`clear ip pim rp-mapping`

Auto-RP Cache Filtering
Accept only (\*, G) join messages destined for the specified Auto-RP
cached address. Accept join and prune messages only for RPs in Auto-RP
cache.

`ip pim accept-rp auto-rp`

BSR
---

En annan metod för att automatiskt hitta RP är PIM Bootstrap Router och
fungerar på liknande sätt som Auto-RP. BSR fungerar som mapping agent i
Auto-RP, de får in information från RPs som de sedan distribuerar
vidare. Dock väljer inte BSR någon bästa RP utan information om alla
skickas ut och övriga får välja själv vilken som är bäst. BSR floodar
detta till all-PIMv2-routers (224.0.0.13). PIM-SM routrar floodar
bootstrap messages på alla non-RPF interfaces vilket leder till att alla
multicast-routrar får informationen. Kommer det in bootstrap message på
non-RPF interface discardas det vilket förhindrar loopar. Alla c-RP kan
berätta för BSR att de är RP och vilka grupper den är med i tack vare
att alla vet unicast-adressen till BSR eftersom den har floodats till
alla. RPs skickar c-RP Advertisments till BSR. Man kan ha redundanta RPs
och redundanta BSRs. Har man flera RPs för samma grupp har BSR en
pseudo-random funktion för att fördela lasten mellan dem. Dock kan
endast en vara preferred BSR och skicka bootstrap messages, de övriga
lyssnar och tar över när preferred BSR tystnar. Den som blir preferred
avgörs av högst prio och sedan högst IP. BSR-meddelanden själva
RPF-checkas.

BSR (default prio är 0)

`interface lo0`
` ip pim sparse-mode`
`ip pim bsr-candidate Loopback0 `<prio>

RP

`interface lo0`
` ip pim sparse-mode`
`ip pim rp-candidate Loopback0 `

Border

`interface gi3`
` ip pim bsr-border`

Verify

`show ip pim bsr-router `
`show ip pim rp mapping `

Anycast RP
----------

Behöver man både redundans och lastdelning kan man sätta upp flera RPs
med samma IP-adress och på så sätt få Anycast RP. Det är inget eget
protokoll i sig utan en implementation feature och man kan använda både
static RP, Auto-RP och BSR. Varje RP måste annonsera samma /32-prefix
till IGP som då står för att dirigera trafiken (PIM Joins) till närmaste
RP. RP-konfiguration görs som vanligt med någon av ovan nämnda metoder.
Om en RP dör är konvergeringstiden den tid det tar för IGP att hitta en
annan väg till samma destination. Varje RP bygger sina egna träd
oberoende av eventuella övriga RPs för samma grupper men för att hålla
allas information konsekvent bör man (med IOS) använda MSDP mellan RPs,
se nedan.

Bidirectional PIM
-----------------

PIM-SM fungerar bra med relativt få multicast senders men när antalet
ökar blir det mindre effektivt. Bidirectional PIM kan hjälpa mot detta
genom att ändra reglerna litegrann. Det är ett tillägg till Sparse mode
konceptet som endast använder shared trees, dvs det finns inga
source-based trees. Det är mest effektivt när de flesta receivers
samtidigt också är senders. För att kunna bygga bi-directional trees
utan att introducera loopar väljs designated forwarders (DFs) på varje
länk. Det är endast dem som får skicka något upstream i trädet. För
downstream hålls (\*,G) state för varje BiDir-grupp med OIL byggd
utifrån mottagna PIM Join messages som vanligt. Istället för att den
första router som tar emot multicast enkapsulerar paketet och skickar
det som PIM Register till RP kommer den att skicka upp det längs det
delade trädet mot RP och gör så med alla multicastpaket som kommer in.
RP kommer också att forwarda i det delade trädet och RP eller routern
närmast källan går inte med i något SPT. Detta gör det viktigt var man
placerar RP. Eftersom det inte finns någon source registration process
kommer inga tunnlar att skapas.

Bidirectional PIM måste konfigureras på alla PIM-enheter.

`ip pim bidir-enable`
`ip pim rp-candidate Loopback0 group-list 10 `**`bidir`**

Show designated forwarders

`show ip pim interface df`

**Phantom RP**
För redundans kan man använda en RP-IP som faktiskt inte finns konfad på
någon enhet. Eftersom inga paket har destination RP-IP utan endast ska
skickas upp mot RP behöver det inte vara en interface-adress. Det räcker
med en route i routingtabellen. Man kan t.ex. konfa prefix som
innehåller RP-IP:n men har olika masklängd på olika enheter, på så sätt
kan andra noder ta över RP (tack vare IGP-konvergens) när primären går
ner.

`interface Loopback1`
` description Primary RP`
` ip address 10.10.11.1 255.255.255.252     <- /30`
` ip pim sparse-mode`
` ip ospf network point-to-point`
` ip router ospf 1 area 0.0.0.0`

`ip pim rp-address `**`10.10.11.2`**` group-list 225.0.0.0/24 bidir`

Source Specific Multicast
=========================

Med SSM kan hostarna själva välja source för trafikströmmen ifall det
finns flera. Det kan även skydda mot dos-attacker eftersom mottagare
berättar för nätverket vilka källor de vill få trafik ifrån. Det ger
också fördelar med att överlappande grupp-adresser kommer att fungera
eftersom olika källor gör det unikt. Det finns inga shared trees med SSM
utan allt hanteras som source trees. Det behövs heller inga RPs eftersom
källan är känd.

Source Specific Multicast kräver IGMPv3 samt någon variant av sparse
mode.

`interface gi2`
` ip igmp version 3`
` ip pim sparse-mode`

Sedan väljer man range som enheterna ska behandla som SSM, dvs droppa
eventuella (\*,G). *Default* innebär 232.0.0.0-232.255.255.255 som är
IANA assigned SSM range.

`ip pim ssm default`

Verify

`show ip mroute`

MSDP
====

Multicast Source Discovery Protocol (RFC 3618) används för inter-domain
IPv4 multicasting och för att låta RPs i ett enskilt AS dela information
om de kör Anycast RP. MSDP kan användas mellan RPs för att berätta vilka
källor de känner till. När en PIM router registrerar en multicastkälla
till sin RP kommer den att använda MSDP för att skicka denna info till
sina peer RPs. Source Active meddelanden innehåller IP-adress för varje
källa för varje grupp, enheter på andra sidan kan då bygga SPT för
respektive sender. Meddelandena skickas var 60:e sekund med TCP över
unicast mellan peers och blir besvarade med SA response paket. Detta
grannskap måste konfigureras och unicast route till andra sidan måste
finnas. [BGP](/Cisco_BGP "wikilink") eller [Multicast
BGP](/Cisco_Multicast#BGP "wikilink") kan användas för detta.

`ip msdp peer [peer_unique_address] connect-source loopback0 remote-as 100`
`ip msdp originator-id [unique_address_interface]`

RPF checken kräver full routing information från andra domäner för att
multicast ska fungera. Om man t.ex. har en stub multicast domain och
inte får in all information kan man konfigurera upstream RP som
*default-peer* för RPF checkar används inte på default peers utan alla
SA messages accepteras.

`ip msdp default-peer`

Verify

`show ip msdp summary`
`show ip msdp peer`
`show ip msdp sa-cache`

### Mesh Group

MSDP mesh group är en optimerings-feature som reducerar mängden
SA-trafik när man har fler än två MSDP peers i samma domän. Alla MSDP
speakers har fully meshed MSDP-konnektivitet mellan varandra, dvs alla
har peering med samtliga routrar i gruppen. Detta gör att SA flooding
kan optimeras genom att SA messages inte behöver floodas till andra mesh
group peers. Värt att notera är också att det inte görs någon RPF check
på inkomna SA messages från mesh group peers utan de accepteras alltid
när MSDP mesh group är konfigurerat.

`ip msdp peer 10.1.1.1`
`ip msdp peer 10.2.2.2`
`ip msdp mesh-group mesh-group1 10.1.1.1`
`ip msdp mesh-group mesh-group1 10.2.2.2`

Convergence
===========

Multicast Subsecond Convergence är möjligt genom att använda flera olika
tekniker.

`ip multicast rpf interval 10`
`ip pim register-rate-limit rate 10`
`ip pim spt-threshold 0`

`interface gi2 `
` ip pim query-interval 30`

**BFD**
Konvergenstider går också att trimma med hjälp av
[BFD](/Cisco_BFD "wikilink").

`ip pim bfd`

LAN
===

Detta gäller både PIM-DM och PIM-SM.

### Prune Override

Om det finns flera routrar i samma L2-segment som vill ha multicast
kommer det att sluta funka när en av dem ber upstream router att pruna
en multicastgrupp. Därför kommer den som på multiaccess-segment tar emot
Prune att vänta 3 sekunder innan den slutar forwarda multicastströmmen
på sitt interfacet. Eftersom Prune går till 224.0.0.13 så får alla
PIM-routrar det och de som vill fortsätta få strömmen kan skicka ett
vanligt Join-meddelande igen då kommer inte upstream sluta forwarda,
detta kallas Prune Override. Detta är inget som konfigureras utan det är
en funktion som är på default.

### Assert Message

Om det finns flera routrar på ett LAN-segment som är aktiva för en
multicastgrupp kommer det att skickas in dubbel trafikström till
hostarna, detta är onödigt. När en router får in ett multicast-paket som
den själv forwarderar in på nätet kommer den att skicka ett PIM Assert
Message. Med hjälp av det kan routrarna jämföra path cost till källan
för SPT där endast vinnaren kommer att forwarda multicastströmmen in på
LANet. Path cost består av kombinationen (AD, Metric) och först jämförs
AD på routingprotokollet som har lärt vägen till källan sedan kollas på
IGP-metricen för att skilja. Är detta också lika går man på högst
IP-adress på interface. Den som förlorar slutar att flooda multicasten.
I hub-and-spoke topologier bör alltid hub vinna förutsatt att man inte
köra PIM i NBMA mode.

<div class="mw-collapsible mw-collapsed" style="width:310px">

Assert message:

<div class="mw-collapsible-content">

[<File:Cisco_PIM_Assert.PNG>](/File:Cisco_PIM_Assert.PNG "wikilink")

</div>
</div>

### Designated Router

PIM Designated Router (DR) väljs på varje segment där det finns multipla
multicast-routrar. Syftet med DR är att ha en nod som signalerar aktiva
källor till RP. Valet baseras på högsta prioritet och vid lika högsta
IP-adress. Processen är preemptive så det är alltid den med bäst prio
som är DR. Detta är en sparse-mode feature.

`interface gi2`
` ip pim sparse-mode`
` ip pim dr-priority 100`

`show ip pim neighbor`

På RP kan begränsa vem som får skicka PIM Register från olika segment
med hjälp av en extended acl, dvs man kan vitlista vem som är en giltig
DR.

`ip access-list extended VLAN100`
` permit ip host 100.0.100.10 any`
` deny   ip 100.0.100.0 0.0.0.255 any`
` permit ip any any`

`ip pim accept-register list VLAN100`

### PIM Snooping

Man kan begränsa multicastpaket för varje grupp så att endast multicast
router ports som har någon downstream receiver med i gruppen får
trafiken. När man slår på PIM snooping så kommer switchen att lära sig
vilka mrouter-portar som ska ha vilka multicast-strömmar i varje vlan
genom att lyssna på PIM hello messages, PIM join/prune messages och
bidirectional PIM designated forwarder-election messages. Join och prune
kommer inte att floodas på alla mrouter-portar utan skickas till den
port med upstream router som finns i payloaden på join/prune messages.
All information om mroutes och routrar kommer att timeas ut baserat på
den information som står i hellos, joins och prunes. Dense mode trafik
ses som unknown och kommer att droppas men Auto-RP-paket kommer alltid
att floodas.

För att använda PIM snooping måste IGMP snooping vara på.

`ip igmp snooping`
`ip pim snooping`

Verify

`show ip pim snooping`

IPv6
====

Multicast routing är inte på default för IPv6 men när man slår på det så
enableas PIM på alla IPv6-interface. IPv6 PIM kör alltid sparse mode.
Reverse-path använder routingtabellen vilket gör det protokoll-oberoende
precis som för IPv4. PIM-grannskap byggs med hjälp av link-local
adresser och det finns tre pakettyper: Query, Report och Done. DR väljs
som vanligt och Hellos skickas var 30:e sekund. Multicast address range:
FF00::/8.

`ipv6 multicast-routing`

`interface gi2`
` ipv6 mld access-group MLD_FILTER`
` ipv6 mld query-max-response-time 10`
` ipv6 mld query-timeout 255`
` ipv6 mld query-interval 125`
` ipv6 mld join-group ff08::10 `

Stänga av PIM

`interface gi3`
` no ipv6 pim`

Static routes, dessa används endast av multicast.

`ipv6 route 2000::/64 tun0 `**`multicast`**

Verify

`show ipv6 pim neighbors`
`show ipv6 pim interface`
`show ipv6 pim tunnel`
`show ipv6 mld groups `

### RP

Med IPv6 kan RP lösas på tre olika sätt. Det finns ingen Auto-RP eller
MSDP för IPv6.

**Static**

`ipv6 pim rp-address 2001:20::20`

`show ipv6 pim range-list`

**BSR**
BSR fungerar på samma sätt för IPv4 men nu konfigureras det med en
adress istället för interface samt att source registration process
skiljer litegrann. Så fort en multicast-router lär sig RP-adressen
skapar den en tunnel dit som kör multicast så när det kommer inte en
mc-ström så skickas den genom tunneln till RP. Tunneln används endast
under registration process, sedan slår sista-hop-routern över till SPT.
Man kan också konfigurera BSR med en lista på RP-kandidater genom att
använda *ipv6 pim bsr announced rp <IPv6 Address>* och därmed behöver
inte RPs annonsera sig själva som candidates.

`ipv6 pim bsr candidate bsr 2001:20::20`

RP

`ipv6 pim bsr candidate rp 2001:20::20`

Verify

`show ipv6 pim bsr election`

**Embedded RP**
Med IPv6 kan också övriga routrar ta reda på vem som är RP utifrån en
adress som kan bakas in i grupp-adressen (RFC 3956). Ser en router denna
adress kan de räkna ut vad RP har för adress ([RP
Calculator](http://www.interlab.ait.asia/tein3/ipv6mcast/asm.php)) och
direkt börja forwarda i det delade trädet. Endast RP behöver
konfigureras och övriga kan lära sig det dynamiskt. Fungerar endast med
grupper i Embedded RP address range: FF70::/12.

På default:

`ipv6 pim rp embedded`

`interface Tunnel0`
` description Pim Register Tunnel (Encap) for Embedded RP`
` no ip address`
` ipv6 unnumbered Loopback0`
` ipv6 enable`
` tunnel source Loopback0`
` tunnel destination ::`
` tunnel ttl 65`

RP (loopback-adressen måste annonseras i IGP så alla kan hitta dit)

`interface Loopback1`
` ipv6 address 2006:6666::5/128`

`ipv6 pim rp-address 2006:6666::5`

Receivers

`ipv6 mld join-group FF7E:540:2006:6666::1`

Verify

`show ipv6 mroute`
`show ipv6 pim group-map`

**Anycast RP**
Man kan använda anycast för att öka tillgängligheten på RP. Att
distribuera RP-infon görs med någon ovan nämnd metod, detta är endast
för att hålla mroute-tabellerna synkade mellan alla RPs.
Loopback-adressen måste annonseras i IGP så alla kan hitta dit.

RP1

`ipv6 pim anycast-rp 2001:20::20 10::2`
`interface Loopback1`
` ipv6 add 10::1/128`
` ipv6 add 2001:20::20/128`

RP2

`ipv6 pim anycast-rp 2001:20::20 10::1`
`interface Loopback1`
` ipv6 add 10::2/128`
` ipv6 add 2001:20::20/128`

Verify

`show ipv6 pim anycast-rp`

### SSM

IPv6 SSM fungerar ungefär som embedded RP multicast fast det inte finns
något embedded RP prefix eftersom MLD tillhandahåller den informationen.
SSM mapping kan användas för hostar som inte stödjer MLDv2, då kan man
antingen använda DNS eller static maps för att kolla upp källan i MLDv1
report.

`interface gi3`
` ipv6 mld join-group FF36:10::10 2001:20::20`

NX-OS
=====

Här följer [Nexus](/Cisco_Nexus "wikilink")-specifik information.
Beroende på skillnader i hårdvara mellan de olika Nexusplattformarna
finns det stöd för olika multicast capabilities, referera alltid till
Ciscos dokumentation. Några grundläggande skillnader mot IOS är att det
saknas stöd för IGMP version 1 och Version 3 Lite, PIM version 1 och
dense mode operation. PIM har även SSM group range 232.0.0.0/8 by
default (även i VRF:er). Se även [IGMP](/Cisco_IGMP#NX-OS "wikilink")
för NX-OS.

### Konfiguration

`feature pim`

`ip pim log-neighbor-changes`
`ip pim rp-address 172.16.1.10 group-list 224.0.0.0/4`
`ip pim bfd`

`interface Ethernet1/1`
` ip address 192.168.1.1/24`
` ip pim sparse-mode`

**VRF**

`vrf context Tenant1`
` ip pim rp-address 172.16.1.10 group-list 224.0.0.0/4`

**Auto-RP**

`ip pim auto-rp rp-candidate loopback1 group-list 224.0.0.0/4`
`ip pim auto-rp mapping-agent loopback1`
`ip pim auto-rp forward listen`

**BSR**

`ip pim bsr bsr-candidate loopback1`
`ip pim bsr rp-candidate loopback1 group-list 224.0.0.0/4`
`ip pim bsr forward listen`

**Neighbor Authentication**

`interface Ethernet1/1`
` ip pim sparse-mode`
` ip pim hello-authentication ah-md5 3 a667d47acc18ea6b`

**Anycast RP**
Anycast-RP (RFC 4610) innebär att man assignar en grupp routrar till en
RP-adress som finns konfad på flera routrar. PIM messages skickas till
den router som routingtabellen tycker är närmast. Detta ger lastdelning
och redundans. Denna feature finns inte på IOS.

`interface loopback10`
` description Anycast-RP-Address`
` ip address 172.16.1.10/32`
` ip pim sparse-mode`

`ip pim rp-address 172.16.1.10`
`ip pim anycast-rp 172.16.1.10 192.168.10.1`
`ip pim anycast-rp 172.16.1.10 192.168.10.2`

**Verify**

`show running-configuration pim`
`show ip mroute`
`show ip pim interface`
`show ip pim group-range`
`show ip route rpf`
`show ip static-route multicast`

Maintenance mode
Man kan isolera routern (ur ett PIM-perspektiv) genom att skicka ut PIM
Hello message med holdtime 0 (goodbye) till alla grannar, då rivs alla
PIM-grannskap direkt.

`ip pim isolate`

IOS-XR
======

IOS-XR har SSM group range 232.0.0.0/8 by default.

**Konfiguration**

`multicast-routing`
` address-family ipv4`
`  interface HundredGigE0/0/0/0`
`   enable`
`  !`
` !`
`!`
`router pim`
` address-family ipv4`
`  rp-address 10.0.0.10`
`  log neighbor changes`

Verify

`show pim group-map `
`show mfib route`
`show pim rpf 192.168.0.10`
`show pim rpf hash`

[Category:Cisco](/Category:Cisco "wikilink")