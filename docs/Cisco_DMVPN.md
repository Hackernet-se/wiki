---
title: Cisco DMVPN
permalink: /Cisco_DMVPN/
---

Dynamic Multipoint VPN är en skalbar VPN-teknik som kan bygga tunnlar
dynamiskt. Målet är att tillhandahålla any-to-any kommunikation utan att
behöva en manuellt konfigurerad full-mesh av point-to-point tunnels.
Tekniker som används är [mGRE](/Cisco_GRE "wikilink"), NHRP och
[CEF](/Cisco_CEF "wikilink") som används i kombination med
routingprotokoll och [IPsec](/Cisco_IPsec "wikilink"). Det har bl.a.
stöd för [VRF](/Cisco_Routing#VRF "wikilink"),
[Multicast](/Cisco_Multicast "wikilink"), [QoS](/Cisco_QoS "wikilink")
och load balancing. Det går köra IPv6 över tunnlar som byggs med IPv4,
dvs private address = IPv6, NBMA address = IPv4.

### Topologier

**Hub and spoke**

-   single hub single dmvpn
-   dual hub dual dmvpn
-   server load balancing

**Dynamic Mesh**

-   dual hub single dmvpn
-   multihub single dmvpn
-   hierarchical

Varje DMVPN är ett IP-nät och man kan designa det på olika sätt. T.ex.
med dual hub single dmvpn så är hub2-router hubb men konfas också som
klient till hub1-router.

NHRP
----

Next Hop Resolution Protocol (RFC 2332). NHRP-processen på hubben agerar
server och håller databasen med de externa IP-adresserna som alla spokes
har. Varje spoke registrerar sin IP som en klient till hubben. Behöver
en spoke skicka paket till något bakom en annan spoke frågar den hubben
om den andres externa IP-adress så den kan bygga en tunnel (förslagsvis
med IPsec) direkt. För detta krävs alltså inget routingprotokoll utan
det sköts av NHRP. Man kan se NHRP som ARP fast det mappar IP till NBMA
IP istället för IP till MAC.

NHRP har stöd för autentisering, detta konfigureras under
tunnel-interfacet.

`ip nhrp authentication NHRP_AUTH_STRING`

<div class="mw-collapsible mw-collapsed" style="width:310px">

Registration request:

<div class="mw-collapsible-content">

[<File:Cisco_NHRP_Registration_Request.png>](/File:Cisco_NHRP_Registration_Request.png "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:310px">

Registration reply:

<div class="mw-collapsible-content">

[<File:Cisco_NHRP_Registration_Reply.png>](/File:Cisco_NHRP_Registration_Reply.png "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:310px">

Resolution request:

<div class="mw-collapsible-content">

[<File:Cisco_NHRP_Resolution_Request.png>](/File:Cisco_NHRP_Resolution_Request.png "wikilink")

</div>
</div>

Konfiguration
=============

DMVPN kan fungera på olika sätt och detta kallas olika faser.

Fas 1
-----

Hub and Spoke: Med Fas 1 används mGRE på hubb och p2p GRE på spokes.
Inga tunnlar sätts upp dynamiskt och all trafik går igenom hubben, enda
fördelen är något simplare konfiguration.

**Static mapping**
Hub

`interface Tunnel0`
` ip nhrp map multicast 172.16.15.X`
` ip nhrp map 192.168.0.X 172.16.15.X`

Spoke

`interface Tunnel0`
` ip nhrp map 192.168.0.X 172.16.15.2`
` tunnel destination 172.16.15.2`

**Dynamic mapping**
Hub

`interface Tunnel0`
` ip nhrp map multicast dynamic`

Spoke

`interface Tunnel0`
` ip nhrp map 192.168.0.1 172.16.15.2`
` ip nhrp nhs 192.168.0.1`
` tunnel destination 172.16.15.2`

Verify

`show dmvpn`

Fas 2
-----

Hub and Spoke with Spoke-to-Spoke tunnels: Routingprotokollet på spokes
lär sig prefix direkt av varandra på tunneln. Forwarding görs
spoke-to-spoke, man använder IGP istället för NHRP. Det finns scenarion
då CEF kan behövas stängas av på spokes. Med Fas 2 används mGRE. Fas 2
går också att köra som static och då nhrp-mappas alla grannskap
manuellt.

Hub

`interface Tunnel0`
` ip address 192.168.0.1 255.255.255.0`
` ip nhrp map multicast dynamic`
` ip nhrp network-id 1`
` tunnel source 172.16.15.2`
` tunnel mode gre multipoint`

Spoke

`interface Tunnel0`
` ip address 192.168.0.2 255.255.255.0`
` ip nhrp network-id 1`
` ip nhrp nhs 192.168.0.1 nbma 172.16.15.2 multicast`
` tunnel source 10.10.10.10`
` tunnel mode gre multipoint`

Verify

`show dmvpn`
`show ip nhrp`
`show ip nhrp nhs redundancy`
`clear ip nhrp`

*Kolla ip nhrp registration timeout ifall recovery tar lång tid efter en
clear*

Fas 3
-----

Scalable Infrastructure: Routingprotokoll på spokes pratar med hubben
för att lära sig prefix samt ha som next-hop men NHRP kickar in och
redirectar trafiken direkt mellan spokes. Med Fas 3 används mGRE. Det är
mest skalbart och CEF behöver aldrig stängas av tack vare NHRP Shortcut
eftersom CEF entry skrivs om efter redirect message. Det är inte ett
unikt meddelande i sig utan hub skickar vidare resolution request till
den spoke som är lämplig.
Hub: *ip nhrp redirect*
Spoke: *ip nhrp shortcut*

Hub

`interface Tunnel0`
` ip address 192.168.0.1 255.255.255.0`
` ip nhrp map multicast dynamic`
` ip nhrp network-id 1`
` `**`ip`` ``nhrp`` ``redirect`**
` tunnel source 172.16.15.2`
` tunnel mode gre multipoint`

Spoke

`interface Tunnel0`
` ip address 192.168.0.2 255.255.255.0`
` ip nhrp network-id 1`
` ip nhrp nhs 192.168.0.1 nbma 172.16.15.2 multicast`
` `**`ip`` ``nhrp`` ``shortcut`**
` tunnel source 10.10.10.10`
` tunnel mode gre multipoint`

Verify

`show dmvpn`
`show ip nhrp`
`show ip nhrp nhs redundancy`
`clear ip nhrp`

*Kolla ip nhrp registration timeout ifall recovery tar lång tid efter en
clear*

IPv6
----

Både underlay och overlay kan köras med IPv6. Detta är oberoende av fas.

Hub

`interface Tunnel0`
` ipv6 address 192:168:1::1/64`
` ipv6 nhrp map multicast dynamic`
` ipv6 nhrp network-id 1`
` tunnel source 2000:192:168:1::1`
` tunnel mode gre multipoint `**`ipv6`**

Spoke

`interface Tunnel0`
` ipv6 address 192:168:1::2/64`
` ipv6 nhrp network-id 1`
` ipv6 nhrp nhs 192:168:1::1 nbma 2000:192:168:1::1 multicast`
` tunnel source 2000:10:10::10`
` tunnel mode gre multipoint `**`ipv6`**

Verify

`show dmvpn ipv6`
`show ipv6 nhrp `

IPsec
=====

Vill man skydda sin trafik kan man kryptera all tunneltrafik. Se även
[Cisco IPsec](/Cisco_IPsec "wikilink").

`crypto isakmp policy 10`
` encryption aes 256`
` authentication pre-share`
` hash sha512`
` group 14`

`crypto isakmp key SECRET address 0.0.0.0 0.0.0.0`

`crypto ipsec transform-set AES256_SHA512 esp-sha512-hmac esp-aes 256`
` mode transport`

`crypto ipsec profile DMVPN`
` set transform-set AES256_SHA512`

`interface Tunnel0`
` tunnel protection ipsec profile DMVPN`

Verify

`show crypto isakmp sa`
`show crypto ipsec sa`
`show crypto socket`
`show crypto map`

För att effektivisera krypteringen på en hub när man kör dual dmvpn kan
man använda en delad socket för crypto-anslutningarna.

`tunnel protection ipsec profile DMVPN `**`shared`**

GDOI-based DMVPN
----------------

Med vanlig DMVPN sätts det upp en permanent IPsec-tunnel mellan hubb -
spoke och dynamiska tunnlar mellan spokes. När en spoke-to-spoke tunnel
sätts upp blir det lite delay pga IPSec negotiation, för att slippa det
kan man använda GDOI. Då är hubb och spokes Group Members. Group Keys
och security policies distribueras till GMs av Key Server som t.ex. kan
vara en separat IOS-router bakom hubb. Se även [GET
VPN](/Cisco_IPsec#GET_VPN "wikilink").

Key Server

`crypto key generate rsa general-keys label GDOI modulus 2048 exportable`

`crypto isakmp policy 10`
` authentication pre-share`

`crypto isakmp key 0 SECRET address 2.2.2.2`
`crypto isakmp key 0 SECRET address 3.3.3.3`
`crypto isakmp key 0 SECRET address `<next spoke>

`crypto ipsec transform-set PHASE2 esp-aes esp-sha-hmac`

`crypto ipsec profile GDOI_PROFILE`
` set transform-set PHASE2`

`ip access-list extended ACL_GRE`
` permit gre any any `

`crypto gdoi group GDOI_GROUP`
` identity number 123`
` server local`
`  rekey transport unicast`
`  rekey authentication mypubkey rsa GDOI`
`  rekey retransmit 60 number 2`
`  sa ipsec 1`
`   profile GDOI_PROFILE`
`   match address ipv4 ACL_GRE`
`   replay time window-size 5`
`  address ipv4 1.1.1.1 `

Hubb och Spoke

`crypto isakmp policy 10`
` authentication pre-share`

`crypto isakmp key 0 SECRET address 1.1.1.1`

`crypto gdoi group GDOI`
` identity number 123`
` server address ipv4 1.1.1.1 `

`crypto map DMVPN local-address Loopback0`
`crypto map DMVPN 10 gdoi`
` set group GDOI`

`interface Gi2`
` description Tunnel Source`
` crypto map DMVPN`

Verify

`show crypto gdoi`

Routingprotokoll
================

**EIGRP**
Med Fas 1 kan man antingen stänga av split-horizon eller skicka en
default route från hub.

Med EIGRP i Fas 2 måste man stänga av split-horizon och next-hop-self på
tunnel-interfacet för att uppdateringar och routing mellan spokes ska
funka. Nackdelen är att man inte kan summera routes på hub utan att
bryta spoke-to-spoke-kommunikation utan då måste allt gå igenom hub.

`interface Tunnel0`
` no ip next-hop-self eigrp 100`
` no ip split-horizon eigrp 100`

Med fas 3 kommer endast det första paketet att gå via hub tack vare nhrp
redirect/shortcut och man kan skicka ut aggregerade routes på hub utan
att påverka spoke-to-spoke. Detta är bra design.

**OSPF**
Det går att använda point-to-multipoint på hubbens tunnel-interface och
p2p på spoksen bara man ser till att timers matchar. Alternativt kan man
köra *ip ospf network non-broadcast* på alla. Alternativt *broadcast*
bara man ser till att hubb är DR. Det man bör ha i åtanke är att
beroende på nätverkstyp så ändras next-hop eller ej. OSPF är inget
optimalt protokoll för DMVPN.

Hub

`interface Tunnel0`
` ip ospf network broadcast`
` ip ospf priority 255`

Spoke, ska inte vara med i DR-election.

`interface Tunnel0`
` ip ospf network broadcast`
` ip ospf prio 0`

**BGP**
Med Fas 1 och BGP måste next-hop-self användas på alla grannskap.

Fas 2 och BGP-konfiguration är som vanligt men för eBGP mellan spokes
måste multihop användas.

`neighbor 2.2.2.2 ebgp-multihop 2`

**RIP**
Med Fas 1 och RIP behöver split horizon stängas av på hubb.

Others
======

### Monitoring

Man kan övervaka sitt DMVPN med hjälp av [SNMP](/Cisco_SNMP "wikilink").

`snmp-server enable traps nhrp nhs`
`snmp-server enable traps nhrp nhc`
`snmp-server enable traps nhrp nhp`

När man använder *if-state nhrp* på en spoke kan den kolla om
NHRP-registreringen fungerar och på så sätt veta om interfacet ska vara
up eller ej när man kör fas 2 eller 3. Detta fungerar ej på hub
interface för det gör ingen registrering utan är alltid up.

`interface tun0`
` if-state nhrp `

På nyare IOS (XE 16.3) kan man även använda [BFD](/Cisco_BFD "wikilink")
för snabbare feldetektering och NHRP kan då registrera sig som klient
till BFD-processen.

`interface Tunnel0`
` bfd interval 1000 min_rx 1000 multiplier 5`

`router eigrp 1`
` bfd interface Tunnel0`

`show nhrp interfaces   #hidden`

### NAT

Man kan köra all sorts nat på spokes men på hubb fungerar endast static
nat. Om en spoke befinner sig bakom dynamisk nat, dvs att dennes
NBMA-adress kan ändras så kan man stänga av unique flag i
NHRP-registreringen. Detta görs med *ip nhrp registration no-unique* på
spoke vilket gör att den registrerade NBMA-adressen får ändras i
efterhand vilket inte är fallet default. Befinner sig två spokes bakom
PAT så kommer de ej att kunna upprätta någon spoke-to-spoke tunnel
mellan varandra. När man kör NAT med DMVPN så måste IPsec transport mode
användas. Se även [Cisco NAT](/Cisco_NAT "wikilink").

`interface tun0`
` ip nhrp registration no-unique`

### VRF

Man kan bygga det precis som man vill routingmässigt genom att separera
underlay och overlay i olika VRF:er (detta kallas också front door VRF).
Detta möjliggör t.ex. att ha default route över DMVPN utan att få
problem med recursive routing. I övrigt görs konfiguration som vanligt.

`vrf definition UNDERLAY`
` address-family ipv4`
` exit`

`crypto keyring VRF_AWARE_PSK vrf UNDERLAY`
` pre-shared-key address 0.0.0.0 0.0.0.0 key DMVPN`

`interface Tunnel0`
` tunnel vrf UNDERLAY`

Verify

`show crypto session fvrf UNDERLAY`
`show crypto session ivrf `

### MPLS

Man kan köra [MPLS](/Cisco_MPLS "wikilink") över DMVPN och därmed MPLS
VPN, detta kallas 2547oDMVPN. Det man ska tänka på är att label switch
path måste vara hub-to-spoke, dvs om man vill ha kommunikation mellan
två spokes måste det gå spoke-hub-spoke. T.ex. om man kör BGP får man
använda *next-hop-self all* för att säkerställa att MPLS VPN-trafik
alltid går igenom hub. Man förlorar dynamiska tunnlar men man kan ha
riktig PE-funkionalitet över DMVPN.

`mpls ip`
`mpls ldp router-id loopback0`

`interface tunnel0`
` mpls ip`

### Per-Tunnel QoS

Med Per-Tunnel QoS feature kan man ha en egress QoS-policy på hubb på
tunnelinstansen som man kan konfigurera antingen per endpoint eller per
spoke. Detta gör att man kan shapea trafiken till enskilda spokes med en
parent policy och sedan skilja på de individuella dataflödena i tunneln
med en child policy. Innan man konfigurerar detta måste man ha en
fungerande DMVPN-uppsättning.

Class default shaper policy map får endast innehålla class class-default
och shape-kommando.

`policy-map Parent1`
` class class-default`
`  shape average 1000000   `
`   service-policy Child1`

Man kan använda NHRP för att bära information om vilken spoke som ska ha
vilken QoS-policy. Definiera en NHRP-grupp på spokes och mappa sedan den
till en policy på hubb.

Spoke 1

`interface Tunnel0`
` ip nhrp group GROUP1`

Hub

`interface Tunnel0`
` ip nhrp map group GROUP1 service-policy output Parent1`
` ip nhrp map group GROUP2 service-policy output Parent2`

Verify

`show policy-map multipoint `
`show dmvpn detail`
`show tunnel endpoints | i Endpoint|QoS`

[Category:Cisco](/Category:Cisco "wikilink")