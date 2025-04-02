---
title: Logstash
permalink: /Logstash/
---

Logstash sparar alla loggar från olika system på ett centralt ställe och
hjälper dig att söka bland dom.

Installation
============

`wget -qO - `[`https://packages.elastic.co/GPG-KEY-elasticsearch`](https://packages.elastic.co/GPG-KEY-elasticsearch)` | sudo apt-key add -`
`echo "deb `[`https://packages.elastic.co/logstash/2.3/debian`](https://packages.elastic.co/logstash/2.3/debian)` stable main" | sudo tee -a /etc/apt/sources.list`
`sudo apt-get update && sudo apt-get -y install logstash`

Konfiguration
=============

**Java**
Ska logstash lyssna på portar under 1000 (t.ex. syslog 514) måste java
tillåtas att binda dessa portar.

`sudo setcap cap_net_bind_service=+epi /usr/lib/jvm/java-8-oracle/jre/bin/java`

Syslog
------

(RFC 3164)

``` bash
sudo dd of=/etc/logstash/conf.d/10-syslog.conf << EOF
input {
  tcp {
    port => 514
    type => syslog
  }
  udp {
    port => 514
    type => syslog
  }
}

filter {
  if [type] == "syslog" {
    grok {
      match => { "message" => "%{SYSLOGTIMESTAMP:syslog_timestamp} %{SYSLOGHOST:syslog_hostname} %{DATA:syslog_program}(?:\[%{POSINT:syslog_pid}\])$
      add_field => [ "received_at", "%{@timestamp}" ]
      add_field => [ "received_from", "%{host}" ]
    }
    syslog_pri { }
    date {
      match => [ "syslog_timestamp", "MMM  d HH:mm:ss", "MMM dd HH:mm:ss" ]
    }
  }
}

output {
  elasticsearch { host => localhost }
  stdout { codec => rubydebug }
}
EOF
```

SSL
---

Logstash forwarder (klienter) använder certifikat för autentisering och
SSL för kommunikation med Logstash server. Skapa cert på servern.

`sudo mkdir -p /etc/pki/tls/certs && sudo mkdir /etc/pki/tls/private`
`sudo nano /etc/ssl/openssl.cnf`

Find the \[ v3_ca \] section and add:

`subjectAltName = IP: 10.0.0.10`
`cd /etc/pki/tls`
`sudo openssl req -config /etc/ssl/openssl.cnf -x509 -days 3650 -batch -nodes -newkey rsa:2048 -keyout private/logstash-forwarder.key -out certs/logstash-forwarder.crt`

Forwarder
---------

[Category:Guider](/Category:Guider "wikilink")