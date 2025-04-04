---
title: Iproute2
permalink: /Iproute2/
---

Ifconfig, arp och route-kommandona är påväg bort, vänj dig vid iproute2.
De två viktigaste verktygen är ip och tc (traffic control)
Med dessa kommandon behöver man inte skriva ut alla bokstäver, likt
switchar och routrar. T.ex. ip a s är samma som ip address show

| Gamla kommandot | Nya kommandot                  | Kommentar                                            |
|-----------------|--------------------------------|------------------------------------------------------|
| `ifconfig`      | `ip addr`, `ip link`, `ip -s`  | Adresser och länk config                             |
| `route`         | `ip route`                     | Routing tables                                       |
| `arp`           | `ip neigh`                     | Neighbors                                            |
| `iptunnel`      | `ip tunnel`                    | Tunnels                                              |
| `nameif`        | `ifrename`, `ip link set name` | Byt namn på ett interface                            |
| `ipmaddr`       | `ip maddr`                     | Multicast                                            |
| `netstat`       | `ip -s`, `ss`, `ip route`      | Visar nät statistik, tex vilka portar man lyssnar på |

ip
--

Version

`ip -V`

**ip address show**

`ip a`
`ip -br a`
`ip a s eth0`

**ip routes show**

`ip r`

**ip link**
ifconfig

`ip l`
`ip -br l`
`ip -s l  #med statistik`

ifup/ifdown

`ip link set eth0 up/down`

Description

`ip link set eth0 alias "LAN interface"`

Promiscuous mode på interface

`ip link set eth0 promisc on`
`ip a | grep PROMISC`

Macchanger

`ip link set dev eth0 address 00:11:22:33:44:55`

**ip neigh**
ARP/NDP

`ip n`

Flush cache

`ip n f`

**Monitor**
Monitor changes in network configuration, routing tables, and ARP/NDP
tables from terminal.

`ip monitor`

### VXLAN

VXLAN är ett tunnlingsprotokoll designat för att lösa
skalbarhetsbegränsningar med VLAN. Det ökar från 4096 till 24 bitar (16
miljoner) id:n. Protokollet körs över en enskild konfigurerbar UDP-port.
EN VXLAN-enhet kan lära sig MAC/IP-adresser tillhörande andra sidan
tunneln antingen dynamiskt likt en switch eller med statiska forwarding
entries.

**Unicast**

`ip link add vxlan0 type vxlan id 10 remote 2.2.2.2 local 1.1.1.1 dev eth0`

VTEP-kommunikation görs alternativt med multicast.

`ip link add vxlan0 type vxlan id 10 group 239.1.1.1 dev eth0 dstport 4789`

Vxlan-interfacet kopplas sedan till en [Open
vSwitch](/Open_vSwitch "wikilink") eller [Linux
Bridge](/Bridge "wikilink").

`brctl addif br0 vxlan0`

Enablea interface

`ip link set up dev vxlan0`

Kolla interface och forwarding table

`ip -d link show vxlan0`
`bridge fdb show dev vxlan0`

Delete interface

`ip link delete vxlan0`

Disable source-address learning, detta kan t.ex. göras om man har BGP
EVPN som synkroniserar FDBs.

`ip link add vxlan0 type vxlan id 10 remote 2.2.2.2 local 1.1.1.1 dev eth0 `**`nolearning`**

Skapa entry manuellt

`bridge fdb add to 00:00:0c:80:bb:07 dst 2.2.2.2 dev vxlan0`

### GRETAP

Generic Routing Encapsulation on linux.

`ip link add GRETAP1 type gretap local 172.16.0.10 remote 192.168.0.10 dev eth0`
`ip link add br0 type bridge`
`ip link set eth1 master br0`
`ip link set eth1 up`
`ip link set br0 up`
`ip link set GRETAP1 up`
`ip link set GRETAP1 master br0`
`ifconfig br0 promisc`

### L2TPv3

Layer Two Tunneling Protocol - Version 3.

`modprobe l2tp_eth`
`ip l2tp add tunnel local 1.1.1.1 remote 2.2.2.2 tunnel_id 100 peer_tunnel_id 200 encap udp udp_sport 5000 udp_dport 5000`
`ip l2tp add session tunnel_id 100 session_id 300 peer_session_id 300`

Show

`ip l2tp show tunnel`

### Network Namespace

Skapa VRF, assigna interface och sätt adress

`ip netns add MGMT`
`ip link set eth1 netns MGMT`
`ip netns exec MGMT ip addr add 10.0.0.101/24 dev eth1`
`ip netns exec MGMT ip route add default via 10.0.0.1`
`ip netns list`

### Subinterface

`ip link add link eth1 name eth1.20 type vlan id 20`
`ip address add 192.168.20.1/24 dev eth1.20 `
`ip link set eth1.20 up`

### MAC VLAN

Med MAC VLAN kan man assigna flera MAC-adresser till samma interface.
Man kan uppnå samma resultat som med [Bridge](/Bridge "wikilink") men
det är mer light-weight. Det kan skapas i 4 modes: private, vepa, bridge
eller passthru beroende på säkerhetskraven. Det går att köra MAC VLAN
tillsammans med [KVM](/KVM "wikilink").

`ip link add link eth0 mac0 type macvlan`

### Blackhole

Discard traffic sent to unwanted destinations

`ip route add blackhole 192.168.2.0/30`

### Configuration Caching

Ska man flytta en IP-adress från ett interface till ett annat är det bra
att flusha cachen emellan för att säkerställa att det inte hänger kvar
något.

`ip a flush dev `<OLD-device>

ss
--

Socket statistics. Användbart och lättmemorerat kommando som ersätter
netstat:

`ss -tulpan`

tc
--

Traffic control. Command wrapper: tcconfig.

**Network Emulator**
Delay

`tc qdisc change dev eth0 root netem delay 100ms 20ms distribution normal`

Packet loss

`tc qdisc change dev eth0 root netem loss 0.3% 25%`

Reorder

`tc qdisc change dev eth0 root netem delay 10ms reorder 25% 50%`

Policing

`tc qdisc add dev eth0 root tbf rate 2mbit burst 32kbit latency 600ms`

Show config

`tc qdisc show dev eth0`

Clear config

`tc qdisc del dev eth0 root`

[Category:Tools](/Category:Tools "wikilink")