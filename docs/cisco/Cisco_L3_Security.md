---
title: Cisco L3 Security
permalink: /Cisco_L3_Security/
---

Huvudartikel: [Cisco Security](/Cisco_Security "wikilink")

Se även [Cisco L2 Security](/Cisco_L2_Security "wikilink").

### Routing

Tillåt ej IP options och source routing är bra praktik!

`ip options drop`
`no ip source-route`

Notera att "ip options drop" kan störa ut IGMP.

ACL
---

Accesslistor finns i flera olika varianter förutom standard och
extended.

**Logging**
Access list logging interval (milliseconds) & log-update threshold
(number of hits)

`ip access-list logging interval 1000`
`ip access-list log-update threshold 10`

**Reflexive ACL**
För att använda reflexive ACL behövs det en ACL för inbound traffic, en
för outbound och en reflexive för att hålla koll på dynamic entries.
Några begränsningar är att trafik endast kan initieras från ena sidan
och det går inte ge olika trafikklasser olika access. Trafik initierad
lokalt i routern behandlas ej heller. Det funkar inte heller med
applikationer som jobbar med olika portnummer, t.ex. FTP.

`ip access-list extended Egress`
` permit ip any any reflect Mirror`
`ip access-list extended Ingress`
` evaluate Mirror`
` deny ip any any`

`interface gi0/1`
` description Outside`
` ip access-group out Egress`
` ip access-group in Ingress`

Timeout

`ip reflexive-list timeout 30`

Verify

`show ip access-lists Mirror`
`show ip access-lists`

**IPv6**
För IPv6 finns det endast extended named ACL:er. Wildcard mask används
inte heller utan det är CIDR notation som gäller.

`ipv6 access-list Deny_ABC`
` deny ipv6 2001:A:B:C::/64 any`
` permit ipv6 any any`

`interface Gi0/1`
` ipv6 traffic-filter Deny_ABC out`

`show ipv6 access-list`

**Lock and Key** (Dynamic ACLs)
Lock and key configuration starts with the application of an extended
ACL to block traffic through the router. Users that want to traverse the
router are blocked by the extended ACL until they Telnet to the router
and are authenticated. The Telnet connection then drops and a
single-entry dynamic ACL is added to the extended ACL that exists. This
permits traffic for a particular time period; idle and absolute timeouts
are possible.

`username DYN autocommand access-enable timeout 5`

`ip access-list extended 100 `
` permit tcp 10.0.0.0 0.0.0.255 host 10.0.0.1 eq telnet`
` dynamic DYN timeout 5 permit ip 10.0.0.0 0.0.0.255 any`

**Turbo ACL**
The turbo ACL feature is designed in order to process ACLs more
efficiently in order to improve router performance. Found only on
high-end platforms.

`show access-list compiled`

CBAC
----

Context-Based Access Control tillhandahåller stateful packet inspection
på IOS-enheter. Man väljer vilka protokoll som ska inspekteras, det
finns många protokoll default. Detta är ett konfigurationsexempel för
ett interface som endast ska släppa in webbtrafik initierad från
insidan.

`ip access-list extended DENY_ALL`
` deny ip any any`
`ip inspect name Web http`
`ip inspect name Web https`

`interface gi0/0`
` description Outside`
` ip access-group DENY_ALL in`
` ip inspect Web out`

Verify

`show ip inspect all`
`show ip inspect sessions`

Vill man att CBAC ska inspektera protokoll som inte använder
standardportar kan lägga till dessa med port-map-kommandot.

`ip port-map http port tcp 8081`
`ip port-map smtp port tcp 2500`

`show ip port-map`

ZFW
---

