---
title: Gammu
permalink: /Gammu/
---

Gammu är ett program för att kunna styra din mobiltelefon eller 3G
modem. Gammu körs med kommandon men finns också webinterface att
använda. Gammu kan prata med enheten över bluetooth, usb eller serielt.
Med Gammu kan du göra följande,

-   Skicka, backupa och ta emot SMS.
-   Ta emot MMS.
-   Visa, importera och exportera telefonboken och kalendern.
-   Komma åt filsystemet.
-   Visa information om telefonen och dess nätverk.
-   Lista, initiera och hantera inkommande samtal.

Förberedelse
------------

Du behöver en mobil eller modem som Gammu har stöd för. Se deras
[databas](http://wammu.eu/phones/).

Installera
----------

`apt-get install gammu usb-modeswitch`

Usb-modeswitch behöver man om man ska använda ett usb modem som visar
sig som både ett usb storage och 3g modem.

Konfiguration
-------------

Skriv kommandot `gammu-detect` så listar den en tty som den tror gammu
har stöd för. Kör sedan `gammu-config` för att skapa en konfig fil mot
rätt port samt välja vilken drivrutin den ska använda.

Filen kommer sparas i `$HOME/.gammurc` vill du använda samma fil för
flera användare flytta den till `/etc/gammurc`.

Kommandon
---------

Ta reda på om du behöver slå in pin eller puk kod.

`gammu --getsecuritystatus`

Slå in pin eller puk kod.

`gammu --entersecuritycode PIN/PUK `<kod>

Skicka ett SMS

`echo Gammu SMS | gammu sendsms TEXT `<nummer>

Huawei
------

För att få igång ett Huawei E367 3G modem behövde jag använda
usb-modeswitch. Samma knep funkar säkert på fler Huawei modem.

`cd /etc/usb_modeswitch.d`
`sudo tar xzf /usr/share/usb_modeswitch/configPack.tar.gz 12d1:1446`
`sudo sed -i -e 's/14ac"/14ac,1506"/' 12d1:1446`
`modprobe usbserial vendor=0x12d1 product=0x1506`

Sedan krävs det att man startar om eller återansluter modemet.

[Category:Guider](/Category:Guider "wikilink")
[Category:Sparco](/Category:Sparco "wikilink")