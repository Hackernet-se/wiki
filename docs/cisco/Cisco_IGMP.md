---
title: Cisco IGMP
permalink: /Cisco_IGMP/
---

Internet Group Management Protocol används mellan end systems och
routrar för att ta reda på om segmentet ska ha multicast-trafik och
isåfall vilken. En router håller inte reda på vilka hostar som är med i
vilka grupper utan endast om gruppen är aktiv eller ej. Hostar använder
det för att joina och lämna multicastgrupper. Switchar kan lyssna på det
för att ta reda på vilka switchportar som ska ha vilken trafik. IGMP
slås på när man konfar multicast routing och
[PIM](/Cisco_PIM "wikilink") på routrar.

Se även [Cisco Multicast](/Cisco_Multicast "wikilink").

Versioner
---------

IGMP härstammar från Host Membership Protocol och finns i flera
versioner, IGMPv1 (RFC 1112) är dock förlegat men det finns
bakåtkompatibilitet. När en IGMPv2-router får in en IGMPv1 Query slutar
den skicka v2-queries och en Version 1 Router Present Timeout startas
som resettas varje gång det kommer in en v1-query. Efter 400 sekunder
går den ut och routern återgår till IGMPv2. Routrar avgör om det är en
IGMPv1-Query som kommer in genom att kolla om Maximum Response Time är
satt.

-   **IGMPv2** (RFC 2236) är bakåtkompatibel med IGMPv1 och är
    defaultversion på Cisco IOS. Version 2 har en förbättrad
    Leave-mekanism och nu finns det även möjlighet att fråga efter
    specifika grupper istället för alla.

<!-- -->

-   **IGMPv3** (RFC 3376) är en nyare revision av IGMP som har en egen
    multicastadress, 224.0.0.22. Den stora nyheten är att end systems
    kan berätta för routrar vilken source de vill ha multicasttrafik
    från, Source-Specifik Multicast. Det är bakåtkompatilbelt med IGMPv1
    och v2.

`show ip igmp interface`

Packets
=======

IGMP-paket skickas med IP och har TTL satt till 1.

-   **Host Membership Query:** är en generell Query som skickas default
    var 60:e sekund till 224.0.0.1 på LAN interface för att kolla om
    någon är intresserad av multicast. Default har hostar 10 sekunder på
    sig att besvara detta.

<!-- -->

-   **Host Membership Report:** skickas antingen som svar på en Query
    och innehåller då alla grupper som hosten är med i eller när en host
    vill joina en ny grupp.

<!-- -->

-   **Leave group message:** skickas till 224.0.0.2 och används av
    hostar för att meddela routrar att de lämnar en grupp.

<!-- -->

-   **Group-Specific Query:** när en router får in ett Leave message
    skickar den ut en gruppspecifik Query (destinationsadress är den
    multicastgruppen) för att se om det fortfarande finns någon på
    segmentet som är intresserad. Detta innehåller Last Member Query
    Interval som default säger att members har 1 sekund på sig att
    svara, det skickas två av dessa när ett Leave kommer in. Om det var
    den sista hosten som skickade Leave message reducerar detta tiden
    det tar innan onödig multicasttrafik slutar skickas från flera
    minuter till ca 3 sekunder.

**IGMP Querier Election**
Finns det flera multicast-routrar på ett segment kommer endast en vara
aktiv och skicka General Queries. När en router får in en General Query
jämförs source-adressen mot det egna interfacets adress och den med
lägst vinner och blir vald IGMP Querier. En nonquerier är inte aktiv
själv men lyssnar efter Queries och när det slutar komma in kan den ta
över. Tiden det tar innan en vald Querier anses död är 2 gånger Query
Interval plus en halv Query Response Interval, default är detta 255
sekunder.

`show ip igmp interface | i querying`

Med IGMPv1 finns det inget inbyggt sätt för hostarna att avgöra vem som
ska stå för Queries. Därför väljer routrarna en som blir DR och den
kommer att skicka IGMP Queries, routern med högst IP vinner.

`show ip igmp interface | i DR `

Timers
------

Man kan konfigurera hur ofta queries ska skickas ut. Varje membership
query message innehåller ett timer-värde (8 bit field) som anger hur
lång tid hostarna har på sig att besvara meddelandet, det räcker att en
host svarar på det så kommer inte multicast-strömmen att upphöra.

`interface gi2`
` ip igmp query-max-response-time 10`
` ip igmp query-interval 60`

Querier

` ip igmp querier-timeout 120`

Verify

`show ip igmp interface | i IGMP`

**Last Member**

`interface gi2`
` ip igmp last-member-query-count 2`
` ip igmp last-member-query-interval 1000`

Man kan även ange att strömmen ska upphöra direkt om det kommer in ett
Leave group message.

` ip igmp immediate-leave group-list IMMEDIATE_LEAVE`

Filtering
---------

