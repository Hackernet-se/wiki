---
title: LibreNMS
permalink: /LibreNMS/
---

LibreNMS är ett övervaknings verktyg för nätverks tjänster. LibreNMS går
att intergrera med bla [Rancid](/Rancid "wikilink") och
[Oxidized](/Oxidized "wikilink"). LibreNMS har auto-discovery, plugins,
API, och en IRC bot för att ta reda på status via IRC. Du kan autha dig
mot bla MySQL(Default), LDAP eller HTTP för att få SSO stöd. LibreNMS
övervakar enheter med hjälp av SNMP ,ping, check_mk_agent eller med
hjälp av Nagios plugins. LibreNMS är en fork av
[Observium](/Observium "wikilink").

Förberedelser
=============

Du behöver en fungerande MySQL databas och en Apache med PHP.

MySQL
-----

LibreNMS har inte stöd för MySQL strict mode än, därför måste det
stängas av.

Öppna:

`vim /etc/mysql/mysql.conf.d/mysqld.cnf`

Lägg till följande inom \[mysqld\] delen:

`innodb_file_per_table=1`
`sql-mode=""`

Och starta om MySQL servern.

Webserver
---------

Installera följande paket: **Ubuntu 16.04**

`apt-get install libapache2-mod-php7.0 php7.0-cli php7.0-mysql php7.0-gd php7.0-snmp php-pear php7.0-curl snmp graphviz php7.0-mcrypt php7.0-json apache2 fping imagemagick whois mtr-tiny nmap python-mysqldb snmpd php-net-ipv4 php-net-ipv6 rrdtool git`

