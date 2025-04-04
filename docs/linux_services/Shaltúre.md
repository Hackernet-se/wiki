---
title: Shaltúre
permalink: /Shaltúre/
---

Shaltúre är ett gäng bra services för att komplettera din IRC server. Du
kan registrera ditt nick, äga kanaler så ingen kan ta över den är några
av sakerna du får.

Dessa services finns,

-   NickServ
-   ChanServ
-   Global
-   InfoServ
-   OperServ
-   SaslServ
-   MemoServ
-   GroupServ
-   StatServ
-   ALIS

Förberedelse
------------

Du behöver ett extra A record tex `services.hackernet.se`

`apt-get install gettext`

Installation
------------

Shaltúre installerar sig i användarens home folder som default. Därför
behöver man klona från git till en mapp som inte heter `Shalture`

`git clone `[`git://github.com/shalture/shalture.git`](git://github.com/shalture/shalture.git)` shalture-source`
`cd shalture-source`
`git submodule init`
`git submodule update`

Sedan är det bara att kompilera programmet.

`./configure --enable-contrib`
`make`
`make install`

Konfiguration
-------------

Konfigurationen är verifierad och funkar på
[InspIRCd](/InspIRCd "wikilink"), men det bör vara samma för andra IRC
servrar.

Börja med att kopiera exempel filen.

`cd ~/shalture/etc && cp shalture.conf.example shalture.conf`

Ändra rad 66 så rätt IRCd modul laddas.

`loadmodule "modules/protocol/inspircd";`

På rad 793 i `serverinfo` fältet ändra följande så dom passar dig.

`name = "services.hackernet.se";`
`desc = "Hackernet IRC Services";`
`numeric = "00A"; #Denna är viktigt att den inte har samma ID som i konfigurationsfilen för din IRC server.`
`netname = "Hackernet";`
`adminname = "Sparco";`
`adminemail = "root@hackernet.se";`
`registeremail = "root@hackernet.se";`

Leta sedan upp `uplink` fältet på rad 938.

`uplink "services.hackernet.se" {`
`host = "irc.hackernet.se";`
`port = "6666";`
`send_password = "password";`
`receive_password = "password";`

På rad 971 i `nickserv` ändra.

`host = "hackernet.se";`

Det kommer ge nickserv FQDN namnet nickserv@hackernet.se. Ändra nu
`host=` på resterande services som kommer i filen.

Leta upp raden `operator` på rad 2217. Ändra till samma som din IRCd
oper är.

### InspIRCd

Konfigurationen som behövs på InspIRCd för att Shaltúre ska funka.
Shaltúre klarar inte av att ansluta över SSL än.

``` bash
<bind address="192.168.1.4" port="6666" type="servers">
<uline server="services.hackernet.se">
<link name="services.hackernet.se" ipaddr="192.168.1.4" port="6666" allowmask="192.168.1.0/24" sendpass="password" recvpass="password">
```

Följande moduler behöver också vara laddade.

``` bash
<module name="m_chanprotect.so">
<module name="m_halfop.so">
<module name="m_services_account.so">
<module name="m_deaf.so">
<module name="m_spanningtree.so">
<module name="m_globops.so">
<module name="m_cban.so">
<module name="m_svshold.so">
<module name="m_hidechans.so">
<module name="m_servprotect.so">
<module name="m_chghost.so">
<module name="m_namesx.so">
<module name="m_uhnames.so">
```

Starta nu Shaltúre

`cd $HOME/shalture/bin/ && ./shalture-services`

Exempel
-------

På din IRC server skriv nu för att få hjälp.

`/msg Nickserv help`
`/msg Chanserv help`

Crontab
-------

Lägg in följande i din crontab för att checka att Shaltúre är igång var
5e minut.

`*/5 * * * * /home/shalture/shalture/etc/shalture.cron >/dev/null 2>&1`

[Category:Guider](/Category:Guider "wikilink")
[Category:Sparco](/Category:Sparco "wikilink")