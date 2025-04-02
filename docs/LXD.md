---
title: LXD
permalink: /LXD/
---

LXD är en container hypervisor för Linux. Det är byggt utifrån LXC. Man
skapar containrar utifrån images.

### Installation

*16.04*

`sudo apt-get -y install lxd`

Version

`lxd --version`

### Images

Kolla tillgängliga källor för images.

`lxc remote list`

Lista tillgängliga images från en viss källa.

`lxc image list images:`

Hämta images

`sudo lxc image copy images:/ubuntu/trusty/amd64 local: --alias=trusty-amd64`
`sudo lxc image list`

### Container

Starta container utifrån image.

`lxc launch trusty-amd64 Test`
`lxc list`

### Remote Hosts

Man kan med lxc-kommandot managera containrar på andra LXD-hostar.

Allow management on remote machine

`lxc config set core.https_address [::]`
`lxc config set core.trust_password PASSWORD`

Control

`lxc remote add hostA `<ip address or DNS>
`lxc exec hostA:containername -- apt-get update`

[Category:Guider](/Category:Guider "wikilink")