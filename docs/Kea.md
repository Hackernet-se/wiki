---
title: Kea
permalink: /Kea/
---

Kea är den nya DHCPv4/DHCPv6-servern från ISC och är en ersättare för
[ISC DHCP](/ISC_DHCP "wikilink"). Målet är att skapa en dhcp server med
hög performance och utbyggbar med extensions för enterprises eller
service providers.

**Features**

-   Fullt fungerande DHCPv4, DHCPv6 och Dynamic DNS server.
-   OpenSSL support.
-   Leases finns sparat i CSV fil, MySQL eller Postgres.
-   On-Line configuration.
-   Statistics
-   API

Installation
------------

`apt-get install build-essential libssl-dev libboost-dev libboost-system-dev make liblog4cplus-dev`
`wget `[`http://ftp.isc.org/isc/kea/1.0.0/kea-1.0.0.tar.gz`](http://ftp.isc.org/isc/kea/1.0.0/kea-1.0.0.tar.gz)` && tar -xvf kea-1.0.0.tar.gz`
`cd kea-1.0.0`
`./configure --prefix=/`
`make`
`make install`

**Ubuntu**

`sudo apt-get install kea-dhcp4-server`

**Fedora**

`dnf install kea`

Konfiguration
-------------

Görs i filen `/etc/kea/kea.conf`. En lista på DHCP options finns bland
kea's egna
[dokumentation](http://kea.isc.org/docs/kea-guide.html#dhcp4-std-options-list).

`# Kea DHCP conf by Hackernet.se`

`{`
`# DHCPv4 configuration starts in this line`
`"Dhcp4": {`

`# Global values`
`    "valid-lifetime": 4000,`
`    "renew-timer": 1000,`
`    "rebind-timer": 2000,`

`# Next we setup the interfaces to be used by the server.`
`    "interfaces-config": {`
`        "interfaces": [ "eth0" ]`
`    },`

`# And we specify the type of lease database`
`    "lease-database": {`
`        "type": "memfile",`
`        "persist": true,`
`        "name": "/var/kea/dhcp4.leases"`
`    },`

`# Global options`
`    "option-data": [`
`        {`
`        "name": "domain-name-servers",`
`        "data": "192.168.1.10, 10.240.100.100"`
`        },`
`        {`
`        "name": "tftp-server-name",`
`        "data": "192.168.1.200"`
`        },`
`        {`
`        "code": 67,`
`        "data": "pxelinux.0"`
`        },`
`    ],`

`#Some clients use siaddr field in the DHCPv4 packet, therefore use following command.`
`"next-server": "192.168.1.200",`


`# List subnets where we will be leasing addresses.`
`    "subnet4": [`
`        {`
`        "subnet": "10.240.100.0/24",`
`        "pools": [ { "pool": "10.240.100.20 - 10.240.100.100" } ],`
`        "option-data": [`
`        {`
`        "name": "routers",`
`        "data": "10.240.100.1"`
`        },`
`        {`
`        "code": 15,`
`        "data": "hackernet.se"`
`        },`
`      ]`
`    }`
`  ]`


`# DHCPv4 configuration ends with this line`
`},`

`    "Logging": {`
`       "loggers": [`
`        {`
`        "name": "kea-dhcp4",`
`        "output_options": [`
`          {`
`          "output": "/var/log/kea4.log",`
`          "maxsize": 20480`
`          }`
`        ],`
`        "severity": "INFO",`
`        },`
`      ]`
`    }`

`}`

Verify

`systemctl status kea-dhcp4-server.service`
`cat /var/kea/dhcp4.leases`

[Category:Guider](/Category:Guider "wikilink")