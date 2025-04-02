---
title: ModSecurity
permalink: /ModSecurity/
---

Open Source Web Application Firewall. Funkar med Apache, Nginx and IIS.
Det följer med ett Core Rule Set (CRS) som har regler för bland annat
SQL injection, cross site scripting, trojaner och session hijacking. För
apache finns det modul.

Installation
------------

`sudo apt-get -y install libapache2-mod-security2`
`sudo apachectl -M | grep --color security2`

Konfiguration
-------------

Det följer med ett gäng rekommenderade inställningar som man kan använda
sig av.

`sudo mv /etc/modsecurity/modsecurity.conf-recommended /etc/modsecurity/modsecurity.conf`
`sudo service apache2 reload`

Default så är ModSecurity inställt på Detection Only. För att slå på
ModSecurity:

`sudo sed -i "s/SecRuleEngine DetectionOnly/SecRuleEngine On/" /etc/modsecurity/modsecurity.conf`

Data leakage detection genererar ganska mycket loggar och det kan man
slå av med:

`sudo sed -i "s/SecResponseBodyAccess On/SecResponseBodyAccess Off/" /etc/modsecurity/modsecurity.conf`

### CRS

För att använda sig av Core Rule Set.

`sudo nano /etc/apache2/mods-enabled/security2.conf`
`...`
`       IncludeOptional /etc/modsecurity/*.conf`
`       IncludeOptional "/usr/share/modsecurity-crs/*.conf"`
`       IncludeOptional "/usr/share/modsecurity-crs/activated_rules/*.conf"`
</IfModule>

### Exkludering

Vill man exkludera enskilda hemsidor kan man lägga in följande i
<VirtualHost>-blocket i sin konfiguration.

<IfModule security2_module>
`   SecRuleEngine Off`
</IfModule>

[Category:Guider](/Category:Guider "wikilink")