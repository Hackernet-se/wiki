---
title: RatticDB
permalink: /RatticDB/
---

[RatticDB](http://rattic.org/) är en open-source password management
databas gjord för att flera ska kunna läsa och skriva samtidigt. Man
hostar den själv och når den via en hemsida.

Förberedelse
------------

Om man vill och det är rekomenderat är följande,

-   Att man använder HTTPS för att logga in på Rattic.
-   Filsystemet där din databas lagras bör vara krypterat.
-   Access loggarna bör vara skyddade.
-   Program som [OSSEC](/OSSEC "wikilink") är bra att använda.

En fungerande [LAMP](/LAMP "wikilink") och en databas skapad åt rattic
samt följande paket.

-   python
-   pip
-   GCC
-   mysql-devel
-   openssl-devel
-   openldap-devel
-   python-devel
-   libxml2-devel
-   libxslt-devel
-   gettext

Installation
------------

Det är rekomenderat att installera under `/opt/apps`.

`mkdir /opt/apps && cd /opt/apps`
`git clone `[`https://github.com/tildaslash/RatticWeb`](https://github.com/tildaslash/RatticWeb)
`cd RatticWeb`
`pip install -r requirements-mysql.txt`
`mkdir static`
`cd conf && cp defaults.cfg local.cfg`

Ändra följande rader,

`[ratticweb]`
`debug = False`
`secretkey = [enter a string of random secret data]`
`hostname = rattic `

`[filepaths]`
`static = /opt/apps/RatticWeb/static`

`[database]`
`engine = django.db.backends.mysql`
`name = rattic`
`user = root`
`password =`
`host =`
`port =`

Skapa sedan tabeller i databasen och fyll static mappen.

`cd /opt/apps/RatticWeb/`
`./manage.py syncdb --noinput`
`./manage.py migrate --all`
`./manage.py collectstatic -c --noinput`
`./manage.py demosetup`

Logga in med användaren `admin` med password `rattic`.

### Nginx konfiguration

Börja med att installera supervisord och gunicorn.

`pip install gunicorn`
`easy_install supervisor`
`wget `[`https://gist.githubusercontent.com/howthebodyworks/176149/raw/88d0d68c4af22a7474ad1d011659ea2d27e35b8d/supervisord.sh`](https://gist.githubusercontent.com/howthebodyworks/176149/raw/88d0d68c4af22a7474ad1d011659ea2d27e35b8d/supervisord.sh)` -O /etc/init.d/supervisord`
`update-rc.d supervisord defaults`
`mkdir /opt/apps/log`

Lägg till följande rader längst ner i `/etc/superviseord.conf`.

`[program:RatticDB]`
`command = /opt/apps/gunicorn_start.sh`
`user = rattic`
`stdout_logfile = /opt/apps/log/gunicorn_supervisor.log`
`redirect_stderr = true`

Skapa en fil som heter `gunicorn_start.sh` under /opt/apps och lägg in
följande.

` #!/bin/bash`
` `
`NAME="RatticDB"                                   # Name of the application`
`DJANGODIR=/opt/apps/RatticWeb/                     # ratticdb project directory`
`USER=rattic                                       # the user to run as`
`GROUP=rattic                                      # the group to run as`
`NUM_WORKERS=3                             # how many worker processes should Gunicorn spawn (2xcores+1)`
`DJANGO_SETTINGS_MODULE=ratticweb.settings         # which settings file should Django use`
`DJANGO_WSGI_MODULE=ratticweb.wsgi                 # WSGI module name`
` `
`` echo "Starting $NAME as `whoami`" ``
` `
`# Activate the virtual environment`
`cd $DJANGODIR`
`export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE`
`export PYTHONPATH=$DJANGODIR:$PYTHONPATH`
` `
`# Start your Django Unicorn`
`# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)`
`exec /usr/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \`
`  --name $NAME \`
`  --workers $NUM_WORKERS \`
`  --user=$USER --group=$GROUP \`
`  --log-level=debug \`
`  --bind=127.0.0.1:8000`

Nginx conf fil.

`server {`
`    listen       443 ssl;`
`    server_name  rattic.hackernet.se;`
`    `
`client_max_body_size 4G;`

`    location /static/ {`
`       alias /opt/apps/RatticWeb/static/;`
`    }`

`    location /media/ {`
`        alias   /opt/apps/RatticWeb/media/;`
`    }`

`    add_header Strict-Transport-Security max-age=15768000;`
`    add_header X-Frame-Options DENY;`
`    add_header X-Content-Type-Options nosniff;`
`    ssl_certificate         /etc/nginx/cert.crt;`
`    ssl_certificate_key     /etc/nginx/cert/cert.pem;`
`    ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;`
`    ssl_ciphers 'ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:!aNULL:!eNULL:!EXPORT:!CAMELLIA:!DES:!MD5:!PSK:!DSS:!RC4';`
`    ssl_prefer_server_ciphers on;`
`    ssl_dhparam /etc/nginx/cert/dhparam.pem;`
`    ssl_session_cache shared:SSL:1m;`
`    ssl_session_timeout  5m;`


`    location / {`
`        proxy_pass `[`http://127.0.0.1:8000`](http://127.0.0.1:8000)`;`
`    }`
`}`
`  server {`
` listen      80;`
` server_name rattic.hackernet.se;`
` `
` # 301 = permanent redirect, 302 = temporary redirect`
` return 301  `[`https://rattic.hackernet.se$request_uri`](https://rattic.hackernet.se$request_uri)`;`
` }`

Starta sedan Rattic med hjälp av supervisord.

`service supervisord start`

### LDAP

Lägg in följande i conf filen. Mer dokumentation finns på [Rattic
Wiki](https://github.com/tildaslash/RatticWeb/wiki/LDAP).

`[ldap]`
`# LDAP server details`
`uri = `[`ldap://localhost`](ldap://localhost)

`# User parameters`
`userbase = ou=users,dc=example,dc=com`
`userfilter = (uid=%(user)s)`

`# Set up the basic group parameters.`
`groupbase = ou=django,ou=groups,dc=example,dc=com`
`groupfilter = (objectClass=groupOfNames)`
`grouptype = GroupOfNamesType`

`# How do I find staff`
`staff = cn=staff,ou=groups,dc=example,dc=com`

[Category:Guider](/Category:Guider "wikilink")
[Category:Sparco](/Category:Sparco "wikilink")