---
title: Cisco MVPN
permalink: /Cisco_MVPN/
---

Multicast VPN (MVPN) möjliggör multicast över
[L3VPN](/Cisco_MPLS#VPN "wikilink"). En viktig komponent för MVPN är
BGP, safi MVPN kan göra två saker: Auto-Discovery routes och C-mcast
signaling. PE-CE är alltid PIM men underlay i core kan göras på en mängd
olika sätt och stäm därför alltid av med Ciscos dokumentation över
MVPN-profilerna.

-   **IOS:**
    <https://www.cisco.com/c/en/us/support/docs/ip/multicast/118985-configure-mcast-00.html>
-   **IOS-XR:**
    <https://www.cisco.com/c/en/us/support/docs/ip/multicast/200512-Configure-mVPN-Profiles-within-Cisco-IOS.html>

[Cisco_MVPN.PNG](/Cisco_MVPN.PNG "wikilink")

MLDP
====

Multicast Label Distribution Protocol (MLDP) är en extension till LDP
som används för att sätta upp P2MP och MP2MP LSP:er i MPLS-nätverk. I
overlay (allt som har med vpn/vrf context att göra) kan man använda PIM
och/eller BGP för control plane. Det finns även in-band signaling med
MLDP, det man gör i praktiken är att stitcha ihop customer pim tree med
MLDP LSP:er i core. Detta är inte superskalbart eftersom P-noder måste
hålla state för kunders multicast-träd. I varje MLDP-träd finns en root,
för att lösa root node redundancy kan man antingen köra med en phantom
root (olika masklängd på loopbacks) eller med två parallella root-noder.
Det senare kräver mer state men har snabbare konvergens eftersom all
signalering redan är gjord. Eftersom alla är med i båda träd kan man
skicka multicastströmmar i valfritt träd. Med MLDP swapas label per hop
men det finns ingen PHP. Det finns stöd för FRR.

MLDP utbyts som en capability, alla plattformar har inte stöd för MLDP.

`show mpls ldp capabilities`
`show mpls mldp neighbors`

Core tree types. Ciscos namn kontra RFC:

-   Default MDT = Multi-directional inclusive PMSI
-   Data MDT = Selective PMSI
-   Partitioned MDT = Multi-directional selective PMSI

![Cisco_mLDP.PNG](img/Cisco_mLDP.PNG)

![Cisco_MVPN_in-band.PNG](img/Cisco_MVPN_in-band.PNG)

IOS
---

Konfiguration

`ip multicast mpls mldp`
`mpls mldp logging notifications`

Exempel

`ip multicast-routing vrf VPN_A distributed`
`!`
`vrf definition VPN_A`
` vpn id 100:100`
` address-family ipv4`
` mdt default mpls mldp 11.11.11.11`
` mdt data mpls mldp 110`
` mdt data threshold 30`

Verify

`show ip multicast mpls vif`
`show mpls mldp database brief`
`show mpls mldp root`
`ping mpls mldp mp2mp `<root>` mdt `<vpn-id>` 0`

Det finns ingen MBB by default.

`mpls mldp make-before-break delay 5000`

IOS-XR
------

Konfiguration

`multicast-routing`
` address-family ipv4`
`  interface Loopback0`
`   enable`
`!`
`mpls ldp`
` mldp`
`  logging notifications`

Verify

`show mpls forwarding p2mp`
`show mpls mldp forwarding`
`show mrib mpls forwarding`

Om man kör t.ex. Segment Routing har man inget behov av LDP, då kan man
köra MLDP only.

`mpls ldp`
` capabilities sac mldp-only`

**MoFRR**
MoFRR bygger två träd, egress PE måste ha IGP ecmp till ingress PE.

`mpls ldp`
` mldp`
`  address-family ipv4`
`   mofrr`

Unified MPLS
------------

MVPN över unified MPLS eller Inter-AS MPLS option C funkar faktiskt men
det är en växel man måste slå på i egress PE.

IOS-XE

`mpls mldp forwarding recursive-fec`

IOS-XR

`mpls ldp mldp address-family ipv4 recursive-fec`

![Cisco_MPLS_Seamless.PNG](img/Cisco_MPLS_Seamless.PNG)

[Category:Cisco](/Category:Cisco "wikilink")