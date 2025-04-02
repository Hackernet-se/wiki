---
title: Rancid
permalink: /Rancid/
---

Really Awesome New Cisco confIg Differ är ett verktyg för
versionshantering av konfigurationsfiler på nätverksutrustning.
Programvaran tillhandahålls av [Shrubbery
Networks](http://www.shrubbery.net/rancid/).

Rancid kan användas för följande:

-   Backup och lagring av konfigurationsfiler
-   Jämförelse av konfiguration
-   Versionsarkivering av konfiguration

Rancid kan hjälpa till i arbetet med följande frågor:

-   Hur vet du när en förändring sker?
-   Vad gör du när en förändring sker?
-   Kan du korrelera nätverkshändelser med ändringar?
-   Upprätthåller du en "basline" eller sätter en
    konfigurationsstandard?

Installation
------------

`sudo apt-get -y install rancid subversion postfix`

Rancid-användare skapas under installationen.

`apt-cache show rancid | grep Version`

Konfiguration
-------------

Filer

-   /etc/rancid/ \#Config file
-   /var/lib/rancid/ \#Most other files
-   /var/lib/rancid/\[gruppnamn\]/router.db \#Devices list

Byt från cvs till subversion samt skapa grupper för dina enheter. Det
går även använda [Git](/Git "wikilink").

`sudo sed -i.bak 's/RCSSYS=cvs; export RCSSYS/RCSSYS=svn; export RCSSYS/g' /etc/rancid/rancid.conf`
`sudo sed -i 's#CVSROOT=$BASEDIR/CVS; export CVSROOT#CVSROOT=$BASEDIR/svn; export CVSROOT#g' /etc/rancid/rancid.conf`
`echo 'LIST_OF_GROUPS="routers switches fws"' | sudo tee -a /etc/rancid/rancid.conf`

Slipp att det räknas som en ändring varje gång en loggfil ändrar
storlek. Modifiera */var/lib/rancid/bin/rancid* (kan behövas kommenteras
ut fler beroende på enhet, man får testa sig fram)

`#{‘dir /all bootflash:’         => ‘DirSlotN’},`
`#{'dir /all disk0:'             => 'DirSlotN'},`

Don't strip passwords from backed up configurations

`sudo sed -i 's/FILTER_PWDS=YES/FILTER_PWDS=NO/g' /etc/rancid/rancid.conf`

Fixa rättigheter för rancid user

`sudo chown -R rancid:rancid /var/lib/rancid`
`sudo su -s /bin/bash rancid`

User rancid

`cd && nano .cloginrc`
`#add autoenable * 0 (tex Cisco ASA kräver manuell enable)`
`add cyphertype * aes256-ctr,aes256-ctr,aes128-cbc,aes256-cbc`
`add method * ssh`
`add user * cisco`
`add password * {cisco} {cisco}`

`chmod 600 .cloginrc`

**Testa inlogg**

`/var/lib/rancid/bin/clogin 172.20.0.100`

### SVN

Lagra i SVN repo. Går även att köra med cvs. Kör som user rancid.

`/var/lib/rancid/bin/rancid-cvs`

Lista filer i SVN:

`svn ls `[`file:///var/lib/rancid/svn/`](file:///var/lib/rancid/svn/)

**Add devices**
nano /var/lib/rancid/switches/router.db

`192.168.0.100:cisco:up`
`sw01.local:cisco:up`
`10.0.0.10:hp:up`

**Removal**
För devices raderas entryt ur router.db.
För grupper görs det genom SVN (raderar alla configs under gruppen
också!):

`svn rm `[`file:///var/lib/rancid/svn/switches`](file:///var/lib/rancid/svn/switches)` --message "Not in use"`

Kör igång

`/usr/lib/rancid/bin/rancid-run`

### Schemaläggning

`su - rancid`
`crontab -e`
`0 * * * * /usr/lib/rancid/bin/rancid-run`
`0 1 * * * find /opt/rancid/var/logs -type f -mtime +30 -exec rm {} \; # Slang gamla loggar`

Web GUI
-------

**CVSWeb**
Endast om man valde cvs.

`sudo apt-get -y install cvsweb`

### WebSVN

`sudo apt-get -y install websvn`

path: /var/lib/rancid/svn
repo: /var/lib/rancid/svn

`sudo ln -s /etc/websvn/apache.conf /etc/apache2/conf-available/websvn.conf`
`sudo a2enconf websvn.conf`
`sudo service apache2 reload`
`sudo chgrp -R www-data /var/lib/rancid/svn`
`sudo chmod g+w -R /var/lib/rancid/svn`

<http://172.20.0.10/websvn>

**Auth**
HTTP authentication för /websvn

`sudo apt-get -y install apache2-utils`
`sudo htpasswd -c /opt/websvnpassword admin`

`sudo nano /etc/websvn/apache.conf`
`AuthType Basic`
`AuthName "Restricted Access"`
`AuthBasicProvider file`
`AuthUserFile /opt/websvnpassword`
`Require user admin`

`sudo service apache2 reload`

**Others**
"ln: failed to create symbolic link ‘/etc/apache2/conf.d/websvn’: No
such file or directory"
workaround:

`sudo mkdir /etc/apache2/conf.d`

Mailnotifiering
---------------

*Postfix*

`sudo nano /etc/aliases`
`rancid-routers:     sysadm`
`rancid-admin-routers:   sysadm`
`sudo newaliases`

Slacknotifiering
----------------

Eftersom Slack har incoming webhook integration kan man skicka
resultatet från backupkörning till en slackkanal.

``` bash
#!/bin/sh

# This script is used to send a status report for the rancid backups to Slack channel.
# It is supposed to be executed by the cron service for the rancid user after rancid-run has completed.

# Finding errors in the latest log files.
for dir in $(find /var/log/rancid -mmin -60 -type f -print)
do
    if [ ! -z "$(cat $dir | egrep -w 'clogin|error')" ]; then
        FAILEDDEVICES="$FAILEDDEVICES$(cat $dir | egrep -w 'clogin|error' | uniq)  -----  "
    fi
done

# Used for getting the log file error entries into a json format.
ERRORMESSAGE='{"text": "Rancid report: There seems to be some issues :(", "attachments":[{"text": "'$FAILEDDEVICES'"}]}'

# Send error messages to slack
[ ! -z "$FAILEDDEVICES" ] && curl -X POST --data-binary "${ERRORMESSAGE}" -H "Content-Type: application/json" https://hooks.slack.com/services/XXX/XXX/XXXXX

# If no errors was found a static message is posted to the channel
[ -z "$FAILEDDEVICES" ] && curl -X POST --data '{"text":"Rancid report: No failed backups last rancid run :)"}' -H "Content-Type: application/json" https://hooks.slack.com/services/XXX/XXX/XXXXX
```

[Category:Guider](/Category:Guider "wikilink")