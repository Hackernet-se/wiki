---
title: Cisco OSPFv3
permalink: /Cisco_OSPFv3/
---

För huvudartikel, se [Cisco OSPF](/Cisco_OSPF "wikilink"). OSPF Version
3 (RFC 5340) togs fram för att stödja IPv6. Man använder termen link
istället för network. De flesta features som finns i v2 finns i v3 och
fungerar i princip likadant men kan konfigureras lite annorlunda. För
OSPF-kommunikation används alltid link-local adresser (med undantag
virtual links). Största anledningen till skillnaderna mellan OSPFv2 och
v3 är pga att IPv4 och IPv6 fungerar på lite olika sätt. Från och med
IOS 15.1(3)S och 15.2(1)T har OSPFv3 stöd för adressfamiljer och man kan
använda det både för IPv4 och IPv6, dock är control plane alltid IPv6
med v3. [IOS-XR](/Cisco_IOS-XR "wikilink") har inte stöd för OSPFv3
IPv4.

### LSA types

Det finns en ny typ av LSA, Link LSA som gäller för link-local scope.

### Network Types

NBMA

Konfiguration
-------------

Prereq

`ipv6 unicast-routing`

Process, det måste finnas en RID som är 32-bitar och skrivs som en
IPv4-adress. Den väljs på samma sätt som i OSPFv2. Finns det ingen
IPv4-adress konfigurerad så måste man konfigurera detta manuellt innan
processen kan starta.

`ipv6 router ospf 1`
` router-id 1.1.1.1`

Interface, det finns inget network-kommando utan man slår på det per
interface. Finns det flera adresser på ett interface kommer alla att
annonseras av OSPFv3. IPv6-granne konfigureras under interface och inte
processen.

`interface gi2`
` ipv6 ospf 1 area 0`
` ipv6 ospf neighbor 2000:1::2`
` ipv6 ospf priority 1`
` ipv6 ospf hello-interval 10`
` ipv6 ospf dead-interval 40`

Verify

`show ipv6 ospf neighbor`
`show ipv6 ospf database`

**Instance**, OSPFv3 har stöd för multipla instanser per länk. Endast
routrar med samma instance-nummer bildar grannskap.

`interface gi2`
` ipv6 ospf 1 area 2 instance 3`

### Authentication

Den första varianten av OSPFv3 (IPv6 only) använder IPv6’s inbyggda
IPsec-autentisering så det finns ingen egen. Eftersom OSPFv3 inte
använder ISAKMP för nyckelutbyte i fas 1 måste fas 2 autentisering och
kryptering konfigureras manuellt.

`interface gi2`
` ipv6 ospf encryption ipsec spi 2001 esp aes-cbc 256 4F814B37EA44ED42549955036FC0A68830A45FAC16424B093511EB4ACF20962D sha1 8A4481AF1A1444A92BB405F3A7FA392DF7222E5F`

` ipv6 ospf authentication ?`
`   ipsec `
`   null`

### Prefix Suppression

Fungerar som med OSPFv2.

`interface gi2`
` ipv6 ospf prefix-suppression`

### Summarization

Fungerar som med OSPFv2.

`ipv6 router ospf 1`
` area 0 range 2000:1::/60`

### Redistribution

Default metric: 1 för BGP, 20 för övrigt

`ipv6 router ospf 1`
` redistribute connected metric 10`
` redistribute rip RIPNG tag 123`
` redistribute eigrp 100 route-map FILTER`

### Virtual Links

Virtual link kan byggas över IPv4 precis som med OSPFv2.

`ipv6 router ospf 1`
` area 1 virtual-link 10.0.0.20`

Verify

`show ipv6 ospf virtual-links `

Multi AF Mode
-------------

Denna konfigurationen är mer homogen med [BGP
AFI-format](/Cisco_BGP#Konfiguration "wikilink") och [EIGRP Named
mode](/Cisco_EIGRP#Named_mode "wikilink").

`router ospfv3 1`
` router-id 1.1.1.1`

` address-family ipv4 unicast`
`  maximum-paths 4`
`  redistribute connected`
` exit-address-family`

` address-family ipv6 unicast`
`  maximum-paths 16`
`  area 0 range 2001:100:1::/48`
` exit-address-family`

`interface gi2`
` ospfv3 1 ipv4 area 0`
` ospfv3 1 ipv6 area 0`

Verify

`show ospfv3`
`show ospfv3 neighbor`
`show ospfv3 interface brief`

Man måste köra IPv6 också eftersom det används för control plane.

`ospfv3 1 ipv4 area 0`
`% OSPFv3: IPV6 is not enabled on this interface`

### Authentication

Med OSPFv3 kan man använda ESP header eller Authentication Header och
det konfigureras antingen per-link eller globalt under arean.

`router ospfv3 1`
` area 10 authentication ipsec spi 500 sha1 8a4481af1a1444a92bb405f3a7fa392df7222e5f`

`interface gi2`
` ospfv3 encryption ipsec spi 700 esp aes-cbc 256 4F814B37EA44ED42549955036FC0A68830A45FAC16424B093511EB4ACF20962D sha1 8A4481AF1A1444A92BB405F3A7FA392DF7222E5F`

Innan OSPFv3 Authentication Trailer var IPsec det enda sättet att
autentisera OSPF-paketen.

`key chain OSPFv3`
` key 1`
`  key-string SECRET`
`  cryptographic-algorithm hmac-sha-512`

`interface gi2`
` ospfv3 authentication ?`
`   ipsec`
`   `**`key-chain`**
`   null`

Verify

`show ospfv3 interface | i Ethernet|authentication|encryption`
`show crypto ipsec policy`

### TTL Security

OSPFv3 TTL security kan endast konfigureras för virtual links och sham
links i Multi AF Mode. TTL Security gör ingen nytta i övrigt eftersom
OSPFv3 control plane görs med link-local-adresser.

### BFD

BFD-support för OSPFv3 kan konfigureras på två sätt, under processen
eller interface. Se även [Cisco BFD](/Cisco_BFD "wikilink").

`address-family ipv4 unicast`
` bfd all-interfaces`

`interface gi2`
` ospfv3 bfd `

[Category:Cisco](/Category:Cisco "wikilink")