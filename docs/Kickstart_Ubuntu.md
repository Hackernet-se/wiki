---
title: Kickstart Ubuntu
permalink: /Kickstart_Ubuntu/
---

Exempel på ks-fil för Ubuntu server

`network --bootproto=static --hostname=host7.hackernet.se --ip=172.20.0.4 --netmask=255.255.255.0 --gateway=172.20.0.1 --nameserver=8.8.8.8 --device=eth0`
`lang en_US`
`langsupport en_US`
`keyboard se`
`mouse`
`timezone Europe/Stockholm`
`rootpw --disabled`
`#Initial user`
`user doge --fullname "skeletor" --password suchpw`
`#Reboot after installation`
`reboot`
`text`
`install`
`#Use Web installation`
`url --url `[`http://se.archive.ubuntu.com/ubuntu`](http://se.archive.ubuntu.com/ubuntu)
`bootloader --location=mbr`
`zerombr yes`
`clearpart --all --initlabel`
`part / --fstype ext4 --size 1 --grow`
`part swap --recommended`
`auth  --useshadow`
`firewall --disabled`
`skipx`

`%packages`
`openssh-server`
`fail2ban`
`open-vm-tools`
`ntp`

[Category:Kickstart](/Category:Kickstart "wikilink")