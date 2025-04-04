---
title: Cisco NAT
permalink: /Cisco_NAT/
---

Network Address Translation används för att skriva om adresser i
IP-paket. Det är inte säkert att NAT fungerar tillsammans med ACL:er som
använder **log** så det bör man ha i åtanke. För att accelerera
NAT-processen finns **ip nat create flow-entries** som är påslaget
default i [IOS](/Cisco_IOS "wikilink")-routrar.

Generell metod för att testa om NAT fungerar.

`debug ip nat`
`telnet 1.1.1.1 `
`who`

Dynamic NAT
-----------

### NAT Overload

Alla adresser göms bakom en IP-adress, kallas även PAT.

`access-list 10 permit [ip-address] [wildcard-mask]`
`ip nat inside source list 10 interface [outside-interface] overload`

Man kan även skapa en pool med endast en ip adress och köra overload på
den.

Verify

`show ip nat translations`
`show ip nat statistics`

### Default Interface

NAT Default interface innebär att all trafik som initieras utifrån och
natas in går till en och samma IP men däremot kan trafik som initieras
inifrån hide natas till interface IP (nat overload).

`ip access-list standard ALL`
` permit any`
`ip nat inside source list ALL interface Gi2 overload`
`ip nat inside source static 172.16.0.20 interface Gi2`

### NAT Pool

`interface Gi0/1`
` ip address 100.10.10.10 255.255.255.0`
` ip nat outside`
`interface Gi0/2`
` ip address 192.168.0.1 255.255.255.0`
` ip nat inside`

`ip access-list standard CLIENT-LIST`
` permit 192.168.0.0 0.0.0.15`

`ip nat pool DYNAMIC 100.10.10.17 100.10.10.19 prefix-length 29`
`ip nat inside source list CLIENT-LIST pool DYNAMIC`

Interface IP ska ej ingå i NAT-poolen däremot bör netmask/prefix-length
inrymma alla adresser i poolen.

Verify

`show ip nat translations`
`show ip nat pool name DYNAMIC`
`show ip nat translations filter range inside global 100.10.10.17 100.10.10.19 total`

### TCP Load Distribution

Man kan gömma flera servrar bakom en ip-adress för att tillhandahålla
lastdelning. Det görs med en rotary address pool samt en acl som anger
den IP som man ska gå emot från outside. Både standard och extended acl
fungerar. När paket/sessioner på ett NAT outside interface träffar
acl:en så översätts det till en av adresserna från poolen enligt
round-robin.

`ip nat pool ROTARY prefix-length 24 type rotary`
` address 10.0.0.10 10.0.0.10`
` address 10.0.0.11 10.0.0.11`
` address 10.0.0.12 10.0.0.12`

`ip access-list extended DISTRIBUTE_LOAD`
` permit tcp any host 100.10.10.15 eq www`

`ip nat inside destination list DISTRIBUTE_LOAD pool ROTARY`

Static NAT
----------

1:1 NAT

`interface Gi0/1`
` ip address 100.10.10.10 255.255.255.0`
` ip nat outside`
`interface Gi0/2`
` ip address 192.168.0.1 255.255.255.0`
` ip nat inside`

NAT

`ip nat inside source static 192.168.0.20 100.10.10.20 [no-alias]`

*Med no-alias besvaras inte ARP-förfrågningar för den IP-adressen på
utsidan.*

Verify

`show ip nat translations`
`show ip nat statistics`
`show ip alias`

*DYNAMIC är IP-adresser som används för NAT.*

### Static PAT

`interface Gi0/1`
` ip address 100.10.10.10 255.255.255.0`
` ip nat outside`
`interface Gi0/2`
` ip address 192.168.0.1 255.255.255.0`
` ip nat inside`

PAT / port forward.

`ip nat inside source static tcp 192.168.0.55 80 100.10.10.10 80`

Verify

`show ip nat translations`
`show ip aliases`

### Static Extendable NAT

Om man vill ha flera ip-adresser som ska natas till samma inside IP.

`ip nat inside source static 10.1.1.1 20.0.0.20 extendable`
`ip nat inside source static 10.1.1.1 20.0.0.30 extendable`

### Static Policy NAT

Policy NAT använder route-maps. Med set interface kan man bestämma
vilket interface paketen ska skickas ut på och därmed natas.

`interface Gi0/0`
` ip nat outside`

`ip access-list extended TO_OUTSIDE`
` permit ip 192.168.0.0 0.0.0.255 any`

`route-map TO_ISP1 permit 10`
` match ip address TO_OUTSIDE`
` set interface Gi0/0`

`ip nat inside source route-map TO_ISP1 interface Gi0/0 overload`

Man kan också låta routingtabellen styra och sedan NATa utifrån vilket
interface som är egress.

`route-map TO_ISP1 permit 10`
` match interface Gi0/0`

`route-map TO_ISP2 permit 10`
` match interface Gi0/1`

`ip nat inside source static 192.168.0.10 100.10.10.10 route-map TO_ISP1`
`ip nat inside source static 192.168.0.10 100.20.20.20 route-map TO_ISP2`

Reversible NAT
--------------

Man kan konfigurera nat som endast funkar efter att ha blivit initierad
från andra hållet.

`ip nat pool POOL 100.10.10.15 100.10.10.19 netmask 255.255.255.0`
`ip nat inside source route-map ROUTE-MAP pool POOL `**`reversible`**` `