Zone-based policy firewall är stateful packet inspection som är en
vidareutveckling av CBAC. Det är
[VRF](/Cisco_Routing#VRF "wikilink")-aware och man skapar zoner som man
binder ett eller flera interface till. Default skapas det en "self"-zon
som allt till och från tillåts samt att trafik mellan interface i samma
zon tillåts. Konfigurationssyntaxen som används kallas Cisco Policy
Language. ZFW kan inte inspektera
[multicast](/Cisco_Multicast "wikilink") eller
[MPLS](/Cisco_MPLS "wikilink")-trafik men det går att att köra ZFW i
transparent mode samt att man kan policea trafiken.

`zone security INTERNET`
`zone security INSIDE`
`interface Gi1`
` zone-member security INTERNET`
`interface Gi2`
` zone-member security INSIDE`

Bind ihop zonerna och ange source zon.

`zone-pair security ZONE-PAIR source INSIDE destination INTERNET`
` service-policy type inspect INSIDE-TO-INTERNET`

För att tillåta trafik mellan zoner måste en policy skapas. ZFW inspect
class-map kan matcha: access-groups, class-maps, group-objects och
protokoll.

`class-map type inspect match-any ALLOW-TRAFFIC`
` match protocol icmp`
` match protocol dns`
` match protocol http`

`policy-map type inspect INSIDE-TO-INTERNET`
` class type inspect ALLOW-TRAFFIC`
`  inspect`
` class class-default`
`  drop`

Verify

`show zone-pair security`
`show policy-map type inspect zone-pair`
`show policy-firewall config `
`show policy-firewall session zone-pair ZONE-PAIR`

**High Availability**
ZFW stödjer HA och session state replikeras för inspect actions mellan
ACTIVE och STANDBY. Dock görs det endast för L4 protokoll TCP/UDP så
ingen ICMP eller L7 inspections. Enheten med högst prio blir ACTIVE, vid
lika avgör högsta IP på control link.

`interface GigabitEthernet0/1`
` description Control link`
` ip address 10.1.1.2 255.255.255.0`

`parameter-map type inspect global`
` redundancy`

`redundancy`
` application redundancy`
`  group 1`
`   name ZFW`
`   preempt`
`   priority 100`
`   control GigabitEthernet0/1 protocol 1`
`   data GigabitEthernet0/1`

Verify

`show redundancy application group 1`

uRPF
----

Unicast Reverse Path Forwarding är en mekanism som förhindrar spoofing
attacks. Source-adressen på paket som kommer in kollas och jämförs mot
den egna FIB:en för att säkerställa att paketen kommer in på det
interface som routern själv hade använt för att nå den adressen.
[CEF](/Cisco_CEF "wikilink") är därför ett prereq för uRPF. uRPF finns i
två modes och tar hänsyn till equal och unequal cost load sharing. Om
default-routen också ska användas vid kontrollen måste **allow-default**
sättas efter interface-kommandot.

**Strict mode**, fungerar såklart inte med asymmetric routing.

`ip verify unicast source reachable-via rx`

Med **Loose mode** räcker det att sourcen är reachable via något
interface.

`ip verify unicast source reachable-via any`

uRPF exemptions, vill man inte kontrollera all trafik kan man matcha
RPF-checken mot en ACL, dvs permita det som RPF inte ska bry sig om att
droppa om det inte klarar checken.

`ip verify unicast source reachable-via rx `<ACL>` `

Verify

`show ip traffic`
`show ip verify source`

Trick för att logga all packets med spoofed sources.

`access-list 100 deny ip any any log`
`interface GigabitEthernet0/1`
` ip verify unicast source reachable-via any 100`

IPSG
----

IP Source Guard hjälper till att skydda mot IP spoofing. Det
konfigureras på access-lagret och använder sig av [DHCP
Snooping](/Cisco_DHCP#Snooping "wikilink")-databasen för att dynamiskt
skapa IP/MAC ACL:er per switchport och allt som inte träffar ACL:en
droppas silently. Det enda som tillåts är paket med den source som
matchar den DHCP snooping binding som finns för porten. Man kan också
sätta upp statiska IP binding entries för hostar som inte använder DHCP.
IPSG kan kontrollera IP-adresser eller både IP-adresser och
MAC-adresser. Det bör konfigureras konsekvent på alla accessportar på
network edge.

Prereq, DHCP Snooping måste faktiskt vara påslaget även om man bara
använder manuella bindings.

`ip dhcp snooping`
`ip dhcp snooping vlan 10`

**L3 check**

`interface gi0/7`
` ip verify source`

**L3+L2 check**

`interface gi0/7`
` switchport port-security`
` ip verify source port-security`

Static binding

`ip source binding 0011.2233.4455 vlan 10 172.20.0.10 int gi0/7`

Verify

`show ip verify source`
`show ip source binding`

[Category:Cisco](/Category:Cisco "wikilink")