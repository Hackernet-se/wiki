---
title: Cisco L2 Security
permalink: /Cisco_L2_Security/
---

Huvudartikel: [Cisco Security](/Cisco_Security "wikilink").

Se även [Private VLANs](/Cisco_VLAN#Private_VLAN "wikilink"), [DHCP
Snooping](/Cisco_DHCP#Snooping "wikilink") och [Cisco L3
Security](/Cisco_L3_Security "wikilink").

### Frame Block

Ändra beteende på en switch så att unknown unicast droppas. Fungerar som
säkerhetsmekansim om CAM går fullt för då floodas inte alla frames.

`switchport block unicast`
`switchport block multicast`

Port Security
-------------

När man slår på port-security på en port så är default MAC learning
method "dynamic". Det betyder att switchen säkrar MAC-adresser ingress
när de passerar interfacet. Om en ny MAC-adress kommer in och max antal
tillåtna MAC-adresser inte har uppnåtts så kommer switchen lagra
MAC-adressen i minne och tillåta trafiken. Man kan även köra något som
kallas "sticky method", då säkrar switchen MAC-adresser på samma sätt
som med dynamic men de sparas i NVRAM istället. Detta gör att de finns
kvar genom reboots. Notera att sticky-adresser ej syns i running config.
Utöver detta kan man ange MAC-adresser statiskt, detta gör man i running
config under interfacet, vilket gör att man även kan spara det i startup
config. En till grej som port-security gör är att kolla att MAC-adresser
som är säkrade inte kommer in på någon annan port i VLANet än där de är
säkrade (oavsett learning method). Port-security fungerar endast på
portar som är statiskt konfigurerade som access eller trunk. Ska port
security kombineras med [HSRP](/Cisco_HSRP "wikilink") bör BIA MAC
användas.

`interface [interface]`
` switchport mode access`
` switchport port-security`
` switchport port-security maximum 1`
` switchport port-security mac-address sticky`
` switchport port-security violation shutdown`

Verify

`show port-security interface`

`errdisable recovery cause psecure-violation`

ACL
---

### PACL

Port ACLs används ingress på Layer 2 interfaces på switchar.

`interface gi0/2`
` ip access-group PACL in`
` mac access-group PACL in`

Verify

`show mac access-group`

### VACL

VLAN ACL är ingress, kollar både lokal och transit-trafik och funkar
även med non-IP traffic.

`access-list 100 permit ip any host 10.0.0.10`

`vlan access-map BLOCK-TO-SERVER 10`
` match ip address 100`
` action drop`
`vlan access-map BLOCK-TO-SERVER 20`
` action forward`

Apply to vlan

`vlan filter BLOCK-TO-SERVER vlan-list 10`

Logging

`vlan access-log maxflow 500`
`vlan access-log threshold 0`

Storm Control
-------------

Storm control är teknik för att låta administratörer dämpa unicast-,
multicast- eller broadcast-trafik på L2-interface. Det kan användas för
att reducera skadan vid broadcast-stormar. Olika switchmodeller fungerar
olika när det gäller [EtherChannels](/Cisco_EtherChannel "wikilink")
kontra fysiska interface för Storm control. För att konfigurera Storm
control måste man ange gränsvärde (rising) men falling är optional.

`interface gi0/7`
` storm-control unicast level bps 1m 500k`
` storm-control multicast level pps 500`
` storm-control broadcast level 10`

Ange vad som ska hända när tröskelvärde överskrids, t.ex. droppa frames
eller skicka snmp-trap.

` storm-control action trap`

Verify

`show storm-control`

802.1x
------

802.1x är ett säkerhetsprotokoll som låter klienter (end devices)
autentisera sig genom att prata EAP (RFC 3748) innan de får tillgång
till tråd/trådlösa nätverk. Switcharna kan prata radius med
authentication server som t.ex. kan vara en Windows-server eller en
Cisco ISE. Authentication port-control används för att ställa en port i
ett av tre operational modes: auto, force-authorized och
force-unauthorized.

`aaa authentication dot1x default group radius`
`dot1x system-auth-control`

`interface gi0/5`
` switchport mode access`
` dot1x port-control auto`

Har man flera hostar på samma port så kan man låta varje mac-adress
autentisera sig.

`interface gi0/5`
` authentication host-mode multi-host`

Om man vill testköra (dry-run) sin autentiseringslösning kan man använda
öppen auth, då skickas authentication data till Radius-servern men
porten agerar vanlig port (alltså tillåter trafik på access vlan).

`interface gi0/5`
` authentication open`

Man kan slå på att alla andra får prata ut genom porten men inkommande
frames accepteras endast om auth går igenom. Detta är t.ex. användbart
för [PXE](/PXE-Deploy "wikilink").

`interface gi0/5`
` authentication control-direction in `

Verify

`show dot1x`

DAI
---

