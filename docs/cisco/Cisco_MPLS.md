---
title: Cisco MPLS
permalink: /Cisco_MPLS/
---

Multiprotocol Label Switching (RFC 3031) är protokoll som routrar kan
använda för att forwardera paket baserat på labels istället för
destination IP address. Routrarna kallas då LSR, Label Switch Router.
Genom att separera forwarding decision från destination IP address kan
besluten baseras på andra faktorer såsom [QoS](/Cisco_QoS "wikilink")
eller Traffic Engineering. Det kan användas för vanlig unicast IP
forwarding men också annat som t.ex. VPN-tjänster. En grupp av paket som
skall till ett visst destinationsnät kommer vanligtvis att skickas samma
väg genom nätverket. I MPLS grupperas dessa paket i klasser som kallas
Forwarding Equivalence Class, FEC. Alla paket som tillhör samma FEC
skickas med samma label. En MPLS-header är 4 bytes och innehåller bl.a.
ett 20-bitars fält som är den unika labeln. Bottom-of-stack bit, QoS
marking och TTL finns också i headern. Olika protokoll kan användas för
control plane, t.ex. LDP,
[MP-BGP](/Cisco_BGP#Multiprotocol_BGP "wikilink") eller [Segment
Routing](/Cisco_SR "wikilink"). MPLS på Cisco-enheter använder sig av
[CEF](/Cisco_CEF "wikilink"). MPLS går även att tunnla över IP (RFC
4023), se [Cisco GRE](/Cisco_GRE "wikilink").

Se även [MPLS-TE](/Cisco_MPLS-TE "wikilink").

Tables
------

