---
title: Netsim-tools
permalink: /Netsim-tools/
---

Orkestrator för Vagrant-Libvirt, Vagrant-Virtualbox och Containerlab.

Installation Ubuntu
-------------------

``` Bash
sudo apt update && sudo apt install -y python3-pip
sudo python3 -m pip install netsim-tools
netlab install ubuntu ansible libvirt
```

Nexus 9300v
-----------

Download box file, example: nexus9300v.9.3.8.box

``` Bash
sudo vagrant plugin install vagrant-mutate
sudo vagrant box add nexus9300v.9.3.8.box --name cisco/nexus9300v
sudo vagrant mutate cisco/nexus9300v libvirt
sudo vagrant box remove cisco/nexus9300v --provider virtualbox
```

Topology file

`---`
`defaults:`
`  device: nxos`

`nodes: [ sw1, sw2 ]`
`links: [ sw1-sw2 ]`

Setup lab and start devices

`sudo netlab create`
`sudo netlab up`
`netlab connect sw1`

[Category:Network](/Category:Network "wikilink")