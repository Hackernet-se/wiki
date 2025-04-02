---
title: UniFi
permalink: /UniFi/
---

Ubiquiti UniFi Controller kan managera accesspunkter, switchar och
gateways av märket Ubiquiti. Det stöds på Ubuntu, Debian och Windows.

Installation
============

*Ubuntu*

`echo "deb `[`http://www.ubnt.com/downloads/unifi/debian`](http://www.ubnt.com/downloads/unifi/debian)` unifi4 ubiquiti" > /etc/apt/sources.list.d/20ubiquiti.list`
`echo "deb `[`http://downloads-distro.mongodb.org/repo/debian-sysvinit`](http://downloads-distro.mongodb.org/repo/debian-sysvinit)` dist 10gen" > /etc/apt/sources.list.d/21mongodb.list`

`apt-key adv --keyserver keyserver.ubuntu.com --recv C0A52C50`
`apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10`
`apt-get -q update && apt-get install -qy --force-yes unifi `

Access web interface

[`https://unifi-ip:8443`](https://unifi-ip:8443)

Lägga till device manuellt
==========================

SSH'a till din Ubiquiti device.

Default username och password är: **ubnt**

För att lägga till devicen kör:

`set-inform `[`http://`](http://)<unifi-wlc>`:8080/inform`

Kolla i webuit efter din device och klicka adopt.

Kör sedan samma set-inform kommando igen.

Factory default
===============

Access point
------------

SSHa och kör följande kommando:

`syswrapper.sh restore-default`

Switch
------

SSHa eller console och kör följande:

`set-default`

CLI kommandon
=============

Visa arp och mac tabellen:

`ubntbox swctrl -d mac show`

Visa port status:

`ubntbox swctrl -d port show`

Visa startup-config:

`cat /var/run/fastpath/startup-config`

[Category:Guider](/Category:Guider "wikilink")