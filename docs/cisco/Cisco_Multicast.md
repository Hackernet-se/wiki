---
title: Cisco Multicast
permalink: /Cisco_Multicast/
---

IP Multicast är att skicka ett meddelande från en source till multipla
destinationer i en ström över ett IP-nät, vilket kan spara väldigt
mycket bandbredd. En multicast-IP är en destinationsadress och alla som
ska ta del av trafiken måste gå med i samma multicastgrupp, dvs lyssna
på den IPn och meddela det till intermediate systems. End systems och
routrar pratar IGMP med varandra för att ta reda på vem som är med i
vilken multicastgrupp. För att routrar ska kunna veta vilka nät som har
intressenter av multicastströmmar används något routing eller
signaleringsprotokoll (control plane), DVMRP, MOSPF eller PIM. För loop
prevention används RPF, inga paket forwarderas utan att klara denna
check. IP Multicast fungerar för protokoll som är connectionless.

För konfiguration se [Cisco PIM](/Cisco_PIM "wikilink"), [Cisco
IGMP](/Cisco_IGMP "wikilink") och [Cisco MLDP](/Cisco_MLDP "wikilink").
Även om framtiden kanske stavas Bit Indexed Explicit Replication.

[<File:Cisco_Multicast.png>](/File:Cisco_Multicast.png "wikilink")

Multicast Addressing
--------------------

Multicast har egna address spaces, för IPv4 används 224.0.0.0/4 (class
D) och för IPv6 FF00::/8. I dessa finns det olika ranges, GLOP (RFC
2770) innebär att varje 16-bitars AS har en egen unik multicast-range på
internet, 233.<ASN>.0/24. Administratively scoped (RFC 2365) är
motsvarigheten till unicasts RFC 1918.

-   Local-link (TTL 1): 224.0.0.0/24
-   Globally scoped: 224.0.1.0 - 238.255.255.255
-   GLOP addresses: 233.0.0.0/8
-   Administratively scoped: 239.0.0.0/8

