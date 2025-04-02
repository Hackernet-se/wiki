---
title: Cisco GRE
permalink: /Cisco_GRE/
---

Generic Routing Encapsulation (RFC 2784) är ett tunnlingsprotokoll
utvecklat av Cisco, det är IP-protokoll 47. Enkapsulering görs genom att
sätta på en 4 byte GRE-header på L3-paketen och sedan sätts en ny
IPv4/IPv6-header på det så att det kan routas till andra änden av
tunneln och dekapsuleras. Diverse protokoll kan tunnlas, t.ex.
[MPLS](/Cisco_MPLS "wikilink") och [IPsec](/Cisco_IPsec "wikilink").
Eftersom det är enkapsulering påverkas MTU så det bör man hålla koll på.
Däremot om man ändrar tunnel mode till "IPIP" så reducerar man
overheaden litegrann för då läggs det endast på en header istället för
två. Och vill man öka overhead kan man köra tunnel i tunnel, man kan
enkapsulera ett paket upp till fyra gånger. GRE kan även köras
multipoint, t.ex. i [DMVPN](/Cisco_DMVPN "wikilink").

### Tunnel Key

GRE Tunnel Key feature kan användas för att logiskt särskilja mellan
flera tunnlar mellan samma noder. Det gör att encapsulation router
lägger till en 4-bytes identifier i GRE-headern (tänk VLAN-taggning). Om
mottagande router ser att det är en mismatch i key value kommer paketet
att droppas.

Utan key, 4 bytes header.
[<File:Cisco_GRE.png>](/File:Cisco_GRE.png "wikilink")

Med key, 8 bytes header.
[<File:Cisco_GRE_key.png>](/File:Cisco_GRE_key.png "wikilink")

Konfiguration
=============

**R1**

`interface Tunnel0`
` ip address 10.0.0.1 255.255.255.252`
` ip mtu 1400`
` ip tcp adjust-mss 1360`
` tunnel source `<local-ip>
` tunnel destination `<R2-ip>

Väljer man ett interface som source används primary IP på det
interfacet.

**R2**

`interface Tunnel0`
` ip address 10.0.0.2 255.255.255.252`
` ip mtu 1400`
` ip tcp adjust-mss 1360`
` tunnel source `<local-ip>
` tunnel destination `<R1-ip>

Verify. Utan keepalives är ett tunnel-interface UP/UP sålänge det inte
är administratively shutdown.

`show ip int br`
`show interface | i Tunnel protocol`

### Keepalive

Eftersom en GRE-tunnel går över andra enheter och länkar måste en
keepalive skickas hela vägen mellan tunnel-interfacen för att routern
ska kunna veta om det är uppe. Detta är ej påslaget default.
Standardvärden för keepalive är 10 sekunders interval med 3 retries.
Detta fungerar med GRE-tunnlar men inte med mGRE eftersom det då inte
finns någon enskild destination att skicka keepalives till så de
interfacen är alltid UP/UP.

En keepalive är ett tomt GRE-paket till sig själv som enkapsuleras och
skickas till andra sidan. När paketet packas upp kommer
destinationsadressen att kollas upp för att avgöra vart det ska skickas
vilket resulterar i att det skickas tillbaka.
[<File:Cisco_GRE_Keepalive.png>](/File:Cisco_GRE_Keepalive.png "wikilink")

`interface Tunnel0`
` keepalive `<interval>` `<retries>

Verify

`show interface tunnel 0 | i Keepalive`

### VRF

Man kan ha tunnel-interfacet i en VRF medans tunneln själv terminerar i
en annan VRF.

`interface Tunnel0`
` vrf forwarding VRF-1`
` ip address 10.0.0.1 255.255.255.252`
` tunnel vrf VRF-2`
` tunnel source `<vrf2-ip>
` tunnel destination `<vrf2-ip>

### Recursive Routing

Tunnel Source och Destination bör alltid läras utanför tunneln. Om det
är problem med Recursive Routing kan man antingen disallow tunnel source
att annonseras med hjälp av en prefix-lista eller lägga statiska routes
med lägre AD.

*`Tunnel0`` ``temporarily`` ``disabled`` ``due`` ``to`` ``recursive`` ``routing`*

### QoS

När paket enkapsuleras och krypteras kan inte QoS-funktioner se
original-headern och klassificera det korrekt eftersom VPN och tunnel
operations appliceras innan QoS policy. Med QoS pre-classify för VPN:er
ändrar man denna ordning och paket kan klassificeras innan de tunnlas.
Man kan även klassa på annat än IP-prec eller DSCP. Se även [Cisco
QoS](/Cisco_QoS "wikilink").

Enable QoS for VPNs feature:

`interface Tunnel0`
` qos pre-classify`

### Others

Man kan koppla ihop loopback-interface med hjälp av GRE genom att sätta
tunnelinterfacen som unnumbered.

`interface Tunnel0`
` ip unnumbered Loopback0`

Drop corrupted and out-of-order VPN packets

`tunnel checksum  `
`tunnel sequence-datagrams`

IPv6
====

IPv6 går att tunnla och enkapsulering av IPv6 är IP protokoll 41.
IPv6-paket går även att tunnla över ett IPv4-nätverk med hjälp av flera
olika tekniker, IPv4 end-to-end reachability är det som krävs.

**Protokoll 41:**

<div class="mw-collapsible mw-collapsed" style="width:310px">

Över IPv6, "tunnel mode ipv6"

<div class="mw-collapsible-content">

