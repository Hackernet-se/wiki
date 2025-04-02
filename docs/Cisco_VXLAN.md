---
title: Cisco VXLAN
permalink: /Cisco_VXLAN/
---

Virtual Extensible LAN (VXLAN) är en network virtualization technology,
med andra ord enkapsuleringsteknik (overlay). Det maximala antalet VLAN
på ett Ethernet-nätverk är 4094 (IEEE 802.1Q). Med VXLAN höjs denna
gräns till 16 miljoner. Ethernet frames enkapsuleras i IP-paket och
transporteras med UDP, default UDP destination port är 4789. Tack vare
att det är vanliga IP-paket som traverserar fabricen kan alla länkar
användas och det finns stöd för ECMP. VXLAN i sig har inget separat
control plane utan signalering får skötas av en extern controller, BGP
EVPN eller flood and learn. Vid det senare så kommer L2 flooding
(unknown unicast, broadcast) att emuleras med multicast och VTEP:arna
kommer på så sätt att lära sig vilka MAC-adresser som finns på andra
sidan. Detta leder till att VXLAN i sig har ingen inbyggd felisolering
så som t.ex. [OTV](/Cisco_OTV "wikilink") har. VXLAN har inte stöd för
service tags så som t.ex. Geneve har. Ska NX-OS manageras av en
third-party controller måste man slå på NXDB. Se även [Cisco
VLAN](/Cisco_VLAN "wikilink").

Flood and Learn
---------------

VXLAN Gateway använder sig av Network Virtualization Endpoint (NVE)
Interface. För att kunna använda multicast måste man köra
[PIM](/Cisco_PIM "wikilink") på underlay network. Om man ska enkapsulera
frames som är VLAN-taggade måste man ta bort taggen när det skickas VLAN
-\> VXLAN och sätta på den igen i andra riktningen, se exemplet
(BD-oriented mode).

`interface lo0`
` ip address 11.11.11.11 255.255.255.255`

`interface nve1`
` source-interface Loopback0`
` member vni 5001 mcast-group 239.0.10.10`

`interface GigabitEthernet2`
` service instance 1 ethernet`
`  encapsulation dot1q 100`
`  rewrite ingress tag pop 1 symmetric`

`bridge-domain 1`
` member vni 5001`
` member GigabitEthernet2 service-instance 1`

**Unicast**
Om man inte kan köra multicast går det lösa med unicast och headend
replication (HER). Då konfigurerar man *member vni* utan mcast-group och
istället pekar ut andra sidan VTEP:s manuellt.

`interface nve1`
` ingress-replication 22.22.22.22 `

Verify

`show nve vni`
`show nve peers`
`show bridge-domain 1`
`show mac address-table nve`

### Nexus

VXLAN är en vanlig overlay-teknik i datacenter. Underlay ska lösa
routing mellan IPv4-loopbacks samt ha stöd för jumbo frames (mtu 9216).
Man kan köra IP Unnumbered mellan leaf och spine. UDP port number är
4789, detta går ej att ställa om. ARP suppression är supporterat. För
tenants IGMP notera att interface nve1 default är en static
mrouter-port.

`feature nv overlay`
`feature vn-segment-vlan-based`
`interface nve1`
`  no shutdown`
`  source-interface loopback0`

Bridge domain med static flood list.

`vlan 100`
` vn-segment 10100`

`interface nve1`
`  member vni 10100`
`    ingress-replication protocol static`
`     peer-ip 10.0.0.3`
`     peer-ip 10.0.0.4`
`     peer-ip 10.0.0.5`

Verify

`show nve int nve1`
`show nve peers`
`show nve vni`
`show nve vni ingress-replication `

**Multicast underlay**
Ingress replication supporteras på Nexus 9000 men inte Nexus 5600 eller
Nexus 7000. Man får då lösa BUM med multicast. Alla noder måste routa
multicast. Best practice är att ha RP i spine-lagret. Använd anycast RP
för lastdelning samt redundans. Notera att multicast kontra unicast är
ett designval som innebär en trade-off mellan control plane scalability
och data plane efficiency.

Spine

`ip pim rp-address 10.0.0.100 group-list 224.0.0.0/4 `
`ip pim anycast-rp 10.0.0.100 10.0.0.2 `
`ip pim anycast-rp 10.0.0.100 10.0.0.3 `

`show ip mroute`

**Nexus 5600**
Nexus 5600 måste köra i store-and-forward switching mode för att
supportera VXLAN encapsulation.

`hardware ethernet store-and-fwd-switching`
`copy run start`
`reload`
`show switching-mode`

#### vPC

När man kör [vPC](/Nexus_vPC "wikilink") med VXLAN måste man sätta en
secondary IP address på det loopback som är source för NVE. Denna ska
vara samma på både vPC-peers och det är så dom presenterar sig själva
som en enda VTEP till remote NVE peers. CFS dubbelkollar att man har
gjort rätt. Däremot om peer-linken går ner så kommer loopback primary
address att användas som source på de VXLAN-enkapsulerade paketen som
skickas iväg.

vPC Best practice när man kör VXLAN.

`vpc domain 1`
` peer-switch`
` peer-keepalive destination 10.0.0.2 source 10.0.0.1`
` peer-gateway`
` ipv6 nd synchronize`
` ip arp synchronize`

Man bör också sätta upp ett nve-peer-link-vlan för att förhindra
suboptimal routing. Detta vlan ska endast tillåtas på trunken som är
peer-link.

`vlan 10`

`vpc nve peer-link-vlan 10`

`interface vlan10`
` ip router ospf 1 area 0`
` ip ospf cost 2`
` ip pim sparse-mode`
` no shut`

EVPN
----

Se [Cisco EVPN](/Cisco_EVPN "wikilink").

GPE
---

VXLAN Generic Protocol Extension finns till för att ge VXLAN tillägg
såsom OAM och versionsmöjligheter.

`interface Tunnel1 `
` ip address 192.168.1.1 255.255.255.0 `
` tunnel source GigabitEthernet2 `
` tunnel mode vxlan-gpe ipv4 `
` tunnel destination 10.0.0.20`
` tunnel vxlan vni 12345`

FHRP över VXLAN
---------------

Man kan använda [FHRP](/Cisco_FHRP "wikilink")-protokoll tillsammans med
VXLAN. De skickar hello packets som då floodas över VXLAN overlayet. Man
måste ge tcam till detta, *hardware access-list tcam region arp-ether
256*. Detta funkar endast med flood and learn VXLAN.

`interface vlan 100`
` ip address 192.168.1.2/24`
`  hsrp 100`
`   ip 192.168.1.1`

Q-in-VNI
--------

Endast VXLAN Bridging funkar med Q-in-VNI.

`interface nve1`
` overlay-encapsulation vxlan-with-tag`

`interface ethernet 1/4`
` switchport mode dot1q-tunnel`
` switchport access vlan 100`
` spanning-tree bpdufilter enable`

Man kan även släppa över LACPDU:er.

`interface nve1`
` overlay-encapsulation vxlan-with-tag tunnel-control-frames lacp`

QinQ-QinVNI

`interface Ethernet1/4`
` switchport trunk allow-multi-tag`

[Category:Cisco](/Category:Cisco "wikilink")