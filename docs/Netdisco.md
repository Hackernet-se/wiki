---
title: Netdisco
permalink: /Netdisco/
---

[Category:Guider](/Category:Guider "wikilink") Netdisco hämtar
MAC-tabeller, ARP-tabeller, VLAN-databaser, LLDP/CDP-grannskap,
firmwareversioner, m.m från routrar och switchar med hjälp av SNMP. Man
schemalägger när data ska samlas in, dvs det är inte
realtidsövervakning.

Denna guide är minimalistiskt utformad, för kommandoförklaringar se
referensguide alternativt google. Referens:

[`https://metacpan.org/pod/App`](https://metacpan.org/pod/App)`::Netdisco`

Installation
------------

*Ubuntu 14.04.1 LTS Server x64*
Denna guide är till stor del hämtad från:
<http://blog.asiantuntijakaveri.fi/2014/08/netdisco2-on-ubuntu-1404.html>

`sudo su -`
`apt-get update && apt-get -y dist-upgrade && apt-get -y install open-vm-tools build-essential wget lftp mtr-tiny zip ntp fail2ban curl`
`echo "net.ipv6.conf.all.disable_ipv6=1" >>/etc/sysctl.conf`

### Databas

`apt-get -y install libdbd-pg-perl libsnmp-perl postgresql pgtune `
`mv /etc/postgresql/9.3/main/postgresql.conf /etc/postgresql/9.3/main/postgresql.conf.old`
`pgtune -i /etc/postgresql/9.3/main/postgresql.conf.old -o /etc/postgresql/9.3/main/postgresql.conf`

Switch to postgres user and create new SQL user

`su - postgres`
`createuser -DRSP netdisco`
`(Enter some DB password here)`
`createdb --owner netdisco netdisco`

Switch back to root

`exit`

### Netdisco

`adduser netdisco --shell /bin/bash --disabled-password --gecos netdisco && su - netdisco`
`curl -L `[`http://cpanmin.us/`](http://cpanmin.us/)` | perl - --notest --local-lib ~/perl5 App::Netdisco`

Konfiguration
-------------

`mkdir ~/bin && mkdir ~/environments && ln -s ~/perl5/bin/{localenv,netdisco-*} ~/bin/`
`~/bin/netdisco-daemon status`

Här är grunden för deploymenten, lägg till de SNMP-communitys som ska
användas. Schemaläggningen är i cron-format. I exemplet görs discoverall
10 över varje timme.
OBS Om detta görs i en virtuell maskin tas förslagsvis en snapshot här.

`cat <<'__EOF__'>~/environments/deployment.yml`
`database:`
` name: 'netdisco'`
` user: 'netdisco'`
` pass: '(PW som sattes tidigare)'`
`safe_password_store: true`
`snmp_auth:`
` - tag: 'default_1'`
`   community: 'puplic'`
`   read: true`
`   write: false`
` - tag: 'default_2'`
`   community: 'public'`
`   read: true`
`   write: false`
` - tag: 'v3example'`
`    user: netdisco`
`    auth:`
`      pass: netdiscokey`
`      proto: SHA`
`    priv:`
`      pass: netdiscokey2`
`      proto: AES`
`schedule:`
` discoverall:`
`    when: '10 * * * *'`
` macwalk:`
`    when: '35 * * * *'`
` arpwalk:`
`    when: '45 * * * *'`
` nbtwalk:`
`    when: '55 * * * *'`
` expire:`
`    when: '15 23 * * *'`
`dns:`
` max_outstanding: 50`
`workers:`
` tasks: 'AUTO * 5'`
`__EOF__`

`~/bin/netdisco-deploy`

Svara ja på allt och sätt credentials för web gui:t.

Skapa script för att starta Netdisco med listener port 5000

`cat <<'__EOF__'>~/run-netdisco.sh`
`#!/bin/bash`
`~/bin/netdisco-web start --port=5000`
`sleep 5`
`~/bin/netdisco-daemon start`
`__EOF__`
`chmod a+x ~/run-netdisco.sh`

`~/run-netdisco.sh`

Switch back to root

`exit`
`echo "( sudo su - netdisco -c '/home/netdisco/run-netdisco.sh' ) &" >/etc/rc.local`
`reboot`

### WEBGUI

Logga in på <http://%5BIP%5D:5000>

Börja med att mata in IP-adress på en switch eller router som ska
övervakas på förstasidan. Vänta och se hur mycket som upptäcks. Är allt
rätt konfigurerat kommer väldigt mycket att upptäckas.

### Enheter som ska övervakas

Logga in på diverse enhet som ska övervakas och lägg till community samt
IP för Netdiscomaskinen.

### Underhåll

upgrade Netdisco

`~/bin/localenv cpanm --notest App::Netdisco`

apply database schema updates

`~/bin/netdisco-deploy`

restart web service

`~/bin/netdisco-web restart`

restart job daemon

`~/bin/netdisco-daemon restart`