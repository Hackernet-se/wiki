---
title: Cisco IPsec
permalink: /Cisco_IPsec/
---

IPsec (RFC 4301) är en teknik för att skydda datakommunikation och
räknas som en secure VPN. Det finns i tunnel och transport mode beroende
på om det ska tunnlas och krypteras eller endast krypteras. IPsec funkar
med IPv4/IPv6 och kan köras över en [GRE](/Cisco_GRE "wikilink")-tunnel.
Virtual Tunnel Interface (VTI) är routebara interface som används för
att terminera IPsec-tunnlar, detta gör IPsec flexibelt och det kan
användas både för unicast och [multicast](/Cisco_Multicast "wikilink").

Se även [Cisco Security](/Cisco_Security "wikilink"), [Cisco
DMVPN](/Cisco_DMVPN "wikilink") och [ASA
VPN](/Cisco_ASA_VPN "wikilink").

**MTU**
IPsec påverkar MTU, detta bör man ta med i beräkningarna. Notera att
packet size inte är linjärt i förhållande till storleken på de
enkapsulerade paketen eftersom ESP jobbar med block. Detta i kombination
med att det finns väldigt många IPsec-algoritmer gör att det inte alltid
är solklart exakt hur det blir men det finns verktyg som hjälper till
att räkna på det. Med hjälp av detta kan man sätta en lämplig IP MTU på
tunnel interface och sedan justera TCP MSS till 40 bytes lägre än det.