I filerna `/etc/php/7.0/apache2/php.ini` och `/etc/php/7.0/cli/php.ini`
se till att **date.timezone** är satt till din tidszon. Se [PHP
tidszoner](http://php.net/manual/en/timezones.php) vad som stöds.

Kör följande kommandon för att enable och disable några php och apache
moduler.

`a2enmod php7.0`
`a2dismod mpm_event`
`a2enmod mpm_prefork`
`phpenmod mcrypt`

Skapa LibreNMS användaren
-------------------------

`useradd librenms -d /opt/librenms -M -r`
`usermod -a -G librenms www-data`

Installation
============

Clona ner repot.

`cd /opt && git clone `[`https://github.com/librenms/librenms.git`](https://github.com/librenms/librenms.git)` librenms`

Webinterface
------------

`cd /opt/librenms`
`mkdir rrd logs`
`chmod 775 rrd`
`vim /etc/apache2/sites-available/librenms.conf`

Lägg in följande rader:

` <VirtualHost *:80>`
`  DocumentRoot /opt/librenms/html/`
`  ServerName  librenms.example.com`
`  CustomLog /opt/librenms/logs/access_log combined`
`  ErrorLog /opt/librenms/logs/error_log`
`  AllowEncodedSlashes NoDecode`
`  <Directory "/opt/librenms/html/">`
`    Require all granted`
`    AllowOverride All`
`    Options FollowSymLinks MultiViews`
`  `</Directory>
</VirtualHost>

Sätt LibreNMS användaren som ägare av mappen:

`chown -R librenms:librenms /opt/librenms`

Aktivera sidan och rewrite module och starta om apache.

`a2ensite librenms.conf`
`a2enmod rewrite`
`service apache2 restart`

Om detta är den enda sidan du hostar glöm inte stänga av default sidan.

`a2dissite 000-default.conf`

Snmpd
-----

Kopiera exempel filen från LibreNMS och ersätt raden
`RANDOMSTRINGGOESHERE` med din egna commmunity sträng:

`cp /opt/librenms/snmpd.conf.example /etc/snmp/snmpd.conf`
`vim /etc/snmp/snmpd.conf`

Starta om snmp servicen:

`service snmpd restart`

Cronjob
-------

Lägg till cronjob scriptet som sköter discovery, alerts och
övervakningen.

`cp librenms.nonroot.cron /etc/cron.d/librenms`

Web installer
-------------

Gå sedan till **<http://librenms.example.com/install.php>** och gå
igenom stegen.

Konfiguration
=============

Scripten finns under **/opt/librenms**. Och mycket av konfigurationen
görs direkt i `config.php` som också finns under **/opt/librenms**.

Lägga till device
-----------------

Kan göras via web interfacet under **Devices \> Add device**

Eller från CLI med **addhost.php** scriptet.

`php addhost.php `<IP>

IRC Bot
-------

Lägg in följande rader i `config.php`

`...`
`$config['irc_host'] = "irc.freenode.org";`
`$config['irc_port'] = 6667;`
`$config['irc_chan'] = "#librenms,#otherchan,#noc";`
`...`

Om servern du vill ansluta mot kör SSL så kan du ange ett **+** före
porten.

`...`
`$config['irc_port'] = "+6667";`
`...`

Om servern har ett lösenord:

`$config['irc_pass'] = "Passphrase123";`

För att ändra namn från LibreNMS till något annat:

`$config['irc_nick'] = "NotLibreNMSbot"`

### Systemd service

`cat <<'__EOF__'>/etc/systemd/system/librenms-irc-bot.service`
`[Unit]`
`Description=IRC bot for LibreNMS`
`After=network.target`

`[Service]`
`ExecStart=/usr/bin/php /opt/librenms/irc.php`
`User=librenms`
`Group=librenms`

`[Install]`
`WantedBy=multi-user.target`
`__EOF__`

Kör sedan följande kommando för att enable tjänsten vid omstart och för
att starta tjänsten.

`systemctl enable librenms-irc-bot.service && systemctl start librenms-irc-bot.service`

### IRC kommandon

Note: Det går bara att autha sig mot boten om man använder MySQL som
inloggning. LDAP stöd är förhoppningsvis påväg se
[issue](https://github.com/librenms/librenms/issues/4023) på LibreNMS
Github.

| Kommando                  | Beskrivning                                                                                                                             |
|---------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| .auth <User/Token>        | <user>: Requsta auth token. <token>: Authar sig. Man måste autha sig för att kunna använda boten.                                       |
| .device <hostname>        | Ger basic info om hosten.                                                                                                               |
| .down                     | Listar alla hostnamn som är nere.                                                                                                       |
| .help                     | Tillgängliga kommandon.                                                                                                                 |
| .join <channel>           | Joinar en kanal om användaren har admin-level.                                                                                          |
| .listdevices              | Listar hostnamnet på alla kända devices.                                                                                                |
| .log \[<N>\]              | Listar N linje ur eventlogen.                                                                                                           |
| .port <hostname> <ifname> | Listar info relaterat till porten.                                                                                                      |
| .quit                     | Boten disconnectar från IRC.                                                                                                            |
| .reload                   | Reloadar konfigurationen.                                                                                                               |
| .status <type>            | Listar status info från den valda typen. En type kan vara **devices**, **services**, **ports**. Förkortning: **dev**, **srv**, **prt**. |
| .version                  | Printar `$this->config['project_name_version']`                                                                                         |

LDAP
----

Kräver att paketet `php-ldap` är installerat. Lägg in följande rader i
`config.php`

`$config['auth_mechanism'] = "ldap";`

`$config['auth_ldap_version'] = 3; # v2 or v3`
`$config['auth_ldap_server'] = "ldap.example.com";`
`$config['auth_ldap_port']   = 389;`
`$config['auth_ldap_prefix'] = "uid=";`
`$config['auth_ldap_suffix'] = ",ou=People,dc=example,dc=com";`
`$config['auth_ldap_group']  = "cn=groupname,ou=groups,dc=example,dc=com";`

`$config['auth_ldap_groupbase'] = "ou=group,dc=example,dc=com";`
`$config['auth_ldap_groups']['admin']['level'] = 10;`
`$config['auth_ldap_groups']['noc']['level'] = 5;`
`$config['auth_ldap_groupmemberattr'] = "memberUid";`

### User levels

-   1: Normal användare. Kräver att en admin tilldelar devices och
    portar som dessa får läsa.
-   5: Får läsa allt om alla devices.
-   10: Admin konto som får skriva och läsa.
-   11: Demo konto. Samma som 10 fast får inte ta bort devices.

Auto discovery
--------------

Det finns stöd för att automatiskt lägga till devices. För att det ska
fungera måste man ange en default SNMP community för v1, v2c eller v3,
man måste också ställa in vilka subnet som är ens egna. Discovery körs
var 6h och inom 5 minuter om det är en ny enhet. Man måste också ha
minst en enhet tillagd före auto discovery funkar. Om LibreNMS hittar en
enhet så försöker den göra ett reverse uppslag mot DNS för att få namnet
på devicen. Om det inte går så kommer den heller inte lägga till
devicen, detta är inställt default men går att stänga av.

### Konfiguration

Börja med att sätta SNMP community eller användarnamn & lösenord om du
kör v3:

`// v1 or v2c`
`$config['snmp']['community'][] = "my_custom_public";`
`$config['snmp']['community'][] = "another_public";`

`// v3`
`$config['snmp']['v3'][0]['authlevel'] = 'AuthPriv';`
`$config['snmp']['v3'][0]['authname'] = 'my_username';`
`$config['snmp']['v3'][0]['authpass'] = 'my_password';`
`$config['snmp']['v3'][0]['authalgo'] = 'MD5';`
`$config['snmp']['v3'][0]['cryptopass'] = 'my_crypto';`
`$config['snmp']['v3'][0]['cryptoalgo'] = 'AES';`

Ange vilka subnät som är dina:

`$config['nets'][] = '192.168.0.0/16';`
`$config['nets'][] = '172.16.0.0/12';`

Det går även att utesluta nätverk om man vill:

`$config['autodiscovery']['nets-exclude'][] = '192.168.1.0/24';`

### Discovery methods

Det finns fyra stycken alternativ för att lägga till devices och en
manuell.

**ARP**

Disable by default.

Kan slås på med följande kommando:

`$config['discovery_modules']['discovery-arp'] = 1;`

**XDP**

Enabled by default.

För att stänga av:

`$config['autodiscovery']['xdp'] = false;`

XDP inkluderar FDP, CDP och LLDP.

**OSPF**

Enabled by default.

För att stänga av:

`$config['autodiscovery']['ospf'] = false;`

**BGP**

Enabled by default.

För att stänga av:

`$config['autodiscovery']['bgp'] = false;`

**SNMP Scan**

Denna metod måste du starta själv. Om den bara körs direkt utan växlar
så kommer den scanna näten i din config fil. Med växeln **-r** kan du
säga till vilket nät den ska skanna.

`snmp-scan.php -r 172.22.0.0/24`

#### Korta hostnamn

Om dina devices vid en SNMP fråga svarar med sitt hostnamn istället för
FQDN kan du lägga på din domän med följande kommando:

`$config['mydomain'] = 'hackernet.se';`

#### Lägg till device med IP

Utifall LibreNMS inte kan göra reverse uppslag mot DNS så kommer inte
devicen att läggas till. Det går att stänga av så att den läggs till
ändå fast med IP istället.

`$config['discovery_by_ip'] = true;`

Nagios plugins
--------------

LibreNMS kan köra Nagios plugins som inte använder Nagios NRPE klient.

Börja med att sätta på services i LibreNMS och peka ut vart Nagios
scripten ligger.

`$config['show_services'] = 1;`
`$config['nagios_plugins']   = "/usr/lib/nagios/plugins";`

Installera **nagios-snmp-plugins** paketet om du vill ha ett några
färdiga script som fungerar.

`apt-get install nagios-snmp-plugins`

I webbinterfacet så finns nu en ny knapp som heter **Services** där man
kan lägga till vilken service som ska köras på vilken host.

Ett tips är att köra scripten med **-h** på i skalet så att man ser
vilka parametrar man behöver ställa in för att det ska fungera.

På [Nagios Exchange](https://exchange.nagios.org/) finns ett stort antal
plugins att ladda hem.

Övervakning
===========

LibreNMS har stöd för att övervaka några standard tjänster direkt från
start med hjälp av snmp eller med deras klient check_mk.

Dessa är några av tjänsterna det finns stöd för och hur dom övervakas:

-   Apache - Agent, extend SNMP
-   BIND9/named - Agent
-   MySQL - Agent, extend SNMP
-   NGINX - extend SNMP
-   NTPD - Agent, extend SNMP,
-   PowerDNS - Agent, extend SNMP
-   PowerDNS Recursor - Agent, extend SNMP
-   TinyDNS/djbdns - Agent
-   OS Updates - extend SNMP
-   DHCP Stats - extend SNMP
-   Memcached - Agent, extend SNMP
-   Unbound - Agent
-   Proxmox - extend SNMP
-   Raspberry PI - extend SNMP

Agent installation
------------------

Agenten pratar default på port 6556/TCP.

Clona librenms-agent repot:

`cd /opt/`
`git clone `[`https://github.com/librenms/librenms-agent.git`](https://github.com/librenms/librenms-agent.git)
`cd librenms-agent`

Kopiera check_mk_agent filen och gör den körbar:

`cp check_mk_agent /usr/bin/check_mk_agent && chmod +x /usr/bin/check_mk_agent`

Skapa följande mappar där du sedan ska lägga scripten till tjänsterna du
vill ha grafer på.

`mkdir -p /usr/lib/check_mk_agent/plugins /usr/lib/check_mk_agent/local`

Kopiera scripten från **agent-local** mappen till
**/usr/lib/check_mk_agent/local** och gör dom körbara med **chmod +x**

Kopiera sedan systemd filen och gör att den startar vid boot och starta
agenten.

`cp check_mk@.service check_mk.socket /etc/systemd/system`
`systemctl enable check_mk.socket && systemctl start check_mk.socket`

För att agenten ska fungera så måste man sätta på **unix-agent** under
modules på varje device i web interfacet. Och enable dom tjänsterna man
vill övervaka under **application**.

MySQL
-----

MySQL scriptet kräver en extra konfigurationsfil med användarnamn och
lösenord till databasen som ska övervakas.

Skapa följande fil **/usr/lib/check_mk_agent/local/mysql.cnf** med
innehållet:

`<?php`
`$mysql_user = 'root';`
`$mysql_pass = 'toor';`
`$mysql_host = 'localhost';`
`$mysql_port = 3306;`

Verifera att scriptet fungerar genom att köra

`/usr/lib/check_mk_agent/local/mysql`

Lägg sedan in en extend rad i **/etc/snmp/snmpd.conf**:

`extend mysql /usr/lib/check_mk_agent/local/mysql`

NGINX
-----

Nginx kräver att status sidan är aktiverad för localhost.

`location /nginx-status {`
`    stub_status on;`
`    access_log   off;`
`    allow 127.0.0.1;`
`    deny all;`
`}`

Verifera att scriptet fungerar genom att köra

`/usr/lib/check_mk_agent/local/nginx`

Lägg sedan in en extend rad i **/etc/snmp/snmpd.conf**:

`extend nginx /usr/lib/check_mk_agent/local/nginx`

Apache
------

Flytta apache scriptet till **/usr/lib/check_mk_agent/local/**

Verifera att scriptet fungerar genom att köra:

`/usr/lib/check_mk_agent/local/apache`

Och lägg sedan in en extend rad i **/etc/snmp/snmpd.conf**:

`extend apache /usr/lib/check_mk_agent/local/apache`

PowerDNS
--------

Flytta powerdns scriptet till **/usr/lib/check_mk_agent/local/**

Verifera att scriptet fungerar genom att köra:

`/usr/lib/check_mk_agent/local/powerdns`

Och lägg sedan in en extend rad i **/etc/snmp/snmpd.conf**:

`extend powerdns /usr/lib/check_mk_agent/local/powerdns`

PowerDNS Recursor
-----------------

Flytta powerdns-recursor scriptet till
**/usr/lib/check_mk_agent/local/**

Verifera att scriptet fungerar genom att köra:

`/usr/lib/check_mk_agent/local/powerdns-recursor`

Och lägg sedan in en extend rad i **/etc/snmp/snmpd.conf**:

`extend apache /usr/lib/check_mk_agent/local/powerdns-recursor`

[Category:Guider](/Category:Guider "wikilink")