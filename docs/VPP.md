---
title: VPP
permalink: /VPP/
---

Vector Packet Processing är en network packet processing stack för
x86-hårdvara. Det kör en Linux user space process och har stöd för bl.a.
IPSEC, GRE, VXLAN, MPLS, VRF, VLAN, Segment Routing. Med denna mjukvara
kan en vanlig server kan bli en router/switch med väldigt hög
throughput. Det är en open source version av Cisco's Vector Packet
Processing (VPP) teknologi.

Installation
------------

Ubuntu 16.04

`echo "deb `[`https://nexus.fd.io/content/repositories/fd.io.ubuntu.xenial.main/`](https://nexus.fd.io/content/repositories/fd.io.ubuntu.xenial.main/)` ./" | sudo tee -a /etc/apt/sources.list.d/99fd.io.list`
`sudo apt update && sudo apt install vpp vpp-lib vpp-dpdk-dkms`

Fedora

`sudo curl -o /etc/yum.repos.d/fdio.repo `[`https://paste.fedoraproject.org/355177/60579220/raw/`](https://paste.fedoraproject.org/355177/60579220/raw/)
`sudo dnf update && sudo dnf install vpp`

Konfiguration
-------------

`cat /etc/vpp/startup.conf`

Service

`sudo systemctl start vpp`
`sudo systemctl status vpp`

VPP lyssnar default på tcp port 5000

`telnet 0 5000`

VPP shell

`show interface`

Bash

`sudo vppctl show ip arp`

**Honeycomb** är en agent man kan köra på samma host som tillhandahåller
yang models via netconf/restconf för remote management.

`sudo yum install honeycomb`

[Category:Network](/Category:Network "wikilink")