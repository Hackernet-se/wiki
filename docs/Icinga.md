---
title: Icinga
permalink: /Icinga/
---

Icinga är ett forkat project av Nagios det betyder att Icinga är
bakåtkompatibel med nästan alla Nagios plugins och add-ons skrivna för
Nagios.

Icinga skapades för att fixa brister i Nagios utveckling och för att
lägga till nya funktioner som ett moderna web 2.0 interface, fler stöd
för databaser(Oracle, PostgreSQL och MySQL) och ett REST API. Dom
släpper också patcher oftare och snabbare än vad Nagios gjorde.

Arkitektur
----------

[200px\|Arkitekturen\|thumb](/File:Icinga_Architecture_v1.5.png "wikilink")
Icinga är uppdelat i tre olika delar.

**Core** sköter all övervakning sparar alla resultat och data på IDO
DBn. Den skickar också ut en alert om något har hänt.

**Icinga Data Out Database** (IDODB) fungerar som lagringsyta för all
övervakningsdata som add-ons eller webinterfacet kan hämta.

**Icinga's user interface** som hämtar data från IDODBn och visar upp
resultatet. Används också för att skicka kommandon mot Core.

Förberedelse
------------

Lägg till lite repon för att få senaste versionen.

### Repository

#### Debian

**Icinga Debian repo**

