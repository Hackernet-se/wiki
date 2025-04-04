---
title: Cisco RIP
permalink: /Cisco_RIP/
---

Routing Information Protocol är ett distance vector routing protocol som
använder hop count som metric, det är designat för små nätverk. I denna
artikel används RIP synonymt med RIPv2 (RFC 2453), RIPv1 skickar inte
med subnet mask i uppdateringarna och har därmed inte stöd för VLSM så
det är väldigt legacy. Varje router kan annonsera sina directly
connected networks plus det som de lär sig från andra RIP-routrar. Som
med övriga distance vector routing protocols på IOS annonseras endast
nätverk som hamnar i routingtabellen vidare, dvs annonsera endast det
som routern själv använder. Man skickar kända nätverk med deras metric
med multicast så alla som lyssnar på 224.0.0.9 får uppdateringar. Med
tanke på att man inte känner till hela topologin utan endast nätverk och
riktning är det större risk för loopar än med t.ex. link-state routing
protokoll. En stor nackdel med RIP är konvergenstiden.

**Type:** Distance Vector

**Algorithm:** Bellman-Ford

**AD:** 120

**Protocols:** IP

**Packets:** 2

Packets
-------

RIP-routrar byter information med varandra genom att skicka
uppdateringar på alla RIP-enableade interface baserat på update timer
(30 sec default). Man skickar all information man har varje gång, max 25
route entries får plats per enskilt paket. Det skickas inga Hellos och
inga grannskap upprättas utan uppdateringar skickas till
01:00:5E:00:00:09 224.0.0.9 UDP port 520 var 30 sekund. RIP har två
meddelandetyper, Requests och Responses. Requests används för att be en
granne skicka en partial eller full update direkt utan att vänta på
Update timer. Skickar en router en request som innehåller en rad med
address family ID 0 och metric 16 vill den ha en full update. Annars ska
grannen svara med uppdateringar för de nät som står speccade i
Requesten, dvs partial update, dock är inte partial requests
implementerat på IOS. Full update frågas efter när en Ciscorouter bootar
upp, ett RIP-interface kommer upp eller *clear ip route \** körs.
[CSR](/Cisco_CSR "wikilink"):er verkar inte använda sig av Requests
överhuvudtaget.

<div class="mw-collapsible mw-collapsed" style="width:310px">

Response packet:

<div class="mw-collapsible-content">

[<File:Cisco_RIP_Update.PNG>](/File:Cisco_RIP_Update.PNG "wikilink")

</div>
</div>

### Metric

För metric används hop count och upp till 15 är användbart, 16 anses som
infinity. Som med alla distance vector protokoll används den route med
lägst metric, dvs bästa vägen, och övriga vägar påverkar inte
routingtabellen. Enda undantaget till denna regel är om next-hop skickar
en högre metric än tidigare då accepteras den direkt, t.ex. vid route
poisoning. Enda sättet att få påverkningsmöjlighet är att annonsera
lägst metric. Om en route failar kan man skicka ut en triggered update
om denna routen med en metric satt till infinity då propagerar
uppdateringen till alla routrar och de slutar använda den failade
routen, detta kallas route poisoning. Däremot sparas routen i den
interna RIP-databasen men markeras som possibly down. En skillnad med
RIP kontra [EIGRP](/Cisco_EIGRP "wikilink") och RIPng är att metric
läggs på när en route skickas iväg istället för när den kommer in. Finns
det flera väger till en destination med samma metric installeras det
default upp till 4 routes i routingtabellen. Detta går att ändra med
**maximum-paths**-kommandot, max är 16.

### Split Horizon

För att förhindra loopar används flera tekniker. Split Horizon, istället
för att skicka exakt alla routes till en granne X tas routes med
next-hop granne X bort från uppdateringen. Detta är påslaget default på
alla interface förutom fysiska Frame Relay och ATM. En ännu kraftfullare
variant är att lägga till Poison Reverse, då skickas uppdateringarna med
next-hop granne X till granne X men med en metric satt till infinity.
Detta har inte Cisco RIPv2 stöd för.

Om två routrar känner till samma nät kommer den som annonserade ut det
först att vara den som gäller för övriga routrar oavsett hop count
eftersom split horizon gör att routes man får in på ett interface aldrig
annonseras ut på det interfacet. Så även om den "sena" routern har en
bättre väg kan den inte berätta det för någon eftersom den har fått in
en uppdatering om routen på de interface där det finns RIP-routrar.
Secondary addresses kommer inte heller att annonseras om man inte
stänger av split horizon. Det går att stänga av split horizon men det är
inte rekommenderat. Det kan dock behövas stängas av på
[DMVPN](/Cisco_DMVPN "wikilink")-hubb.

