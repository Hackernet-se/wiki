---
title: Open vSwitch
permalink: /Open_vSwitch/
---

Open vSwitch är en virtuell multi layer switch, open source licensierad
under Apache 2.0. Det används oftast med hypervisors för att koppla ihop
vms med varandra mellan hostar och nätverk, t.ex. med KVM eller Xen. Det
kan också användas med dedikerad switchhårdvara eller SDN-lösningar.
Open vSwitch har stöd för de flesta traditionella tekniker inklusive
STP, VLAN, LACP, GRE, VXLAN, BFD, QoS och net/sflow. Open vSwitch består
i huvudsak av VSWITCHD, OVSDB-server och en kernel-modul. Det går även
köra distribuerat över flera hostar likt VMwares vDS och Cisco [Nexus
1000V](/Nexus_1000V "wikilink").

**Tools**

-   ovs-vsctl: configuring the ovs-vswitchd configuration database
-   ovs-ofctl: monitor and administer OpenFlow switches
-   ovs-dpctl: administer Open vSwitch datapaths
-   ovs−appctl: query and controll Open vSwitch daemons

Installation
------------

*Ubuntu*

`apt-cache show openvswitch-switch | grep Version`
`sudo apt-get install openvswitch-switch`

*Fedora*

`sudo dnf info openvswitch | grep Version`
`sudo dnf install openvswitch`

`sudo systemctl start openvswitch`
`lsmod | grep openv`

Start at boot

`sudo systemctl enable openvswitch`

Konfiguration
-------------

Skapa en virtuell switch och koppla interface till den.

`ovs-vsctl add-br br0`
`ovs-vsctl add-port br0 eth0`
`ovs-vsctl list-ifaces br0`

Show

`ovs-vsctl show`
`ovs-vsctl list-br`
`ovs-ofctl show br0`

/etc/network/interfaces

`allow-ovs ovsbr0`
`iface ovsbr0 inet manual`
`  ovs_type OVSBridge`
`  ovs_ports eth1`

Adress till hosten

`ifconfig eth0 0`
`dhclient br0`

### Interface

*default all ports are VLAN trunks*
Access

`ovs-vsctl set port eth1 vlan_mode=access tag=1`

Trunk

`ovs-vsctl set port eth1 vlan_mode=tagged`

Hybrid

`ovs-vsctl set port eth1 vlan_mode=native-untagged trunks=[1,3] tag=2`

Show

`ovs-vsctl list port eth1`

### Bond

`ovs-vsctl add-bond br0 bond0 eth0 eth1 lacp=active trunks=10,11,12`
`ovs-vsctl list port bond0`

### STP

`ovs-vsctl set bridge br0 stp_enable=true`

### SVI

`ovs-vsctl add-port br0 vlan90 tag=09 -- set interface vlan09 type=internal`

Interface till vms

`ip tuntap add mode tap vport1`
`ip tuntap add mode tap vport2`
`ovs-vsctl add-port testbridge vport1`
`ovs-vsctl add-port testbridge vport2`
`ovs-vsctl show`

Kolla mac-tabell

`ovs-appctl fdb/show testbridge`

Controller
----------

`ovs-vsctl set-controller br0 tcp:10.0.0.20:6633`
`ovs-vsctl list controller`

Tappar man konnektivitet med controllern sätter man antingen upp flows
själv eller inte alls beroende på standalone eller secure mode.

`ovs-vsctl get-fail-mode br0`

Ta bort controller

`ovs-vsctl del-controller br0`

OpenFlow
--------

Open vSwitch har stöd för OpenFlow.

`ovs-vsctl -- set bridge br0 protocols=openflow14`

Patch Port
----------

Med patchportar kan man koppla ihop flera ovs:er med varandra internt
inom en host.
Sw1

`ovs-vsctl add-port br1 patch1-2`
`ovs-vsctl set interface patch1-2 type=patch`
`ovs-vsctl set interface patch1-2 options:peer=patch2-1`

Sw2

`ovs-vsctl add-port br2 patch2-1`
`ovs-vsctl set interface patch2-1 type=patch`
`ovs-vsctl set interface patch2-1 options:peer=patch1-2`

`ovs-vsctl show`

sFlow
-----

Open vSwitch kan streama telemetry med sFlow.

`service sflowovsd start`

[Category:Network](/Category:Network "wikilink")