För varje [VRF](/Cisco_Routing#VRF "wikilink") skapas det nya tabeller,
**show cef table \| begin active**

RIB

`show ip route`
`show ip route vrf NAME`

LIB, innehåller all labels known to LSR

`show mpls ldp bindings`
`show mpls ldp binding summary`
`show mpls ldp bindings vrf NAME`

FIB, används för paket utan label

`show ip cef`
`show ip cef vrf NAME`

LFIB, används för paket med label

`show mpls forwarding-table`
`show mpls forwarding-table vrf NAME`

LDP
===

För att veta vilka labels en LSR ska sätta på paketen som ska skickas
iväg används Label Distribution Protocol (TDP är legacy). Routrar bygger
LDP-grannskap och utbyter sedan dynamiskt labels med varandra för att
kunna bygga korrekta forwarding tables. Det fungerar ungefär som ett
routingprotokoll. För unicast IP routing så utbyts en label per prefix i
routingtabellen, Cisco IOS använder independent label distribution
control. Dyker det upp något nytt i routingtabellen skapas en ny lokal
label i LIB och sedan annonseras det till alla LDP-grannarna. På så sätt
kan en label-switched path (LSP) byggas. Dessa är enkelriktade och en
enskild LSR känner inte till hela pathen för det behövs inte. En label
går aldrig längre än till grannen utan där poppas eller byts den mot
nästa routers label. MPLS låter routingtabellen och IGP stå för path
selection och därmed loop-prevention och convergence.

LDP använder sig utav två sorts paket för att kommunicera. För neighbor
discovery skickas Hello-paket till 224.0.0.2 UDP 646 var 5:e sekund. När
grannskap är bildat görs all informationsöverföring (updates) med
unicast som skickas på TCP 646.

<div class="mw-collapsible mw-collapsed" style="width:240px">

**LDP Hello:**

<div class="mw-collapsible-content">

[<File:Cisco_MPLS_LDP_Hello.PNG>](/File:Cisco_MPLS_LDP_Hello.PNG "wikilink")

</div>
</div>

MPLS-nätet måste använda något routingprotokoll för att lära sig routes
och dra nytta av label-annonsering, vanligtvis används ett IGP för
detta. När en ny lokal label skapas, pga nylärd route från IGP,
annonseras det till alla LDP-grannarna (även den man fick
route-uppdateringen ifrån, frame-mode MPLS har inte hört talas om split
horizon :). Detta händer för alla routes på alla LSR. Router-ID väljs på
exakt samma sätt som för [OSPF](/Cisco_OSPF#Konfiguration "wikilink").
Om man har en LSR med LDP-grannskap till säg 5 andra enheter så kommer
alla grannskap gå ner om man stänger ett av sina 5 interface eftersom
LDP skapar sitt ID utifrån tillgängliga IGP interface. Det ändras om ett
interface försvinner vilket det gör om man t.ex. shutar ett av dem. Hold
time ska kommas överens om och är default 15 sekunder (3x Hello). Om två
LSR inte kommer överens om timers, label distribution method etc kan man
öka intevallet mellan försöken med *mpls ldp backoff*-kommandot. T.ex.
från 5 sekunder till att börja med till 120 sekunder mellan varje
försök.

Global

`mpls label protocol ldp  #Default`
`mpls ldp router-id loopback0 [force]`
`show mpls ldp parameters `

Man kan per interface slå på MPLS, höja MTU för att stödja MPLS-headers
och ändra vilken adress som ldp ska bygga grannskap med. Om man har
flera länkar till samma LSR och ska sätta upp flera parallella
LDP-sessioner måste man använda samma transport address på alla
interface. LDP RID används default som transport address.

`interface gi1/1`
` mpls ip`
` mpls mtu 1508`
` mpls ldp discovery transport-address interface`

**Verify**

`show mpls interfaces [vrf NAME]`
`show mpls ldp neighbor`
`show mpls ldp discovery`

Graceful restart

`mpls ldp graceful-restart`
`show mpls ldp graceful-restart`

Allow MPLS forwarding for ip default route

`mpls ip default-route `

### Labels

Special-Purpose Label Values

-   0 – IPv4 Explicit null – Instead of popping label at PHP, the second
    last router sets top label to zero, this means EXP bits are
    preserved.
-   1 – Router alert – Alerts LSR that packet needs a closer look. Can’t
    be forwarded in hardware, software needed.
-   2 – IPv6 Explicit null
-   3 – Implicit null – Pop label

Label range, default på IOS är 16-1048575 (label range kan skilja
beroende på modell). Att byta label range tar effekt när MPLS startas
om, det görs snabbast med de globala kommadona *no mpls ip* -\> *mpls
ip*.

`mpls label range 200-299`
`show mpls label range`

**Advertisments**
Default på Cisco IOS allokeras och annonseras labels för allt, detta går
att ändra.

`no mpls ldp advertise-label`
`mpls ldp advertise-lable for `<dest prefix>` to `<ldp peer>

För att slippa hålla koll på prefix-listor kan man konfigurera att det
endast ska allokeras (och därmed annonseras) labels för /32-routes i
RIB:en.

`mpls ldp label`
` allocate global host-routes`

Label space

`show mpls ldp discovery`
`10.0.0.10:`**`0`**
`0 betyder platform wide label space`
`1 betyder interface label space`

Disable PHP

`mpls ldp explicit-null`

### TTL

När en ingress E-LSR får in ett IP-paket sänker den IP TTL med ett och
sedan pushar den en label och kopierar TTLen till MPLS-headern. När
sedan paketet traverserar en LSR sänks endast MPLS-TTLen men vid egress
E-LSR kopieras MPLS-TTLen till IP TTL och skickas vidare. Detta går att
ändra på så att IP-TTL inte kopieras utan MPLS-TTL sätts till 255 av
ingress E-LSR för att hela MPLS-nätet verkligen ska vara som ett router
hop. Detta behöver endast konfigureras på PE.

`no mpls ip propagate-ttl`

### Session Protection

Om två directly connected LDP-grannar tappar kontakten flushas alla
bindings från LIB. Men det behöver inte betyda att det inte fortfarande
finns IP-reachability mellan dem en annan väg. Session Protection är en
optimerings-feature som gör att LIB inte flushas sålänge det finns en
annan väg till LDP-peer, targeted LDP sätts då upp för att hålla LIB
synkat. Dvs om det slutar att komma in multicast hellos så skickas det
unicast UDP-paket till grannes LDP transport address för att förhindra
timeout. När sedan directly connected grannskapet kommer tillbaka
behöver inte allt synkas om. Detta är en global inställning och måste
konfigureras på båda sidor annars kommer inte andra sidan acceptera
targeted hellos. Max hops är 255 och för Hello och Hold time gäller 10
sekunder respektive 90 sekunder default.

`mpls ldp session protection`
`mpls ldp discovery targeted-hello accept`
`mpls ldp discovery targeted-hello holdtime 30`

`show mpls ldp neighbor detail | i Targeted|Session `

Både session protection och accept unicast hellos kan begränsas med ACL.
Med show mpls ldp neighbor kommandot ser man att det finns en lista på
Addresses bound to peer LDP Identity, det är så de fattar vilka andra
IP-adresser som kan användas för LDP-kommunikation. LDP session holdtime
rekommenderas enligt följande formel: Session Holdtime \<= (Hello
holdtime - Hello interval) \* 3

### Security

Med tcp-autentisering kan man säkra LDP-kommunikationen. ACL ska träffa
LDP ID som andra sidan har och måste vara standard.

`ip access-list standard LDP-PEERS`
` permit host 10.0.0.5`
` permit host 10.0.0.6`
`mpls ldp password required for LDP-PEERS`
`mpls ldp neighbor 10.0.0.5 password SECRET`

Kräv lösenord för alla LDP-grannskap. Om man inte har angett något
lösenord för en specifik granne kommer fallback att användas om det
finns konfigurerat.

`mpls ldp password required`
`mpls ldp password fallback SECRET`

Verify

`show mpls ldp discovery detail | i Ethernet|Password`

### IGP

LDP går att autokonfa tillsammans med [IS-IS](/Cisco_IS-IS "wikilink")
och [OSPF](/Cisco_OSPF "wikilink"), dvs slå på LDP på de interface som
är aktiva i IGPn, detta kan antingen göras per interface eller under
routingprocessen. Man kan även använda *prefix suppression* så kommer
det inte att genereras lika många labels för ens core-nätverk.

`router ospf/isis 1`
` mpls ldp autoconfig`

**Synchronization**
Länkkostnaden för nyetablerade grannskap sätts till max tills LDP är
klar med labelutbyte och berättar för link-state IGP att det är okej att
använda länken.

LDP deklarerar LDP sync up så fort alla dessa nödvändiga villkor är
uppfyllda.

-   LDP session är up
-   LDP har skickat alla sina label bindings till åtminstone en peer
-   LDP har tagit emot åtminstone en label binding ifrån en peer

Slå på det under IGP-processen.

`router ospf/isis 1`
` mpls ldp sync`

Alternativt per interface.

`interface gi2`
` mpls ldp igp sync`

På IOS-XE är det rekommenderat att sätta IGP sync holddown timer till
något non-infinite för att undvika device isolation som kan uppstå vid
vissa felscenarion.

`mpls ldp igp sync holddown 120000`

Verify

`show mpls ldp igp sync`
`show mpls interface detail | i Interface|IGP`

VPN
===

MPLS VPN (RFC 4364) är en populär MPLS-applikation och det räknas som
trusted VPN. PHP för transport label används default för att slippa en
lookup. För PE-PE label utbyten används
[MP-BGP](/Cisco_BGP#Multiprotocol_BGP "wikilink"), det kan dock gå via
route reflector precis som vanligt för ökad skalbarhet. För att
VPN-trafik ska fungera måste PE ha en route till next-hop PE, det går ej
med en default route. Control plane kommer att fungera men ej data plane
eftersom forwardering med labels lärda från BGP endast fungerar om det
finns en /32-route i RIB. För L2 VPN se [Cisco
VPLS](/Cisco_VPLS "wikilink") och för multicast se [Cisco
MLDP](/Cisco_MLDP "wikilink"). Det går även att integrera
[NAT](/Cisco_NAT#MPLS_VPN "wikilink") med MPLS VPN.

`ip bgp-community new-format`
`show ip bgp community ?  #`*`Så`` ``står`` ``det`` ``antingen`` ``aa:nn`` ``eller`` ``1-4294967295`*

**Route Distinguisher:** är ett 64-bitars nummer som skickas med
BGP-uppdateringarna och används för att göra routes unika mellan VRFer.
Det används med adressfamiljerna vpnv4 och vpnv6.

**Route Target:** skickas med BGP-uppdateringarna som ett Extended
Community PA. Det används för att bestämma vilken/vilka VRFer routsen
ska in i.

Import och export bestämmer vad som ska redistribueras mellan VRF och
BGP.

Add IBGP neighbor. Man konfar inte next-hop-self eftersom VPNv4 sätter
det default.

`router bgp 100`
` neighbor 10.0.0.10 remote-as 100`
` address-family vpnv4 unicast`
`  send-community extended`

Default är att droppa VPNv4 updates för RTs som det inte finns någon
lokal vrf för. Detta kan man ändra på.

`router bgp 100`
` no bgp default route-target filter`

Man kan dölja MPLS-nätet endast för VPN-kunder.

`no mpls ip propagate-ttl forwarded `

Label Mode avgör hur det ska allokeras labels. Har man VPN-kunder med
många routes kan man av effektivitetsskäl byta till per-vrf mode och då
kommer varje kund få en label per PE oavsett hur stor routingtabellen är
i den VRF:en och därmed sparas det minne. Däremot måste en routing
lookup göras när paketet kommer fram eftersom alla paket har samma label
oavsett var de ska. Det finns därför en mellanvariant som kallas per-ce
där det allokeras en label per next-hop per vrf och man sparar minne
samtidigt som man slipper routing lookup.

`mpls label mode all-vrfs protocol all-afs per-prefix  #Default`
`mpls label mode all-vrfs protocol bgp-vpnv6 per-vrf`
`mpls label mode vrf INTERNET protocol bgp-vpnv4 per-ce`

Man kan partitionera upp nätverket genom att skapa RR-grupper som
filtrerar på route-targets.

`address-family vpnv4`
` bgp rr-group EXTCOM-LIST`

### 6VPE

6VPE (RFC 4659) är en teknik för att köra IPv6 över IPv4 MPLS-nät.
Adressfamilj VPNv6 måste aktiveras på IPv4 iBGP-grannskapen mellan
PEs/RRs. VPNv6 prefixen har en IPv4-mappad IPv6-adress som next-hop
genom MPLS-nätet och en IPv4 LSP finns mellan PEs. Next-hop-adressen
måste finns i IPv4-routingtabellen och en LSP måste existera för
destinationen.

`router bgp 100`
` address-family vpnv6`
`  neighbor 10.0.0.10 activate`
`  neighbor 10.0.0.10 send-community extended`

Inter-AS MPLS VPN
-----------------

**Back to Back VRFs** *Option 10A*
PE använder iBGP för att distribuera labeled VPN-routes inom sitt AS som
vanligt. PE kommunicerar med andra sidan PE med ett sub-interface,
länknät och eBGP-grannskap per VRF. Det krävs ingen MPLS mellan PE utan
det är unlabeled IP-adresser som annonseras. Detta är dock inte den mest
skalbara lösningen.

**VPNv4 eBGP** *Option 10B*
PE använder iBGP för att distribuera labeled VPN-routes inom sitt AS som
vanligt. PE använder sedan eBGP för att distribuera labeled VPN-routes
till PE i ett annat AS, som i sin tur distribuerar dem till PE routrar i
sitt AS. Det kan finnas flera vägar mellan de olika AS för redundans och
ökad kapacitet. Service Providers måste komma överens om detta. Detta är
mer skalbart eftersom det räcker med ett BGP-grannskap per koppling
mellan AS. Följande fetmarkerade kommando slår på att /32-routes för
eBGP-grannar autoläggs in i RIB och därmed möjliggör label forwarding,
så fungerar ej IOS XR utan där måste man lägga till statiska routes
manuellt.

`interface GigabitEthernet1/0`
` description Connection to other AS`
` `**`mpls`` ``bgp`` ``forwarding`**

`router bgp 100`
` no bgp default route-target filter`
` neighbor 2.2.2.2 remote-as 200`
` neighbor 10.0.0.10 description iBGP`
` address-family vpnv4`
`  neighbor 2.2.2.2 activate`
`  neighbor 10.0.0.10 activate`
`  neighbor 10.0.0.10 next-hop-self`

`show bgp vpnv4 unicast all labels`

**VPNv4 between RRs** *Option 10C*
(eller PEs using multihop eBGP)

Istället för att använda PEs för att hålla koll och distribuera
VPN-routes bygger man grannskap mellan RRs i varje AS. Dock måste PE
hålla koll på labeled routes till alla andra PE/RR i sitt AS och skicka
med eBGP till andra sidan AS så deras PE/RR hittar till PE/RR i det egna
AS. Då kan PE/RR i olika AS bygga eBGP multi-hop grannskap (det måste
finnas LSP mellan dessa) och utbyta labeled VPN-routes. Om P routrar får
känna till PE i andra AS fungerar det som vanligt med dubbla labels. Men
om det däremot inte är uppsatt så måste det trippel labelas. En för
kundens IP till egress PE, en satt av ASBR för egress PE och en för IGP
next-hop. Använder man RR är detta ett väldigt skalbart alternativ.

`router bgp 100`
` neighbor 10.0.0.10 description eBGP`
` address-family vpnv4`
`  neighbor 10.0.0.10 next-hop-unchanged`

**Option AB**
Control plane: BGP VPNv4
Data plane: subinterfaces / back-to-back VRF
Notera att option AB ej är supporterat på IOS-XR.

`vrf definition VRF1`
` address-family ipv4`
`  inter-as-hybrid next-hop 10.0.0.2`
`!`
`router bgp 100`
` no bgp default route-target filter`
` neighbor 2.2.2.2 remote-as 200`
` address-family vpnv4`
`  neighbor 2.2.2.2 activate`
`  neighbor 2.2.2.2 inter-as-hybrid`

BGP-LU
------

BGP Labeled Unicast (RFC 3107) tillhandahåller MPLS-transport mellan
IGP-domäner. Genom att annonsera loopbacks och label bindings går det
att kommunicera med routrar över IGP-gränser. BGP-LU annonseras mellan
edge routrar och transport-routrarna i mitten märker inget. De
vanligaste use casen för BGP-LU är Inter-AS MPLS VPN Option C,
Seamless/Unified MPLS, CSC VPN och IGP free data center.

`router bgp 100`
` address-family ipv4`
`  neighbor 10.0.0.10 send-community both`
`  neighbor 10.0.0.10 next-hop-self`
`  neighbor 10.0.0.10 send-label `

Show

`show bgp ipv4 unicast labels`

Notera att man på IOS måste ha med **set mpls-label** i sina route-map
entries om ska använda route-maps för policy med BGP-LU.

ICMP
====

MPLS Echo skickas unicast till LDP-grannen med L3 destination address
127.0.0.1 på UDP 3503.

<div class="mw-collapsible mw-collapsed" style="width:240px">

**Echo Request:**

<div class="mw-collapsible-content">

[<File:Cisco_MPLS_Echo_Request.png>](/File:Cisco_MPLS_Echo_Request.png "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:240px">

**Echo Reply:**

<div class="mw-collapsible-content">

[<File:Cisco_MPLS_Echo_Reply.png>](/File:Cisco_MPLS_Echo_Reply.png "wikilink")

</div>
</div>

Man kan med MPLS-ping testa konnektivitet till en FEC, så detta funkar
endast ifrån en LSR samt inga VPN-prefix fungerar heller utan endast det
man lärt sig med LDP.

`ping mpls ipv4 10.1.1.1/32 `

Med MPLS-traceroute kan man få ut mer information jämfört med vanlig
traceroute eftersom det skickas mer data i payloaden.

`traceroute mpls ipv4 10.1.1.1/32`

6PE
===

IPv6 Provider Edge (RFC 4798) är en teknik för att köra IPv6 över ett
IPv4+MPLS-nät. IPv6 prefix med tillhörande label utbyts genom att skicka
det med IPv4 iBGP mellan PEs (eller via route reflector). Alla
IPv6-prefix finns i den globala routingtabellen till skillnad från 6VPE.
IPv6 prefixen har en IPv4-mappad IPv6-adress som next-hop inom
MPLS-nätet och IPv4 LSP:er används mellan 6PEs. Detta gör att man inte
behöver konfigurera next-hop-self. Däremot om IPv4-adressen inte finns i
routingtabellen eller om det inte finns någon LSP kommer IPv6-prefixet
att stå som inaccessible.

`router bgp 100`
` address-family ipv6`
`  neighbor 10.0.0.10 activate`
`  neighbor 10.0.0.10 send-label`

`show bgp ipv6 unicast labels`

IOS-XR
======

`mpls ldp`
` log`
`  hello-adjacency`
`  neighbor`
`  graceful-restart`
`  session-protection`
` !`
` graceful-restart`
` discovery`
`  targeted-hello holdtime 30`
`  targeted-hello interval 10`
` !`
` router-id 10.10.0.101`
` neighbor`
`  password encrypted 10422A2A0D33371D030A796571`
` !`
` session protection`
` address-family ipv4`
`  discovery targeted-hello accept`
`  label`
`   local`
`    allocate for host-routes`
`    advertise`
`     explicit-null`

`router isis 1`
` address-family ipv4 unicast`
`  mpls ldp auto-config`

Verify

`show mpls interfaces`
`show isis mpls ldp`

**Unified MPLS**
ABR/RR, för att next-hop-self ska funka.

`router bgp 100`
` ibgp policy out enforce-modifications`

RR (som måste finnas i data path) kan stå för att stoppa in alla
PE-prefix (/32) i bgp-tabellen.

NX-OS
=====

Förutsättningar

`install feature-set mpls`
`feature-set mpls`
`feature mpls l3vpn`
`feature mpls ldp`

`interface loopback 1`
` ip address 10.0.0.1/24`

`mpls ldp configuration`
` session protection`
` router-id loopback 1`

Aktivera på interface

`interface e1/1`
` mpls ip`

Synk med routing protokoll

`router isis P1`
` mpls ldp sync`

Authentication

`ip prefix-list `<namn>` permit `<granne1>`/32`
`mpls ldp configuration`
` password required for `<prefix-list>
` password option 1 for `<prefix-list>` key-chain `<key-chain-name>

[Category:Cisco](/Category:Cisco "wikilink")