IGMP filtering tillåter att man konfigurerar filter för IGMP-trafik på
SVI, per-port eller per-VLAN per-port. Det är ett komplement till IGMP
Snooping, som är ett prereq för filtering. Med IGMPv1-2 discardas hela
paketen ifall filtret träffas medans i IGMPv3 kan man filtrera och
skriva om fält i paketen. Man kan styra minimum IGMP-version och på en
trunk kan man filtrera per VLAN.

ACL Group and channel access control & limit (per interface)

`access-list 12 permit 224.10.10.0 0.0.0.255`
`interface Gi0/0`
` ip igmp access-group 12`
` ip igmp limit 10`

Profile, only allow the specific multicast range

`ip igmp profile 1`
` permit`
` range 224.0.O.O 224.255.255.255`
`int Gi0/0`
` ip igmp filter 1`

IGMP minimum version (global)

`ip igmp snooping minimum-version 2`

Verify

`show ip igmp snooping filter`
`show ip igmp profile`

IGMP Snooping
=============

Switchar kan använda IGMP snooping för att avlyssna IGMP-meddelanden och
ta reda på vilka switchportar som ska ha vilka mac-adresser, dvs är med
i vilken multicastgrupp. Om inte IGMP snooping är på floodas
multicast-frames av switchar precis som broadcast och unknown unicast
eftersom en multicast-MAC-adress aldrig finns i CAM då de aldrig används
som source utan endast destination. På de flesta L3-switchar är IGMP
Snooping påslaget default. Switchar behöver veta om det finns flera
multicast-routrar på segmentet och på vilka portar de sitter därför
lyssnas det efter ett flertal paket-typer: IGMP General Query
(01:00:5e:00:00:01), OSPF (01:00:5e:00:00:05/6), PIMv1 och HSRP
(01:00:5e:00:00:02), PIMv2 Hellos (01:00:5e:00:00:0d) och DVMRP probes
(01:00:5e:00:00:04). IGMP snooping kontrollerar endast distribution av
multicast-trafik till hostar medans routrar får frames för alla grupper.

När det kommer in en IGMP Report på en port tas Group Destination
Address och läggs som forwarding på porten samt router-porten i
CAM-tabellen, på så sätt har man fungerande multicast-forwarding. Kommer
det in en annan IGMP Report med samma GDA läggs även den porten med som
forwarding. Kommer det ett Leave-meddelande tas porten bort från
forwarding och det kollas om det var den sista nonrouter-porten som var
forwarding. Om det var den sista porten skickas Leave vidare till
routern annars discardas det eftersom det är ointressant att skicka
vidare. Eftersom switchar interceptar IGMP Reports får inte hostar
varandras Reports utan alla måste skicka det, detta påverkar Report
Suppression.

Global

`ip igmp snooping`
`no ip igmp snooping vlan 10`

Immediately remove a VLAN from multicast forwarding when an IGMP leave
is received.

`ip igmp snooping vlan 11 immediate-leave`

Verify

`show ip igmp snooping`
`show ip igmp snooping groups`
`show ip igmp snooping mrouter`

**L2 only environment**
Om en switch inte har någon mrouter port, t.ex. om det är en L2 only
environment, kommer inte multicast-trafik att forwarderas vilket kan
leda till blackholing. En mrouter port kan vara statically assigned
eller dynamically learned. När det finns en mrouter port kommer IGMP
reports att skickas på den. Man kan även ändra detta beteende så att en
switch agerar proxy och själv skickar ut membership queries för att
komma runt detta problem så att det forwarderas multicast-trafik.

`ip igmp snooping querier`
`show ip igmp snooping mrouter `

### CGMP

Cisco Group Management Protocol är ett protokoll som används av
L3-enheter för att berätta för Cisco-switchar vilka hostar som ska ha
multicast-trafik (OBS CGMP är gammalt och har spelat ut sin roll, IGMP
Snooping är att föredra). Routrar lär sig vilka mac-adresser som är med
i vilka multicast-grupper genom IGMP så de kan skicka ut
CGMP-meddelanden som switchar lyssnar på. Då kan de ställa sina
CAM-tabeller utifrån den informationen och inga hostar som inte ska ha
multicast-trafik får det. CGMP skickas till 01:00:0c:dd:dd:dd så alla
switchar får meddelandena. När en router kopplas till en switch skickar
den ett CGMP-Join med Group Destination Address satt till 0 och Unicast
Source Address satt till sig själv, då vet switchen var det finns en
multicast-router. Detta skickas ut var 60:e sekund sålänge routern vill
annars skickas ett CGMP-Leave med samma GDA och USA. Det som är skillnad
mot vanlig IGMP är att även L2-informationen kollas på när en router får
in ett IGMP Join och CGMP är konfigurerat. Denna mac-adress och
multicast-grupp kan nu annonseras ut med CGMP-Join. När en switch får in
ett CGMP-Join kollar den sin CAM-tabell efter USA och kan då lägga in
multicast-mac-adressen (GDA) på samma interface, då blir den porten
forwarding även för multicasttrafiken som den hosten har skickat IGMP
Join för. Vill en host inte vara med i en viss grupp längre skickar den
IGMP Leave och routern använder även här L2-informationen och det
skickas ut ett CGMP Leave och switcharna kan ta bort GDA från porten där
hosten sitter. Alla enheter som ska använda CGMP måste konfigureras för
det, detta funkar ej om RGMP används.

