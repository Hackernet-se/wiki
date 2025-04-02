---
title: Cisco VTP
permalink: /Cisco_VTP/
---

VTP står för VLAN Trunking Protocol men tänk VLAN Management Protocol då
det används för att managera VLAN-databaser på flera switchar centralt
från en switch. Det går endast över ISL/802.1q-länkar så trunk mellan
switcharna är ett måste. VTP annonserar VLAN ID, namn, typ och tillstånd
men dock inget om vilka portar som tillhör vilket VLAN. VTP jobbar med
revisionsnummer för att veta vilka databas som är korrekt uppdaterad,
högre revisionsnummer vinner. Se även [Cisco
VLAN](/Cisco_VLAN "wikilink").

*OBS* VTP har potentialen att sänka en hel L2-miljö på några enstaka
sekunder, förstå hur det fungerar och räkna med riskerna.

### Max VTP Vlan

I varje switchmodell så finns det ett max antal vlan den kan få ifrån
servern, slår detta i taket så går switchen in i transparent mode, dvs
den tar inte emot nya utan kör på det som finns.

| Switch              | Max Vlan |
|---------------------|----------|
| 2960TT,2960S,2960CX | 255      |
| 2960CG,2960X,3750   | 1005     |
| 3650                | 4096     |

### Versioner

VTP finns i version 1, 2 och 3. VTPv1 är default.

Skillnader mellan v1 och v2.

-   Stöd för diverse Token Ring VLAN
-   Stöd för unknown TLV records, v1 ignorerar dessa.
-   VLAN-databasen konsistenscheckas ej om ändringen kommer med VTP.
    Implementation optimization.

Pakettyper
----------

Gäller VTPv1 och v2.
**Summary advertisements**
Skickas av server och client var 5 minut eller vid VLAN-modifikation och
innehåller allt utom själva VLAN-databasen. Innehåller VTP domain name,
revision number, identity of last updater, time stamp of last update,
MD5 sum of VLAN database, VTP password och antalet efterkommande Subset
advertisements.

<div class="mw-collapsible mw-collapsed" style="width:250px">

Exempel:

<div class="mw-collapsible-content">

[<File:Cisco_VTP_Summary.png>](/File:Cisco_VTP_Summary.png "wikilink")

</div>
</div>

**Subset advertisement**
Skickas ut efter en VLAN-förändring och innehåller hela databasen. Kan
dock behövas flera paket ifall det är en stor databas.

<div class="mw-collapsible mw-collapsed" style="width:250px">

Exempel:

<div class="mw-collapsible-content">

[<File:Cisco_VTP_Subset.png>](/File:Cisco_VTP_Subset.png "wikilink")

</div>
</div>

**Advertisement requests**
Skickas av server och client när de vill ha hela VLAN-databasen, t.ex.
när de får in en Summary Advertisement med högre revisionsnummer.
Skickas även av klienter när de startas om eller blir client.

<div class="mw-collapsible mw-collapsed" style="width:250px">

Exempel:

<div class="mw-collapsible-content">

[<File:Cisco_VTP_Request.png>](/File:Cisco_VTP_Request.png "wikilink")

</div>
</div>

**VTP join messages**
Skickas av server och client var 6 sekund om pruning är påslaget.
Berättar om vilka VLAN som är aktiva.

<div class="mw-collapsible mw-collapsed" style="width:250px">

Exempel:

<div class="mw-collapsible-content">

[<File:Cisco_VTP_Join.png>](/File:Cisco_VTP_Join.png "wikilink")

</div>
</div>

Konfiguration
=============

`vtp version [version]`

Vill man byta vlan.dat kan man göra det, det har bara lokal signifikans.

`vtp file `*`filename`*

VTP kan stängas av per interface

`no vtp`
`show vtp interface`

Debug

`debug sw-vlan vtp events`
`debug sw-vlan vtp packets`

### Domain

Domän måste vara samma på alla enheter annars ignoreras updates, har man
inget domännamn konfigurerat lånar man det som andra sidan skickar med i
sina paket (v3 gör ej så). Byt namn på domän för att resetta revision
number.

`vtp domain [domain]`
`show vtp status`

Använd lösenord för att skydda din miljö annars kan t.ex. domäner
propagera till switchar automatiskt. Detta skyddar ej mot eavesdropping
utan endast mot unauthorized switches. En MD5-summa räknas fram av
VLAN-databasen och lösenordet för att sedan skickas med Summary
advertisement. Hidden password är VTPv3 only och då hashas lösenordet i
vlan.dat också, v1/2 funkar inte ifall det finns ett hidden password
konfigurerat.

`vtp password SECRETZ {hidden|secret}`
`show vtp password`

### Modes

**Server**
På VTP-servrar skapar, modifierar och tar man bort VLAN, detta
propageras sedan ut till klienter och övriga servrar. Detta är default
för Cisco IOS men uppdateringar skickas inte förrens VTP domain är
konfigurerat. Uppdateringar accepteras från server och client och VLAN
sparas i vlan.dat.

`vtp mode server`

