---
title: Cacti
permalink: /Cacti/
---

Cacti är en grafningslösning för nätverk. <http://www.cacti.net/>

Installation
------------

Ubuntu 14.04

`sudo apt-get update && sudo apt-get upgrade && sudo apt-get -y install snmpd snmp mysql-server \`
`apache2 libapache2-mod-php5 php5-mysql php5-cli php5-snmp php5-gd ntp`

`sudo apt-get -y install cacti`

“libphp-adodb” = “Ok”. “Configuring Cacti” = “Apache2” “Configuring
cacti” = dbconfig-common MySQL = lösenordet du skapa tidigare

Konfiguration
=============

Logga in på webbgränsnittet, där görs den mesta konfigurationen.

[`http://[serverip]/cacti`](http://%5Bserverip%5D/cacti)

admin/admin

**1 minute polling**
OBS "Fix the RRA settings first, because this is the one thing you must
get right from the start. Once you start collecting data with bad RRA
settings, it is extremely difficult to correct it. And by “extremely
difficult”, I mean “just throw it away and start over”."

<http://www.tolaris.com/2013/07/09/cacti-and-1-minute-polling/>

Tänk på:

-   Både in och out under stycket: Adjust “Step” and “Heartbeat” on all
    Data Source templates
-   Starta om crond för att ändringarna ska läsas in

VM-snapshots är din vän.

**Spine**
Spine Polling Daemon är en ersättare för polling-scriptet som körs
default.

`sudo apt-get install cacti-spine`

“Settings” -\> “Configuration” -\> “Poller” -\> “Poller Type” och välj
“Spine”.

**Visual**
Höj vissa standardvärden för att kunna se längre descriptions.
“Settings” -\> “Visual”

-   Maximum Title Length
-   Maximum Field Length

**Interface Description**

`|host_description| - |query_ifName| - |query_ifAlias|`

Plugins
-------

Cacti har ett pluginsystem där man kan lägga de plugins man vill.
Exempel på användbara plugins:

-   [Aggregate](http://docs.cacti.net/plugin:aggregate)
-   [Intropage](http://docs.cacti.net/userplugin:intropage)

**Templates**

-   [Advanced
    Ping](http://www.tolaris.com/2015/07/11/advanced-ping-with-cacti/)

Weathermap
==========

En av de absolut coolaste grejerna med cacti är en plugin som heter
weathermap. Det funkar som plugin för Cacti eller MRTG men går också att
integrera med Observium. Den senaste versionen av weathermap är från Apr
10, 2013, var beredd på att nästan hälften av knapparna i det grafiska
gränssnittet inte fungerar som det ska, man får testa sig fram.

[Exempel](http://maps.harsbo.se)

Download and unzip php-weathermap-latest.zip

``` bash
 wget http://network-weathermap.com/files/php-weathermap-0.97c.zip
 sudo apt-get install unzip
 unzip php-weathermap-0.97c.zip
 sudo mv weathermap /usr/share/cacti/site/plugins
 sudo sed -i '63i$plugins = array();' /usr/share/cacti/site/include/config.php
 sudo sed -i '64i$plugins[] = 'weathermap';' /usr/share/cacti/site/include/config.php
 sudo sed -i -r 's/ENABLED=false/ENABLED=true/g' /usr/share/cacti/site/plugins/weathermap/editor.php
 sudo touch /usr/share/cacti/site/plugins/weathermap/configs/wmap.conf
 sudo chown www-data /usr/share/cacti/site/plugins/weathermap/{output,configs}
 sudo chown www-data /usr/share/cacti/site/plugins/weathermap/configs/wmap.conf
```

Nästa steg görs i det grafiska gränssnittet. Först ska "wmap" enableas
sedan görs resten i Weathermap GUI Editor.

Bakgrundsbilder laddas upp till
/usr/share/cacti/site/plugins/weathermap/images/ och kan sedan väljas i
editorn.

**wmap.conf**
Storlek i pixlar

`WIDTH 1900`
`HEIGHT 900`

Tidsstämpel

`TIMEPOS 1300 40 Created: %b %d %Y %H:%M:%S`

Template nodes

`NODE DEFAULT`
` LABELBGCOLOR 169 5 10`
` LABELFONTCOLOR 216 248 3`
` MAXVALUE 100`

Template links

`LINK DEFAULT`
` WIDTH 5`
` BANDWIDTH 1000M`

**Noder**

`NODE Firewall01`
` LABEL Firewall01`
` LABELOFFSET W   #Sätt label i förhållande till nod. N, S, W, E, C`
` ICON images/Firewall.png`
` POSITION 500 500`

**Länkar**

`LINK Switch01-Firewall01`
` WIDTH 8   #i pixlar`
` INFOURL /cacti/graph.php?rra_id=all&local_graph_id=101`
` OVERLIBGRAPH /cacti/graph_image.php?local_graph_id=101&rra_id=0&graph_nolegend=true&graph_height=100&graph_width=300`
` BWSTYLE angled   #skriv längs med istället för horisontellt`
` BWLABEL bits   #byt från procent till bits`
` BWFONT 106   #måste finnas definierade `
` BWLABELPOS 75 25   #placera label`
` TARGET /var/www/cacti/rra/traffic_in_1000.rrd`
` NODES Switch01 Firewall01`
` BANDWIDTH 100M`
` ARROWSTYLE compact`

**Aggregera länkar**

`TARGET /var/www/cacti/rra/traffic_in_1000.rrd /var/www/cacti/rra/traffic_in_1001.rrd`

**Multiple via**

`VIA x y`
`VIA x2 y2`

**Visningssida för Weathermap**
Detta är ett exempel på en simpel visningssida för den nyskapade
Weathermap:n Med lite html-kunskaper och fantasi går detta att utveckla
väldigt mycket. [Inspiration](http://forums.cacti.net/about24433.html)

`sudo ln -s /usr/share/cacti/site/plugins/weathermap/output /var/www/html/`

``` html4strict
 sudo dd of=/var/www/html/index.html << EOF
 <html>
 <head>
 <title>Internet Load Map</title>
 <META HTTP-EQUIV="REFRESH" CONTENT="60">
 </head>
 <body bgcolor="#000000">
 <img src="../output/12345.png"></img>
 </body>
 </html>
 EOF
```

`sudo sed -i "s/12345/$(find /usr/share/cacti/site/plugins/weathermap/output/ \`
`-name "*.thumb.png" -exec basename \{} .thumb.png \;)/g" /var/www/html/index.html`

**Felsökning**
Om error codes i loggen:
<http://network-weathermap.com/manual/0.97b/pages/errorcodes.html>

Extern hemsida
--------------

Visa cacti-grafer på en extern hemsida.

1\) Enable guest access Console -\> Settings -\> Authentication

-   Guest User : guest

Console -\> User Management -\> guest

-   Enabled : on
-   Realm Permissions : View Graphs = on

2\) Logga in med Guest usern en gång

3\) Lägg in en img src i din html kod där är X.X.X.X ipadressen till
cactin

`<.img src="`[`http://X.X.X.X/cacti/graph_image.php?action=edit&local_graph_id=55&rra_id=1`](http://X.X.X.X/cacti/graph_image.php?action=edit&local_graph_id=55&rra_id=1)`">`

&local_graph_id=55 där 55 är IDet på grafen, &rra_id=1 1an betyder
att den kör på en dag 2 är 1 vecka osv.

[Category:Guider](/Category:Guider "wikilink")