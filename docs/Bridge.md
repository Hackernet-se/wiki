---
title: Bridge
permalink: /Bridge/
---

Linux Bridge är en kernel-modul som introducerades i kernel 2.2 och
administreras med kommandot brctl. Man kan göra om portar på en
Linuxmaskin till switchportar. Se även [Open
vSwitch](/Open_vSwitch "wikilink") och [Linux
VXLAN](/Iproute2#VXLAN "wikilink").

Installation
------------

`sudo apt-get install bridge-utils`
`sudo yum install bridge-utils`

Konfiguration
-------------

`ifconfig eth0 0.0.0.0`
`ifconfig eth1 0.0.0.0`
`brctl addbr bridge1`
`brctl addif bridge1 eth0 eth1`
`brctl show`

`brctl delif bridge1 eth0`

**/etc/network/interfaces**

`auto bridge`
`iface bridge`
` bridge-vlan-aware yes`
` bridge-ports eth0 eth1 eth7`
` bridge-vids 3 4 6-10   #allowed vlan`
` bridge-pvid 1          #native vlan`
` bridge_waitport 0      #portfast`
` bridge-stp on`
` mstpctl-treeprio 20480`

**VLAN**

`aptitude install vlan ifenslave`
`echo "8021q" >> /etc/modules`

**Spanning-Tree**

`sudo brctl stp bridge1 on `

**/etc/network/interfaces**

`auto bond0`
`iface bond0 inet manual`
`       up ifconfig bond0 0.0.0.0 up`
`       slaves eth0 eth1`
`       bond-mode 4       #bond-mode 4 = 802.3ad`
`       bond-miimon 100`
`       bond-downdelay 200`
`       bond-updelay 200`
`       bond-lacp-rate 1`
`       bond-xmit-hash-policy layer2+3`

Kolla packet

`cat /proc/net/bonding/bond0`

### MAC Table

Man kan kolla MAC-tabellen på en brygga med följande kommando:

`brctl show`
`brctl showmacs `<bridge_name>

[Category:Network](/Category:Network "wikilink")