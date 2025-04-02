---
title: Cisco DHCP
permalink: /Cisco_DHCP/
---

Dynamic Host Configuration Protocol (RFC 2131) är ett protokoll som
dynamiskt distribuerar nätverkskonfiguration.

**Bakgrund**
DHCP har utvecklats från Bootstrap protocol (RFC 951) som i sin tur har
utvecklats pga tillkortakommanden hos Reverse ARP. Alla tre protokoll
bygger på att klienten initialt broadcastar en discovery och servern
svarar med en IP-adress. RARP fungerar precis som ARP men frågar efter
sin egen MAC-adress och har satt IP till 0.0.0.0. Servern måste vara
förkonfigurerad med klientens MAC-adress och en IP-adress. Servern måste
även befinna sig i samma L2-domän som klienten. BOOTP togs fram för att
förbättra processen med adresstilldelning till klienter. Det använder
helt egna meddelanden och rullar på IP och UDP. Den stora fördelen mot
RARP är att det går att tilldela klienterna subnätmask, default gateway,
DNS-servrar och boot-server (hörs på namnet att det funkar).
BOOTP-discovery går även att forwarda till andra subnät. Den stora
nackdelen är att det har samma administrativa börda som RARP, dvs alla
MAC-adresser och IP-adresser måste förkonfigureras på servern. Nästa
steg är i utvecklingen är DHCP.

DHCP använder samma format som BOOTP, dvs servrar lyssnar på UDP port 67
och klienter kommunicerar från UDP port 68, men har satsat mer på att
vara dynamisk. Det uppnås med pooler, leasing och adressåtervinning. Det
finns även extensions för att registrera klienters FQDN till DNS.

### Paket

<div class="mw-collapsible mw-collapsed" style="width:250px">

-   Discover

<div class="mw-collapsible-content">

