---
title: Hastebin
permalink: /Hastebin/
---

Hastebin används för att tex dela kod eller nån log fil med någon. Det
funkar på samma sätt som Pastebin. Hastebin är väldigt enkelt att
använda och är stilrent. En fördel med hastebin är att dom har klienter
som man kan köra i sitt skal så man kan tex köra cat på en fil och
output är hastebin.

[Hackernets egna hastebin server](http://paste.hackernet.se/)

Installation
------------

Clona hastebins git repo,

`git clone `[`https://github.com/seejohnrun/haste-server`](https://github.com/seejohnrun/haste-server)

Kör sedan. Vill du ändra nån inställning i `config.js` gör det före
detta steget.

`npm install`
`npm start`

Konfiguration
-------------

Det finns 3 olika sätt att lagra sina paste på. Memcache, redis eller på
fil.

### Memcache

Förutsätter att du redan har memcache server installerat på samma eller
en annan server.

Du behöver också modulen för memcache.

`npm install memcache`

Under `storage` i `config.js` ändra till.

` "storage": {`
`   "type": "memcached",`
`   "host": "127.0.0.1",`
`   "port": 11211,`
`   "expire": 2592000`
` },`

expire säger hur många sekunder en paste ska finnas kvar sedan den
senast öppnades.

### Redis

Förutsätter också att du har en redis server och du behöver modulen för
redis.

`npm install redis`

Under `storage` i `config.js` ändra till.

` "storage": {`
`   "type": "redis",`
`   "host": "0.0.0.0",`
`   "port": 6379,`
`   "db": 2,`
`   "expire": 2592000`
` },`

### File

Under `storage` i `config.js` ändra till.

` "storage": {`
`   "type": "file",`
`   "path": "./data",`
`   "expire": 2592000`
` },`

När du är klar med `config.js` kör sedan.

`npm install`
`npm start`

Tjänsten går nu att nå på <http://><IP>:7777

Reverse proxy
-------------

Låt en reverse proxy dela ut tjänsten tex Apache.

`<VirtualHost *:80>`
`    ServerAdmin root@hackernet.se`
`    ServerName paste.hackernet.se`

`    <IfModule mod_proxy.c>`
`        ProxyVia On`
`        ProxyRequests Off`
`        ProxyPass / `[`http://127.0.0.1:7777/`](http://127.0.0.1:7777/)
`        ProxyPassReverse / `[`http://127.0.0.1:7777/`](http://127.0.0.1:7777/)
`        ProxyPreserveHost on`
`        <Proxy *>`
`            AllowOverride All`
`            Order allow,deny`
`            allow from all`
`        `</Proxy>
`    `</IfModule>

`        ErrorLog ${APACHE_LOG_DIR}/hastebin.log`

`        # Possible values include: debug, info, notice, warn, error, crit,`
`        # alert, emerg.`
`        LogLevel warn`

`        CustomLog ${APACHE_LOG_DIR}/access.log combined`


</VirtualHost>

Se till att modulerna `proxy` och `proxy_http` är igång.

Systemd service
---------------

Under `/etc/systemd/system` skapa filen `haste.service` med texten.
Anpassa `/opt/haste-server` efter vart du installerat det.

`[Service]`
`ExecStart=/usr/bin/node /opt/haste-server/server.js`
`Restart=always`
`StandardOutput=syslog`
`SyslogIdentifier=hastebin`
`User=root`
`WorkingDirectory=/opt/haste-server`

`[Install]`
`WantedBy=multi-user.target`

Kör sedan dessa 2 kommandona för att skapa en symlänk och starta
hastebin.

`systemctl enable /etc/systemd/system/haste.service`
`systemctl start haste.service`

Klient
------

Dom har flera klienter för linux och för windows.

### Lightweight client

Skriv denna raden i ditt skal för att klienten ska fungera.

`haste() { a=$(cat); curl -X POST -s -d "$a" `[`https://paste.hackernet.se/documents`](https://paste.hackernet.se/documents)` | awk -F '"' '{print "`[`https://paste.hackernet.se/"$4`](https://paste.hackernet.se/%22$4)`}'; }`

För att använda klienten skriv,

`cat testfil.txt | haste`

[Category:Guider](/Category:Guider "wikilink")