`no ip split-horizon`

Om två routergrannar ser sig själva som next-hop för samma nätverk (kan
hända om Split Horizon är avstängt) kommer de att turas om att uppdatera
varandra med grannens metric plus 1 och den blir högre och högre för att
tillslut nå infinity och den ena slutar. Med RIP kan detta ta lång tid.
Detta kallas Counting to infinity och är en möjlig konsekvens av
distance vector protokoll.

**Source Validation**
RIP har en inbyggd kontrollmekanism som kollar på source-adressen på
uppdateringarna som kommer in. Detta går att ändra så att man kan godta
uppdateringar oavsett vilken IP de kommer ifrån. Följande RIP-kommando
stänger av sanity checks against source address of routing updates.
Unnumbered IP interfaces har inte denna check.

`no validate-update-source`

**Route tag**
Med RIPv2 kom stöd för route tags, det är ett 2 byte integer value som
man kan sätta på routes för att tagga dem. Route tagging stöds endast
vid redistribution och används om man vill skilja på internal och
external routes.

Konfiguration
=============

RIP-processen startar inte utan ett network-kommando.

`router rip`
` version 2`
` no auto-summary`
` distance 120`
` network 10.0.0.0`

Version per interface

`interface gi2`
` ip rip send version 1`
` ip rip receive version 1`

Ett passivt interface skickar inte ut några uppdateringar men däremot
tas fortfarande uppdateringar emot och behandlas.

` passive-interface default`
` no passive-interface gi2`

Verify

`show ip protocols`
`show ip rip database`

Clearing routing process

`clear ip route *`

Debug

`debug ip ripv2`
`debug ip ripv2 events`

**Unicast**
RIP bygger inga grannskap men man kan använda unicast. Det skickas då
dubbla uppdateringar, en till konfigurerad granne med unicast och en
till multicast/broadcast som vanligt. Neighbor-kommandot används på
vissa nätverkstyper, t.ex. multipoint Frame Relay subinterface.

`neighbor 10.0.0.10`

**Broadcast**
255.255.255.255

`interface gi2`
` ip rip v2-broadcast`

Subnet broadcast

`interface gi2`
` ip broadcast-address 10.0.0.255`

Authentication
--------------

En RIP-router vet om någon annan stödjer autentisering genom att kolla
på AFI-fältet i uppdateringen, 0xFFFF betyder authentication. Det finns
stöd för plain-text och MD5 och implementeras med hjälp av key-chain.
Ett högre nyckelvärde godtar lägre nyckelvärde om key-string är samma
men ej tvärtom. Använder man autentisering sänks antalet prefix som får
plats i ett RIP-meddelande från 25 till 24. Key chain måste skapas innan
det används för RIP authentication!

`key chain RIP-KEYS`
` key 1`
`  key-string HACKER`

`interface gi2`
` ip rip authentication mode md5`
` ip rip authentication key-chain RIP-KEYS`

Verifiera vilka interface som använder vilken key chain

`show ip protocols | b rip`

Convergence
-----------

Optimization & Scalability

Om det ska skickas fler routes än vad som får plats i ett Response
packet kommer det att skickas flera paket direkt efter varandra. Detta
kan överbelasta CPU på mindre routrar om det handlar om många paket. Man
kan konfigurera ett tidsintervall mellan paketen för att ta hänsyn för
detta.

`output-delay `<milliseconds>

Hur många obehandlade uppdateringar som tillåts.

`input-queue 150`

**Triggered Updates**
RIP går att göra till ett event-drivet protokoll (RFC 2091), då skickas
en full update en gång först för att sedan endast skicka partial updates
vid förändringar. RIP har stöd för triggered updates på serial
point-to-point interface, dvs om en förändring sker kan en partial
update skickas ut direkt. Eftersom RIP använder UDP går det inte att
lita på att exakt alla paket är rätt. Det konfigureras per interface och
shut/noshut för att aktivera.

`ip rip triggered`

Suppress triggered updates when next regular update due within 10
seconds

`flash-update-threshold 10`
`show ip protocols | i Flash`