Complete IANA list:
[IPv4](http://www.iana.org/assignments/multicast-addresses/multicast-addresses.xhtml),
[IPv6](http://www.iana.org/assignments/ipv6-multicast-addresses/ipv6-multicast-addresses.xhtml)

Utifrån IP-adress räknas multicast mac-adress fram så att enheterna vet
vad de ska skicka till och ta emot frames för utöver BIA och broadcast.
En multicast-adress för IPv4 mappas till MAC address
01:00:5E:\<low-order 23 bits\> och IPv6 mappas till MAC
33:33:\<low-order 32 bits\>.

### Distribution Trees

Multicastroutrar skapar distributions-träd för att styra vilken väg
multicasttrafiken tar genom nätverket. Det finns två typer av
trädtopologier, source trees och shared trees. Source trees kallas också
shortest-path tree och det skapas ett spanning tree från root/source
till alla leaves. Ett source tree består av source och destination och
betecknas S,G, t.ex. (172.20.0.40, 225.0.10.10). Till skillnad från
source trees har shared trees en gemensam rot oavsett source, denna
punkt kallas rendezvous point. Ett shared tree betecknas \*,G vilket
betyder any source. Trafik tunnlas från routern närmast källan till RP
för att sedan distribueras ut i det delade trädet.

### Source Specific Multicast

Med SSM kan hostarna själva välja source för trafikströmmen ifall det
finns flera. Det kan även skydda mot dos-attacker eftersom mottagare
berättar för nätverket vilka källor de vill få trafik ifrån och inte vem
som helst. Det ger också fördelar med att överlappande grupp-adresser
kommer att fungera eftersom olika källor gör strömmarna unika. Det finns
inga shared trees med SSM utan allt hanteras som source trees. SSM har
232.0.0.0/8 IANA-reserverat. Se
[SSM-konfiguration](/Cisco_PIM#Source_Specific_Multicast "wikilink").

Multicast Routes
----------------

Static mroutes kan användas i situationer när man behöver konstruera
multicast-strömmar att gå över en länk som inte kör IGP, t.ex. tunnlar,
eller fixa RPF failures som man får när multicast routing inte körs på
alla länkar. Genom att lägga till en static mroute så kommer RPF att
titta på den i första hand eftersom den har en bättre administrative
distance (AD = 0) än det som finns i unicast RIB:en. Finns det flera
equal cost paths till sender kommer endast interface med aktiva
PIM-grannskap att användas. Och efter det kommer den med högst PIM
neighbor IP att vinna, detta gör att RPF är deterministiskt. I nyare
versioner av IOS används alltid longest match av RPF vilket inte var
fallet förr.

`ip mroute 10.0.0.0 255.255.255.0 gi2`
`ipv6 route 1000::/64 gi2 multicast`

Verify. Notera att endast routes med next-hop över interface där det
finns PIM neighbors genererar RPF entries och därmed syns med dessa
kommandon.

`show ip rpf `<mcast-source>
`show ipv6 rpf `<mcast-source>

**CEF**
Såhär fungerar CEF default

`224.0.0.0/4          drop`
`224.0.0.0/24         receive`

Troubleshooting
---------------

Active IP Multicast Sources sending \>= 4 kbps.

`show ip mroute active`

**mtrace**
Show the multicast path from the source to the receiver. Detta är en
IGMP-baserad trace.

`mtrace 10.0.0.10 20.0.0.20 224.1.4.4`

**mstat**
Show the multicast path, användbart för att upptäcka congestion.

`mstat 10.0.0.10 20.0.0.20 224.1.4.4`

**mrinfo**
Show multicast neighbor router information (legacy-kommando).

`mrinfo`

**Packet Debugging**

`interface gi2`
` no ip mfib cef input`
` no ip mfib cef output`

`debug ip mfib pak 239.1.1.10`

Multicast Helper
----------------

Syftet med denna funktion är att tillåta broadcasts över ett multicast
capable network. Det fungerar precis som det mer vanliga **ip
helper-address** men då konverteras broadcast till unicast. IP multicast
helper-map konverterar broadcast till en utvald multicast-adress. Man
måste ha ett fungerande multicast-nät för kunna nyttja detta samt en
extended ACL som pekar ut vilken trafik som får göras om till multicast.

Ingress router

`ip forward-protocol udp `<port-number>

`interface gi2`
` ip multicast helper-map broadcast `<mcast-address>` `<acl>

Egress router

`ip forward-protocol udp `<port-number>

`interface gi2`
` ip multicast helper-map `<mcast-group>` `<directed-broadcast-IP>` `<acl>

Default så skickas broadcasten ut till 255.255.255.255 oavsett vad man
satt *directed-broadcast-IP* till, vill man ha det till något annat
måste man använda **ip broadcast-address <IP>** på interfacet.

IGMP Static Group
-----------------

Man kan skicka ut multicastpaket på ett interface även fast det inte
finns någon enhet som pratar PIM eller IGMP, detta kallas Static Group.
Routern som konfas med detta kommer att skicka PIM Join request upstream
för att ta del av strömmen och sedan forwardera ut det på de interface
med den statiska gruppen.

`interface gi2`
` ip pim sparse-mode`
` ip igmp static-group 232.1.1.1 source 10.1.1.3`

BGP
---

Man kan skicka information om multicast-strömmar mellan domäner med
hjälp av MP-BGP extensions. När man lär sig ett prefix med multicast BGP
så kommer RPF att kollas mot den IP som står som next-hop i
uppdateringen. Dvs BGP handlar inte om hur man hittar till en
destination eftersom en multicast-adress alltid kommer vara destination
utan man berättar vilka sources man har från en viss next-hop och då kan
man klara rpf-checken. Så man måste se till att populera även denna
BGP-tabell, det kan t.ex. göras med redistribution från ett
unicast-protokoll. Man måste köra PIM mellan domänerna för att shared
och shortest-path trees ska kunna signaleras. Man måste även utbyta
unicast routes för multicast-källorna för att alla multicast routrarna
ska kunna använda RPF. Se även [Cisco
MP-BGP](/Cisco_BGP#Multiprotocol_BGP "wikilink").

`router bgp 100`
` address-family ipv4 multicast`
`  neighbor 10.0.0.20 activate`

Verify

`show bgp ipv4 multicast summary`

[Category:Cisco](/Category:Cisco "wikilink")