[`https://cway.cisco.com/tools/ipsec-overhead-calc/`](https://cway.cisco.com/tools/ipsec-overhead-calc/)

Konfiguration
=============

Dead Peer Detection (DPD) & NAT Keepalives

`crypto isakmp keepalive 30 `
`crypto isakmp nat keepalive 30`

Capabilities, Encryption Layer Interface

`show crypto eli`

Errors and Invalid SPI Recovery Feature

`crypto isakmp invalid-spi-recovery `

### Legacy

IPsec VPN med crypto maps och IKEv1 är den äldsta och minst skalbara
varianten av IPsec VPN.

`crypto isakmp policy 10`
` encryption aes 256`
` authentication pre-share`
` group 20`
` lifetime 86400`

`show crypto isakmp policy`

PSK Authentication

`crypto isakmp key S3cr3ts address 3.3.3.3`

`show crypto isakmp key`

**Fas 2**

`crypto ipsec transform-set PHASE2 esp-aes esp-sha-hmac`
` mode tunnel`
`ip access-list extended CRYPTO`
` permit ip 192.168.1.0 0.0.0.255 192.168.2.0 0.0.0.255`

`crypto map VPNMAP 10 ipsec-isakmp`
` set peer 3.3.3.3`
` set transform-set PHASE2`
` match address CRYPTO`

Interfaces

`interface GigabitEthernet0/1`
` description Internet`
` ip address 2.2.2.2 255.255.255.0`
` crypto map VPNMAP`

`interface GigabitEthernet0/2`
` description Inside`
` ip address 192.168.1.1 255.255.255.0`

Verify Fas 1 och 2. Inget förhandlas förens det skickas trafik som
triggar tunneln.

`show crypto isakmp sa`
`show crypto ipsec sa`
`show crypto session`

Loopback

`crypto map VPNMAP local-address Loopback0`

Reverse Route Injection

`crypto map VPNMAP 10 ipsec-isakmp`
` set reverse-route distance 10`

`show crypto route`

GRE over IPsec with Profile
---------------------------

En fördel med att tunnla trafiken med [GRE](/Cisco_GRE "wikilink") är
att routingprotokoll kan användas över tunneln. Trafiken krypteras efter
att det har enkapsulerats med GRE. Man bör manuellt ange **ip mtu** på
tunnel-interfacet för det tar ej hänsyn till ESP-enkapsuleringen som
lägger till overhead.

`crypto isakmp policy 10`
` encryption aes 256`
` authentication pre-share`
` group 20`
` lifetime 86400`

`crypto isakmp key S3cr3ts address 3.3.3.3    `

`crypto ipsec transform-set PHASE2 esp-aes esp-sha-hmac `
` mode transport  #`*`Spara`` ``overhead`` ``genom`` ``att`` ``köra`` ``i`` ``transport`` ``mode`*

`crypto ipsec profile GRE_OVER_IPSEC`
` set transform-set PHASE2 `

`interface Tunnel0`
` ip address 1.1.1.1 255.255.255.0`
` ip mtu 1400`
` ip tcp adjust-mss 1360`
` tunnel source Loopback0`
` tunnel destination 3.3.3.3`
` tunnel protection ipsec profile GRE_OVER_IPSEC`

Verify

`show crypto ipsec profile`
`show crypto session`

Local och remote i IPsec SA kommer att förhandlas som
*tunnel-endpoint*/32 \<-\> *tunnel-endpoint*/32 protokoll GRE vilket gör
att det aldrig behövs mer än en entry per tunnel.

#### FVRF

Om interfacet som terminerar tunneln ligger i en vrf måste man använda
en keyring som man lägger i en isakmp-profil.

`crypto keyring VPN_PEERS vrf Outside`
` pre-shared-key address 3.3.3.3 key SecretKey`

`crypto isakmp profile VPN_PROFILE`
`  keyring VPN_PEERS`
`  match identity address 3.3.3.3 255.255.255.255`
`  keepalive 10 retry 5`

VTI
---

Med VPN som byggs med Virtual Tunnel Interface kan man både använda
dynamic routing och multicast. Det fungerar likadant som GRE över IPsec
men annan enkapsulering används. Payloaden enkapsuleras direkt i IPsec
som är en IP-enkapsulering därför stöds inget annat än IP (så t.ex.
IS-IS fungerar ej). Detta gör att tunnel-interfacet vet sin korrekta
mtu. VTI konfigureras likadant som GRE över IPsec med profil men med en
skillnad, här följer därför endast skillnaden samt att transform set
alltid måste köras i tunnel mode.

`crypto ipsec transform-set PHASE2 esp-aes esp-sha-hmac `
` mode tunnel`

`interface Tunnel0`
` `**`tunnel`` ``mode`` ``ipsec`` ``ipv4`**

Verify

`show crypto ipsec sa`
`show crypto route`
`show crypto session`

Local och remote kommer alltid att förhandlas som **0.0.0.0/0 \<-\>
0.0.0.0/0** vilket gör att det aldrig behövs mer än en entry per tunnel.

### Dynamic VTI

Man kan även låta VTI:s skapas dynamiskt.

`interface Virtual-Template1 type tunnel  `
` ip unnumbered Loopback0 `
` tunnel mode ipsec ipv4 `
` tunnel protection ipsec profile VTI_PROFILE`

`crypto isakmp profile VTI_ISAKMP_PROFILE`
` keyring default  `
` match identity address 0.0.0.0    `
` virtual-template 1`

Verify

`show interfaces virtual-template 1`
` ...`
` Tunnel linestate evaluation down - no IPv4 tunnel destination address`
` Tunnel source UNKNOWN`
` ...`

`show interfaces virtual-access 1`
` ...`
` Tunnel vaccess, cloned from Virtual-Template1`
` Tunnel linestate evaluation up`
` Tunnel source 10.0.0.1, destination 10.0.0.2`
` ...`

Andra sidan konfigureras som en vanlig point-to-point IPsec tunnel.

`interface Tunnel10`
` ip address 10.0.0.2 255.255.255.0`
` tunnel source Loopback0  `
` tunnel mode ipsec ipv4  `
` tunnel destination 1.1.1.1`
` tunnel protection ipsec profile IPSEC`

NAT-T
-----

IOS märker med hjälp av NAT-Discovery (RFC 3947) om paketen till och
från remote peer natas och byter då till UDP 4500. Detta är på default
men kan stängas av. Båda sidor måste ha stöd NAT-T för att det ska
funka.

`no crypto ipsec nat-transparency udp-encapsulation`

IKEv2
-----

IKEv2 har inbyggt stöd för NAT traversal och ID är alltid skyddat till
skillnad från IKEv1 aggressive mode.

Key ring

`crypto ikev2 keyring IKEv2_KEYRING`
` peer SITE2`
`  address 3.3.3.3`
`  pre-shared-key local PSK01`
`  pre-shared-key remote PSK02`

Proposal

`crypto ikev2 proposal IKEv2_PROPOSAL`
` encryption aes-cbc-256`
` integrity sha512`
` group 20`

`show crypto ikev2 proposal`

*Används aes-gcm måste prf köras på båda sidor.*

Profile

`crypto ikev2 profile IKEv2_PROFILE`
` match identity remote address 3.3.3.3 255.255.255.255`
` identity local address 2.2.2.2`
` authentication remote pre-share`
` authentication local pre-share`
` keyring local IKEv2_KEYRING`

`show crypto ikev2 profile`

Policy

`crypto ikev2 policy IKEv2_POLICY`
` proposal IKEv2_PROPOSAL`

`show crypto ikev2 policy`

Transform set

`crypto ipsec transform-set SITE2 esp-aes 256 esp-sha-hmac`
` mode tunnel`

`show crypto ipsec transform-set`

Crypto map

`crypto map IKEv2_MAP 1000 ipsec-isakmp`
` set peer 3.3.3.3`
` set transform-set SITE2`
` match address CRYPTO`
`interface gi2`
` crypto map IKEv2_MAP`
`show crypto map`

Verify

`show crypto ikev2 sa`

High Availability
-----------------

För att få till HA kan man sätta upp det på olika sätt. Man kan t.ex. ha
loopbacks som tunnel endpoints och sedan sköta konvergering med
routingprotokoll. Man kan även bygga redundans genom att ha flera
peer-adresser i sin crypto-map.

`crypto map VPNMAP 10 ipsec-isakmp`
` set peer 2.2.2.2 default`
` set peer 3.3.3.3`

**Stateless IPsec redundancy**
Det finns inget samspel mellan IPSec och [HSRP](/Cisco_HSRP "wikilink"),
dvs HSRP kan inte hålla koll på IPSec's SA state och IPSec vet inte när
HSRP gör en failover. Men det går att konfigurera crypto-mapen att
sourcea IKE fas 1 och 2 från HSRP VIP och HSRP group names bör matcha på
båda enheterna. Även om HSRP konvergerar snabbt kan det ta en stund
innan IPsec-tunnlar är uppsatta på nytt efter en failover pga
renegotiation. Därför är denna metod inte optimal utan det man t.ex. kan
göra istället är att ha uppe två tunnlar parallellt och sedan styra
routingen med [IP SLA](/Cisco_Routing#IP_SLA "wikilink").

`crypto dynamic-map VPNMAP 10`
` set transform-set PHASE2`
` match address ACL`
` reverse-route`

`crypto map CRYPTO 10 ipsec-isakmp dynamic VPNMAP`

`interface GigabitEthernet0/1`
` standby 1 name IPSEC`
` crypto map CRYPTO redundancy IPSEC`

**Stateful IPsec redundancy**
Det går även att synka SA-states mellan IOS-routrar vilket möjliggör
snabbare överslag. Phase1/Phase2 session states synkroniseras mellan
ACTIVE och STANDBY så inget behöver förhandlas om vid failover. Detta
sköts automatiskt med hjälp av SCTP, men ingen konfiguration synkas utan
det måste sättas upp symmetriskt. Utöver ovanstående
HSRP/IPsec-konfiguration behövs synkronisering sättas upp.

`ipc zone default`
` association 1`
`  protocol sctp`
`   local-port 5000`
`   local-ip 10.0.0.1`
`   remote-port 5000`
`   remote-ip 10.0.0.2`

`redundancy inter-device`
` scheme standby IPSEC`

Verify

`show redundancy inter-device`
`show crypto ha`

QoS
---

Eftersom trafiken är enkapsulerad och krypterad måste
QoS-markeringar/beslut fattas innan, man kan använda QoS pre-classify på
crypto map. Se även [Cisco QoS](/Cisco_QoS "wikilink").

`crypto map VPNMAP 10 ipsec-isakmp `
` qos pre-classify`

GET VPN
=======

Group Encrypted Transport VPN är en Cisco proprietary VPN-teknik som
inte använder point-to-point-tunnlar utan istället tillhandahåller
any-to-any kryptering genom att alla inblandade enheter kör med samma
IPsec-nycklar. Group Domain Of Interpretation (RFC 3547) är ett group
key management protocol som används för att distribuera dessa nycklar
till alla Group Members (IOS devices) som vill ha det. GDOI körs mellan
GM och Key Server. KS är en IOS-enhet som är ansvarig för att skapa och
hålla koll på GET VPN control plane. All policy konfigureras på den som
t.ex. krypteringsalgoritmer, timers och vilken trafik som ska krypteras.
Detta laddas sedan ner av GMs under registreringen. Även om inte all
policy är intressant för alla kommer det fortfarande att hämtas från KS.
GET VPN har stöd för multipla KS för HA och GMs kan konfigureras att
registrera med flera. Den KS med högst prio blir primary KS och övriga
blir secondary. Vid lika används högst IP som tiebreaker. Nycklarna
refreshas med jämna mellanrum (default 24h) genom en rekey-process.
Detta görs med UDP 848 antingen med unicast eller multicast. Använder
man unicast kommer varje GM att skicka ACK message som svar på den nya
nyckeln. Det är endast primary KS som skickar rekey messages. Normalt
sett får GMs skicka trafik utan kryptering innan man har registrerat sig
med KS, detta kallas Fail-Open.

GET VPN använder Tunnel mode IPSec men istället för att använda tunnel
endpoints i den nya IP-headern återanvänds orginal-IP. Detta gör att GET
VPN inte passar bra att köra över internet eftersom där kan inte privata
adresser routas. Därför är GET VPN bäst lämpat för privata nät, t.ex.
som gör över MPLS VPN eller VPLS. Vill man däremot köra det över
internet kan man kombinera det med [DMVPN](/Cisco_DMVPN "wikilink").

GDOI Payloads

-   GDOI SA
-   SA KEK: används för att säkra GET VPN control plane
-   SA TEK: används för att säkra data plane
-   Key Download (KD)
-   Sequence Number (SEQ)
-   Proof of Possession (POP)

### Konfiguration

**Key Server**
Generera RSA-nycklar

`crypto key generate rsa general-keys label GDOI_KEYS modulus 2048 exportable`

KS har all IPsec-konfiguration som sedan laddas ner av gruppmedlemmarna

`crypto isakmp policy 10`
` authentication pre-share`

`crypto isakmp key 0 SECRET address 2.2.2.2   #GM-1`
`crypto isakmp key 0 SECRET address 3.3.3.3   #GM-2 `
`crypto isakmp key 0 SECRET address 4.4.4.4   #GM-3 `

`crypto ipsec transform-set PHASE2 esp-aes esp-sha-hmac`

`crypto ipsec profile GDOI_PROFILE`
` set transform-set PHASE2`

`ip access-list extended SYMMETRIC_ACL`
` permit ip 172.16.0.0 0.0.255.255 172.16.0.0 0.0.255.255 `

`crypto gdoi group GDOI_GROUP`
` identity number 123`
` server local`
`  rekey transport unicast`
`  rekey authentication mypubkey rsa GDOI_KEYS`
`  rekey retransmit 60 number 2`
`  sa ipsec 1`
`   profile GDOI_PROFILE`
`   match address ipv4 SYMMETRIC_ACL`
`   replay time window-size 5`
`  address ipv4 1.1.1.1 `

**Group Member**

`crypto isakmp policy 10`
` authentication pre-share`

`crypto isakmp key 0 SECRET address 1.1.1.1   #KS`

`crypto gdoi group GDOI_GROUP`
` identity number 123`
` server address ipv4 1.1.1.1 `

`crypto map GETVPN local-address Loopback 0`
`crypto map GETVPN 10 gdoi`
` set group GDOI_GROUP`

`interface Gi2`
` description To KS`
` crypto map GETVPN`

**Verify**

`show crypto gdoi`
`show crypto gdoi ks`
`show crypto gdoi gm`

**COOP KS**
För redundans och lastdelning kan man ha flera KS som då konfigureras
likadant. Generera RSA-nycklar på primary KS och exportera både public
och private till alla COOP KS. Notera att på vissa IOS-versioner går det
att köra KS och GM på samma enhet men det är inte officially supported.

`crypto key export rsa GDOI_KEYS pem terminal 3des CISCO123 `
`crypto key import rsa GDOI_KEYS pem exportable terminal CISCO123`

**Suite B**
GET VPN har stöd för Suite B men måste sättas upp för det genom att på
KS konfigurera de säkra algoritmer som ska användas.

`show crypto gdoi feature suite-b `

[Category:Cisco](/Category:Cisco "wikilink")