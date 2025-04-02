---
title: Cisco ASA VPN
permalink: /Cisco_ASA_VPN/
---

Huvudartikel: [Cisco ASA](/Cisco_ASA "wikilink").
Se även [Cisco IPsec](/Cisco_IPsec "wikilink").

Site-to-site
============

Policy-Based
------------

Förutsättningar för att sätta upp VPN-tunnlar är att klocka måste gå
rätt och att NAT-regler måste ligga i rätt ordning.

Kolla hur man gör på aktuell version

`vpnsetup site-to-site steps`
`vpnsetup ipsec-remote-access steps`

### Fas 1

`crypto isakmp policy 10`
` authentication pre-share`
` encryption aes-256`
` hash sha`
` lifetime 28800`
` group 2`

PSK

`tunnel-group `<other-side>` type ipsec-l2l`
`tunnel-group `<other-side>` ipsec-attributes`
` ikev1 pre-shared-key *****`
`crypto map VPNMAP 10 set peer `<other-side>

Visa befintlig PSK

`more system:running-config | i pre-shared-key|tunnel-group`
`tunnel-group 1.3.3.7 type ipsec-l2l`
`tunnel-group 1.3.3.7 ipsec-attributes`
` ikev1 pre-shared-key hemlignyckeln2000`

### Fas 2

`crypto ipsec ikev1 transform-set SITE2-FAS2 esp-aes-256 esp-sha-hmac`
`crypto map VPNMAP 10 set transform-set SITE2-FAS2`
`access-list CRYPTO-to-SITE2 extended permit ip 172.16.20.0 255.255.255.0 172.16.40.0 255.255.255.0`
`crypto map VPNMAP 10 match address CRYPTO-to-SITE2`
`crypto map VPNMAP 10 set security-association lifetime seconds 3600`
`crypto map VPNMAP 10 set pfs group5`

Följande steg behöver endast göras vid första VPN-tunneluppsättningen.

`crypto map VPNMAP interface OUTSIDE`
`crypto ikev1 enable OUTSIDE `

### NAT Exempt

`object network LAN1`
` subnet 172.16.20.0 255.255.255.0`
`object network LAN2`
` subnet 172.16.40.0 255.255.255.0`
`nat (inside,outside) 1 source static LAN1 LAN1 destination static LAN2 LAN2`

Route-Based
-----------

I ASA version 9.7 inplementerades stöd för route-based vpn med tunnel
interface.
För IKEv2 krävs minst version 9.8.1!

Tunnel interface har ingen security level.

IKEv2 behåller inte riktigt nomenklaturen med faser men ändå.

### Fas 1

`crypto ikev2 policy 5`
` encryption aes-256`
` integrity sha256`
` group 19`
` prf sha256`
` lifetime seconds 86400`

PSK

`tunnel-group 1.2.3.4 type ipsec-l2l`
`tunnel-group 1.2.3.4 ipsec-attributes`
` ikev2 remote-authentication pre-shared-key hemlig123`
` ikev2 local-authentication pre-shared-key hemlig123`

### Fas 2

`crypto ipsec ikev2 ipsec-proposal IKEV2-PROPOSAL01`
` protocol esp encryption aes-256`
` protocol esp integrity sha-256`

`crypto ipsec profile IKEV2-PROFILE01`
` set ikev2 ipsec-proposal IKEV2-PROPOSAL01`
` set pfs group19`
` set security-association lifetime seconds 3600`

Följande steg behöver endast göras vid första VPN-tunneluppsättningen.
crypto ikev2 enable OUTSIDE

### Tunnel interface

`interface Tunnel5`
` nameif VPN-TUNNEL5`
` ip address 169.254.2.1 255.255.255.0`
` tunnel source interface OUTSIDE`
` tunnel destination 1.2.3.4`
` tunnel mode ipsec ipv4`
` tunnel protection ipsec profile IKEV2-PROFILE01`

Routa det som finns på andra sidan tunneln:

`route VPN-TUNNEL5 10.10.10.0 255.255.255.0 169.254.253.1`

Next-hop kan vara vad som då en next-hop krävs (namnet på interface som
styr).

### NAT

Tunnel interface ej går att välja som interface i NAT får man se till
att inte göra NAT Exempt som policy-based. Detta då trafiken lämnar ASAn
via tunnel interface och ej utsidan tex OUTSIDE.

### Access

Antingen kan man tillåta trafik in från andra sidan genom att låta ASAn
automatiskt lägga till allow regler för allt som det byggs tunnel för
(inklusive ssl vpn) annars kan man styra det med outside-aclen (för
tunnel interface acl per tunnel). Kolla om autoregler är påslaget:

`show run all | i permit-vpn`

Notera att autoregler är påslaget som standard. Stäng av autoregel för
vpn:

`no sysopt connection permit-vpn`

Tillåt trafik in från andra sidan med hjälp av ACL:
Policy-based

`access-list OUTSIDE-IN extended permit ip object LAN2 object LAN1`

Route-based

`access-list ACL-VPN-TUNNEL5 extended permit ip object LAN2 object LAN1`
`access-group ACL-VPN-TUNNEL5 in interface VPN-TUNNEL5`

**Troubleshoot**

`show crypto isakmp sa detail`
`show crypto ipsec sa`
`show vpn-sessiondb detail l2l`

**Reverse route**
Reverse route injection (RRI) tillåter att det installeras static routes
för det som finns på andra sidan av tunneln i routingtabellen när
tunneln blir aktiv. Kan t.ex. användas om man vill redistribuera
VPN-routes till ett routingprotokoll.

`crypto map VPNMAP 10 set reverse-route`

Remote Access
=============

AnyConnect
----------

AnyConnect SSL split tunnel
Objekt och pool

`ip local pool AnyConnect-Pool 172.20.0.51-172.20.0.100 mask 255.255.255.0`
`object network VPN_POOL`
` subnet 172.20.0.0 255.255.255.0`

ACL

`access-list AnyConnect-SplitTunnel standard permit 10.0.0.0 255.255.255.0  # LAN`
`access-list OUTSIDE-V1 remark ----- Allow AnyConnect to LAN`
`access-list OUTSIDE-V1 extended permit ip object VPN_POOL object LAN`

Enable anyconnect

`webvpn`
` enable OUTSIDE`
` anyconnect image disk0:/anyconnect-win-3.1.10010-k9.pkg 1`
` anyconnect enable`
` tunnel-group-list enable`
` cache`
`  disable`
` error-recovery disable`

Group policy

`group-policy GroupPolicy_Hackernet internal`
`group-policy GroupPolicy_Hackernet attributes`
` wins-server none`
` dns-server value 10.0.0.10`
` vpn-tunnel-protocol ssl-client `
` split-tunnel-policy tunnelspecified`
` split-tunnel-network-list value AnyConnect-SplitTunnel`
` default-domain value hackernet.se`

Tunnel group

`tunnel-group Hackernet type remote-access`
`tunnel-group Hackernet general-attributes`
` address-pool AnyConnect-Pool`
` default-group-policy GroupPolicy_Hackernet`
`tunnel-group Hackernet webvpn-attributes`
` group-alias Hackernet enable`

no nat

`nat (INSIDE,OUTSIDE) 5 source static any any destination static VPN_POOL VPN_POOL no-proxy-arp route-lookup`

Skapa lokala users

`username juan password cisco`
`username juan attributes`
` service-type remote-access`
` vpn-group-policy GroupPolicy_Hackernet`

[Category:Cisco](/Category:Cisco "wikilink")