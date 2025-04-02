---
title: Cisco MPLS-TE
permalink: /Cisco_MPLS-TE/
---

Det finns olika tekniker för att göra TE i ett MPLS-nät. Det mest
flexibla och skalbara är Segment Routing, se [egen
artikel](/Cisco_SR "wikilink").

RSVP
----

Resource Reservation Protocol (RFC 2205) är ett kontrollplansprotokoll
(IP protokoll \#46) designat för att reservera resurser genom ett
nätverk. Hostar/routrar kan begära att få vissa QoS-nivåer av nätverket.
RSVP reserverar resurser men det är upp till varje enhet att ha en
QoS-teknik för att leverera bandbredden. Till skillnad från vanlig QoS
som är per frame/paket är detta per flöde, se även [Cisco
QoS](/Cisco_QoS "wikilink").

Resource Reservation Protocol - Traffic Engineering (RFC 3209) är en
extension till [RSVP](/Cisco_RSVP "wikilink") som används för Traffic
Engineering i MPLS-nät. Det fungerar både som MPLS label distribution
protocol och MPLS signaling protocol. En ingress LSR kan använda RSVP-TE
för att notifiera alla LSR:er längs pathen till egress att den vill
sätta upp en LSP. Bandbredd kan då allokeras genom hela MPLS-nätverket.
RSVP är unidirectional och det sätts upp en LSP per riktning. Det
fungerar både med IPv4 och IPv6. Default kommer MPLS-TE tunnlar att
föredra TE metric value över IGP metric för deras dynamiska path
selection. Dock är TE metrics tagna ifrån IGP metric default.

Paket

-   Path messages: används av ingress LSR för att begära LSP setup
    hop-by-hop längs hela pathen.
-   Resv messages: används av egress LSR för att svara på Path message
    från ingress.

För att hålla LSP aktuell skickas periodvis PATH refresh och RESV
refresh meddelanden. Om det inte finns tillräckliga resurser att tillgå
någonstans längs vägen kommer den LSR:en att besvara ingress LSR som då
får hitta en annan väg eller misslyckas med LSP-uppsättningen.

### Konfiguration

RSVP konfigureras på alla enheter genom nätverket och enableas på alla
interface flödena ska traversera. Det behöver inte köras på alla enheter
för att det ska funka men då kan man inte reservera bandbredd på dem
heller.

`interface Gi2`
` ip rsvp bandwidth 1000 100  #kbps`

Om man inte specificerar total bandbredd och per-flow bandbredd kommer
75% av interfacets bandbredd kunna reserveras av ett enskilt flöde.

Verify

`show ip rsvp`
`show ip rsvp interface`
`show ip rsvp reservation`

Om man kör LLQ/CBWFQ bör man stänga av RSVPs WFQ och klassificering.

`ip rsvp resource-provider none`
`ip rsvp data-packet classification none`

Traffic Engineering
-------------------

MPLS TE är unidirectional tunnels från source (head-end) till
destination (tail-end) i form av LSP:er som används för att forwardera
trafik. RSVP-TE Explicit Route Object (ERO) är pathen för MPLS LSP som
inkluderar en sekvenserad lista av LSR:er som LSP:n måste passera igenom
mellan ingress och egress LSR. RSVP-TE använder pathen som beskrivs i
ERO för att signalera och sätta upp LSP:n. Pathen kan vara admin
specified eller automatiskt uträknad på headend utifrån en algoritm som
constrained shortest path first (CSPF). Det finns strict path och loose
path. Ingen LDP behövs.

Traffic Parameter Attributes:
TE metric, Maximum bandwidth, Maximum reservable bandwidth, Unreserved
bandwidth, Administrative group.

En sak som är bra att känna till med RSVP-TE är att om den primära vägen
går ner (oavsett om det finns FRR eller inte) så kommer inte trafiken
att skifta tillbaka till den ursprungliga vägen direkt efter att felet
är åtgärdat. Det krävs att head-end signalerar berörd LSP igen (kollar
om det finns en mer optimal väg). På både IOS och IOS XR sker detta
periodiskt varje timme som standard. Det går även att signalera om en
LSP manuellt. Om det finns en bättre väg kommer trafiken att skiftas
över till den med MBB (make before break).

**Konfiguration**

`mpls traffic-eng tunnels`

Per interface, detta måste konfas på alla core-interface.

`interface gi2`
` mpls traffic-eng tunnels`
` ip rsvp bandwidth`

IGP, OSPF använder opaque LSA:er och IS-IS använder nya TLV:er för att
skicka TE attribut.

`router ospf 1`
` mpls traffic-eng router-id Loopback0`
` mpls traffic-eng area 0`

`router isis 1`
` mpls traffic-eng router-id Loopback0`
` mpls traffic-eng level-2`

Tunnel. För att tunneln ska användas måste man routa över den, detta kan
t.ex. göras med statisk routing eller autoroute. Eftersom det inte är en
vanlig GRE-tunnel uppstår ingen recursive routing. Record route används
för loop detection.

`interface Tunnel0`
` ip unnumbered Loopback0`
` tunnel mode mpls traffic-eng`
` tunnel destination x.x.x.x`
` tunnel mpls traffic-eng path-option 1 dynamic`
` tunnel mpls traffic-eng autoroute destination`
` tunnel mpls traffic-eng record-route`

Verify

`show mpls traffic-eng tunnel`
`show ip rsvp interface`
`show ip route`
`show ip rsvp reservation detail`

`traceroute mpls traffic-eng tunnel 0`

Dry run

`show mpls traffic-eng topology path destination 10.10.10.10 bandwidth 50000 `
`show mpls traffic-eng link-management admission-control `

Logging, detta är för att skicka traps.

`mpls traffic-eng logging lsp`
`mpls traffic-eng logging tunnel`

**Auto-Bandwidth**
Med auto-bw mäter routern själv trafikmängden på tunneln periodiskt.
Sedan kan olika bw-reservationer signaleras allt eftersom utifrån
tunnels behov. Med statistics interval kan man t.ex. mäta LSP:n i 60
sekunder och sedan fatta ett beslut. Man bör känna till att auto-bw inte
funkar klockrent med burstig trafik eftersom det inte alltid är så
snabbt i förändring. Underflow och Overflow är tröskelvärden för
event-baserad statistikinsamling. Detta är inte heller alltid
supersnabbt vid förändring. Det är rekommenderat att köra: tunnel
load-interval \< global sampling frequency \< tunnel adjust frequency.

`int tun0`
` tunnel mpls traffic-eng auto-bw`

Notera att senaste requested/signaled bandwidth sparas i running config.

**TE - inter-area/multi-level**
IOS implementerar Inter-Area MPLS TE genom att definiera ett Explicit
Route Object (ERO), dvs en explicit-path som innehåller adresser till
ABR eller L1/L2-router som ett loose hop i path:en. Detta resulterar i
en pseudo-dynamic path calculation där Head End dynamiskt kalkylerar
cSPF till sin exit ABR. Den kommer sedan dynamiskt kalkylera exit path
till nästa ABR och så vidare tills man har nått tail end. Detta uppnås
genom en loose hop expanderas i den fullt definierade explicita path:en,
dvs Head End och ABRs definierar de hop som finns i den egna lokala
flooding domain.

`ip explicit-path name INTER_AREA_TE enable`
` next-address loose `<ABR1>
` next-address loose `<ABR2>

### Autotunnel - Fast Reroute

RSVP-TE kan använda sig av backup LSPer för snabbare konvergens. Med
hjälp av autotunnel backup kan dessa autoskapas efter behov och man
behöver därmed inte assigna något till protected interfaces. Dynamiska
backup NHOP/NNHOP tunnels skapas när en LSP requestar FRR protection,
dvs tunnel signaleras när det finns något aktivt flöde som ska skyddas
och det finns alternativa vägar. FRR föredrar NNHOP över NHOP backup
tunnels om båda finns tillgängliga. För NNHOP FRR måste man ha record
route.

PLR

`mpls traffic-eng auto-tunnel backup`

Head-end

`interface Tunnel0`
` tunnel mpls traffic-eng fast-reroute`

**SRLG**
SRLG-information distribueras med IGP och funkar endast för backup
tunnels som är skapade av Autotunnel backup.

`interface Gi0/1`
` mpls traffic-eng srlg 1`
` mpls traffic-eng srlg 2`
`!`
`interface Gi0/2`
` mpls traffic-eng srlg 2`
` mpls traffic-eng srlg 3`
`!`
`mpls traffic-eng auto-tunnel backup`
`mpls traffic-eng auto-tunnel backup srlg exclude force `

### Autotunnel - Mesh

Autoskapa tunnlar till alla PE:s som finns med i en acl.

`mpls traffic-eng auto-tunnel mesh`

`interface Auto-Template1`
` ip unnumbered Loopback0`
` tunnel mode mpls traffic-eng`
` tunnel destination access-list 1`

`access-list 1 permit 1.1.1.1`
`access-list 1 permit 1.1.1.2`

Primary, configure tunnels to directly connected neighbors.

`mpls traffic-eng auto-tunnel primary onehop`

### Inter-AS TE

Med ASBR Forced Link Flooding kan man låta länkar som inte är med i IGP
att installeras i TE database som point-to-point. Man konfigurerar
länken som passiv för MPLS TE och anger neighbor TE-ID och ip-adress.

`mpls traffic-eng passive-interface nbr-te-id 1.1.1.2 nbr-if-addr 10.0.0.2 nbr-igp-id isis 49.0000.0000.0002.00`

### Multicast

Om man routar multicast i sitt core samtidigt som man kör MPLE-TE med
autoroute announce kommer RPF att titta på fel best path. Workaround är
att slå på att IGP håller två set med best paths under SPF calculation,
en för unicast (TE tunnels och physical interfaces) och en för multicast
(endast physical interfaces).

`router ospf 1`
` mpls traffic-eng multicast-intact`

IOS-XR
======

### Auto-Tunnel Backup

`ipv4 unnumbered mpls traffic-eng lo0`
`mpls traffic-eng`
` auto-tunnel backup`
`  tunnel-id min 6000 max 6500`
` !`
` interface GigabitEthernet0/0/0/0`
`  auto-tunnel backup`

Verify

`show mpls traffic-eng auto-tunnel backup summary`

### Mesh

`ipv4 unnumbered mpls traffic-eng Loopback0`
`ipv4 prefix-list PE`
` 10 permit 10.0.0.1/32`
` 20 permit 10.0.0.2/32`
`!`
`mpls traffic-eng`
` auto-tunnel mesh`
`  group 1`
`   attribute-set PE`
`   destination-list PE`
`  !`
`  tunnel-id min 1000 max 1499`
` !`
` attribute-set auto-mesh PE`
`  logging events lsp-status state`
`  signalled-bandwidth 100 class-type 0`
`  autoroute announce`
`  fast-reroute`
`  record-route`

[Category:Cisco](/Category:Cisco "wikilink")