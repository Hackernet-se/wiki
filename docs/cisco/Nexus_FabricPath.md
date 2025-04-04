---
title: Nexus FabricPath
permalink: /Nexus_FabricPath/
---

FabricPath är en Ethernet fabric-teknologi framtagen av Cisco för
Nexus-plattformen. Det är designat för att ge hög skalbarhet och
flexibilitet inom ett datacenter genom att kombinera funktioner från
både lager 2 och lager 3. Det är MAC-in-MAC overlay som ersätter
[Spanning-tree protocol](/Cisco_STP "wikilink") med fördelen att inte
behöva några blockerade länkar i ett switchat core (L2MP).
FabricPath-enheterna nyttjar protokollet Intermediate System to
Intermediate System ([IS-IS](/Cisco_IS-IS "wikilink")) för att utbyta
information om hur miljön ser ut (vilka switch ID som finns var) och
bygger ett SPT (Shortest Path Tree) baserat på den informationen. Ingen
STP körs inom FabricPath-nätverket men alla FabricPath Layer 2 gateway
devices ska ha samma låga prio för att FP ska vara STP-root och utifrån
sett är alla FP-enheter en enda stor STP-switch.

För data plane så enkapsuleras ethernet frames med en FabricPath-header
med outside source address och outside destination address vilket sedan
kan routas. FP använder conversational learning och BUM skickas i ett
MDT som automatiskt byggs av alla enheter, så alla får denna trafik och
det är loopfritt. För att veta hur multidestinationstrafik ska
forwarderas används FTAG-fältet i FP-headern. Eftersom det används
multipla FTAG:s som hashas emellan ger detta lastdelning. För att synka
FTAG:ar används en extension till FabricPath IS-IS som heter DRAP
(Dynamic Resource Allocation Protocol). DRAP används också för att
assigna unika switch ID:n inom FP-domänen men detta går även att konfa
manuellt.

När man ska spegla portar ([SPAN](/Cisco_SPAN "wikilink")) kan man välja
om man ska strippa fabricpath-headern eller inte.
[BFD](/Cisco_BFD "wikilink") kan man använda om man kör fabricpath som
DCI-lösning för att snabba upp konvergens. När man kör vPC i kombination
med FabricPath skapas en logisk switch genom att samma FP switch-id
annonseras ut från båda noderna i vPC-domänen, detta kallas vPC+. Se
även [Nexus vPC](/Nexus_vPC "wikilink").

Wireshark kan inte avkoda FabricPath-frames.
[<File:Cisco_FabricPath.PNG>](/File:Cisco_FabricPath.PNG "wikilink")

**MAC Learning**
\* Traditional = Learn SRC MAC of all received traffic

-   FabricPath = Only learn SRC MAC if you already know DST MAC

`show mac address-table learning mode`

Konfiguration
-------------

Aktivera FabricPath

`install feature-set fabricpath`
`feature-set fabricpath`

Skapa nyckel för autentisering

`key chain FABRICPATH`
` key 0`
`  key-string topsecret123`

Global konfiguration med autentisering och fast convergence

`fabricpath switch-id 1`
`fabricpath timers linkup-delay 60`

`fabricpath domain default`
` spf-interval 50 50 50`
` lsp-gen-interval 50 50 50`
` authentication-type md5   #LSP authentication`
` authentication key-chain FABRICPATH`
` authentication-check`
` log-adjacency-changes `

Konfigurera interface för FabricPath

`interface Ethernet1/25`
` switchport`
` switchport mode fabricpath`
` no fabricpath isis hello-padding`
` fabricpath isis authentication-type md5   #hello authentication`
` fabricpath isis authentication key-chain FABRICPATH`

`show fabricpath isis interface br`

VLAN

`vlan 10`
` mode fabricpath`
` name Server`
`vlan 20`
` mode fabricpath`
` name DB`
`exit`

Show

`show fabricpath switch-id`
`show fabricpath topology`
`show fabricpath conflict all`
`show fabricpath route`
`show fabricpath isis`

Effektivisera LSP-hanteringen genom att byta IS-IS network type från
broadcast till p2p.

`interface e1/1`
` medium p2p`

**Traffic Engineering**
FabricPath gör ECMP default men man kan styra vilka länkar som används
genom att manipulera IGP-metricen. Detta görs per interface.

`interface e1/1`
` fabricpath isis metric 400`

**BFD**
Man kan slå på [BFD](/Cisco_BFD#NX-OS "wikilink") på alla FP-interface
men notera att VLAN 1 måste vara i fabricpath mode. BFD-klienten blir
fabricpath-isis. Echo mode inte är supporterat.

`fabricpath domain default`
` bfd`

`show bfd neighbors fabricpath `

### Anycast HSRP

De aktiva HSRP-routrarna annonserar anycast switch ID som source switch
ID för HSRP MAC i FabricPath IS-IS. Alla andra kan då lastdela genom att
skicka till vilken HSRP-router som helst i gruppen. Max antal aktiva
HSRP-routrar är 4 st. Se även [Cisco HSRP](/Cisco_HSRP "wikilink").

`hsrp anycast 1 ipv4`
` switch-id 111`
` vlan 10,11,12`
` priority 120`
` no shutdown`

Man måste köra HSRP version 2 på alla SVI:er som ska dra nytta av
Anycast HSRP.

`show hsrp anycast`

### Troubleshooting

`ping fabricpath switch-id 101`

Send OAM Path Trace Request message to the egress switch ID

`traceroute fabricpath switch-id 101`

Operation, Administration, and Maintenance

`fabricpath-oam`
`show fabricpath oam loopback database`

[Category:Cisco](/Category:Cisco "wikilink")