För att skydda sitt L2-nätverk mot MITM-attacker som använder G-ARP kan
man använda Dynamic ARP inspection. DAI kräver [DHCP
Snooping](/Cisco_DHCP#Snooping "wikilink") eftersom inkomna
ARP-meddelanden valideras mot snooping-databasen. Om inte ARP:en stämmer
överens mot det som står i databasen kommer frames att droppas,
*SW_DAI-4-DHCP_SNOOPING_DENY*. Man slår på DAI per VLAN man vill
skydda.

`ip arp inspection vlan 10`
`show ip arp inspection vlan 10`

Man kan även kontrollera IP-avsändare och mottagare i paketen utifrån
ARP-information. Detta kollar även ARP bodies efter invalid eller
oväntade IP-adresser som 0.0.0.0, 255.255.255.255 och alla
multicast-adresser.

`ip arp inspection validate ip`

Konfigurera interface som trusted för ARP. På dessa inspekteras ej
ARP-meddelanden.

`interface gi0/7`
` ip arp inspection trust`

Static entries behövs för hostar som inte använder DHCP.

`arp access-list ARP_ACL`
` permit ip host 10.0.0.30 mac host 0011.2233.4455`

`ip arp inspection filter ARP_ACL vlan 10`

Eftersom DAI gör att switchen jobbar mer kan man överlasta den genom att
skicka ett stort antal ARP-meddelanden. DAI har därför default en limit
på 15 ARP-meddelanden per port per sekund.

`interface gi0/7`
` ip arp inspection limit 15 `

Logging

`ip arp inspection vlan 10 logging acl-match`

`ip arp inspection log-buffer entries 32`
`ip arp inspection log-buffer logs 5 interval 1`

Verify

`show ip arp inspection`

MACsec
------

En del Nexus-switchar har line rate encryption capabilities. MACsec
Layer 2 security krypterar paketen hop-by-hop. Detta skyddar mot
wiretapping och MITM samtidigt som det gör att man kan inspektera,
monitorera, QoS-tagga och forwardera frames som vanligt fast trots att
det är krypterat on the wire. För att upptäcka MACsec peers och
förhandla nycklar mellan MACsec-deltagare används MACsec Key Agreement
(MKA) protocol. Sedan används Secure Association Key (SAK) för att
kryptera och avkryptera på data plane. En MACsec keychain kan ha
multipla PSKs, var och en med egen key ID och valfri lifetime. En
MACsec-session kan t.ex. faila pga key/key name (CKN) mismatch eller att
key duration har gått ut. Om den failar så kan man ha en fallback
session som tar över, då måste man ha en fallback key konfad. En
fallback session gör att man slipper nertid när primary session går ner
och man får lite tid på sig att fixa problemet.

**Overview**
[<File:Cisco-MACsec.PNG>](/File:Cisco-MACsec.PNG "wikilink")

MACsec funkar på:

-   Layer 2 switchports (access and trunk)
-   Layer 3 routed interfaces (no subinterfaces)
-   Layer 2 and Layer 3 port channels

**Konfiguration**

`feature macsec`

`key-chain macsec-psk no-show`

`key chain KC1 macsec`
` key 100`
`  key-octet-string abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789 cryptographic-algorithm AES_256_CMAC`
`  send-lifetime 00:00:00 Oct 04 2018 duration 100000`

Om man inte anger någon key lifetime så defaultar det till unlimited.

Policy

`macsec policy MACsec01`
` cipher-suite GCM-AES-256`
` security-policy `**`should-secure`**

Här kan man även välja "**must-secure**" = packets not carrying MACsec
headers will be dropped.

Apply

`interface e1/15`
` macsec keychain KC1 policy MACsec01 fallback-keychain KC-fallback`

Notera att man inte kan ändra en policy utan man får skapa en ny och
attacha på interfacet.

Verify

`show macsec policy`
`show macsec mka session/summary`
`show interface capabilities | i "Ethernet|MACSEC`

### XPN

MACsec Extended Packet Numbering (XPN). Varje MACsec frame innehåller
ett 32-bitars packetnummer som är unikt för varje given SAK. Om dessa
tar slut så blir det SAK rekey för data plane keys. För
högkapacitetslänkar så tar dessa slut rätt snabbt och kontrollplan måste
göra SAK rekey. Med XPN så används ett 64-bitars nummer istället och
därmed elimineras behovet av frekvent SAK rekey.

`mka policy MACSEC`
` macsec-cipher-suite gcm-aes-xpn-256`
`!`
`key chain MACSEC macsec`
` key 1000`
`  cryptographic-algorithm aes-256-cmac`
`  key-string 7 075E701D1F58485446435A5D557B7A757962647342`
`!`
`interface HundredGigE1/0/1`
` macsec network-link`
` mka policy MACSEC`
` mka pre-shared-key key-chain MACSEC`

### Certificate Based MACsec

Cisco IOS-XE har stöd för Certificate Based MACsec med Local
Authentication. Då används EAP-TLS för authentication. MKA och MACsec
implementeras efter lyckad authentication med certificate-based MACsec.

`show mka session interface g1/0/1 details`

IPv6
----

**RA guard**
RA guard blockerar unwanted eller rogue router advertisement. Denna
feature körs i ingress direction.

`interface GigabitEthernet0/1`
` ipv6 nd raguard`

Verify

`show ipv6 snooping features`
`show ipv6 nd raguard`

**DHCPv6 Guard**
DHCPv6 Guard blockerar reply och advertisments som kommer från
unauthorized DHCP servers.

`show ipv6 dhcp guard`

**Binding table**

`show ipv6 neighbor binding`

**Device tracking**

`show ipv6 neighbor tracking`

**ND inspection/snooping**

`show ipv6 nd inspection`

**SeND**
Secure Neighbor Discovery is a protocol that enhances NDP with three
additional capabilities: Address ownership proof, Message protection,
Router authorization.

MAC access control list
-----------------------

Work in progress

[Category:Cisco](/Category:Cisco "wikilink")