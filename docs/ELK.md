---
title: ELK
permalink: /ELK/
---

Elasticsearch, Logstash, och Kibana 4 för centraliserad loggning. Det är
användbart för att försöker identifiera problem med servrar och program,
eftersom det tillåter att söka igenom alla loggar på ett och samma
ställe.

**Elasticsearch** lagrar alla loggar
**Logstash** är ett open source-verktyg för att samla in loggar.
Logstash kan samla loggar av alla slag.
**Kibana 4** är ett webbgränssnitt som kan användas för att söka och
visa loggarna som Logstash har indexerat.

Installation
------------

*Ubuntu 14.04*
**Java**

`sudo apt-get -y install software-properties-common`
`sudo add-apt-repository -y ppa:webupd8team/java`
`sudo apt-get update && sudo apt-get -y install oracle-java8-installer`

**Elasticsearch**

`wget -O - `[`http://packages.elasticsearch.org/GPG-KEY-elasticsearch`](http://packages.elasticsearch.org/GPG-KEY-elasticsearch)` | sudo apt-key add -`
`echo "deb `[`http://packages.elastic.co/elasticsearch/2.0/debian`](http://packages.elastic.co/elasticsearch/2.0/debian)` stable main" | sudo tee -a /etc/apt/sources.list.d/elasticsearch-2.0.list`
`sudo apt-get update && sudo apt-get -y install elasticsearch`
`sudo sed -i 's/#network.host: 192.168.0.1/network.host: localhost/g' /etc/elasticsearch/elasticsearch.yml`

*Init.d*

`sudo service elasticsearch restart`
`sudo update-rc.d elasticsearch defaults 95 10`

**Kibana**

`echo 'deb `[`http://packages.elastic.co/kibana/4.1/debian`](http://packages.elastic.co/kibana/4.1/debian)` stable main' | sudo tee /etc/apt/sources.list.d/kibana.list`
`sudo apt-get update && sudo apt-get -y install kibana`
`sudo sed -i 's/host: "0.0.0.0"/host: "localhost"/g' /opt/kibana/config/kibana.yml`
`sudo update-rc.d kibana defaults 96 9`
`sudo service kibana start`

**Nginx**

`sudo apt-get -y install nginx apache2-utils`
`sudo htpasswd -c /etc/nginx/htpasswd.users kibanaadmin`
`sudo nano /etc/nginx/sites-available/default`

`server {`
`   listen 80;`
`   server_name kibana.local;`

`   auth_basic "Restricted Access";`
`   auth_basic_user_file /etc/nginx/htpasswd.users;`

`   location / {`
`       proxy_pass `[`http://localhost:5601`](http://localhost:5601)`;`
`       proxy_http_version 1.1;`
`       proxy_set_header Upgrade $http_upgrade;`
`       proxy_set_header Connection 'upgrade';`
`       proxy_set_header Host $host;`
`       proxy_cache_bypass $http_upgrade;        `
`   }`
`}`
`sudo service nginx restart`

<http://IP>

**Logstash**
Se [Logstash](/Logstash "wikilink")

[Category:Guider](/Category:Guider "wikilink")