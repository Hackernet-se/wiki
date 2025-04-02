---
title: Apache
permalink: /Apache/
---

Apache är en av världens mest använda webbservrar. Och hostar idag ca
35-40% av alla hemsidor i världen. Apache är en väldigt enkel webbserver
att konfigurera och har även flera användbara tillägg.

Installation
------------

`sudo apt-get install apache2`

### Apache kommandon

`a2ensite` För att aktivera en sida. Tillgängliga sidor finns i mappen
`/etc/apache2/sites-available`

`a2dissite` För att inaktivera av en sida. Aktiverade sidor finns i
mappen `/etc/apache2/sites-enabled`

`a2dismod` För att stänga av ett tillägg. Aktiverade tillägg finns i
mappen `/etc/apache2/mods-enabled`

`a2enmod` För att aktivera ett tillägg. Tillgängliga tillägg finns i
mappen `/etc/apache2/mods-available`

Konfiguration
-------------

vHosts är bra att använda om man bara har en IP utåt och vill dela port
80/443 med flera hemsidor men ha olika domännamn. För att få virtualhost
att fungera så räcker det att man lägger till denna raden i apache
configen.

`ServerName hackernet.se`

Kopiera default filen under sites-available.

`cp /etc/apache2/sites-available/default /etc/apache2/sites-available/hackernet`

Öppna den nya filen och lägg till raden precis under `ServerAdmin` och
över `DocumentRoot`

Ändra även `DocumentRoot` och `Directory` ifall du vill att en annan
hemsida ska visas istället för orginal.

Aktivera sedan sidan med

`a2ensite hackernet`

### Apachectl

Kolla grundläggande konfiguration:

`apachectl -S`

Kör ett configtest:

`apachectl -t`

Permissions
-----------

Följande är en bra grund för filrättigheter.

`chown root:www-data /var/www/html -R`
`chmod g+s /var/www/html`
`chmod o-wrx /var/www/html -R`

www-data, apache2′s user, har nu grupp-ägarskapet för default web root
och alla filer däri. g+s säger åt filsystemet att alla nya filer som
skapas får samma grupp-ägarskap.

Log files
---------

`tail -f /var/log/apache2/access.log`

SSL
---

Enable module

`sudo a2enmod ssl && sudo a2enmod headers && sudo service apache2 restart`

**Certifikat**
Fixa ett certifikat, antingen från en CA (t.ex. [Let's
Encrypt](/Let%27s_Encrypt "wikilink")) eller
[self-signed](/Digitala_Certifikat#Self-signed "wikilink").

Konfiguration med säkerhet i fokus.

[`https://cipherli.st/`](https://cipherli.st/)

Aktivera vHost

`sudo a2ensite hackernet && sudo service apache2 restart`

Dölj Version
------------

Skriv följande i `Apache.conf/httpd.conf`

`ServerTokens ProductOnly`
`ServerSignature Off`

ApacheBench
-----------

Benchmarking tool

*`sudo`` ``apt-get`` ``install`` ``apache2-utils`*
`ab -n 500 -c 100 `[`http://example.com/`](http://example.com/)

Known errors
------------

### \[warn\] _default_ VirtualHost overlap on port 443, the first has precedence

Kan man få när man försöker skapa flera vhost på port 443. Man märker
också problemet att alla olika vhostar på port 443 pekar på samma sida.

För att fixa lägg till `NameVirtualHost *:443` i din `ports.conf` eller
`httpd.conf` fil.

``` apache
 <IfModule mod_ssl.c>
     # If you add NameVirtualHost *:443 here, you will also have to change
     # the VirtualHost statement in /etc/apache2/sites-available/default-ssl
     # to <VirtualHost *:443>
     # Server Name Indication for SSL named virtual hosts is currently not
     # supported by MSIE on Windows XP.
     NameVirtualHost *:443
     Listen 443
 </IfModule>
```

[Category:Guider](/Category:Guider "wikilink")