`wget -O - `[`http://packages.icinga.org/icinga.key`](http://packages.icinga.org/icinga.key)` | apt-key add -`
`echo deb `[`http://packages.icinga.org/debian`](http://packages.icinga.org/debian)` icinga-jessie main >> /etc/apt/sources.list `
`echo deb-src `[`http://packages.icinga.org/debian`](http://packages.icinga.org/debian)` icinga-jessie main >> /etc/apt/sources.list`
`apt-get update`

**Debian backports repo**

`echo deb `[`http://ftp.se.debian.org/debian/`](http://ftp.se.debian.org/debian/)` jessie-backports main >> /etc/apt/sources.list`
`apt-get update`

**Debmon repo**

`wget -O - `[`http://debmon.org/debmon/repo.key`](http://debmon.org/debmon/repo.key)` 2>/dev/null | apt-key add -`
`echo 'deb `[`http://debmon.org/debmon`](http://debmon.org/debmon)` debmon-jessie main' >/etc/apt/sources.list.d/debmon.list`
`apt-get update`

#### Ubuntu

**Icinga Ubuntu repo**'

`wget -O - `[`http://packages.icinga.org/icinga.key`](http://packages.icinga.org/icinga.key)` | apt-key add -`
`echo deb `[`http://packages.icinga.org/ubuntu`](http://packages.icinga.org/ubuntu)` icinga-trusty main >> /etc/apt/sources.list`
`echo deb-src `[`http://packages.icinga.org/ubuntu`](http://packages.icinga.org/ubuntu)` icinga-trusty main >> /etc/apt/sources.list`
`apt-get update`

**Icinga PPA repo**

`add-apt-repository ppa:formorer/icinga`
`apt-get update`

Installation
------------

### Core

För att installera Icinga2 core skriv,

`apt-get install icinga2`

Utan plugins vet inte Icinga hur den ska kolla en tjänst. Enklast är att
tanka hem en färdig bundle med plugins.

`apt-get install nagios-plugins`

### Icinga Data Out Database

Guiden utgår ifrån att du kommer köra en lokal MySQL databas.

Installera MySQL

`apt-get install mysql-server mysql-client`

Logga in och skapa en databas samt en användare med rättigheter.

`mysql -u root -p`
`CREATE DATABASE icinga;`
`GRANT SELECT, INSERT, UPDATE, DELETE, DROP, CREATE VIEW, INDEX, EXECUTE ON icinga.* TO 'icinga'@'localhost' IDENTIFIED BY 'icinga';`

Lägg sedan till MySQL ido paketet. Paketet har en wizard som du kan
använda eller skippa och göra det manuellt om du vill.

`apt-get install icinga2-ido-mysql`

Om du vill få upp wizarden igen skriv
`dpkg-reconfigure icinga2-ido-mysql`

För att ansluta manuellt använd conf filen
`/etc/icinga2/features-available/ido-mysql.conf` [Exempel conf
MySQL](http://docs.icinga.org/icinga2/latest/doc/module/icinga2/chapter/object-types#objecttype-idomysqlconnection)

Importera MySQL schemat.

`mysql -u root -p icinga < /usr/share/icinga2-ido-mysql/schema/mysql.sql`

Enabla featuren ido-mysql

`icinga2 feature enable ido-mysql`

Starta om icinga2 för att det ska gälla.

`service icinga2 restart`

### Icinga's user interface

Icinga erbjuder tre st web interface, Icinga Web 2, Icinga Web och
Classic UI.

Guiden utgår ifrån att du har färdig [LAMP](/LAMP "wikilink") server.
Vill du LDAP/AD koppla inlogget krävs PHP LDAP library.

#### Icinga Web 2

Det finns två sätt att installera Web 2. Första med hjälp av repot eller
andra med git. Över repot sker många steg automatiskt men du får kanske
inte senaste versionen. Med GIT får du senaste versionen men får göra
fler steg själv.

##### Repo

`apt-get install icingaweb2 icingacli`

Skapa sedan en setup token med,

`icingacli setup token create`

För att visa den ifall du skulle glömma av den skriv,

`icingacli setup token show`

Surfa sedan till <http://ip/icingaweb2/setup> för att följa wizarden.

##### Git

Börja med att klona repot.

`git clone `[`git://git.icinga.org/icingaweb2.git`](git://git.icinga.org/icingaweb2.git)

Flytta sedan repot och gå till dess plats.

`mv icingaweb2 /usr/share/icingaweb2 && cd /usr/share/icingaweb2`

Skapa en konfigurationsfil till Apache eller Nginx.

**Apache**

`./bin/icingacli setup config webserver apache --document-root /usr/share/icingaweb2/public > /etc/apache2/sites-available/icingaweb2`
`a2ensite icingaweb2`
`service apache2 restart`

**Nginx**

`./bin/icingacli setup config webserver nginx --document-root /usr/share/icingaweb2/public`

Både webusern och cli usern måste ha tillgång till conf och loggar.
Permissions sköter man med en special grupp.

`addgroup --system icingaweb2 && usermod -a -G icingaweb2 www-data`

Skapa ett configuration directory. Default är `/etc/icingaweb2`

`./bin/icingacli setup config directory`

Skapa en setup token med kommandot.

`./bin/icingacli setup config directory`

Visa setup token ifall du glömmer bort den.

`./bin/icingacli setup token show`

Surfa sedan till <http://><ip>/icingaweb2/setup för att följa wizarden.

Kommandon
---------

Icinga har en hög olika [CLI
kommandon](http://docs.icinga.org/icinga2/latest/doc/module/icinga2/chapter/cli-commands#cli-command-feature).

### Features

Kolla vilka features som är enablat.

`icinga2 feature list`

### systemctl/init

`systemctl status icinga2`
`/etc/init.d/icinga2 status`

|             |                                                                                                                                                             |
|-------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| start       | The start action starts the Icinga 2 daemon.                                                                                                                |
| stop        | The stop action stops the Icinga 2 daemon.                                                                                                                  |
| restart     | The restart action is a shortcut for running the stop action followed by start.                                                                             |
| reload      | The reload action sends the HUP signal to Icinga 2 which causes it to restart. Unlike the restart action reload does not wait until Icinga 2 has restarted. |
| checkconfig | The checkconfig action checks if the /etc/icinga2/icinga2.conf configuration file contains any errors.                                                      |
| status      | The status action checks if Icinga 2 is running.                                                                                                            |

Konfiguration
-------------

| \|Path                     | Description                                                           |
|----------------------------|-----------------------------------------------------------------------|
| /etc/icinga2               | Contains Icinga 2 configuration files.                                |
| /etc/init.d/icinga2        | The Icinga 2 init script.                                             |
| /usr/sbin/icinga2          | The Icinga 2 binary.                                                  |
| /usr/share/doc/icinga2     | Documentation files that come with Icinga 2.                          |
| /usr/share/icinga2/include | The Icinga Template Library and plugin command configuration.         |
| /var/run/icinga2           | PID file.                                                             |
| /var/run/icinga2/cmd       | Command pipe and Livestatus socket.                                   |
| /var/cache/icinga2         | status.dat/objects.cache, icinga2.debug files                         |
| /var/spool/icinga2         | Used for performance data spool files.                                |
| /var/lib/icinga2           | Icinga 2 state file, cluster log, local CA and configuration files.   |
| /var/log/icinga2           | Log file location and compat/ directory for the CompatLogger feature. |