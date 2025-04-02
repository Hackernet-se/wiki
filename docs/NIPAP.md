---
title: NIPAP
permalink: /NIPAP/
---

NIPAP är ett IPAM-system som är skrivet i python och är open source. Det
finns både webgui och cli för att managera datan som sparas i en
postgres-DB.
Demo: <http://nipap-demo.spritelink.net/>

Installation
============

*Debian eller Ubuntu*

`echo "deb `[`http://spritelink.github.io/NIPAP/repos/apt`](http://spritelink.github.io/NIPAP/repos/apt)` stable main extra" > /etc/apt/sources.list.d/nipap.list`
`wget -O - `[`https://spritelink.github.io/NIPAP/nipap.gpg.key`](https://spritelink.github.io/NIPAP/nipap.gpg.key)` | apt-key add -`
`apt-get update && apt-get -y install nipapd`

Svara Yes på frågorna för att autoskapa databas

`apt-get -y install nipap-www`

Återigen yes för att skapa ett användarkonto för frontend till backend

Konfiguration
=============

I denna guide görs allt på samma maskin men frontend accessas från andra
maskiner. Det behövs ett konto för att logga in på webguit.

`nipap-passwd add --user user1 --password mypasswort --name "the man"`

### [Apache](/Apache "wikilink")

`apt-get -y install apache2 && apt-get -y install libapache2-mod-wsgi`
`nano /etc/apache2/sites-available/000-default.conf`
`<VirtualHost *:80>`
`       DocumentRoot /var/www/html`
`       ErrorLog ${APACHE_LOG_DIR}/error.log`
`       CustomLog ${APACHE_LOG_DIR}/access.log combined`

`       WSGIScriptAlias / /etc/nipap/nipap-www.wsgi`
`       <Directory "/etc/nipap">`
`       Order allow,deny`
`       Allow from all`
`       <Files nipap-www.wsgi>`
`       Require all granted`
`       `</Files>
`       `</Directory>
</VirtualHost>

`chown -R www-data:www-data /var/cache/nipap-www && chmod -R u=rwX /var/cache/nipap-www`
`sudo service apache2 restart`

### LDAP

Börja med att installera python-ldap modul.

`apt-get install python-ldap`

Ändra sedan i `/etc/nipap/nipap.conf` filen till följande.

`default_backend = ldap`

`basedn = dc=hackernet,dc=se`
`uri = `[`ldap://IP`](ldap://IP)
`binddn_fmt = uid={},ou=users,dc=hackernet,dc=se`
`search = uid={}`
`search_binddn = cn=admin,dc=hackernet,dc=se`
`search_password = secretpw`
`rw_group = cn=nipap,dc=hackernet,dc=se`

Skapa sedan en grupp som heter nipap och som har stöd för
[memberOf](/OpenLDAP#memberOf "wikilink"). Användare i denna gruppen får
read/write rättigheter.

CLI
===

Med ett cli går det snabbare att fylla databasen om det handlar om stora
datamängder.

`apt-get -y install nipap-cli`
`nipap-passwd add --user cli-master-flash --password olasamigossenior --name "the CLI man"`
`touch ~/.nipaprc && chmod 0600 .nipaprc && nano .nipaprc`
`[global]`
`hostname = localhost`
`port     = 1337`
`username = cli-master-flash`
`password = olasamigossenior`
`default_vrf_rt = none`
`default_list_vrf_rt = all`

`nipap address add prefix 192.0.2.0/24 type assignment description "MGM-network"`
`nipap address add prefix 172.20.0.10 type host node "SW01" description "L3-switch"`

Debug
=====

`sudo nipapd -d -f --no-pid-file`

[Category:Guider](/Category:Guider "wikilink")