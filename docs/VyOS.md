---
title: VyOS
permalink: /VyOS/
---

VyOS är ett Linux-baserat network operating system med mjukvaru-routing,
firewall och VPN funktionalitet. Det är en community fork av Vyatta Core
med [JunOS](/Juniper_JunOS "wikilink")-liknande syntax och bygger på
Debian och Quagga routing engine. Det har bl.a. stöd för
[DMVPN](http://vyos.net/wiki/DMVPN),
[VXLAN](http://vyos.net/wiki/VXLAN),
[OSPF](http://vyos.net/wiki/User_Guide#OSPF),
[BGP](http://vyos.net/wiki/User_Guide#BGP) och
[IPv6](http://vyos.net/wiki/IPv6). Men saknar tyvärr stöd för Multicast
routing och MPLS. Det finns möjlighet att installera
[FastNetMon](/FastNetMon "wikilink") direkt på en VyOS-router, se länk
[1](https://github.com/pavel-odintsov/fastnetmon/blob/master/docs/VyOS_INSTALL.md)

Installation
============

Ladda ner OVA alternativt installera från iso eller netbootxyz. PW: vyos

`vyos@vyos:~$ install image `

Uppgradering
============

`add system image `[`https://s3.amazonaws.com/s3-us.vyos.io/rolling/current/vyos-rolling-latest.iso`](https://s3.amazonaws.com/s3-us.vyos.io/rolling/current/vyos-rolling-latest.iso)
`show system image`

Konfiguration
=============

Byt till konfigurationsläge.

`configure`

Ändringar måste commitas. För att spara till startup config används
save.

`commit`
`save`

Show run

`show conf`

Show run kommandon

`show configuration commands`

**SSH**

`set service ssh port '22'`
`set service ssh listen-address '172.20.0.1'`

Logga in med ssh-nyckel

`set system login user vyos authentication public-keys user@mgm key 'AAAAC3NzaC1lZAAAIGCW6VcUwAzbX0gipoiDYBxxxxxxxxx'`
`set system login user vyos authentication public-keys user@mgm type 'ssh-ed25519'`

**Live logging**

`monitor log`

**System**

`set system domain-name hackernet.se`
`set system host-name vyos01`
`set system name-server 208.67.222.222`
`set system name-server 208.67.220.220`
`set system time-zone Europe/Stockholm`

**Backup**

`set system config-management commit-archive location scp://user@172.20.0.20:/vyos_backups/`

Testa backuptagning manuellt.

`copy file running://config/config.boot to scp://user@172.20.0.20:/vyos_backups/`

**Interface**

`configure`
`set interfaces ethernet eth0 address '10.0.0.1/24'`
`set interfaces ethernet eth0 description 'INSIDE'`
`show interfaces`

**Default route**

`set protocols static route 0.0.0.0/0 next-hop 10.0.10.1 distance '1'`

Verify

`show ip route`

**Comments**
Man kan lägga in kommentarer var som helst i konfigurationen.

`comment `*`path-config-section`*` "comment"`

Default editerar man från top level (\[edit\]) men för att undvika att
alltid skriva långa kommandon kan man ställa sig var som helst i
strukturen och använda relativa paths. "up" är för att backa.

`edit interfaces ethernet eth0 `
`set address '10.0.0.1/24'`

**Öka ring queue buffer size**

`sudo ethtool -g eth0`
`sudo ethtool -G eth0 tx 4096 rx 4096`

NAT
---

Overload/PAT

`set nat source rule 10 outbound-interface eth0`
`set nat source rule 10 source address 10.0.0.0/24`
`set nat source rule 10 translation address masquerade`

IPv6
----

Din ISP måste supporta IPv6 prefix delegation. Följande funkade för
Bahnhof.

Slå på prefix-delegation(pd) på ditt wan interface, och assigna ett
prefix till ditt interface i detta fallet eth2.

`set interfaces ethernet eth0 address 'dhcpv6'`
`set interfaces ethernet eth0 description 'WAN'`
`set interfaces ethernet eth0 dhcpv6-options pd 0 interface eth2 sla-id '2'`
`set interfaces ethernet eth0 dhcpv6-options pd 0 length '56'`

Sätt sedan på router-advert på eth2 för att ge ut en IPv6 address och
DNS server till klienterna.

`set service router-advert interface eth2 name-server '2001:4860:4860::8888'`
`set service router-advert interface eth2 name-server '2001:4860:4860::8844'`
`set service router-advert interface eth2 prefix ::/64`

Router-on-a-stick
-----------------

Sub-interfaces

`set firewall name LOCAL default-action 'drop'`
`set firewall name LOCAL rule 10 action 'accept'`
`set firewall name LOCAL rule 10 state established 'enable'`
`set firewall name LOCAL rule 10 state related 'enable'`
`set firewall name OUTSIDE default-action 'drop'`
`set firewall name OUTSIDE rule 10 action 'accept'`
`set firewall name OUTSIDE rule 10 state established 'enable'`
`set firewall name OUTSIDE rule 10 state related 'enable'`
`set interfaces ethernet eth0 vif 2 address '172.20.0.1/24'`
`set interfaces ethernet eth0 vif 2 description 'LAN'`
`set interfaces ethernet eth0 vif 3 address 'dhcp'`
`set interfaces ethernet eth0 vif 3 description 'WAN'`
`set interfaces ethernet eth0 vif 3 firewall in name 'OUTSIDE'`
`set interfaces ethernet eth0 vif 3 firewall local name 'LOCAL'`

Zerotier
--------

``` Bash
sudo -i
curl -s https://install.zerotier.com | sudo bash
cd /var/lib && mv /var/lib/zerotier-one /config/scripts/ && ln -s /config/scripts/zerotier-one
/var/lib/zerotier-one/zerotier-cli join af78xxxxxxx
```

**Upgrade**

``` Bash
sudo -i
apt update && apt install zerotier-one
```

netboot.xyz
-----------

DHCP-server + TFTP-server + netboot.xyz, all-in-one.

`set service dhcp-server shared-network-name LAN subnet 172.20.0.0/24 bootfile-server 172.20.0.1`
`set service dhcp-server shared-network-name LAN subnet 172.20.0.0/24 bootfile-name netboot.xyz.efi`
`set service tftp-server directory /config/tftproot`
`set service tftp-server listen-address 172.20.0.1`
`commit`

`sudo -i`
`mkdir /config/tftproot && cd /config/tftproot/ && wget `[`https://boot.netboot.xyz/ipxe/netboot.xyz.efi`](https://boot.netboot.xyz/ipxe/netboot.xyz.efi)

OBS funkar endast med EFI-klienter (med Secure Boot avstängt).

[Category:Network](/Category:Network "wikilink")