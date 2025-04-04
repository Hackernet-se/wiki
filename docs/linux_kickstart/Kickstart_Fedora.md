---
title: Kickstart Fedora
permalink: /Kickstart_Fedora/
---

Fedora 23

`# Network information`
`network  --bootproto static --ip 172.10.0.20 --netmask 255.255.255.0 --gateway 172.10.0.1 --nameserver 172.10.0.1 --device=eno16780032 --ipv6=auto --activate`
`network  --hostname=fedora.hackernet.se`

`graphical`
`auth --enableshadow --passalgo=sha512`
`url --url="`[`http://download.fedoraproject.org/pub/fedora/linux/releases/23/Server/x86_64/os`](http://download.fedoraproject.org/pub/fedora/linux/releases/23/Server/x86_64/os)`"`
`firstboot --enable`
`ignoredisk --only-use=sda`
`keyboard --vckeymap=se --xlayouts='se'`
`lang en_US.UTF-8`
`rootpw --lock`
`timezone Europe/Stockholm --isUtc`
`user --groups=wheel --name=skeletor --password=$6$0mOr4b/kgDAOoxgg$vgPmtqFEZB0//fc3J9RW90eM6nDIISyE0IxT.06ufRvGnfx6ET2ollSHP46OefzAvYUs5hqbqHXzUzhptDefM1 --iscrypted --gecos="skeletor"`
`bootloader --location=mbr --boot-drive=sda`
`autopart --type=lvm`
`zerombr`
`clearpart --all --initlabel`
`reboot`

`%packages`
`@^server-product-environment`
`%end`

`%anaconda`
`pwpolicy root --minlen=0 --minquality=1 --notstrict --nochanges --emptyok`
`pwpolicy user --minlen=0 --minquality=1 --notstrict --nochanges --emptyok`
`pwpolicy luks --minlen=0 --minquality=1 --notstrict --nochanges --emptyok`
`%end`

Fråga efter hostnamn
====================

Få fedora/centos/redhat att fråga efter hostnamn under installation.

`%pre`
`#!/bin/sh`
`exec < /dev/tty3 > /dev/tty3 2>&1`
`chvt 3`
`hn=""`

`while [ "$hn" == "" ]; do`
` clear`
`  echo " *** Please enter the following details: *** "`
`   echo`
`    read -p "Hostname: " hn`
`    done`
`    clear`
`    chvt 1`
`    echo "network --device=link --bootproto=dhcp --noipv6 --hostname ${hn}.hackernet.se --activate" > /tmp/network.txt`
`%end`

[Category:Kickstart](/Category:Kickstart "wikilink")