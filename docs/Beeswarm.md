---
title: Beeswarm
permalink: /Beeswarm/
---

Beeswarm är ett IDS-projekt som ger enkel konfiguration, driftsättning
och hantering av honeypots. Med honeypots kan man upptäcka om man har
[Hackers](http://www.imdb.com/title/tt0113243/) i sitt nätverk.
Projektets hemsida: <http://www.beeswarm-ids.org/>

[Image:Beeswarm_overview.png](/Image:Beeswarm_overview.png "wikilink")

-   **Server:** Managerar och tar in rapporter från honeypots och
    klienter.
-   **Honeypot:** Lyssnar på olika tjänster t.ex. SSH, SMTP, FTP, HTTP
-   **Klient:** Försöker logga in på honeypotsen med fake-credentials,
    om någon annan försöker logga in med samma credentials vet man att
    trafik har avlyssnats.

Installation
------------

*Ubuntu*

`sudo apt-get install libffi-dev build-essential python-dev python-pip libssl-dev libxml2-dev libxslt1-dev ntp`
`sudo pip install pydes --allow-external pydes --allow-unverified pydes`
`sudo pip install beeswarm`

*OBS om följande händer: "The required version of setuptools (\>=6.0.1)
is not available, and can't be installed while this script is running.
Please install a more recent version first, using 'easy_install -U
setuptools'"*
Kör:

`sudo easy_install -U setuptools`
`sudo pip install beeswarm`

**På server:**

`mkdir server_workdir && cd server_workdir`
`beeswarm --server --customize`

Svara på frågorna samt kopiera lösenordet, webgui next.

[`https://10.1.2.3:5000`](https://10.1.2.3:5000)
`+Drone -> 2 minuter på dig att registrera drone`

**På honeypot:**

`sudo su -`
`mkdir /root/drone_workdir && cd /root/drone_workdir`
`beeswarm --config `[`https://10.1.2.3:5000/ws/drone/add/f12345`](https://10.1.2.3:5000/ws/drone/add/f12345)

På honeypoten måste beeswarm köras som root för att kunna binda
portar.
Resten görs i webguit

Autostart
---------

`sudo touch /root/beeswarm.sh && sudo chmod 700 /root/beeswarm.sh && sudo nano /root/beeswarm.sh`

**Server**

`#!/bin/sh`
`su - user1 -c "/usr/local/bin/beeswarm --server --workdir /home/user1/server_workdir"`

**Honeypot**

`#!/bin/sh`
`/usr/local/bin/beeswarm --workdir /root/drone_workdir`

**Klient**

`#!/bin/sh`
`su - user1 -c "/usr/local/bin/beeswarm --workdir /home/user1/drone_workdir"`

Lägg in följande i rc.local

`/root/beeswarm.sh > /dev/null 2>&1 &`

Uppgradering
------------

`sudo pip install --upgrade beeswarm --allow-external pydes --allow-unverified pydes`

NTP
---

Tidssynk är mycket viktigt och om klockorna går fel slutar det att
funka. Detta kan hända till och med när NTP är installerat, om man kör
default-inställningar. Så trimma dem.

`sudo nano /etc/ntp.conf `
`server 0.ubuntu.pool.ntp.org minpoll 6 maxpoll 6`

*6 betyder var 64 sekund*

[Category:Guider](/Category:Guider "wikilink")