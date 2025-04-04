---
title: SmokePing
permalink: /SmokePing/
---

SmokePing är ett verktyg för att mäta latens i ett nätverk. Den kan
mäta, lagra och visa latens och paketförlust. SmokePing använder rrdtool
för att för att lagra data och har ett webgui för att visa graferna.

Installation
============

`sudo apt-get update && sudo apt-get upgrade`
`sudo apt-get -y install smokeping`

Skapa symlänk till smokeping apache config

`cd /etc/apache2/conf-available && sudo ln -s ../../smokeping/apache2.conf smokeping.conf`

Enable Apache konfig och CGI

`sudo a2enconf smokeping && sudo a2enmod cgid`
`sudo service apache2 restart`

Om detta failar se sendmail nedan.

Konfiguration
=============

Generella inställningar, byt cgiurl.

`sudo nano /etc/smokeping/config.d/General`

Om man inte vill använda sendmail

`sudo nano /etc/smokeping/config.d/pathnames`
`sendmail = /bin/false`

Ifall man vill få larm

`sudo nano /etc/smokeping/config.d/Alerts`

Här görs inställningar gällande vilka hostar som ska övervakas och hur
de ska struktureras (Görs med antal plustecken).

`sudo nano /etc/smokeping/config.d/Targets`
`+ Site1`
`menu =  Site1`
`title = Site1`

`++ LocalMachine`
`menu = Local Machine`
`title = This host`
`host = localhost`
`#alerts = someloss`

`++ GW`
`menu = GW`
`title = GW`
`host = 192.168.0.1`

Restart

`sudo service smokeping restart && sudo service apache2 reload`

Access

[`http://dinserver/cgi-bin/smokeping.cgi`](http://dinserver/cgi-bin/smokeping.cgi)

[Category:Guider](/Category:Guider "wikilink")