L3-enhet

`interface gi2`
` ip cgmp`

Clear, skicka ut ett CGMP Leave med USA = 0 och GDA = 0 då kommer alla
switchar att rensa alla CAM-entries som de satt tack vare CGMP.

`clear ip cgmp`

**RGMP**
Router-Port Group Management Protocol (RFC 3488) är ett annat
Cisco-protokoll som routrar kan använda för att kommunicera till
switchar vilken multicast-trafik de vill ha. Genom att begränsa oönskad
multicast-trafiken som routrar får in minskar man overhead. Alla
RGMP-paket går till 01-00-5e-00-00-19, 224.0.0.25. Konfigurerar man RGMP
disableas CGMP och vice versa.

-   **Hello:** skickas var 30: sekund. När en switch får in ett RGMP
    Hello på en port slutar all multicast-forwardering på den porten.
-   **Join:** för att en router ska få multicast-trafik av en switch
    måste den skicka RGMP Join för de grupper den vill ha.
-   **Leave:** när en router inte längre vill ha trafik för en viss
    grupp skickar den ett RGMP Leave.
-   **Bye:** när man slår av RGMP skickas ett RGMP Bye och switchen
    återgår till att forwardera all multicast-trafik.

`interface gi2`
` ip rgmp`

IGMP Proxy
==========

IGMP proxy låter hostar i unidirectional link routing (UDLR) miljöer som
inte har någon direktkoppling till någon downstream router att joina
multicast-grupper.

`interface gi2`
` ip igmp unidirectional-link `
`interface gi3`
` ip igmp mroute-proxy lo2`
`interface lo2`
` ip igmp helper-address udl gi2 `
` ip igmp proxy-service `

Verify

`show ip igmp udlr`

MVR
===

Multicast VLAN Registration finns till för att effektivisera trafiken på
switchens upplänkar om det finns många multicast-mottagare för samma
grupper i olika VLAN. MVR använder ett dedikerat VLAN genom alla
switchar som används för att leverera multicast feeden till alla
receivers. Man måste ange detta, dvs i vilket VLAN källan för trafiken
befinner sig. MVR går ej att köra samtidigt som multicast routing är
påslaget.

`no ip multicast-routing`
`mvr`
`mvr vlan 200`
`mvr group 239.1.1.10`
`mvr mode dynamic  #skapa mroute states dynamiskt`

`interface gi1`
` description Uplink`
` mvr type source`

`interface gi2`
` mvr type receiver`

Verify

`show mvr`
`show mvr interface`
`show mvr members`

MLD
===

Med IPv6 är multicast en central del eftersom broadcast inte finns och
nu heter det Multicast Listener Discovery istället för IGMP. Det är inte
ett eget protokoll utan en del av ICMPv6. MLD slåss på default när man
slår på ipv6 multicast-routing på en router. Alla paket använder
link-local adresser med TTL 1 och har Router Alert option satt. MLDv1
motsvarar IGMPv2 och MLDv2 motsvarar IGMPv3 för Source-Specific
Multicast, RFC 4604.

-   **Query:** samma som IGMP. 0 är för generella queries annars
    specifik gruppadress. Skickas till FF02::1.
-   **Report:** samma som IGMP och innehåller en specifik gruppadress.
-   **Done:** motsvarar Leave message och innehåller en specifik
    gruppadress. Skickas till FF02::2.

Gå med i grupp manuellt

`ipv6 mld join-group FF08::10`

Gå med i SSM-grupp

`ipv6 mld join-group FF36::8 2001::25`

Verify

`show ipv6 mld interface`
`show ipv6 mld snooping querier`

Defaults per interface

`ipv6 mld query-max-response-time 10`
`ipv6 mld query-timeout 255`
`ipv6 mld query-interval 125`

Membership limit on interface

`ipv6 mld limit 100`

NX-OS
=====

Här följer [Nexus](/Cisco_Nexus "wikilink")-specifik information. En
skillnad mot IOS är att det saknas stöd för IGMP version 1 och Version 3
Lite. IGMP Snooping är på default och gör IP lookups default. En annan
skillnad är att IGMP snooping querier inte konfas på L3 interface utan
under VLAN:et. Se även [PIM](/Cisco_PIM#NX-OS "wikilink") för NX-OS.

`interface Ethernet1/1`
` ip address 192.168.10.1/24`
` ip pim sparse-mode`
` ip igmp version 3`

`vlan configuration 10`
` ip igmp snooping querier 192.168.1.1`

Verify

`show ip igmp snooping`
`show ip igmp snooping querier`
`show ip igmp route`

[Category:Cisco](/Category:Cisco "wikilink")