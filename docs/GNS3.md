---
title: GNS3
permalink: /GNS3/
---

GNS3 är en programvara där du kan emulera nätverks enheter så som Cisco
routrar, Juniper brandväggar och Extreme switchar och mycket mera. Sedan
kopplar man ihop enheterna i en topologi så att man kan pröva tex nya
features eller öva inför certifikat utan att behöva köpa hem riktig
hårdvara. Ska man köra stora labbar så kommer GNS3 att kräva en hel del
CPU och RAM från din hårdvara.

GNS3 är uppdelat i en server och en client så att man inte behöver
emulera på sin egen laptop tex.

Supported hårdvara
==================

Hårdvara som kan emuleras av GNS3 finns längst ner på följande sida:

[`https://docs.gns3.com/1FFbs5hOBbx8O855KxLetlCwlbymTN8L1zXXQzCqfmy4/index.html`](https://docs.gns3.com/1FFbs5hOBbx8O855KxLetlCwlbymTN8L1zXXQzCqfmy4/index.html)

Images
======

Vissa tillverkare har lagt ut images på nätet som man kan tanka utan att
behöva registrera sig. Medans vissa kräver att man har ett konto hos
dom.

Cisco
-----

Några Cisco images finns på denna sidan.

[`http://commonerrors.blogspot.se/search/label/GNS3%20IOS`](http://commonerrors.blogspot.se/search/label/GNS3%20IOS)

Extreme Networks
----------------

[`https://github.com/extremenetworks/Virtual_EXOS`](https://github.com/extremenetworks/Virtual_EXOS)

Installation
============

Det rekommenderade sättet att köra GNS3 är att deploya deras färdiga
server VM och sedan ansluta mot den med clienten.

Server
------

Ladda ner servern till den hypervisor du tänkt använda.

[`https://gns3.com/software/download-vm`](https://gns3.com/software/download-vm)

Packa upp filen och deploya den.

Default username och password är **gns3**.

Client
------

För att slippa registrera sig på deras hemsida så kan man tanka hem
clienten via deras Github.

[`https://github.com/GNS3/gns3-gui/releases`](https://github.com/GNS3/gns3-gui/releases)

Filen man ska tanka heter **all-in-one** och innehåller allt man behöver
för att köra en lokal instans av GNS3 också.

Efter installationen är klar starta GNS3 och välj **Run everything on a
remote server**.

Tips n Tricks
=============

Dynamips
--------

Om dynamips kraschar testa följande:

-   Öka på mängden ram images har blivit tilldelad.
-   Pröva en annan image.
-   Byt platform.

[Category:Guider](/Category:Guider "wikilink")