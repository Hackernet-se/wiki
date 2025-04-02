---
title: Ookla Speedtest Mini
permalink: /Ookla_Speedtest_Mini/
---

Installation
------------

*Debian/Ubuntu*

`wget `[`http://c.speedtest.net/mini/mini.zip`](http://c.speedtest.net/mini/mini.zip)` (Du kan behöva registrera dig på deras hemsida)`
`unzip mini.zip`

`apt-get install apache2`
`apt-get install php5 php5-mysql php5-mcrypt php5-gd libapache2-mod-php5`
`service apache2 restart`

Kommande rad är ej obligatorisk. Den skapar endast en fil som verifierar
att php'n fungerar

`echo "`

<?php phpinfo(); ?>

" \> /var/www/phpinfo.php

`cp -R /[location to extracted folder]/mini /var/www/`

[400px](/File:asdf.JPG "wikilink")

Byt namn på index-php.html filen till index.html och lämna dem
resterande orörda.

`cd /var/www/mini`
`mv index-php.html index.html `

Du skall nu kunna komma åt din speedtestserver via webbläsaren på
"<http://dinserverip/mini>"

[400px](/File:speedtest.JPG "wikilink")

[Category:Guider](/Category:Guider "wikilink")