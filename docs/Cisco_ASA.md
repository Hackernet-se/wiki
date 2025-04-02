---
title: Cisco ASA
permalink: /Cisco_ASA/
---

Adaptive Security Appliance är Ciscos VPN- och brandväggsenhet. Detta är
skrivet för 8.4 och senare.
Hårdvara och mjukvara
[kompatibilitet](http://www.cisco.com/c/en/us/td/docs/security/asa/compatibility/asamatrx.html)

Konfiguration
-------------

Grunder

`conf t`
` hostname ASA`

IP adress

`int e0/0`
` mac-address 0011.2233.4455`
` security-level 100`
` nameif inside`
` ip address 10.0.0.1 255.255.255.0`
` no shut`

Default route och DNS

`route outside 0.0.0.0 0.0.0.0 190.10.160.1 1`
`same-security-traffic permit inter-interface`
`dns domain-lookup outside`
`dns name-server 8.8.8.8`

### ASDM

ASDM är en javamjukvara man kan använda för GUI till ASA.

`asdm image disk0:/asdm-752.bin`
`show asdm image`

Slå på det och vitlista IP/nät som får ansluta.

`http server enable`
`http 10.0.0.0 255.255.255.0 inside`

Skapa användare så att det går att logga in. Peka autentisering mot
lokal databas.

`username admin password cisco privilege 15`
`aaa authentication http console LOCAL`

### SSH

`ssh 10.0.0.0 255.255.255.0 inside`
`ssh timeout 60`
`ssh version 2`
`aaa authentication ssh console LOCAL`
`domain-name inhouse.local`
`crypto key generate rsa modulus 2048`

### Mgmt VRF

Man kan sedan 9.5 lägga management-interface i en egen routingtabell.

`int gi0/1`
` management-only`
`show route management-only`
`show asp table routing management-only`

### Management access

Vill man managera sin brandvägg genom en VPN-tunnel måste man
komplettera ssh/http-kommandon med:

`management-access inside`

### Upgrade

`copy `[`http://`](http://)`<webbserver.se>/filer/asa952-smp-k8.bin disk0:/`
`boot system disk0:/asa952-smp-k8.bin`
`show bootvar`
`wr`
`reload`

### Reset

`clear configure all`
`crypto key zeroize rsa`

Setup basic firewall

`configure factory-default`

Diverse
-------

**ICMP-inspection**
Default så är inte icmp-inspection påslaget.

`fixup protocol icmp`

Alternativt

`policy-map global_policy`
` class inspection_default`
`  inspect icmp`

**Traceroute**
Tillåt traceroute genom en ASA

`access-list ACL extended permit icmp any any time-exceeded`
`access-list ACL extended permit icmp any any unreachable`

**Accelerated Security Path**

`show asp drop`
`capture asp-drop type asp-drop all`
`show capture asp-drop`

**ARP Inspection**
Static entries

`arp inside 193.10.161.37 0c0c.0c0c.0c03 alias`
`---`

**Botnet Filtering**

`#köp licens`
`#Enable DNS Client`

**NTP**

`clock timezone CEST 1 0`
`clock summer-time CEDT recurring last Sun Mar 2:00 last Sun Oct 3:00 60`
`ntp server 94.199.180.200 source outside`
`show ntp status`

**uRPF**

`ip verify reverse-path interface outside`
`show run ip verify reverse-path`

**Logging**

`logging enable`
`logging console 4`

Om man kör syslog med TCP så slutar ASA:n att forwarda trafik om
anslutning till syslog-servern tappas, ändra detta.

`logging permit-hostdown`

**Jumbo Frames**

`jumbo frame-reservation`
`mtu inside 9000`
`mtu outside 9000`

**Global Timeouts**

`timeout xlate 10:00:00`
`timeout uauth 10:00:00 absolute`
`timeout uauth 09:00:00 inactivity`

**Certificate Management**

`show crypto ca certificate`
`(config) crypto ca export`
`show crypto key mypubkey rsa`

**Permanent Self-Signed Certificate**

`crypto ca trustpoint ASDM_TrustPoint0`
`id-usage ssl-ipsec`
`no fqdn`
`subject-name CN=ASA`
`enrollment self`
`crypto ca enroll ASDM_TrustPoint0 noconfirm`

SNMP
----

`snmp-server host inside 10.0.0.50 community PUBLIC version 2c`
`show snmp-server oidlist   #"hidden command"`

Se även [Cisco SNMP](/Cisco_SNMP "wikilink").

DHCP
----

[Cisco DHCP](/Cisco_DHCP "wikilink")

### Klient

`int e0/0`
` ip address dhcp setroute`
`exit`
`dhcp-client client-id interface outside`

### Server

`dhcpd address 10.0.0.50-10.0.0.60 inside`
`dhcpd enable inside`
`dhcpd dns 8.8.8.8 interface inside`

*OBS ASA doesn't respond to unicast dhcp requests*

### Relay

`dhcprelay server 192.168.10.11 inside`
`dhcprelay enable DMZ`

Verify

`show dhcpd state`

NAT
---

Se även [Cisco NAT](/Cisco_NAT "wikilink").

### PAT

`nat (inside,outside) 1 source dynamic any interface`

### Dynamic

`object network outside-pool`
` range 193.10.161.190 193.10.161.199`
`object network inside_10`
` subnet 10.0.0.0 255.255.255.0`
` nat (inside,any) dynamic outside-pool`

### Static

`object network dmz_global`
` host 193.10.161.31`
`object network dmz_server`
` host 172.16.0.5`
` nat (dmz,outside) static dmz_global`

### Exempt

`object network LAN1`
` subnet 1.1.1.0 255.255.255.0`
`object network LAN2`
` subnet 2.2.2.0 255.255.255.0`
`nat (inside,outside) 1 source static LAN1 LAN1 destination static LAN2 LAN2`

*1an är viktig så att regeln hamnar först*

**Verify**

`show run nat`
`show nat proxy-arp`

Port Forwarding
---------------

`object network websrv `
` host 10.1.1.3`
` nat (inside,outside) static interface service tcp 80 80`
`exit`
`access-list outside_access_in permit tcp any object websrv eq http`

### ACL

`access-list ACL1 permit tcp any object dmz_server eq http`
`access-list ACL1 line 15 permit tcp any object dmz_server eq https`
`access-group ACL1 in interface outside`
`show access-list ACL1`

Matcha på DNS-namn

`object network hackernet.se`
` fqdn v4 hackernet.se`

Routing
-------

Se även [Cisco Routing](/Cisco_Routing "wikilink").

### Static

`route inside 10.0.1.0 255.255.255.0 {next hop address} 10`

### OSPF

`router ospf 1`
` area 1`
` network 10.0.0.0 255.255.255.0 area 1`

### RIP

`router rip`
` no auto-summary`
` version 2`
` network 10.0.0.0`

### EIGRP

`router eigrp 1`
` network 10.0.0.0 255.255.255.0`

### BGP

Ska man köra BGP genom en ASA måste man stänga av att TCP option 19
strippas vilket det gör default. Samt måste TCP sequence number
randomization stängas av.

`access-list BGP extended permit tcp any eq bgp any`
`access-list BGP extended permit tcp any any eq bgp`
`tcp-map BGP`
`tcp-options range 19 19 allow`
` class-map BGP`
`  match access-list BGP`
`policy-map global_policy`
` class BGP`
`  set connection advanced-options BGP`
`  set connection random-sequence-number disable`

Modular Policy Framework
------------------------

Application Inspection

`access-list dmz_ftp permit tcp any any eq ftp`

Class Map

`class-map FTP-class-MAP`
`match access-list dmz_ftp`

Policy Map

`policy-map FTP-policy-MAP`
`class FTP-class-MAP`
`inspect ftp`

Service Policy

`service-policy FTP-policy-MAP interface dmz`

### QoS

`priority-queue inside`

Class Map

`class-map VOIP`
`match dscp 46`

Policy Map

`policy-map inside-policy`
`class VOIP`
`priority`

Service Policy

`service-policy inside-policy interface inside`

Se även [Cisco QoS](/Cisco_QoS "wikilink").

### Tweaking Connections

`access-list ACL1 permit tcp any object dmz_server eq http`
`class-map TCP-Sessions`
`match access-list ACL1`
`policy-map Conn-Limits`
`class TCP-Sessions`
`set connection conn-max 500 embryonic-conn-max 50`
`set connection timeout embryonic 0:05:00 half-closed 0:10:00`
`service-policy Conn-Limits interface outside`

### TCP Intercept

`access-list ACL1 permit tcp any object dmz_server eq http`
`class-map no-syn-flood-class`
`match access-list ACL1`
`policy-map NO-SYN-FLOOD`
`class no syn-flood-class`
`set connection embryonic-conn-max 50`
`service-policy NO-SYN-FLOOD interface outside `

### Advanced Application Inspection - HTTP

`policy-map type inspect http http-inspect-pmap`
`parameters`
`protocol-violation action dropconnection log`
`match req-resp content-type mismatch`
`drop-connection log`
`policy-map global_policy`
`class inspection_default`
`inspect http http-inspect-pmap`

### VLAN - !5505

`int e0/2`
` no shut`
`int e0/2.10`
` vlan 10`
` security-level 100`
` nameif VLAN10`
` ip add 10.0.10.1 255.255.255.0`
` no shut`
`exit`

EtherChannel
------------

Se även [Cisco EtherChannel](/Cisco_EtherChannel "wikilink").

`interface e0/2`
` channel-group mode Active`
`interface e0/3`
` channel-group mode Active`
`interface port-channel1`
` port-channel load-balance src-port`
` port-channel min-bundle 1`
` lacp max-bundle 8`
` duplex auto`
` speed auto`
` nameif DMZ`
` security-level 50`
` ip add 10.0.10.1 255.255.255.0`
` no shut`

### Redundancy

Samma som etherchannel fast endast ett ben är aktivt i taget. Användbart
om asan är kopplad till 2 switchar utan [MLAG](/Arista_MLAG "wikilink")
(t.ex. [vPC](/Nexus_vPC "wikilink")).

`interface e0/4`
` no shut`
`interface e0/5`
` no shut`
`interface redundant1`
` member interface e0/4`
` member interface e0/5`
` nameif outside`
` security-level`
` ip address 193.10.161.31`
` no shut`

Transparent - 5505
------------------

`firewall transparent`
`int BVI 1`
`ip add 193.10.161.38 255.255.255.0`
`exit`
`int e0/0`
`switchport access vlan 1`
`no shut`
`int e0/1`
`switchport access vlan 2`
`no shut`
`interface vlan 1`
`security-level 100`
`nameif inside`
`bridge-group 1`
`no shut`
`interface vlan 2`
`security-level 0`
`nameif outside`
`bridge-group 1`
`no shut`

AAA
---

`aaa-server OUR-GROUP protocol radius`
`aaa-server OUR-GROUP (inside) host 10.0.0.50`
` key ********`
` radius-common-pw *********`
` exit`

### Cut-through User AAA

`access-list outside_authentication permit tcp any object dmz-server eq http`
`username bob password cisco priv 2`
`username bob attributes`
`service-type remote-access`
`exit`
`aaa authentication match outside_authentication outside LOCAL`

Failover
--------

`#Criteria`
`ASA1`
`int e0/0`
`ip address 193.10.161.38 255.255.254.0 standby 193.10.161.39`
`int e0/1`
`ip address 10.0.0.1 255.255.255.0 standby 10.0.0.2`
`failover lan interface Fail-1 e0/3`
`failover interface ip Fail-1 10.1.1.1 255.255.255.252 standby 10.1.1.2`
`failover key cisco`
`failover link Fail-2 e0/4`
`failover interface ip Fail-2 10.2.2.1 255.255.255.252 standby 10.2.2.2`
`failover replication http`
`failover lan unit primary`
`failover mac address e0/0 0000.1111.2222 0000.3333.4444`
`failover`

`ASA2`
`int e0/3`
`no shut`
`exit`
`failover lan interface Fail-1 e0/3`
`failover interface ip Fail-1 10.1.1.1 255.255.255.252 standby 10.1.1.2`
`failover key cisco`
`failover lan unit secondary`
`failover`

Virtual Firewall
----------------

`mode multiple`
`changeto context admin`
`changeto system`
`mac-address auto`
`class silver`
`limit resource asdm 3`
`context newcontext`
`member silver`
`allocate-interface e0/3`
`allocate-interface e0/4`
`config-url disk0:/newcontext.cfg`

Save in all contexts

`wr mem all`

### Active/Active Failover

`changeto system`
`prompt hostname priority`
`failover group 1`
`primary`
`preempt 120`
`exit`
`failover group 2`
`secondary`
`preempt 120`
`exit`
`context Ctx-1`
`join-failover-group 1`
`exit`
`context Ctx-2`
`join-failover-group 2`
`exit`
`int e0/4`
`no shut`
`int e0/5`
`no shut`
`exit`
`failover lan unit primary`
`failover lan interface Fail-1 e0/4`
`failover interface ip Fail-1 10.1.1.1 255.255.255.252 standby 10.1.1.2`
`failover link Fail-2 e0/4`
`failover interface ip Fail-2 10.2.2.1 255.255.255.252 standby 10.2.2.2`
`failover`

`int e0/3`
`no shut`
`exit`
`failover lan unit secondary`
`failover lan interface Fail-1 e0/3`
`failover interface ip Fail-1 10.1.1.1 255.255.255.252 standby 10.1.1.2`
`failover`

SLA
---

`route outside 0.0.0.0 0.0.0.0 1.1.1.1 1 track 1`
`sla monitor 10`
` type echo protocol ipIcmpEcho 1.1.1.1 interface outside`
` num-packets 3`
` frequency 5`
`sla monitor schedule 10 life forever start-time now`
`track 1 rtr 10 reachability`

VPN
---

Se [ASA VPN](/Cisco_ASA_VPN "wikilink")

REST API
--------

Man kan lägga till en agent så att ASAn får ett REST API.

`copy `[`http://`](http://)<webbserver>`/asa-restapi-122-lfbff-k8.SPA disk0:`
`rest-api image disk0:/asa-restapi-122-lfbff-k8.SPA`
`rest-api agent`

Sedan behöver webbservern konfigureras om inte det är gjort, se
[ASDM](/Cisco_ASA#ASDM "wikilink")

Använd en REST-klient (Firefox/Chrome)

`https:`<asa-ip>`/api/objects/networkobjects`

### Docs

Följer med agenten

[`https://`](https://)<asa-ip>`/doc/ `

[Category:Cisco](/Category:Cisco "wikilink")