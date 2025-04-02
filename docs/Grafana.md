---
title: Grafana
permalink: /Grafana/
---

Grafana är webbaserat grafverktyg. Grafana behöver hämta datan som ska
grafas ifrån någonstans. Detta kan göras från bl.a. influxDB,
Elasticsearch, [Graphite](/Graphite "wikilink") eller
[Prometheus](/Prometheus "wikilink").

Installation
------------

`echo "deb `[`https://packagecloud.io/grafana/stable/debian/`](https://packagecloud.io/grafana/stable/debian/)` wheezy main" | sudo tee -a /etc/apt/sources.list`

**Wheezy** (och andra debianversioner)

`sudo apt-get -y install curl`
`curl `[`https://packagecloud.io/gpg.key`](https://packagecloud.io/gpg.key)` | sudo apt-key add -`
`sudo apt-get update`
`sudo apt-get -y install grafana`

**Ubuntu**

`curl `[`https://packages.grafana.com/gpg.key`](https://packages.grafana.com/gpg.key)` | sudo apt-key add -`
`sudo add-apt-repository "deb `[`https://packages.grafana.com/oss/deb`](https://packages.grafana.com/oss/deb)` stable main"`
`sudo apt-get update && sudo apt-get install grafana`

### Alternativ installation

Finns officiell docker-container

`docker run -i -p 3000:3000 grafana/grafana`

Konfiguration
-------------

Detta startar tjänsten som user grafana, som skapades under
installation. Default HTTP-port är 3000 och default user är admin med pw
admin.

**Init.d**

`sudo service grafana-server start`
`sudo update-rc.d grafana-server defaults 95 10`

**Systemd**

`systemctl daemon-reload`
`systemctl start grafana-server`
`systemctl status grafana-server`
`sudo systemctl enable grafana-server.service`

**grafana.ini** I grafana.ini finns systeminställningarna. De går också
att se på <http://IP:3000/admin/settings>

`sudo nano /etc/grafana/grafana.ini`

Förslagsvis byts lösenordet för admin, det kan även göras i webguit.

[Category:Guider](/Category:Guider "wikilink")