**Timers**
Varje router har för varje route en tillhörande *invalid after* timer
(default 180 sekunder) som tickar varje sekund och resetas varje gång
den kommer in en uppdatering innehållandes routen. Kommer det inte in
någon uppdateringen med routen blir den invalid och *holddown timern*
startar. Då börjar routern skicka ut uppdateringar om att denna route
inte är nåbar (infinte metric) genom sig själv eftersom det har hänt
något med routen ur det egna perspektivet så övriga routrar får hitta en
annan väg. Samtidigt som den inte accepterar några uppdateringar
gällandes denna route tills holddown timear ut (default 180 sekunder).
Huvudsyftet med holddown är fördröja processandet av uppdateringar om
nätverk vars nåbarhet inte är säker eftersom de mottagna uppdateringarna
kanske inte innehåller up-to-date information.

Det finns också en *flushed after* timer som tickar och resetas på samma
sätt som invalid after. Om routern inte hör något på 240 sekunder
(default) tas routen bort från routingtabellen. Denna finns för att en
route inte ska vara oviss för evigt. Eftersom invalid after är 180
sekunder och flushed after är 240 får inte holddown köra klart utan det
bryts efter 60 sekunder. Det finns även en sleep timer som avgör hur
länge en inkommen flash update ska ligga innan routing-infon används,
denna timer är disabled default.

Timers går att tuna men det bör vara samma överallt.

`timers basic 10 60 60 80 100 `
`show ip protocols | include seconds`

Per interface

`ip rip advertise `<seconds>

**BFD**
[BFD](/Cisco_BFD "wikilink") kan användas med RIP unicast.

`router rip`
` bfd all-interfaces`
` neighbor 1.1.1.1 bfd`

RIP requires you to be advertising a route other than the transit link
for the BFD relationship to establish.

`show ip rip neighbors`

Summarization
-------------

Make RIPv2 classless

`no auto-summary`

Eftersom RIP är ett distance vector routingprotokoll görs summary per
interface. Det måste finnas en mindre specifik route i rib för att
summeringen ska annonseras ut. Däremot installerar inte RIP någon
discard route default men man kan manuellt skapa null routes om man
vill.

`int gi2`
` ip summary-address rip 10.0.0.0 255.255.0.0`

*no auto-summary* behövs också för detta.

Default route
-------------

Det finns flera olika metoder för att skicka en default route till en
granne. Det krävs ingen gateway of last resort för att RIP ska kunna
originera en default route.

`int gi2`
` ip summary-address rip 0.0.0.0 0.0.0.0`

Default-information

`router rip`
` default-information originate`

Static

`ip route 0.0.0.0 0.0.0.0 null 0`
`router rip`
` network 0.0.0.0      #Alt 1`
` redistribute static  #Alt 2`

Default-network (deprecated)

`ip route 20.0.0.0 255.0.0.0 null 0`
`ip default-network 20.0.0.0 `

Finns det en default route i rib så skickas det ut men metricen måste
vara valid för RIP.

`router rip`
` default-metric 3`

**Conditional Default Routing**

`ip prefix-list TRACK seq 5 permit 1.1.1.1/32`
`route-map TRACK_ROUTE permit 10`
` match ip address prefix-list TRACK`
`router rip`
` default-information originate route-map TRACK_ROUTE`

Filtering
---------

**Prefix-list**

`router rip`
` distribute-list gateway     #Filtering incoming updates based on gateway`
` distribute-list prefix      #Filter prefixes in routing updates`

Exempel, filtrera allt från en RIP sender.

`ip prefix-list ROUTERS seq 5 deny 192.168.0.3/32`
`ip prefix-list ROUTERS seq 10 permit 0.0.0.0/0 le 32`
`ip prefix-list PREFIXLIST seq 10 permit 0.0.0.0/0 le 32`

`router rip`
` distribute-list prefix PREFIXLIST gateway ROUTERS in`

**ACL**
Extended ACL tolkas av RIP distribute som:

`access-list 100 permit ip host `<sending router>` host `<prefix>

Exempel

`access-list 100 deny ip host 10.0.0.10 host 172.20.0.0`
`access-list 100 permit ip any any`

`router rip`
` distribute-list 100 in Gi2`

Det går även att blockera specifika avsändare med hjälp av interface ACL

`access-list 10 deny 2.2.2.2 0.0.0.0`
`access-list 10 permit any`

`interface gi2`
` ip access-group 10 in`

**Offset list**
Lägg till 5 på hop count till det som skickas ut på interface Gi2

`router rip`
` offset-list 10 out 5 Gi2`
`access-list 10 permit any`

