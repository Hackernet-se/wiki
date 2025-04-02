---
title: Nexus VDC
permalink: /Nexus_VDC/
---

Virtual Device Context kan användas för att virtualisera Nexusswitchar
på Nexusswitchar. En fysisk switch blir flera logiska med egna fysiska
portar och processer. Detta är en partitioneringsteknik och varje VDC
manageras för sig. Eftersom varje VDC har egen data plane, control plane
och mgmt plane innebär detta en viss grad av fault isolation däremot kan
inte olika VDC:er köra olika versioner av NX-OS. Det fysiska mgmt0
interface delas dock men varje VDC får ha egen IP-adress. Varje VDC har
även egna unika MAC-adresser, detta tas ifrån backplanet (show sprom
backplane). Notera att [FCoE](/Cisco_FCoE "wikilink") kräver sin egna
VDC. Se även [Cisco Nexus](/Cisco_Nexus "wikilink").

**User rights**
Default-VDC

-   Network-Admin = VDC-Admin
-   Network-Operator = VDC-Operator

Non-Default VDC

-   VDC-Admin = all read/write for that particular VDC
-   VDC-Operator = read only access to that particular VDC

Konfiguration
-------------

*Requires Advanced Services license*

Skapa Admin VDC, denna kontrollerar övriga VDC:er. Denna har t.ex. hand
om VDC creation, resource allocation, NX-OS upgrade,
[Ethanalyzer](/Cisco_SPAN#Ethanalyzer "wikilink"), System wide
[QoS](/Cisco_QoS "wikilink"), Port Channel load balancing hash,
[EEM](/Cisco_IOS#EEM "wikilink") applets. Inga line cards tillåtna.

`conf`
`system admin-vdc`

Skapa VDC

`vdc `<name>` id 2`
` cpu-share 10`
` allocate interface Ethernet1/1-8`
` boot-order 1`
` limit-resource vlan minimum 512 maximum 4094`

`vdc VDC3 id 3`
` cpu-share 10`
` allocate interface Ethernet2/1-8`
` boot-order 2`
` limit-resource vlan minimum 512 maximum 4094`

Notera att ändringar av en VDC är disruptive. Man kan inte heller
allokera enskilda interface till en VDC utan man allokerar en (eller
flera) interface-range. Vilka interface som kan ingå i en range avgörs
av hardware port group (asic) dvs detta skiljer sig mellan olika
plattformar och linjekort. Skriver man en ogiltig range så kommer dock
NX-OS korrigera det automatiskt. Man kan alltså råka sno interface ifrån
en annan VDC om man inte tänker sig för.

Hoppa mellan VDC:ers CLI.

`switchto vdc `<namn>
`switchback`

Alias

`cli alias name changeto switchto vdc`

Default visas VDC hostname som <admin-vdc>-<vdc-name>, detta går att
stänga av.

`no vdc combined-hostname `

### High Availability

Man kan konfa vad som ska hända om en VDC kraschar. Man kan ha olika
settings för single kontra dual supervisor. Det man kan välja på är
RESTART vdc, BRINGDOWN vdc, RELOAD supervisor, SWITCHOVER to standby
supervisor.

`ha-policy single-sup bringdown dual-sup switchover`

### Verify

`show vdc`
`show vdc resource`
`show vdc membership`
`copy running-config startup-config vdc-all`

Notera att det finns en VDC med ID 0, den används endast som en
container för interface som inte får vara med i någon annan VDC.

Nexus är en switch men varje VLAN representeras internt av en bridge
domain. Detta gör att flera VDC:er kan deploya VLAN med samma ID.

`show vlan internal bd-info vlan-to-bd all-vlan`

Har man för lite ström för att klara ett PSU-bortfall startas inte alla
linjekort, *show module* säger "pwr-denied". Man kan ändra detta
beteende för att stänga av redundans.

`power redundancy-mode combined`

### Routing tables

Man kan styra hur mycket minne en VDC minimum och maximum får till IPv4
och IPv6 unicast och multicast routes.

`vdc VDC3`
` limit-resource u4route-mem minimum 2 maximum 100`

`show vdc resource u4route-mem detail`

Man ska såklart monitorera hur mycket resurser sina VDC:er använder men
man kan också kolla hur mycket minne som behövs för en viss mängd
routes.

`show routing ip unicast memory estimate routes 100000 next-hops 2`

### Storage VDC

Man kan använda en Storage VDC för att köra Ethernet och FCoE i samma
switch.

`license fcoe module 2`

`system qos`
` service-policy type network-qos default-nq-7e-4q8q-policy`

`vdc SAN type storage`
` allocate interface e2/1-8`
` allocate fcoe-vlan-range 100-101`

[Category:Cisco](/Category:Cisco "wikilink")