**Client**
Behöver ej ha VTP domain konfigurerat utan tar det från den första
VTP-uppdateringen som tas emot. Dock måste vtp mode client konfigureras.
Uppdateringar accepteras från server och client och VLAN sparas i
vlan.dat. Eftersom klienter originerar uppdateringar kan en klient med
högre revisionsnummer uppdatera databasen på en server.

`vtp mode client`

**Transparent**
Enheter i VTP mode transparent släpper igenom VTP frames om VTP domain
matchar men behandlar dem aldrig själv, *VTP LOG RUNTIME: Relaying
packet received on trunk Gi0/2 - in TRANSPARENT MODE*. VLAN på dessa
enheter sparas lokalt i running config och vlan.dat. OBS transparent
mode forwarderar VTP om domain är NULL.

`vtp mode transparent`

**Off**
Finns endast med VTPv3 och stänger av VTP-forwarding helt.

`vtp mode off`

### Pruning

VTP pruning erbjuder en dynamisk mekanism som automatisk konfigurerar
vilka VLAN som ska tillåtas på trunkar inom VTP-domänen. Slå på pruning
för att hindra flooding i alla VLAN till switchar som inte har portar i
alla VLAN. För utbyte av information om aktiva VLAN används VTP join
messages. VTP pruning kan läras av VTP-klienter, så om man slår på det
på en VTP-server och den börjar skicka ut join messages så kommer också
klienterna att slå på pruning automatiskt.

`vtp pruning`

By default är alla VLAN utom 1 prune eligible. Vill man att endast vissa
VLAN ska vara med i VTP pruning kan man lägga dem per trunk i Prune
Eligible List.

`switchport trunk pruning vlan VLAN-RANGE`

Verify

`show interface trunk`

VTPv3
=====

Med VTPv3 introduceras *primary server* och det är bara dennes
VLAN-databas som får modifieras och skickas ut i domänen. Alla andra
servrar blir secondary. Vilken switch som är primary server måste
switcharna vara eniga om för att kommunicera. Är switchar oeniga blir
det konflikt och ingen databas synkas, **show vtp devices conflicts**.
Detta minskar ytterliggare risken för att oavsiktligt skriva över en
VLAN-databas.

Skillnader mellan v2 och v3.

-   Möjligt att använda krypterade lösenord även i vlan.dat.
-   Stöd för private och extended vlan, dvs över 1005.
-   Off mode, alla VTP-meddelanden droppas, globalt eller per interface.
-   Stöd för mer än bara VLAN-databassynk, det finns även en instans för
    [MST](/Cisco_MST "wikilink")-konfiguration samt forwarda VTP-frames
    för UNKNOWN features ifall det hittas på något i framtiden.
-   Stöd för att flagga VLAN som [RSPAN](/Cisco_SPAN#RSPAN "wikilink"),
    dvs disables MAC learning i VLANet på alla switchar.
-   Serverrollen, se nedan.

Bakåtkompabilitet får man när man kör v1/v2 på ena sidan och v3 på den
andra då kommer v3 känna av det och återgå till v2 vilket tvingar den
första switchen att använda v2-only. v2-sidan kan aldrig uppdatera
v3-domänen så allt i v2 bör vara client.

Konfiguration

`vtp domain hackernet.se`
`vtp version 3`

Skapa VLAN

`vtp mode server`
`vlan 100`
*`VTP`` ``VLAN`` ``configuration`` ``not`` ``allowed`` ``when`` ``device`` ``is`` ``not`` ``the`` ``primary`` ``server`` ``for`` ``vlan`` ``database.`*

För att bli primary krävs lösenordet. Primary är endast operational
state, det är inget som sparas i running eller startup.

`vtp primary`

Ta primary utan att först kontrollera efter conflicting devices (som
annars kan ta lite tid).

`vtp primary vlan force`

Verify

`show vtp status`
`show vtp devices  #Endast v3-enheter syns`
`show vtp counters`

### Extended VLANs

Varje gång man skapar en routed port eller SVI i en L3-switch binds ett
VLAN till det interfacet för intern kommunikation till control plane.
Detta görs lokalt och kan därmed skilja mellan switcharna i miljön.
Detta leder till att om man skapar ett högnummer-VLAN på en VTP server
switch utan SVI:er så funkar det bra men det kanske inte skapas på alla
switchar även om VTP fungerar som det ska, *"VLAN_CREATE_FAIL"* pga
"VLAN 1007 currently in use by GigabitEthernet0/3". Vilka VLAN en switch
använder till detta beror på global policy i switchen.

`show vlan internal usage`

Default är att starta allokering på VLAN 1006 och gå uppåt.

`vlan internal allocation policy ascending`

På nyare switchar kan man ändra detta till att starta på vlan 4094 och
gå neråt istället.

`vlan internal allocation policy descending`

### MST

[MST](/Cisco_MST "wikilink")-konfiguration kan också distribueras med
hjälp av VTPv3. Precis som för VLAN får endast ändringar göras på
primary server (som ej behöver vara samma som för feature VLAN).

`vtp mode server mst`
`vtp mode client mst`

*OBS att ändra VTP mode för MST påverkar spanning tree så det bör göras
under kontrollerade former.*

Ta primary-rollen

`vtp primary mst `
`vtp primary mst force`

Verify

`show vtp status`

[Category:Cisco](/Category:Cisco "wikilink")