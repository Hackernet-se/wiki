---
title: Nginx
permalink: /Nginx/
---

[Category:Guider](/Category:Guider "wikilink") Nginx används som
webbserver av mer än 60% av världens top 100,000 hemsidor. Men Nginx kan
vara mycket mer än bara en webbserver. Ett litet urval vad Nginx kan
användas som:

-   Reverse proxy
-   Load balancer
-   HTTP Cache
-   RTMP Server

Installation
============

-   <btn data-toggle="tab" class="">\#tab1\|CentOS 7</btn>
-   <btn data-toggle="tab" class="">\#tab2\|Ubuntu 16.04</btn>

<div class="tab-content">
<div id="tab1" class="tab-pane fade in active">

Börja med att installera epel-repot:

`yum install epel-release:`

Installera Nginx:

`yum install nginx`

Starta Nginx:

`systemctl start nginx`

Gör så Nginx startar automatiskt vid reboot:

`systemctl enable nginx.service`

Lägg till firewalld regler om det behövs.

`firewall-cmd --permanent --zone=public --add-service=http `
`firewall-cmd --permanent --zone=public --add-service=https`
`firewall-cmd --reload`
`  `

</div>
<div id="tab2" class="tab-pane fade">

Installera Nginx:

`apt-get update`
`apt-get -y install nginx`

Kolla så Nginx körs:

`systemctl status nginx`
`  `

</div>
</div>

Kommandon
=========

-   Testa om det är en giltig konfiguration innan man startar om
    nginx:`nginx -t`
-   Ladda om confen utan att starta om nginx:`nginx -s reload`

Konfiguration
=============

Reverse Proxy
-------------

Nginx fungerar utmärkt som en reverse proxy för webbtrafik.

Exempel

