---
title: Quagga
permalink: /Quagga/
---

Quagga är en network routing software suite och har stöd för
[OSPF](/Cisco_OSPF "wikilink"), [BGP](/Cisco_BGP "wikilink"),
[RIP](/Cisco_RIP "wikilink") och [IS-IS](/Cisco_IS-IS "wikilink").
Konfigurationsyntaxen är generellt väldigt lik [Cisco
IOS](/Cisco_IOS "wikilink"). Quagga har en core daemon som heter zebra
och sedan klienter till det, ospfd, isisd, ripd, ospf6d, ripngd och
bgpd. Zebra är en IP-routing manager som står för kommunikation med
kernel, interface och redistribution mellan olika routingprotokoll.

Installation
============

Vill man ha senaste versionen kan man behöva ta ner paketet och
installera manuellt annars funkar pakethanterare.

`dnf install quagga`
`apt-get install quagga`

Allow routing in os

`echo "net.ipv4.conf.all.forwarding=1" | sudo tee -a /etc/sysctl.conf `
`echo "net.ipv4.conf.default.forwarding=1" | sudo tee -a /etc/sysctl.conf`
`sudo sysctl -p`

Konfiguration
=============

Slå på det som är önskvärt genom att editera daemons-filen.

`sudo nano /etc/quagga/daemons`

Lägg sedan in grundkonf för zebra.

`sudo cp /usr/share/doc/quagga/examples/zebra.conf.sample /etc/quagga/zebra.conf`
`sudo service quagga restart`

File Permissions

`sudo chown quagga.quaggavty /etc/quagga/*.conf`
`sudo chmod 640 /etc/quagga/*.conf`

Zebra-only CLI

`telnet localhost zebra`

**VTYSH**, CLI som används för att sköta all quagga-konfiguration.

`sudo cp /usr/share/doc/quagga/examples/vtysh.conf.sample /etc/quagga/vtysh.conf`
`sudo chown quagga:quaggavty /etc/quagga/vtysh.conf && sudo chmod 660 /etc/quagga/vtysh.conf`
`sudo su -`
`export VTYSH_PAGER=more `
`vtysh`

wr för att spara

OSPF
----

Se [Cisco OSPF](/Cisco_OSPF "wikilink") för mer info om OSPF.

`sudo cp /usr/share/doc/quagga/examples/ospfd.conf.sample /etc/quagga/ospfd.conf`
`sudo nano /etc/quagga/ospfd.conf && sudo service quagga restart`
`hostname ospfd`
`router ospf`
` network 10.0.0.0/24 area 0`

OSPF-only CLI

`telnet localhost ospfd`

wr för att spara

BGP
---

Se [Cisco BGP](/Cisco_BGP "wikilink") för mer info om BGP.

`sudo cp /usr/share/doc/quagga/examples/bgpd.conf.sample /etc/quagga/bgpd.conf`
`sudo nano /etc/quagga/bgpd.conf && sudo service quagga restart`
`hostname bgpd`
`router bgp 100`
` bgp router-id 10.0.0.1`
` network 10.0.0.0/24`
` neighbor 10.0.0.2 remote-as 100`

BGP-only CLI

`telnet localhost bgpd`

wr för att spara

### EVPN

Ethernet VPN (RFC 7432) är en modernare variant än VPLS för att
tillhandahålla Ethernet multipoint services över MPLS eller IP. Det är
öppet så det finns interoperability med andra network vendors, se t.ex.
[Cisco VXLAN](/Cisco_VXLAN "wikilink").

OBS detta finns än sålänge endast i en community fork av Quagga som
heter FRR.

VTEP

`router bgp 100`
` address-family evpn`
`  neighbor 10.0.0.10 activate`
`  advertise-all-vni`
` exit-address-family`

Route reflector

` address-family evpn`
`  neighbor 10.0.0.11 activate`
`  neighbor 10.0.0.11 route-reflector-client`
` exit-address-family`

Verify

`show bgp evpn route`
`show evpn vni`
`show evpn mac vni 100`

[Category:Network](/Category:Network "wikilink")