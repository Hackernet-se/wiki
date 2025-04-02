---
title: FastNetMon
permalink: /FastNetMon/
---

High performance DoS/DDoS load analyzer. Kan lyssna på bl.a.
[Netflow](/Cisco_NetFlow "wikilink"), IPFIX, sFLOW, PCAP,
[SPAN](/Cisco_SPAN "wikilink") och [PF_RING](/Ntopng "wikilink"). Om en
överbelastningsattack upptäcks exekveras ett script. Vad scriptet gör
avgör man själv, t.ex. maila/SMSa admin eller null routa prefix med
[ExaBGP](/ExaBGP "wikilink").

Installation
============

*Debian, Ubuntu, CentOS, Fedora*

`wget `[`https://raw.githubusercontent.com/pavel-odintsov/fastnetmon/master/src/fastnetmon_install.pl`](https://raw.githubusercontent.com/pavel-odintsov/fastnetmon/master/src/fastnetmon_install.pl)` -Ofastnetmon_install.pl `
`sudo perl fastnetmon_install.pl`

Första gången man startar det skapas konf-filer.

`sudo /opt/fastnetmon/fastnetmon --daemonize`

Konfiguration
=============

Det mesta görs i huvudkonf-filen.

`nano /etc/fastnetmon.conf`

Starta i screen

`screen -S fastnetmon -d -m /root/fastnetmon/fastnetmon`

### Networks

Lägg in dina egna IP-nät så fastnetmon vet vad som är lokalt.

`nano /etc/networks_list`
`10.10.0.0/24`
`20.20.0.0/24`

### Klient

Kolla live.

`/opt/fastnetmon/fastnetmon_client`

### Notify

Default: notify_script_path =
/usr/local/bin/notify_about_attack.sh
Skapa script

`nano /usr/local/bin/notify_about_attack.sh`
`chmod +x /usr/local/bin/notify_about_attack.sh`

### NetFlow

`netflow_port = 2055`
`netflow_host = 0.0.0.0`
`netflow_sampling_ratio = 1`

### Graphite

Det finns även integration med [Graphite](/Graphite "wikilink") (och
således [Grafana](/Grafana "wikilink"))

`graphite = on`
`graphite_host = 127.0.0.1`
`graphite_port = 2003`

### Loggar

`tail -f /var/log/fastnetmon.log`

[Category:Guider](/Category:Guider "wikilink")