` server {`
` listen 80;`
` server_name sub.domän.se;`
` location / {`
` proxy_pass `[`http://10.0.0.10:3000`](http://10.0.0.10:3000)`;`
` include /etc/nginx/proxy_params;`
`    }`
` }`

Rewrite & Redirect
------------------

### Tabort www

Om man inte vill ha www i sin URL så skapar man 2 servrar som man sedan
kör en redirect till.

``` bash
server {
    listen 80;
    server_name domän.se;
}
 server {
    listen 80;
    server_name www.domän.se;
    return 301 $scheme://domän.se$request_uri;
 }
```

### Redirect HTTP till HTTPS

Här behöver man också skapa 2st server delar.

``` bash
server {
  listen      80;
  server_name domän.se;
  return 301  https://domän.se$request_uri;
}
server {
  listen      443 ssl;

  # let the browsers know that we only accept HTTPS
  add_header Strict-Transport-Security max-age=2592000;
}
```

### Redirect HTTP till HTTPS, ej standardport

Nginx har en egen HTTP-statuskod för detta.

` server {`
` listen      1234 ssl;`
` server_name sub.domän.se;`
` ...`
` error_page  497 `[`https://$host:1234$request_uri`](https://$host:1234$request_uri)`;`
` ...`
` }`

HTTPS
-----

Konfigurationsexempel med säkerhet i fokus.

[`https://syslink.pl/cipherlist/`](https://syslink.pl/cipherlist/)

` server {`
` listen 443 ssl;`
` server_name secure.domän.se;`
` add_header Strict-Transport-Security max-age=15768000;`
` add_header X-Frame-Options DENY;`
` add_header X-Content-Type-Options nosniff;`
` ssl_certificate         /path/to/cert.crt;`
` ssl_certificate_key     /path/to/key.pem;`
` ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;`
` ssl_ciphers 'ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:!aNULL:!eNULL:!EXPORT:!CAMELLIA:!DES:!MD5:!PSK:!DSS:!RC4';`
` ssl_prefer_server_ciphers on;`
` ssl_dhparam /path/to/dhparam.pem;`
` ...`
` }`

Generera DH-parametrar med tidtagning. Det tar lång tid!

`time openssl dhparam -out /path/to/dhparam.pem 4096`

### Nyckelsäkerhet

Av säkerhetsskäl bör endast root har rätt att läsa de privata nycklarna.
Nginx processer fungerar default enligt:

-   1 nginx master process körs som root
-   x nginx workers körs som www-data

Nginx master process läser SSL-nycklarna, inte worker-processerna.
Därför fungerar det utmärkt att köra följande.

`sudo chown root:root certificate.key`
`sudo chmod 400 certificate.key`

### SPDY

SPDY är ett protokoll utvecklat av Google för att göra
HTTPS-handskakning lite snabbare. Alla moderna webbläsare har stöd för
det.
Din nginx måste vara kompilerad med –with-http_spdy_module.

`nginx -V`
`sudo sed -i -r 's/listen 443 ssl/listen 443 ssl spdy/g' /etc/nginx/sites-available/dinSSLsite`
`sudo service nginx reload`

<http://SPDYCheck.org>

RTMP
----

Nginx rtmp modul fungerar utmärkt om man vill kunna streama något till 2
platser samtidigt tex till Twitch och Hitbox utan att behöva ha igång 2
instanser av tex OBS/Xsplit.

För att få in RTMP modulen så måste man compilera nginx från början.

`apt-get update && apt-get install build-essential libpcre3 libpcre3-dev libssl-dev`

Hämta hem senaste versionen av nginx och rtmp modulen.

`wget `[`http://nginx.org/download/nginx-1.7.9.tar.gz`](http://nginx.org/download/nginx-1.7.9.tar.gz)
`wget `[`https://github.com/arut/nginx-rtmp-module/archive/master.zip`](https://github.com/arut/nginx-rtmp-module/archive/master.zip)

Packa upp filerna

`tar -zxvf nginx-1.7.9.tar.gz`
`unzip master.zip`
`cd nginx-1.7.9`

Lägg sedan till rtmp modulen i nginx.

`./configure --add-module=../nginx-rtmp-module-master`
`make`
`make install`

Om du inte fått några error så är nginx med rtmp modulen installerade.

Ändra och lägg till följande rader i din conf fil.
`/usr/local/nginx/conf/nginx.conf`

`rtmp {`
`   server {`
`       listen 1935;`
`       chunk_size 8192;`

`       application stream {`
`           live on;`
`           meta copy;`
`           push `[`rtmp://live-ams.twitch.tv/app/live_XYZ_ZXY`](rtmp://live-ams.twitch.tv/app/live_XYZ_ZXY)`;`
`           push `[`rtmp://live.hitbox.tv/push/username?key=XYZ`](rtmp://live.hitbox.tv/push/username?key=XYZ)`;`
`       }`
`   }`
`}`

För att starta nginx server skriv

`/usr/local/nginx/sbin/nginx`

För att stoppa nginx servern.

`/usr/local/nginx/sbin/nginx -s`

Ställ in din klient att streama mot <rtmp://><ip>/stream

PHP
---

För att kunna visa PHP sidor behövs PHP-FastCGI.

`apt-get install php5-cli php5-cgi spawn-fcgi php-pear`
`wget -O /usr/bin/php-fastcgi `[`http://www.linode.com/docs/assets/1548-php-fastcgi-deb.sh`](http://www.linode.com/docs/assets/1548-php-fastcgi-deb.sh)` && chmod +x /usr/bin/php-fastcgi`
`wget -O /etc/init.d/php-fastcgi `[`http://www.linode.com/docs/assets/1549-init-php-fastcgi-deb.sh`](http://www.linode.com/docs/assets/1549-init-php-fastcgi-deb.sh)` && chmod +x /etc/init.d/php-fastcgi && update-rc.d php-fastcgi defaults`
`/etc/init.d/php-fastcgi start`

Lägg till följande i din conf fil.

``` apache
    location ~* \.php$ {
        include fastcgi_params;
        try_files $uri =404;
        fastcgi_pass 127.0.0.1:9000;
        fastcgi_param SCRIPT_FILENAME $request_filename;
    }
```

skapa en php info fil i din rooten på webbservern för att testa din php
conf.

``` php
echo "<?php phpinfo(); ?>" > info.php
```

Naxsi
-----

Third party Nginx-modul, motsvarighet till
[ModSecurity](/ModSecurity "wikilink"). Går att köra i learning mode.

`sudo apt-get install nginx-naxsi`

Tips n Trix
===========

Fail2ban
--------

`sudo nano /etc/fail2ban/jail.conf`
`[nginx-http-auth] `
`enabled = true`

Enable directory listing
------------------------

Om du vill att nginx ska lista filerna i en mapp som inte har någon
index fil. Lägg följande under `location` som du vill lista.

`autoindex on;`

Rate Limit
----------

Man kan begränsa bandbredden för en viss IP eller subnät.

``` bash
 location / {
  if ( $remote_addr ~* 192.100.20.0/24 ) {
    limit_rate 5k;
  }
 }
```