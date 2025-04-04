---
title: Cisco PE-CE
permalink: /Cisco_PE-CE/
---

PE routers redistribuerar routes till BGP och konverterar dem till VPNv4
NLRI. Denna NLRI annonseras till andra PE med hjälp av MP-BGP. Dessa PE
konverterar tillbaka VPNv4 routes och skickar det vidare till CE.
Se även [Cisco BGP](/Cisco_BGP "wikilink"), [Cisco
Routing](/Cisco_Routing "wikilink") och [Cisco
MPLS](/Cisco_MPLS "wikilink").

RIP
---

RIP är det simplaste protokollet och om man använder **transparent** så
kommer RIPs metric att tas ifrån BGP MED attribute som är en kopia av
RIP metricen från andra sidan. Detta gör att man kan få till bra path
selection även om det finns backdoor links. RIPv1 stöds inte. Se även
[Cisco RIP](/Cisco_RIP "wikilink").

`router rip`
` version 2`
` address-family ipv4 vrf Cust_A`
`  redistribute bgp 100 metric transparent`
`  network 192.168.1.0`

`router bgp 100`
` address-family ipv4 vrf Cust_A`
`  redistribute rip`
` exit-address-family`

OSPF
----

OSPF för PE-CE (RFC 4577), se även [Cisco OSPF](/Cisco_OSPF "wikilink").
MPLS-nätet skickar OSPF VRF routing information i MP-BGP-uppdateringar
och det kommer att agera som en OSPF super-backbone vilket gör att man
faktiskt inte behöver köra med area 0 någonstans men man kan såklart
göra det. Man kan t.o.m. ha area 0 på flera siter. När routes går från
MP-BGP till OSPF ska down biten sättas, detta för att förhindra loopar.
När routes redistribueras från OSPF till MP-BGP ska domain-id vara
konfat. Om OSPF domain-id är samma på båda sidor kommer routes att
exporteras som type-3 inter-area LSA och om de inte är samma kommer
routes att exporteras som type-5 external LSA. Om man inte specifikt
anger något Domain ID på IOS så kommer process ID att användas. På
IOS-XR sätts NULL ifall man inte har konfigurerat något.

`interface gi0/0`
` description Link to CE`
` vrf forwarding Cust_A`
` ip ospf 2 area 0`

`router ospf 2 vrf Cust_A`
` router-id 10.0.0.10`
` `**`domain-id`` ``1.1.1.1`**
` redistribute bgp 100 subnets`

`router bgp 100`
` address-family ipv4 vrf Cust_A`
`  redistribute ospf 2 vrf Cust_A`
` exit-address-family`

OSPF har inbyggd loop prevention genom att tagga alla routes som har
redistribuerats från MPLS-nätet till OSPF med en down bit i LSA:n. Om
detta kommer till en VRF-aware OSPF-process (t.ex. på en annan PE)
kommer det att droppas. Så detta behövs på en CE som kör VRF Lite annars
kommer LSA:er som kommer ifrån MPLS Superbackbone att ignoreras. I nyare
IOS sätts down bit på både typ 3 och typ 5 LSA, förr var det endast typ
3. Det finns även en domain tag som skickas med prefixen, default är det
208.0.0.0 + ASN fast i decimal format. Syftet med domain tag är loop
prevention, det är fallback för DN bit som man kan behöva att kringgå om
man kör vrf-lite.

`router ospf 1 vrf Cust_A`
` capability vrf-lite `

### Sham-Link

Om kund har en bakväg mellan sina siter av t.ex. redundansskäl kommer
OSPF att föredra den framför MPLS-nätet eftersom routes som gått över
L3-VPN:n skickas med BGP och då blir inter-area eller externa för OSPF.
Intra-area routes är preferred över inter-area och external routes
oavsett metric. OSPF sham link tillhandahåller en logisk länk mellan två
VRFer på PE. Det är en tunnel som ser ut som en point-to-point länk för
OSPF. Med hjälp av detta kan man lura OSPF att tro att den bästa vägen
är över MPLS-nätet. Detta är endast control plane dvs för SPF
calculations och best-path selection medans forwarding görs som vanligt
med information från MP-BGP. Sham-links har source på interface som
finns i kundens VRF, t.ex. Loopbacks uppsatta för detta ändamål. Deras
IP-adresser bör annonseras på något annat sätt än OSPF (typ BGP).

