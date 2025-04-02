---
title: Ntopng
permalink: /Ntopng/
---

High-Speed Web-based Traffic Analysis and Flow Collection.

Installation
------------

14.04

`wget `[`http://www.nmon.net/apt-stable/14.04/all/apt-ntop.deb`](http://www.nmon.net/apt-stable/14.04/all/apt-ntop.deb)` && sudo dpkg -i apt-ntop.deb`
`sudo apt-get clean all && sudo apt-get update && sudo apt-get -y install ntopng ntopng-data nbox libzmq3 libhiredis0.10`
`sudo service apache2 restart`

16.04

`wget `[`http://packages.ntop.org/apt-stable/16.04/all/apt-ntop.deb`](http://packages.ntop.org/apt-stable/16.04/all/apt-ntop.deb)` && sudo dpkg -i apt-ntop.deb`
`sudo apt-get clean all && sudo apt-get update && sudo apt-get -y install ntopng ntopng-data nbox nprobe`
`sudo service apache2 restart`

Konfiguration
-------------

Konfigurationen ligger i **/etc/ntopng.conf** men allt kan göras med
nbox gui:

[`https://`](https://)<IP>

credentials: nbox:nbox
ntopng konfas och startas från webgui:t

Portspegling
------------

Det finns olika sätt att få den speglade trafiken till ntop.

-   **vSwitch:** Promiscuous mode
-   **dvSwitch:** Distributed Port Mirroring
-   **Fysisk switch:** [SPAN](/Cisco_SPAN "wikilink")/RSPAN/ERSPAN

Listener Port

`echo "auto eth1" | sudo tee -a /etc/network/interfaces`
`echo "iface eth1 inet manual" | sudo tee -a /etc/network/interfaces`

NetFlow
-------

In ntopng flows are collected through nProbe that act as probe/proxy.
The communication between nProbe and ntopng happens though ZeroMQ that
decouples ntopng from nProbe.

OBS nprobe kräver licens, se även [Cisco
NetFlow](/Cisco_NetFlow "wikilink").

`sudo nprobe --zmq "tcp://*:5556" -i none [eth0] -n none --collector-port 2055 &`
`sudo ntopng -i tcp://127.0.0.1:5556`

**nProbe modes** [left\|607x607px](/File:Nprobe.PNG "wikilink")

[Category:Guider](/Category:Guider "wikilink")