[<File:Cisco_GRE_IPv6.PNG>](/File:Cisco_GRE_IPv6.PNG "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:310px">

Över IPv4, "tunnel mode ipv6ip"

<div class="mw-collapsible-content">

[<File:Cisco_GRE_IPv6IP.PNG>](/File:Cisco_GRE_IPv6IP.PNG "wikilink")

</div>
</div>

#### Manual tunnel

IPv6-IP-tunnlar använder IP-protokoll 41 och vill man filtrera det i en
acl får man använda protokollnumret. Detta har något lägre overhead än
GRE.

`interface Tunnel0`
` ipv6 address 10::1/64`
` tunnel source loopback0`
` tunnel destination 10.0.0.20`
` tunnel mode ipv6ip`

#### Automatic 6to4

Tanken med automatiska 6to4-tunnlar är att lösa IPv6-routing över ett
IPv4-nätverk baserat på next-hop adresser inbakade i IPv6-adressen.
IPv6-prefixet 2002::/16 är reserverat för detta ändamål och lösningen
blir point-to-multipoint natively. Destination för tunneln anges inte
manuellt utan det fås fram för varje flow som ska forwarderas genom att
ta ut 32 bitar från destination IPv6 address på de paket som kommer in
och ska till en annan IPv6-site. Det betyder att alla site prefix
inklusive adressen på tunnel-interfacet måste tas ut från den range som
är en kombination av det reserverade IPv6-prefixet och 6to4 border
routerns för övriga nåbara IPv4-adress, dvs 2002:\<32-bitar ipv4\>::/48.

`interface Loopback0`
` description Border Router IPv4 Address`
` ip address 192.168.0.1 255.255.255.255`

`interface Tunnel0`
` tunnel source Loopback0`
` tunnel mode ipv6ip 6to4`
` ipv6 address 2002:C0A8:0001::10/64`

`ipv6 route 2002::/16 tunnel 0`

#### ISATAP

Intra-Site Automatic Tunnel Addressing Protocol (RFC 5214) är framtaget
för möjliggöra IPv6-kommunikation mellan IPv4-only hosts och
IPv6-enheter. IPv4-domänen fungerar som ett multi-access segment för
IPv6 där IPv4-adresserna är endpointsen. Klienter som vill använda
ISATAP frågar sin DNS-server om A record för "ISATAP", som bör peka på
ISATAP-routern. Hosten tunnlar sedan ett router discovery packet (med
hjälp av IPv6-in-IPv4 encapsulation) och skickar det till
ISATAP-routern. Routern svarar med en RA som innehåller prefixet som ska
användas och då kan klienten sätta ihop sin egna gångbara IPv6-adress
utifrån ISATAP identifier (0000:5efe) och sin egen IPv4-adress. Adress
måste tas med hjälp av EUI-64 och då genereras interface ID automatiskt.
ISATAP är också point-to-multipoint natively

Man behöver ej ange destination address manuellt.

`interface Tunnel0`
` ip address 2001:0:0:500::/64 eui-64`
` no ipv6 nd suppress-ra`
` tunnel mode ipv6ip isatap`

Ett äldre alternativ till ISATAP är "IPv6 Automatic IPv4-compatible"
(*tunnel mode ipv6ip automatic*) men det är inte rekommenderat att köra.

#### 6RD

IPv6 Rapid Deployment (RFC 5969) är en generalisering av automatic 6to4
tunneling mechanism. Det är en stateless transition mechanism som kör
IPv4 protocol 41 (IPv6 in IPv4). Notera att MTU i en 6RD-domän måste
vara välmanagerat.

Definitioner
\* 6RD CE: "Customer Edge" router som sitter mellan IPv6-enabled LAN
site och IPv4-enabled SP network. Denna router har ett 6rd tunnel
interface som agerar endpoint för IPv6-in-IPv4 enkapsuleringen och
forwarderingen.

-   6RD Border Relay (BR): Border Relay router står hos service
    provider. Den har ett IPv4-interface, ett 6rd tunnel interface för
    multi-point tunneling och ett IPv6-interface som når IPv6-internet.
-   6RD Delegated Prefix: Detta-IPv6 prefix bestäms av CE och används av
    hostarna på LAN site. Det funkar motsvarande DHCPv6 PD prefix.
-   6RD Prefix: Detta IPv6-prefix bestäms av SP och används av hela
    6rd-domänen.
-   BR IPv4 address: Border Relays IPv4-adress. Denna adress används av
    varje CE för att skicka paket till BR som ska till
    IPv6-destinationer utanför 6rd-domänen.
-   CE IPv4 address: IPv4-adress på CE som används för IPv4
    internetaccess (t.ex. DHCP-assignad), denna kan vara global eller
    privat inom 6rd-domänen. Denna adress används för att skapa 6rd
    delegated prefix samt skicka och ta emot IPv6-paket.

**Konfiguration**
Tunnel 6rd ipv4 prefix-len 0 är default.

BR

`ipv6 general-prefix RD 6rd Tunnel0`
`!`
`interface Tunnel0`
` no ip address`
` ipv6 address RD ::/128 anycast`
` tunnel source Loopback0`
` tunnel mode ipv6ip 6rd`
` tunnel 6rd prefix 2002::/32`
`! `
`ipv6 route 2002::/32 Tunnel0`

CE

`ipv6 general-prefix RD 6rd Tunnel0`
`!`
`interface Tunnel0`
` no ip address`
` ipv6 enable`
` tunnel source Loopback0`
` tunnel mode ipv6ip 6rd`
` tunnel 6rd prefix 2002::/32`
` tunnel 6rd br 4.4.4.4`
`!`
`ipv6 route 2002::/32 Tunnel0`
`ipv6 route ::/0 Tunnel0 2002:0:404:404::`
`!`
`interface GigabitEthernet1`
` description LAN`
` ipv6 address RD ::/64 eui-64`

Verify

`show tunnel 6rd`

[Category:Cisco](/Category:Cisco "wikilink")