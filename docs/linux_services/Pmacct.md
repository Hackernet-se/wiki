---
title: Pmacct
permalink: /Pmacct/
---

Pmacct är ett verktyg för att samla ihop och aggregera data om
IP-trafik, som t.ex. [Ntopng](/Ntopng "wikilink"). Det kan (med dess
underkomponenter) samla in [interface-trafik](/Cisco_SPAN "wikilink")
(libpcap), [NetFlow](/Cisco_NetFlow "wikilink"), IPFIX, sFlow och ULOG.
Man kan spara datan i minne, flat-files eller diverse databaser, t.ex.
[MySQL](/MySQL "wikilink"), PgSQL, SQLite, MongoDB. pmacct kan användas
för att skicka data till bl.a. RRDtool, Net-SNMP, MRTG och
[Cacti](/Cacti "wikilink"). Det går även att peera med routrar med
[BGP](/Cisco_BGP "wikilink") eller [IS-IS](/Cisco_IS-IS "wikilink") för
att få ut routinginformation (passiv granne, dvs annonserar aldrig
något).

**pmacct:** commandline pmacct client, used to retrieve data from a
memory plugin

**pmacctd:** libpcap-based accounting daemon, it captures packets from
an interface it is bound to.

**nfacctd:** NetFlow accounting daemon, it listens for NetFlow packets
v1/v5/v7/v8/v9 and IPFIX on one or more interfaces (IPv4 and IPv6).

Installation
============

*Ubuntu 15.10*

`sudo apt-get -y install pmacct`
`pmacct -V`
`sudo systemctl status pmacctd`

Verifiering

`whereis pmacct`
`whereis pmacctd`
`whereis nfacctd`

Konfiguration
=============

Inputs
------

Välj en input

### libpcap

`sudo ip link set up dev eth1`
`sudo nano /etc/pmacct/pmacctd.conf`
`daemonize: true`
`promisc: true`
`interface: eth1`

Start

`sudo systemctl start pmacctd`

### Netflow

`sudo nano /etc/pmacct/nfacctd.conf`
`nfacctd_port: 9999`
`nfacctd_ip: 172.20.0.12`
`nfacctd_time_new: true`

Start

`sudo systemctl start nfacctd`

### BGP

`bgp_daemon: true`
`bgp_daemon_ip: 172.20.0.12`
`bgp_daemon_max_peers: 1`
`bgp_table_dump_file: /etc/pmacct/output/bgp-$peer_src_ip-%Y_%m_%dT%H_%M_%S.txt`
`bgp_table_dump_refresh_time: 3600`

Data
----

Var ska datan lagras

### Memory

`sudo mkdir /var/spool/pmacct/`

*/etc/pmacct/\*\*acctd.conf*

`imt_mem_pools_number: 0`
`plugins: memory[plugin1]`
`imt_path[plugin1]: /var/spool/pmacct/plugin1.pipe`
`aggregate[plugin1]: proto, src_host, src_port, dst_host, dst_port`

Kolla live

`pmacct -p /var/spool/pmacct/plugin1.pipe -s`

### Flat-files

`plugins: print`

### MySQL

Databas måste skapas först.

`plugins: mysql`
`sql_db: pmacct`
`sql_host: localhost`
`sql_user: root`
`sql_passwd: pmacct`
`sql_refresh_time: 3600`
`sql_history: 60m`
`sql_history_roundoff: h`
`sql_table_version: 1`

### SQLite

Databas måste skapas först.

`plugins: sqlite3`

[Category:Guider](/Category:Guider "wikilink")