PE1

`interface Loopback 20`
` ip vrf forwarding Cust_A`
` ip address 3.3.3.3 255.255.255.255`

`router ospf 2 vrf Cust_A`
` area 0 sham-link 3.3.3.3 1.1.1.1 cost 10`

PE2

`interface Loopback 20`
` ip vrf forwarding Cust_A`
` ip address 1.1.1.1 255.255.255.255`

`router ospf 2 vrf Cust_A`
` area 0 sham-link 1.1.1.1 3.3.3.3 cost 10`

Verify

`show ip ospf sham-links`

EIGRP
-----

När man använder EIGRP som PE-CE skickas metric values, route type,
source AS\#, remote Router ID med i BGP-uppdateringarna som extended
communities. Detta gör att när man kör EIGRP \<-\> BGP (VPN) \<-\> EIGRP
blir routsen internal, däremot om routsen har kommit från något annat än
EIGRP, dvs saknar dessa communities, blir de external ur EIGRPs
perspektiv. EIGRP-prefix som redistribueras in i BGP kommer också att ha
ett Cost value som används för path selection. Se även [Cisco
EIGRP](/Cisco_EIGRP "wikilink").

`router eigrp 100`
` address-family ipv4 vrf Cust_A autonomous-system 200`
`  redistribute bgp 100 metric 10000000 0 255 1 1500`
`  no auto-summary`
` exit-address-family`

`router bgp 100`
` address-family ipv4 vrf Cust_A`
`  redistribute eigrp 200`
` exit-address-family`

### Site-of-Origin

SoO skickas som extended community (både i BGP och EIGRP) och används
för loop prevention för VPN-kunder som är multi-homed. Kommer det in
routes med SoO satt till det man själv har discardas dem. Samma resultat
går också att uppnå med route tagging men är lite mer omständigt att
konfigurera. Beroende på designval så sätter man samma SoO-värde på båda
PE downlinks.

`route-map SoO permit 10`
` set extcommunity soo 100:2`

`interface Gi2`
` description Link to CE`
` vrf forwarding Cust_A`
` ip vrf sitemap SoO`

BGP
---

Om man använder BGP för PE-CE behövs ingen redistribution eftersom det
är samma routing-protokoll som MPLS-nätet använder samt att skalbarhet
och kontroll (policy) är bra. Det går även att köra iBGP som PE-CE, se
RFC 6368.

Cost Community
Syftet med Cost Communities är att förhindra suboptimal routing och
routing loops. Det går att stänga av.

`router bgp 100`
` bgp bestpath cost-community ignore`

**SoO Attribute**
Site-of-Origin används för loop prevention och konfigureras på PEs
grannskap till CE. Uppdateringar med det konfigurerade SoO-värdet kommer
varken skickas eller accepteras, dvs det är filtrering både ingress och
egress.

`router bgp 100`
` address-family ipv4 vrf Cust_A`
`  neighbor 1.1.1.1 soo 10:12`

Samma resultat går att uppnå med en route-map som sätter denna community
men det kan bli omständigt att konfigurera.

IS-IS
-----

IS-IS är inget vanligt PE-CE protokoll men det går at köra på IOS. ISIS
har ingen loop prevention så man måste filtrera om man ska köra dual
homed/redundant kopplat till mpls-nätet.

`router isis 10`
` vrf CustA`
` net 49.0000.0000.0010.00`
` redistribute bgp 100 level-1-2`

Route Leaking
-------------

Med hjälp av route targets kan man bygga vilken logisk topologi man vill
för sina L3 VPN:er.

`vrf definition Cust_A`
` rd 65000:1`
` address-family ipv4`
`  route-target both 65000:1`
`  route-target import 65000:999`

`vrf definition Cust_B`
` rd 65000:2`
` address-family ipv4`
`  route-target both 65000:2`
`  route-target import 65000:999`

`vrf definition Shared`
` rd 65000:999`
` address-family ipv4`
`  route-target export 65000:999`
`  route-target import 65000:1`
`  route-target import 65000:2`

[Category:Cisco](/Category:Cisco "wikilink")