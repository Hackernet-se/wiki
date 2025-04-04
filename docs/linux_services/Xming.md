---
title: Xming
permalink: /Xming/
---

Xming är en X server för Windows. Med Xming kan köra program som kräver
X över SSH med hjälp av tex PuTTy.

Xming kan vara skönt att köra när man inte vill sätta upp SSH tunnlar.

Installation
------------

[Ladda hem
Xming.](/sourceforge:projects/xming/files/latest/download "wikilink")

Default på allt fungerar bra. Jag väljer att installera utan SSH klient.
Välj sedan att starta Xming.

Konfiguration
-------------

Öppna PuTTy, under Connection --\> SSH --\> X11.

Välj Enable X11 forwarding.

I fältet X display location skriv, `localhost:0`

Testa nu att ansluta till en server och skriv,

`echo $DISPLAY`

Då bör du få ett svar i stil med `localhost:10.0`
Annars dubbelkolla att X11Forwarding Yes är konfat i
/etc/ssh/sshd_config

Tips and tricks
---------------

#### Starta fler än ett program från samma skal.

Skriv ett `&` efter kommandot.

`firefox &`

#### För att inte tappa X11 forwarding om man SSHar till en annan maskin.

X11 forward inställningen följer inte med default om man SSHar till en
annan maskin från sin första om man inte anger ett stort X i SSH
kommandot.

`ssh -X `<hostname>

### Tips på bra program som funkar utmärk med X11 forward.

vncviewer - VNC klient.

rdesktop - RDP klient.

Wireshark - Lyssna på paket.

Firefox - Webbläsare

[Category:Guider](/Category:Guider "wikilink")