Dubbel-NAT
----------

Har man överlappande subnät får man antingen NATa på båda sidorna eller
bara ena. I detta exemplet kommunicerar 172.20.0.10 (server1) mot ip
172.20.0.50 som natas till 30.0.0.5 (server2) medans server2 ser server1
från 30.0.0.50.

`ip nat inside source static 172.20.0.10 30.0.0.50`
`ip nat outside source static 30.0.0.5 172.20.0.50 add-route`

Utan add-route måste en statisk route användas för att peka 172.20.0.50
till outside interface.

`show ip nat translations`

Stateful NAT
------------

Stateful NAT with [HSRP](/Cisco_HSRP "wikilink"). During failovers, NAT
translated IP addresses on devices may be different from the IP address
before the failover, because no state information is exchanged between
active and standby devices. HSRP Virtual IP Address (VIP) cannot be used
by NAT pools.

`interface gi2`
` standby 100 name SNAT`
`ip nat stateful id 1 redundancy SNAT mapping-id 10`
`ip nat pool SNATPOOL 10.1.1.1 10.1.1.9 prefix-length 24`
`ip nat inside source route-map ROUTE-MAP pool SNATPOOL mapping-id 10 overload`

Primary

`ip nat stateful id 1 primary 10.10.10.10 peer 10.22.22.22 mapping-id 10`

Backup

`ip nat stateful id 1 backup 10.2.2.2 peer 10.10.10.10 mapping-id 10`

Verify

`show ip snat distributed verbose`

NVI
---

Med Nat Virtual Interface kan man adressöversätta mellan VRF:er och man
använder inte *inside* och *outside* med denna metod. NAT Virtual
Interfaces are not supported in the Cisco IOS XE software.

`interface Gi0/1`
` ip nat enable`
`interface Gi0/2`
` ip nat enable`

`ip nat source static 192.168.0.1 100.10.10.10`

Show

`show ip nat nvi translations`
`show ip nat translations verbose`

IPv6
----

NAT – Protocol Translation kan användas vid IPv4 till IPv6 migreringar
och ger bi-directional connectivity mellan domänerna.

`interface gi 0/0`
` ipv6 nat`
`interface gi 0/1`
` ipv6 nat`
`ipv6 nat v6v4 source 3001:11:0:1::1 150.11.3.1`
`ipv6 nat v4v6 source static 150.11.2.2 2000::960b:0202`
`ipv6 nat prefix 2000::/96`

NAT-PT kräver ett /96 prefix

Verify

`show ipv6 nat translations`

**NPTv6**
IPv6-to-IPv6 Network Prefix Translation är NAT från IPv6 till IPv6.
Eftersom det finns en 1:1-relation mellan inside och outside prefix
behöver inte routern hålla något state i data plane för NAT:en. Detta
underlättar multihoming.

`nat66 prefix 2002:ABC1::/64 Outside 2002:ABC2::/64`

`interface GigabitEthernet0`
` nat66 inside`
`interface GigabitEthernet1`
` nat66 outside`

Verify

`show nat66 prefix`
`show nat66 statistics`

CGNAT
-----

Carrier-grade NAT är large-scale NAT (LSN), det kan vara NAT44, NAT64
och/eller NAT66. Nyckeln till att kunna hantera fler NAT-sessioner än
vanligt är att ingen information om destination lagras. CGNAT enableas
globalt, dvs man kan inte köra annan NAT samtidigt.

`ip nat settings mode cgn`

Dynamic Port Address CGNAT

`ip nat settings pap`
`ip nat pool PUBLIC-POOL 1.1.1.10 1.1.1.20 prefix-length 24`
`ip nat inside source list NAT-ACL pool PUBLIC-POOL overload`
`ip access-list extended NAT-ACL`
` permit ip 10.0.0.0 0.255.255.255 any`

MPLS VPN
--------

NAT-integration med MPLS VPN tillåter flera MPLS VPN att konfigureras
att fungera tillsammans på samma enhet. NAT kan skilja på vilken VPN den
får in trafik på även om alla använder samma IP-adresser. Detta låter
flera kunder använda samma services men ändå vara skiljda logiskt. Se
även [Cisco MPLS](/Cisco_MPLS "wikilink").

`interface Gi0/1`
` ip address 100.10.10.10 255.255.255.0`
` ip nat outside`
`interface Gi0/2`
` vrf forwarding VPN1`
` ip address 192.168.0.1 255.255.255.0`
` ip nat inside`
`interface Gi0/3`
` vrf forwarding VPN2`
` ip address 192.168.0.1 255.255.255.0`
` ip nat inside`

`access-list 1 permit 192.168.0.0 0.0.255.255`
`ip nat pool SHARED 100.10.10.20 100.10.10.40 netmask 255.255.255.0`

`ip nat inside source list 1 pool SHARED vrf VPN1 overload`
`ip nat inside source list 1 pool SHARED vrf VPN2 overload`

`ip route vrf VPN1 0.0.0.0 0.0.0.0 Gi0/1 100.10.10.1`
`ip route vrf VPN2 0.0.0.0 0.0.0.0 Gi0/1 100.10.10.1`

Verify

`show ip nat translations vrf VPN1`

[Category:Cisco](/Category:Cisco "wikilink")