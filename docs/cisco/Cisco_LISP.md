---
title: Cisco LISP
permalink: /Cisco_LISP/
---

Locator/Identifier Separation Protocol (RFC 6830) är en routing och
adresseringsarkitektur utvecklat av Cisco men är en öppen standard.
Vanligtvis används en IP-adress för att representera både identitet och
lokation men med LISP separeras dessa som RLOC och EID (som går att mixa
mellan IPv4 och IPv6). Att separera identitet och lokation är möjligt
eftersom LISP tunnlar trafik med UDP, dvs det är overlay. Med hjälp av
en registreringsprocess skapas det en mapping database på en ciscorouter
som agerar Map Server och Map Resolver. Denna databas håller alla EID
\<-\> RLOC mappings och det är den man frågar för att få veta var
trafiken för olika IP-adresser ska tunnlas. LISP control plane använder
udp 4342 och data plane trafik skickas till udp 4341.

### Terminology

-   Routing Locator (RLOC)
-   Endpoint ID (EID)
-   Egress Tunnel Router (ETR)
-   Ingress Tunnel Router (ITR)
-   Egress/Ingress Tunnel Router (xTR)
-   Proxy Ingress Tunnel Router (P-ITR)

[<File:Cisco_LISP.png>](/File:Cisco_LISP.png "wikilink")

Konfiguration
-------------

**Map Server/Resolver**
På MS/MR konfar man vilka sites som får registrera sig, med sites menas
de prefix/adresser som ska LISP:as. Dvs det är inte en vitlista på RLOCs
som får registrera sig däremot måste MS/MR kunna nå alla RLOC-adresser.
Det går att ha dessa roller på olika enheter men det finns ingen större
vinning med det eftersom MS/MR inte behöver finnas i data plane. För att
göra MS/MR-funktionen redundant kan man bygga IP anycast.

`router lisp`
` ipv4 map-server`
` ipv4 map-resolver`

` site SITE_A`
`  authentication-key SITE_A_KEY`
`  eid-prefix 192.168.1.0/24`

*alla lokala ip-adresser på MS/MR används default av LISP*

**Branch Site**
MS/MR ska vara nåbar med unicast i default-vrfen. Man kan ha flera RLOCs
på samma site för redundans och lastdelning, då ska alla konfas likadant
vad gäller RLOC-adresser. Med priority kan man styra vilken RLOC som ska
användas. Har två stycken samma prio kan man styra lastdelning med
weight. RLOC:ar inom samma site kommer automatiskt proba varandra för
att kolla att de lever.

`router lisp`
` ipv4 itr map-resolver 10.0.0.10`
` ipv4 itr`
` ipv4 etr map-server 10.0.0.10 key SITE_A_KEY`
` ipv4 etr`

` database-mapping 192.168.1.0/24 IPv4-interface GigabitEthernet2 priority 1 weight 1`

Verify

`show lisp`
`show lisp site`
`show ip lisp map-cache `
`show ip lisp database`

`clear ip lisp map-cache *`

*map cache default TTL: 24h*

### Data Center

Genom att tillåta registrering av mer specifika routes (/32-routes) kan
man lösa VM mobility mellan datacenter. IP-adressen på roaming device
måste vara inom EID-prefixet. En LISP xTR konfigurerad för LISP VM
mobility och dynamiska EIDs är en LISP-VM router. Den avgör dynamiskt om
en VM finns i det direktanslutna subnätet eller någon annanstans.
LISP-VM routers är RLOCs som används för enkapsulering till EID.

`router lisp`
` site DATA_CENTER`
`  authentication-key DC_KEY`
`  eid-prefix 10.8.0.0/16 accept-more-specifics`

### PxTR

Proxy xTR kan användas för att lisp-siter ska kunna nå non-lisp-aware
sites. Då skickas paketen native ip ut ur nätverket och sedan
lisp-enkapsulerat på vägen tillbaka till siten.

`router lisp`
` ipv4 proxy-etr`
` ipv4 proxy-itr 2.2.2.2  #local ip`
` ipv4 itr map-resolver 8.8.8.8`
` map-cache `*`EID-prefix`*` map-request`

**MTU**
PMTUD är på default.

`router lisp`
` ipv4 path-mtu-discovery min 576 max 65535`
` ipv6 path-mtu-discovery min 1280 max 65535`

### VRF

EIDs och RLOCs kan separeras i olika VRF:er.

`router lisp`
` locator-table vrf UNDERLAY`

` eid-table vrf Cust_A instance-id 101`
`  database-mapping 192.168.1.0/24 10.0.0.10 priority 1 weight 1`

[Category:Cisco](/Category:Cisco "wikilink")