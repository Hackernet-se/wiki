---
title: Tor
permalink: /Tor/
---

[Category:Guider](/Category:Guider "wikilink") Tor är en
anonymiseringsprogram och används bla för att komma åt deep web.

Installation
============

Källa: <https://www.torproject.org/docs/debian.html.en>

Ubuntu 18.04 LTS

`sudo su -`
`echo "deb `[`https://deb.torproject.org/torproject.org`](https://deb.torproject.org/torproject.org)` bionic main" >> /etc/apt/sources.list`
`curl `[`https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc`](https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc)` | gpg --import`
`gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | apt-key add -`
`apt-get update && apt-get -y install deb.torproject.org-keyring ntp && apt-get -y install tor`

Verifiera

`tor --version`

Konfiguration
=============

TCP 9001 och 9030 behöver port forwardas till maskinen.

`nano /etc/tor/torrc`

### Exempel

SwedishNSA är en non-exit tor-nod. Statistik finns på
<https://metrics.torproject.org/rs.html>.

`mv /etc/tor/torrc /etc/tor/torrc.orig`
`wget `[`https://raw.githubusercontent.com/torproject/tor/master/contrib/operator-tools/tor-exit-notice.html`](https://raw.githubusercontent.com/torproject/tor/master/contrib/operator-tools/tor-exit-notice.html)` -O /etc/tor/tor-exit-notice.html`

`cat<<'__EOF__'>/etc/tor/torrc`
`SocksPort 0 `
`Log notice file /var/log/tor/notices.log`
`RunAsDaemon 1`
`DataDirectory /var/lib/tor`
`ORPort 9001`
`ORPort [2001:2002:beef:ffff::11]:9001`
`Address swedishnsa.hackernet.se`
`Nickname SwedishNSA`
`ContactInfo Helikopter `<tor AT hackernet dot se>
`DirPort 9030 # what port to advertise for directory connections`
`DirPortFrontPage /etc/tor/tor-exit-notice.html`
`ExitPolicy reject *:* # no exits allowed`
`__EOF__`

`systemctl restart tor`

Kolla att det kommer igång som det ska

`tail -f /var/log/tor/notices.log`

Torport
=======

En torport kan vara en fysisk port eller ett nätverk som sätter allt som
är inkopplat bakom tornätverket, helt transparant, vare sig man vill
eller inte. Detta är ingen Transparent Proxy utan en Isolating proxy.
Man behöver en maskin med två interface. Det ena behöver internetaccess
och kan vara DHCP-klient. Det andra är DHCP-server för det som ska
torifieras, [ISC_DHCP](/ISC_DHCP "wikilink"). Stäng även av
IP-forwardering för att undvika eventuella IP-läckor.

`sudo apt-get -y install tor`

Tor kan göra det mesta själv

`sudo dd of=/etc/tor/torrc << EOF`
`Log notice file /var/log/tor/notices.log`
`VirtualAddrNetwork 10.192.0.0/10`
`AutomapHostsSuffixes .onion,.exit`
`AutomapHostsOnResolve 1`
`TransPort 9040`
`TransListenAddress 10.0.0.1 #Interface-IPn på torporten`
`DNSPort 53`
`DNSListenAddress 10.0.0.1`
`EOF`

Men behöver lite hjälp från iptables

`sudo iptables -F`
`sudo iptables -t nat -F`
`sudo iptables -t nat -A PREROUTING -i p2p1 -p tcp --dport 22 -j REDIRECT --to-ports 22`
`sudo iptables -t nat -A PREROUTING -i p2p1 -p udp --dport 53 -j REDIRECT --to-ports 53`
`sudo iptables -t nat -A PREROUTING -i p2p1 -p tcp --syn -j REDIRECT --to-ports 9040    `
`sudo sh -c "iptables-save > /etc/iptables.rules"`

Välj det interface som är din torport. Med p22-regeln kan man ssha till
hosten från "tornätet".

`sudo nano /etc/network/if-pre-up.d/iptables`
`#!/bin/bash`
`/sbin/iptables-restore < /etc/iptables.rules`
`sudo chmod +x /etc/network/if-pre-up.d/iptables    `

### Välj land

Vill man gå i specifika länder kan man specca det i torrc

`ExitNodes {us},{uk}`