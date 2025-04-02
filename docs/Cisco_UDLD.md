---
title: Cisco UDLD
permalink: /Cisco_UDLD/
---

UDLD är en echo-mekanism på lager 2 som gör att enheter som är anslutna
via fiberoptiska eller partvinnade Ethernet-kablar kan övervaka det
fysiska välmåendet av interface och kablar för att kunna upptäcka när en
enkelriktad länk existerar. UDLD-meddelanden skickas var 7:e sekund på
koppar och var 15:e sekund på fiber, med destination 01:00:0C:CC:CC:CC.
Meddelandet innehåller switch-id, port-id och Timeout Echo Value som
tillsammans bildar originator samt en lista på switch/port-par som hörts
på segmentet. Om det kommer ett UDLD-meddelande där switchen själv inte
finns med betyder det att andra sidan inte hör switchen och man kan utgå
ifrån unidirectional link. Kommer det in UDLD med sig själv som
originator betyder det self-looped port. Om något av detta händer blir
interfacet error disabled (oavsett mode). UDLD är good guy protocol som
kan användas i kombination med
[STP](/Cisco_STP "wikilink")/[MST](/Cisco_MST "wikilink"). Om man inte
kör Bridge Assurance eller [BFD](/Cisco_BFD "wikilink") bör man köra
UDLD.

<div class="mw-collapsible mw-collapsed" style="width:200px">

UDLD-paket:

<div class="mw-collapsible-content">

[<File:Cisco_UDLD.png>](/File:Cisco_UDLD.png "wikilink")

</div>
</div>

### Normal vs Aggressive mode

Vad som ska hände när det slutar komma in UDLD-meddelanden beror på
vilket mode UDLD är konfigurerat i. I Normal mode försöker switchen
aktivt återuppta grannskap genom att skicka 8 UDLD frames, sedan händer
ingenting och porten förblir up. Med Aggressive mode försöker switchen
att återuppta grannskap genom att skicka 8 UDLD frames men om det inte
lyckas blir porten error disable. I Aggressive mode blir ett interface
endast error disable om länken går “Bidirectional” -\> “Unidirectional”,
dvs den måste först ha varit uppe och haft fungerande grannskap.

Normal och Aggressive mode är kompatibelt med varandra eftersom det
endast handlar om lokalt beteende vid avsaknad av UDLD-meddelanden.

### Konfiguration

Global, gäller fiberportar.

`udld enable|aggressive`

Per interface, gäller oavsett media.

`interface gi0/20`
` udld port [aggressive]`

Verify

`show udld`
`show udld neighbors`

Restore alla interface som är error-disabled pga link failure.

`udld reset`

Auto Recovery

`errdisable recovery cause udld`
`show errdisable recovery`

På vissa plattformar kan man välja att UDLD endast ska rapportera errors
istället för att err-disablea porten.

`udld fast-hello error-reporting`

Time in seconds between sending of messages in steady state.

`udld message time <7-90>`

[Category:Cisco](/Category:Cisco "wikilink")