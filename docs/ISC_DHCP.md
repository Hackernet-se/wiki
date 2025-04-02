---
title: ISC DHCP
permalink: /ISC_DHCP/
---

[Category:Guider](/Category:Guider "wikilink") "ISC's DHCP software is
the most widely used open source DHCP implementation on the Internet.
The same software can be used for LAN too. It is a carrier and
enterprise grade solution to your host configuration needs." - nixCraft

Se även [Kea DHCP](/Kea "wikilink").

Installation
------------

`sudo apt-get -y install isc-dhcp-server`
`sudo sed -i -r 's/INTERFACES=""/INTERFACES="eth0"/g' /etc/default/isc-dhcp-server`

Konfiguration
-------------

`sudo dd of=/etc/dhcp/dhcpd.conf << EOF`
`# Uppsatt av:`

`# You must prevent the DHCP server from receiving DNS information `
`# from clients, set the following global option (this is a security feature):`
`ddns-update-style none;`

`# You need to set your domain name and name server:`
`option domain-name "exempel.se";`
`option domain-name-servers 8.8.8.8, 208.67.222.222;`

`# Increase the lease time. The time is set in seconds:`
`default-lease-time 7200;`
`max-lease-time 14400;`

`# If this DHCP server is the official DHCP server for the local`
`# network, the authoritative directive should be uncommented.`
`# The authoritative directive indicate that the DHCP server `
`# should send DHCPNAK messages to misconfigured clients. `
`# If this is not done, clients will be unable to get a correct `
`# IP address after changing subnets until their old lease has `
`# expired, which could take quite a long time.`
`authoritative;`

`# Use this to send dhcp log messages to a different log file (you also`
`# have to hack syslog.conf to complete the redirection).`
`log-facility local7;`

`# No service will be given on this subnet, but declaring it helps the`
`# DHCP server to understand the network topology.`
`subnet 10.0.100.0 netmask 255.255.255.0 {`
`}`

`#Ranges`
` `
`subnet 10.0.1.0 netmask 255.255.255.0 {`
`       range 10.0.1.100 10.0.1.200;`
`       option subnet-mask 255.255.255.0;`
`       option broadcast-address 10.0.1.255;`
`       option routers 10.0.1.1;`
`}`

`subnet 10.0.2.0 netmask 255.255.255.0 {`
`       range 10.0.2.100 10.0.2.200;`
`       option subnet-mask 255.255.255.0;`
`       option broadcast-address 10.0.2.255;`
`       option routers 10.0.2.1;`
`}`

`## Slut`
`EOF`

Testa

`sudo dhcpd -t /etc/dhcp/dhcpd.conf`