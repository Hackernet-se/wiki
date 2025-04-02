---
title: Roundcube
permalink: /Roundcube/
---

Roundcube är en webbaserad IMAP-mailklient som är skriven i PHP och kan
användas tillsammans med en LAMP-stack, eller något annat operativsystem
som stödjer PHP. Webbservern behöver tillgång till IMAP-servern är hämta
mail och till en SMTP-server för att kunna skicka mail. Roundcube är
gratis och öppen källkod enligt GNU General Public License (GPL).

<https://roundcube.net>

Installation
------------

Exempelinstallation

`sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get -y install apache2 mysql-server roundcube roundcube-mysql`
`sudo rm -R /var/www/html && sudo ln -s /usr/share/roundcube/ /var/www/html && sudo service apache2 restart`
`sudo dpkg-reconfigure roundcube-core`
`sudo php5enmod mcrypt && sudo service apache2 restart`

Konfiguration
-------------

Peka mot din mailserver.

`sudo nano /etc/roundcube/main.inc.php`
`$rcmail_config['default_host'] = array("ssl://10.0.0.11");`
`$rcmail_config['default_port'] = 993;`
`$rcmail_config['imap_auth_type'] = LOGIN;`
`$rcmail_config['smtp_server'] = 'tls://10.0.0.11';`
`$rcmail_config['smtp_port'] = 25;`
`$rcmail_config['smtp_user'] = '%u';`
`$rcmail_config['smtp_pass'] = '%p';`
`$rcmail_config['smtp_auth_type'] = 'LOGIN';`

[Category:Guider](/Category:Guider "wikilink")