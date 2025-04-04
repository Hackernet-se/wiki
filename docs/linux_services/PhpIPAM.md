---
title: PhpIPAM
permalink: /PhpIPAM/
---

[phpIPAM](http://phpipam.net/) är en IPAM-lösning som har stöd för bl.a.
subnet scanning, IPv4/IPv6, AD/LDAP, VLAN, VRF, mail notifications.

Installation
============

*Ubuntu 16.04*
**Apache**

`sudo apt-get -y install apache2`

**MySQL**

`sudo apt-get -y install mysql-server`
`mysql_secure_installation`

**PHP**

`sudo apt-get -y install php7.0 libapache2-mod-php7.0 && sudo systemctl restart apache2`
`sudo apt-get -y install php7.0-cli php7.0-curl php7.0-gmp php7.0-json php7.0-ldap php7.0-mcrypt php7.0-mysql php7.0-xml php-pear && sudo systemctl restart apache2`

Ladda ner tarball från hemsida.

`wget `[`https://sourceforge.net/projects/phpipam/files/phpipam-1.2.1.tar`](https://sourceforge.net/projects/phpipam/files/phpipam-1.2.1.tar)

Packa upp och lägg i directory för webbservern.

`sudo tar -xf phpipam-1.2.1.tar -C /var/www/`
`sudo rm /var/www/html/index.html && sudo mv /var/www/phpipam/* /var/www/html/`
`sudo cp /var/www/html/config.dist.php /var/www/html/config.php`
`sudo a2enmod rewrite && sudo service apache2 restart`

Nu kan man göra resten i webgui. *<http://><IP>/*
Om något fattas eller är fel möts man av ett felmeddelande som berättar
vad som är fel. T.ex. om man har lagt siten i en undermapp,
<http://><IP>/phpipam/, måste man konfa om config.php och .htaccess
(trailing slash viktigt).

Välj: *Automatic database installation* och använd root-kontot.

Följ sedan instruktionerna, logga in.

Konfiguration
=============

### CLI

Eftersom allt ligger i en SQL-databas kan man använda vanlig SQL-syntax
för att manipulera datan.

`use phpipam;`

VLAN

`insert into vlans (name,number,description) values("Client", "1338", "Klient-vlan") `

VRF

`insert into vrf (name,rd,description) values("vrf2", "11:22", "bla2") `

### Pretty links

Gör att din URL ser bättre ut. rewrite måste vara påslaget i apache för
att det ska fungera.

-   No: ?page=administration&link2=settings
-   Yes: /administration/settings/

Ändra base i **config.php** filen för phpIPAM. (Om phpipam ligger i
rooten på webbservern så kan du skippa detta steg.)

`define('BASE', "/phpipam/");`

Slå på rewrite i apache.

`a2enmod rewrite`

Lägg till följande rader i apache confen.

`...`
`Options FollowSymLinks`
**`AllowOverride`` ``all`**
`Order allow,deny`
`Allow from all`
`...`

Sätt på pretty links under **Administration \> phpIPAM settings** eller
ändra i databasen.

`use phpipam;`
`update settings set prettyLinks='Yes/No' where settings.id=1;`

### AD

Inlogg mot AD.

### [HTTPS](/Apache#SSL "wikilink")

Aldrig fel med SSL.

`sudo a2enmod ssl && sudo a2ensite default-ssl && sudo systemctl restart apache2`

### SMTP

Backup
------

DB-backup kan schemaläggas med [cron](/cron "wikilink")

`# Backup IP address table, remove backups older than 30 days`
`@daily /usr/bin/mysqldump -u root -pPASSWORD phpipam > /var/www/html/db/bkp/phpipam_bkp_$(date +"\%y\%m\%d").db`
`@daily /usr/bin/find /var/www/html/db/bkp/ -ctime +30 -exec rm {} \;`

### Restore

Dra upp en ny databas och läs in backupen.

`` CREATE DATABASE `phpipam`; ``
`exit`
`mysql -u root -p < ./backupfile.sql`
`` GRANT ALL on `phpipam`.* to phpipam@localhost identified by 'ipamadmin'; ``

Logga in med Admin/ipamadmin på webgui.

[Category:Guider](/Category:Guider "wikilink")