`show ip protocols | i metric`

*offset-list 0* träffar alla routes

**Administrative Distance**
Det går att filtrera routes med hjälp av AD. Exempel: filtrera vissa
prefix från en viss granne. AD 255 = UNKNOWN.

`access-list 10 permit 192.168.0.0`
`access-list 10 permit 172.30.0.0`

`router rip`
` distance 255 20.0.0.20 0.0.0.0 10`

Filtrera routes som träffar acl 10 men kan komma från alla routrar.

` distance 255 0.0.0.0 255.255.255.255 10`

Redistribution
--------------

Med auto-summary påslaget redistribueras endast classful networks. RIP
har heller ingen seed metric.

`router rip`
` no auto-summary`
` redistribute ospf 1 metric 3`

Detta sätter samma metric på alla routes som redistribueras. Vill man ha
ökad flexibilitet kan man använda en route-map som matchar routes mot
ACLer och sätter metric därefter. Default-metric används som fallback
ifall en route inte träffar route-mapen. T.ex. redistribuerade OSPF E2
routes (cost 20) kommar att ha infinite metric när **transparent**
används om man inte manipulerar metricen.

`default-metric 5`

Om man redistribuerar mellan t.ex. RIP och
[OSPF](/Cisco_OSPF "wikilink") på flera punkter måste man förhindra
suboptimal routing. Ett sätt att göra detta är genom att flagga
redistribuerade routes med högre AD lokalt på redistributionsnoderna.
RIP kan inte skilja på internal och external routes så det andra
routingprotokollet får lösa det.

`router ospf 1`
` distance ospf external 180`

Man kan också tagga routes som blivit redistribuerade för att kunna
filtrera bort dem och på så sätt undvika routingloop.

`route-map TAG`
` set tag 100`
`route-map FILTER-TAG deny 10`
` match tag 100`
`route-map FILTER-TAG permit 20`

`router rip`
` redistribute ospf 1 route-map TAG`
` distribute-list route-map FILTER-TAG in`

RIPng
=====

RIP Next Generation är RIP för IPv6. Även om namnet låter flashigt har
inte mycket av de underliggande mekanismerna förändrats även om UDP 521
istället för 520 nu används för att undvika krock med RIPv1/v2.
Destinationsaddress för uppdateringarna är FF02::9. 15 hop är max metric
och 16 är infinity men däremot ökas metric vid mottagandet av
annonsering istället för skickandet som i tidigare versioner. Allt
loopundvikande sker på samma sätt. En uppdatering kan innehålla så många
entries som får plats i packetet vars max storlek avgörs av IPv6 MTU på
länken. RIPng har inte stöd för autentisering utan precis som med
[OSPFv3](/Cisco_OSPFv3 "wikilink") sköts detta av IPsec, däremot har
inte Ciscos implementation stöd för detta. Passive interfaces och static
neighbors finns inte heller men nyheter är Route Poisoning (utökning av
Split Horizon) och multipla RIPng-processer.

<div class="mw-collapsible mw-collapsed" style="width:310px">

Response packet:

<div class="mw-collapsible-content">

[<File:Cisco_RIPng_Update.png>](/File:Cisco_RIPng_Update.png "wikilink")

</div>
</div>

### Konfiguration

Prereq

`ipv6 unicast-routing`
`ipv6 cef`

En del features konfigureras under RIP-processen.

`ipv6 router rip 1`
` poison-reverse`
` no split-horizon`
` maximum-paths 16  #Max är 32`
` distance 120`

Sätt IP-adresser på interfacen och enablea sedan RIP.

`interface gi 0/0`
` ipv6 address 2001:10:10:10::1/64`
` ipv6 rip 1 enable`

Verify

`show ipv6 rip`
`show ipv6 protocols`
`show ipv6 rip next-hops`
`debug ipv6 rip events`

Annonsera endast default route. Precis som med RIPv2 behöver det inte
finnas någon default-route i RIB för att det ska kunna annonseras.
Default metric för denna är 1.

`interface gi2`
` ipv6 rip 1 default-information only `

Aggregate

`interface gi2`
` ipv6 rip 1 summary-address 2001:10:10:10::/64`

Filtering

`ipv6 router rip 1`
` distribute-list prefix-list FILTER in`

Slå på [VRF](/Cisco_Routing#VRF "wikilink")-stöd.

`ipv6 rip vrf-mode enable`

[Category:Cisco](/Category:Cisco "wikilink")