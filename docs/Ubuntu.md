---
title: Ubuntu
permalink: /Ubuntu/
---

Ubuntu är en dist som bygger på Debian men har egna repos, även om en
del paket synkas från Debians repos.

First 5 minutes
===============

Gör följande för att öka säkerheten. Switch user till root:

`sed -i -r 's/PermitRootLogin yes/PermitRootLogin no/g' /etc/ssh/sshd_config`
`systemctl restart ssh`

### Hostname

`echo "hostname" > /etc/hostname`
`hostname -F /etc/hostname`

### Tidszon

`dpkg-reconfigure tzdata`

### Ändra namn på NIC

Ändra i filen `/etc/udev/rules.d/70-persistent-net.rules`

Finns inte filen kan man skapa den. Man måste köra alla 3 kommandon för
varje interface man vill lägga till i
`/etc/udev/rules.d/70-persistent-net.rules`

`export INTERFACE=eth0`
`export MATCHADDR=$(ip addr show $INTERFACE | grep ether | awk '{print $2}')`
`/lib/udev/write_net_rules`

Pakethanterare
==============

Både Debian och Ubuntu tillhandahåller flera pakethanterare.

### Apt

Se [Apt](/Apt "wikilink")

### dpkg

Debian packaging tool
**Lista på installerade program**

`dpkg --get-selections`
`dpkg -l`

Tips o trix
-----------

**Automatiska uppdateringar**

`sudo apt-get -y install unattended-upgrades`
`sudo dpkg-reconfigure -plow unattended-upgrades`

**Minimal Ubuntu Server**
Vill man reducera mängden CPU och RAM som behövs för ens vm kan man
under installationen trycka f4 och välja att installera en minimal
variant av Ubuntu Server.

**Mer funktionalitet**
Är man trött på att det saknas funktioner på sin maskin kan man lägga
till alla paketen med följande kommando:

`sudo aptitude install '~T'`

Diverse
-------

Network IDS - psad

`sudo apt-get install -y psad && sudo psad --sig-update`
`sudo service psad restart && sudo service psad status`

Host IDS - Aide

`sudo apt-get install -y aide && sudo aideinit`
`sudo aide -u`

Log Reporting

`sudo apt-get install -y logwatch`
`sudo echo "/usr/sbin/logwatch --output mail --mailto ${email_address} --detail high" >> /etc/cron.daily/00logwatch`

[Category:Distar](/Category:Distar "wikilink")