[<File:Cisco_DHCP_Discover.png>](/File:Cisco_DHCP_Discover.png "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:250px">

-   Offer

<div class="mw-collapsible-content">

[<File:Cisco_DHCP_Offer.png>](/File:Cisco_DHCP_Offer.png "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:250px">

-   Request

<div class="mw-collapsible-content">

[<File:Cisco_DHCP_Request.png>](/File:Cisco_DHCP_Request.png "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:250px">

-   ACK

<div class="mw-collapsible-content">

[<File:Cisco_DHCP_ACK.png>](/File:Cisco_DHCP_ACK.png "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:250px">

-   Release

<div class="mw-collapsible-content">

[<File:Cisco_DHCP_Release.png>](/File:Cisco_DHCP_Release.png "wikilink")

</div>
</div>

Server
======

*Cisco IOS DHCP server*
Default är DHCP-tjänsten på och besvarar alla förfrågningar från nät som
det finns en pool för men det går att stänga av helt.

`no service dhcp`
`ip dhcp bootp ignore`

**Konfiguration**
Exclude IP Addresses, Create DHCP Address Pool, Specify the Network, Set
DNS Server, Set the Default Gateway

`ip dhcp excluded-address [start ip-address] [end ip-address]`
`ip dhcp pool [poolname]`
` network [ip-address] [subnet-mask]`
` dns-server [ip-address of primary dns-server] [ip-address of secondary dns-server]`
` default-router [ip-address]`
` lease 1  #days`
`exit`

Enskild klient, man måste matcha på client id.

`ip dhcp pool R1`
` host 10.0.0.11 255.255.255.0 `
` client-identifier 0052.31`

Man kan lägga databasen på flash.

`ip dhcp database flash:/`
`show ip dhcp database`

Verify

`show ip dhcp pool`
`show ip dhcp binding`
`show ip dhcp import`

Clear

`clear ip dhcp binding *`

Låt en IOS DHCP server acceptera requests med tomt giaddr-fält, t.o.m.
om option 82 är satt (se nedan).

`ip dhcp relay information trust-all`

IOS kommer att arpa/pinga en pool-adress innan den assignas till en
klient. Om det inte besvaras antar DHCP-servern att adressen är ledig
och kan därmed dela ut den till en klient. Default är 2 stycken pings
men det går att stänga av.

`ip dhcp ping packets 0`

**IOS AutoInstall**
ip dhcp pool SWITCH-DEPLOY

` network 10.0.0.0 255.255.255.0`
` option 150 ip 10.1.1.10`
` option 67 ascii configs/base_config.txt`

Klient
======

Client-Identifier är default en kombination av hardware address,
interface name och cisco. Detta id görs om till en HEX-sträng som
presenteras för servern.

`interface Ethernet 1`
` ip dhcp client client-id ascii R1`
` ip address dhcp`

Verify

`show dhcp lease`

**Release & Renew**
Release-kommandot gör att det skickas 3 stycken Release-meddelanden
unicast till DHCP-servern. När renew-kommandot används skickar klienten
en unicast DHCP Request, gällande samma IP, till servern som då kan
välja att acka det eller ej.

`release dhcp ethernet 3/1`
`renew dhcp ethernet 3/1`

**Broadcast**, bestäm om broadcastbiten ska vara satt till 1 eller 0,
dvs att DHCP-svaren skickas tillbaka med broadcast eller unicast.
Default är detta påslaget till skillnad från många andra operativsystem.

`ip dhcp-client broadcast-flag`

**AD**, konfigurera vad default routen man får med DHCP ska ha för
administrative distance. Default är 254.

`ip dhcp-client default-router distance <1-255>`

Relay
=====

Gör om broadcast till unicast vilket möjliggör att man kan ha en central
DHCP-server istället för en på varje nät. Relay måste ha interface-konf
*ip dhcp relay information trusted* för att acceptera paket med option
82 satt, av t.ex. en switch.

`interface Ethernet 1`
` ip helper-address 10.0.0.10`

Allows the DHCP relay agent to switch the gateway address (giaddr field
of a DHCP packet) to secondary addresses when there is no DHCPOFFER
message from a DHCP server.

`ip dhcp smart-relay`

Verify

`show ip helper-address`

Snooping
========

DHCP snooping är en säkerhetsmekanism för att filtrera bort untrusted
DHCP-paket och hålla koll på klienter genom att lyssna på DHCP-trafik
och bygga en DHCP snooping binding database. Snooping hindrar rogue DHCP
servers från att svara på requests och skyddar mot klienter som begär
väldigt många leases, dvs DOS-attack. Det kollar också att MAC-adressen
i DHCP-paketet matchar adressen det kommer ifrån samt kollar om release
och decline kommer in på rätt portar enligt binding database. Paket som
inte kommer från rätt port filtreras. Vissa andra säkerhetsmekanismer
använder sig av informationen i snooping binding database, se [IP Source
Guard](/Cisco_L3_Security#IPSG "wikilink") och [Dynamic ARP
Inspection](/Cisco_L2_Security#DAI "wikilink").

Man måste slå på Switch DHCP snooping och sedan DHCP snooping för varje
vlan man vill skydda.

`ip dhcp snooping`
`ip dhcp snooping vlan 10`

Globala default-inställningar

`no ip dhcp snooping information option allow-untrusted`
`ip dhcp snooping information option`
`no ip dhcp snooping database `
`ip dhcp snooping database write-delay 300`
`ip dhcp snooping database timeout 300`
`ip dhcp snooping verify mac-address`
`ip dhcp snooping verify no-relay-agent-address`

De interface som har en legit DHCP-server måste trustas. Man kan även
sätta en rate limit på DHCP-paket.

`interface gi1`
` ip dhcp snooping trust`
` ip dhcp snooping limit rate 10`

Stäng av option 82 om servern ej accepterar requests med giaddr 0.0.0.0.
Om en router ser option 82 förväntar den sig non-zero giaddr.

`no ip dhcp snooping information option`

Lägg databasen i en fil

`ip dhcp snooping database flash:/snooping.db`

Har man flera switchar i sin topologi måste downstream-portas trustas
också (alternativt att option 82 stängs av).

`ip dhcp snooping information option allow-untrusted`

Verify

`show ip dhcp snooping`

Recovery

`errdisable recovery cause dhcp-rate-limit `

### Option 82

DHCP Relay Agent Information Option (RFC 3046) är framtaget för att låta
relay agent skicka med circuit specific information i requesten som
forwardas till DHCP-servern. Det som skickas med är exempelvis vilken
ethernetport i switchen som requesten kom in på och mac-adress på
relayen. Det är påslaget default om man kör DHCP snooping vilket innebär
att denna information samt giaddr 0.0.0.0 läggs till DHCP-paketen men
det går att stänga av med *no ip dhcp snooping information option*.

[<File:Cisco_DHCP_Option82.png>](/File:Cisco_DHCP_Option82.png "wikilink")

DHCPv6
======

Med DHCPv6 används UDP port 546 för klienter och port 547 för servrar.
Default gateway annonseras inte av DHCP utan det sköts av RA.
DHCP-paketen har också uppdaterade namn:

-   **Solicit:** Sent by a client to locate servers (FF02::1:2).
-   **Advertise:** Sent by a server in response to a Solicit message to
    indicate availability.
-   **Request:** Sent by a client to request addresses or configuration
    settings from a specific server.
-   **Reply:** Sent by a server to a specific client in response to a
    Solicit, Request, Renew, Rebind, Information-Request, Confirm,
    Release, or Decline message.

DHCPv6 rapid configuration only uses the Solicit and Reply message.

`ipv6 dhcp server DHCP_POOL rapid-commit`

All_DHCP_Servers multicast group FF05::1:3.

`ipv6 dhcp server join all-dhcp-servers`

### Stateful

Functions exactly the same as IPv4 DHCP in which hosts receive both
their IPv6 address and additional parameters from the DHCP server.

`ipv6 dhcp pool STATEFUL`
` address prefix 10::/64`
` dns-server 2001:4860:4860::8888`
` domain-name hackernet.se`

Interface

`interface gi2`
` ipv6 address 10::1/64`
` ipv6 dhcp server STATEFUL`
` ipv6 nd managed-config-flag`
` ipv6 nd prefix 10::/64 14400 14400 no-autoconfig`

**managed-config-flag** sätter en flagga i RA som säger att hostarna kan
använda DHCPv6. **no-autoconfig** säger att stateless configuration inte
ska användas.

### Stateless

SLAAC is used to get the IP address and DHCP is used to obtain “other”
configuration options, usually things like DNS, NTP, etc.

`ipv6 dhcp pool STATELESS`
` dns-server 2001:4860:4860::8888`
` domain-name hackernet.se`

Interface

`interface gi2`
` ipv6 address 10::1/64`
` ipv6 dhcp server STATELESS`
` ipv6 nd other-config-flag`

Verify

`show ipv6 dhcp pool`

### Client

DHCPv6 client, server, och relay-funktionalitet är mutually exclusive på
ett interface.

`interface gi3`
` ipv6 enable `
` ipv6 address dhcp`

Verify

`show ipv6 dhcp interface`

### Prefix Delegation

DHCPv6 Prefix Delegation kan användas för att mangera adresser på länkar
och subnät och använder sig av prefix delegation options i DHCP-paketen.
DHCPv6 client application frågar efter PD, det fungerar både med
stateful och stateless. Man har vanligtvis /56-prefix på servern och
sedan kan klienten dela upp det och använda för att assigna /64-nät på
flera av sina interface.

-   **IANA**: Identity Association for Non Temporary address
-   **IAPD**: Identity Association for Prefix Delegation

Server

`ipv6 local pool PREFIX1 2001:192:168::/48 56`
`ipv6 dhcp pool POOL`
` prefix-delegation pool PREFIX1`

`interface gi2`
` ipv6 dhcp server POOL`

Klient

`interface gi2`
` description Uplink to DHCP server`
` ipv6 dhcp client pd SERVER_PREFIX`

`interface gi3`
` ipv6 address SERVER_PREFIX ::1:0:0:0:101/64`
`interface gi4`
` ipv6 address SERVER_PREFIX ::2:0:0:0:101/64`

NX-OS
=====

`feature dhcp`

**Relay**

`interface vlan 15`
` ip dhcp relay address 10.0.0.10`

Verify

`show ip dhcp relay`

Smart relay

`ip dhcp smart-relay global`

NX-OS har stöd för olika Option 82 suboptions när DHCP-paket skickas
till DHCP-server.

`ip dhcp relay information option`
`ip dhcp relay sub-option type cisco`
`ip dhcp relay information option vpn`

Authorized ARP
==============

Man kan låta DHCP-processen populera ARP-cachen, dvs ta
MAC-IP-mappningar från DHCP-databasen. Med Authorized ARP stängs den
vanliga dynamiska ARP:n av på interfacen.

`ip dhcp pool NAME`
` update arp`
`int gi2`
` arp authorize`
` arp timeout `<seconds>

[Category:Cisco](/Category:Cisco "wikilink")