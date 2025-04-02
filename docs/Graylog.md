---
title: Graylog
permalink: /Graylog/
---

Graylog är en syslogserver för att man ska kunna analysera syslog, göra
sökningar och se trender på ett ställe. Det är open source och är
baserat på Elasticsearch, Java och MongoDB. Autentisering kan kopplas
till AD eller [LDAP](/OpenLDAP "wikilink").

Dokumentation: <http://docs.graylog.org/en/2.0/>

Installation
============

Det snabbaste sättet att komma igång är att ladda ner färdig appliance
och köra på hypervisor. <https://www.graylog.org/download>

Installera själv, *Ubuntu*
MongoDB

``` bash
sudo apt-get update && sudo apt-get -y upgrade && sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10
echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
sudo apt-get update && sudo apt-get -y install mongodb-org
```

Elasticsearch

``` bash
sudo apt-get install software-properties-common curl && sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update && sudo apt-get -y install oracle-java8-installer
wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb http://packages.elastic.co/elasticsearch/1.7/debian stable main" | sudo tee -a /etc/apt/sources.list.d/elasticsearch-1.7.x.list
sudo apt-get update && sudo apt-get -y install elasticsearch
sudo sed -i -e 's\#cluster.name: elasticsearch\cluster.name: graylog-prod\' /etc/elasticsearch/elasticsearch.yml
sudo sed -i -e 's\#network.host: 192.168.0.1\network.host: localhost\' /etc/elasticsearch/elasticsearch.yml
sudo sed -i -e 's\#discovery.zen.ping.multicast.enabled:\discovery.zen.ping.multicast.enabled:\' /etc/elasticsearch/elasticsearch.yml
sudo service elasticsearch restart && sudo update-rc.d elasticsearch defaults 95 10
curl -XGET 'http://localhost:9200/_cluster/health?pretty=true'
```

Graylog

``` bash
wget https://packages.graylog2.org/repo/packages/graylog-1.3-repository-ubuntu14.04_latest.deb
sudo dpkg -i graylog-1.3-repository-ubuntu14.04_latest.deb
sudo apt-get update && sudo apt-get -y install apt-transport-https graylog-server pwgen
SECRET=$(pwgen -s 96 1) && sudo -E sed -i -e 's/password_secret =.*/password_secret = '$SECRET'/' /etc/graylog/server/server.conf
```

Password for user admin, ändra CHANGETHIS

``` bash
PASSWORD=$(echo -n CHANGETHIS | shasum -a 256 | awk '{print $1}') && sudo -E sed -i -e 's/root_password_sha2 =.*/root_password_sha2 = '$PASSWORD'/' /etc/graylog/server/server.conf
```

Graylog-konf

``` bash
sudo sed -i -e 's\#root_timezone = UTC\root_timezone = Europe/Stockholm\' /etc/graylog/server/server.conf
sudo sed -i -e 's\#rest_transport_uri = http://192.168.1.1:12900/\rest_transport_uri = http://127.0.0.1:12900/\' /etc/graylog/server/server.conf
sudo sed -i -e 's/elasticsearch_shards = 4/elasticsearch_shards = 1/' /etc/graylog/server/server.conf
sudo sed -i -e 's/#elasticsearch_cluster_name = graylog2/elasticsearch_cluster_name = graylog-prod/' /etc/graylog/server/server.conf
sudo sed -i -e 's/#elasticsearch_discovery_zen_ping_multicast_enabled/elasticsearch_discovery_zen_ping_multicast_enabled/' /etc/graylog/server/server.conf
sudo sed -i -e 's/#elasticsearch_discovery_zen_ping_unicast_hosts/elasticsearch_discovery_zen_ping_unicast_hosts/' /etc/graylog/server/server.conf
sudo start graylog-server
```

Graylog-web

``` bash
sudo apt-get install graylog-web
SECRET=$(pwgen -s 96 1) && sudo -E sed -i -e 's/application\.secret=""/application\.secret="'$SECRET'"/' /etc/graylog/web/web.conf
sudo sed -i -e 's\graylog2-server.uris=""\graylog2-server.uris="http://127.0.0.1:12900/"\' /etc/graylog/web/web.conf
sudo start graylog-web
```

Konfiguration
=============

[`http://`](http://)<graylog_IP>`:9000/`

Vill man ha web ui med HTTPS kan man t.ex. lägga det bakom en [Nginx
proxy](/Nginx "wikilink").

### Input

System -\> Inputs -\> Syslog UDP -\> Launch:

-   Title: syslog
-   Port: 5514
-   Bind address: graylog_private_IP

Launch

### Port 514

Graylog får inte binda till port 514 eftersom det är en lågnummerport
utan man får lösa det med en redirect.

`iptables -t nat -A PREROUTING -i eth0 -p udp -m udp --dport 514 -j REDIRECT --to-ports 5514`

### Klienter

Ställ in så dina maskiner skickar sin syslog till <Graylog-IP> UDP 514.

[Category:Guider](/Category:Guider "wikilink")