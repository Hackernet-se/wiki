---
title: Nexus vPC
permalink: /Nexus_vPC/
---

Virtual Port-Channel är Ciscos MLAG-variant för
[Nexus](/Cisco_Nexus "wikilink")-switchar. Båda switchar i paret är
aktiva för data plane men den ena noden står för control plane och tar
därmed hand om BPDUer och LACPDUer. Det är inte delad management plane,
som t.ex. [Cisco VSS](/Cisco_VSS "wikilink"). För att avgöra om noderna
i paret har kompatibel konfiguration (consistency validation) skickas en
kopia med Cisco Fabric Services över peer-länken. Alla mac-adresser och
IGMP snooping som switcharna lär sig synkroniseras också mha CFS över
peer-länken. Peer-länken är med i [STP](/Cisco_STP "wikilink") men
BPDU-hanteringen är modifierad så peer link kommer aldrig att bli
blocking/discarding. Icke-vPC portar kommer att hanteras av den lokala
STP-processen på varje switch. Se även [Cisco
EtherChannel](/Cisco_EtherChannel "wikilink").

Det går att köra dynamisk routing över vPC men generellt sett är det
inte rekommenderat samt att det endast går på vissa releaser. Det
konfigureras under vPC-domänen med *layer3 peer-router*.

Initial setup
-------------

Aktivera vPC

`feature vpc`
`feature lacp`

vPC peers skickar varje sekund keepalives mellan varandra. Man kan t.ex.
använda mgmt-portarna för keepalives, det är endast små UDP-paket som
ska skickas och tas emot.

<div class="mw-collapsible mw-collapsed" style="width:300px">

Keepalive message:

<div class="mw-collapsible-content">

[<File:Nexus-vPC-Keepalive.PNG>](/File:Nexus-vPC-Keepalive.PNG "wikilink")

</div>
</div>

Exempel: skapa en dedikerad vrf för keepalives och assigna interface.

`vrf context VPC-KEEPALIVE`
`interface po1`
` no switchport`
` vrf member VPC-KEEPALIVE`
` ip address 10.255.255.1/30`
` no shut`

**Domänkonfiguration**
En VPC-domän har default en restore-delay på 30 sekunder.

`vpc domain `<number>
` role priority 1`
` system-priority 1000`
` system-mac 00:00:11:11:22:22`
` peer-keepalive destination 10.255.255.2 source 10.255.255.1 vrf VPC-KEEPALIVE`
` peer-gateway`
` auto-recovery`
` ip arp synchronize`
` ipv6 nd synchronize`

Default-värden för keepalive: udp-port 3200, vrf management, interval
1000, timeout 5, precedence 6, hold-timeout 3

"system-priority" och "system-mac" bestämmer vilken LACP system priority
och actor system som ska användas i LACPDU:er. System MAC används även
för BPDU:er. Om man kör [FabricPath](/Nexus_FabricPath "wikilink") lägg
även till: *fabricpath switch-id <id>* under domänkonfigurationen.
Auto-recovery är på default och det bör det vara, det ser till att man
kan bli forwarding trots att peer aldrig kommer upp, t.ex. om man endast
har en switch eller den andra inte startar efter ett strömavbrott.

Konfigurera vPC peer-link

`interface port-channel2`
` switchport`
` switchport mode trunk`
` spanning-tree port type network  #för Bridge Assurance`
` vpc peer-link`

Verify

`show vpc `
`show vpc peer-keepalive `
`show vpc role`
`logging level vpc 5`

För att byta role: *vpc role preempt*

Konfiguration
-------------

Skapa vPC:er genom att assigna interface. Status på dessa vPC member
ports signaleras med CFS mellan peers.

`interface Ethernet1/20`
` switchport mode trunk`
` channel-group 20 mode active`

`interface port-channel20`
` switchport mode trunk`
` vpc 20`

**LACP**
NX-OS har ”graceful convergence” aktiverat som standard. Denna funktion
förbättrar hanteringen av handskakningen för LACP. När en PortChannel
går mot en enhet som inte kör NX-OS så ska denna funktion stängas av för
att minska risken att en individuell port går ner i ”suspended state”.
Notera att man emot vmware esxi bör slå på graceful convergence,
CSCuy84084.

`interface port-channel10`
` no lacp graceful-convergence`

**Individual port**
Portar som inte får in LACPDU:er räknas som "individual". Man kan välja
om portar som inte lyckas med LACP-förhandling ska fallbacka till
individuella switchportar eller suspendas. Detta är t.ex. användbart om
man har servrar med multipla NIC som ska
[PXE](/PXE-Deploy "wikilink")-boota. Individuella switchportarna kommer
att fortsätta skicka LACPDU:er för att försöka etablera LACP
negotiation. Standardparametrarna för hanteringen av individuella portar
inom en PortChannel skiljer sig mellan Nexus 7000 och Nexus 5000. När
man uppgraderar till nyare NX-OS så läggs "no lacp suspend-individual"
till i running config på interface med default-konfiguration, innan
syntes inte detta. När Nexus 5000 ansluts till andra nätverksenheter,
använd suspend-individual för PortChannel:n.

`interface port-channel10 `
` lacp suspend-individual`

**Verify**
show vpc brief

`show port-channel database`
`show vpc consistency-parameters vpc 5`
`show vpc orphan ports`
`show lacp neighbor`

Vid en Type 1 mismatch för ett visst vlan så kommer vlanet endast att
suspendas på vPC:er på secondary vPC peer, detta kallas graceful
consistency check och är på default.

Advanced troubleshooting

`show cfs status`
`show cfs peers`
`show cfs internal notification log name vpc`

**Load balancing method**

`show port-channel load-balance `

Notera att på Nexus 7000 går det endast ändra load balancing method i
default VDC:n och detta slår chassis-wide, däremot går det att ställa in
per linjekort.

**Multicast**
Peers utbyter metrics över CFS för nya sources.

`show ip pim internal vpc rpf`

**BDPU**
Ändra så att VPCer använder Cisco OUI i BPDUer istället för
0026.fxxx.0000.

`Nexus7000(config-vpc-domain)# mac-address bpdu source version 2 `

vPC Enhancements
----------------

**Peer-switch**
vPC Peer-switch möjliggör för ett vPC-par att presentera sig som en
logisk enhet i STP genom att de delar på ett virtuellt bridge ID. Båda
peer-enheterna kommer även att skicka ut dessa identiska BPDU:er, samt
processa inkommande BPDU:er. Om peer-switch inte är påslaget, är det
endast primär-enheten skickar ut BPDU:er och sekundär-enheten agerar
proxy för primären och forwarderar inkommande BPDU:er till den över
peer-länken. Tack vare peer-switch kortas trafikavbrottet till följd av
en peer-krasch ned avsevärt, enligt Cisco själva till under sekunden, på
grund av att ingen logisk topologiförändring sker i STP. Det
rekommenderas att använda sig av peer-switch i en vPC-domän.

Med peer-switch påslaget är båda peer-enheterna tvungna att ha exakt
samma spanning tree-konfiguration för samtliga vPC VLAN. Peer-switch
måste även det vara konfigurerat på båda sidor. För att slå på
peer-switch:

`vpc domain 1`
` peer-switch`

**Peer-gateway**
vPC Peer-gateway tillåter en vPC peer-enhet att agera gateway för paket
som adresserats till den andra peer-enhetens MAC-adress. På så vis
behålls routingen lokalt istället för att i onödan traversera
peer-länken. Denna funktion är huvudsakligen till för att på ett bättre
sätt hantera enheter som inte använder standard-ARP för sin default
gateway, till exempel vissa lastbalanserare. Det finns inga nackdelar
med denna teknologi och rekommenderas att aktivera i alla
vPC-installationer, även denna funktion ska aktiveras på båda
peer-enheterna. Båda vpc-peers blir också aktiva forwarders för HSRPs
vMAC. För att slå på peer-gateway:

`vpc domain 1`
` peer-gateway`

**ARP Sync**
För att snabba upp återskapandet av ARP-tabellen efter exempelvis
peer-flap eller att ett SVI gått up kan man använda sig av
ARP-synkronisering mellan vPC-enheterna. Efter att något av tidigare
nämnda händelser inträffat kommer båda enheterna då att synkronisera
sina ARP-tabeller med varandra över peer-länken. Det rekommenderas
starkt att alltid aktivera IP ARP synchronization på båda
peer-enheterna. För att aktivera ARP sync:

`vpc domain 1`
` ip arp synchronize`

`show ip arp vpc-statistics `

**Nexus 9000**
Om man slår på vPC Fast Convergence så enablear man en feature som heter
MCT Down Handler. Då skapas en lista med member ports, layer-3
interfaces (SVI:er) och alla vlan de använder. Om peer-linken failar så
skickas ett suspend-meddelande till alla dem samtidigt. Det betyder att
SVI:erna inte stängs ner först vilket förhindrar traffic loss.

`vpc domain 1`
` fast-convergence`

Detta används för att förbättra konvergens av Layer 2
[EVPN](/Cisco_EVPN "wikilink") VXLAN.

`interface port-channel 10`
` lacp vpc-convergence`

**Hybrid Setup - Spanning Tree**
Om man har en mix av enheter på vPC och icke-vPC-portar kopplade till
sin vPC-domän kan man ändå välja att switcharna skickar ut olika BPDU:er
och därmed lastdela trafiken VLAN-baserat. Denna konfig overidar annan
stp rootprio-konf.

`spanning-tree pseudo-information`
` vlan 10,20 root priority 16384`
` vlan 10 designated priority 4096`
` vlan 20 designated priority 61440`

Failover Behavior
-----------------

Olika fel kan uppstå i ett datacenter och vPC har vissa mekanismer för
att hantera det. Om peer-länken går ner så används peer-keepalive för
att kolla status på peeren. Om båda noder är aktiva kommer sekundären
att stänga ner alla sina vPC-portar, detta för att förhindra loopar. Går
både peer-länk och peer-keepalive ner samtidigt kan det vara svårt att
upptäcka samt möjlig service disruption. Kör man heartbeats på
mgmt-porten så märks åtminstone att man tappat mgmt av noderna.
Heartbeat-gränser går att konfigurera.

Om hela ena noden går ner så kommer den kvarvarande att ta över all
forwardering. Var länkar redan innan device failure överlastade kan det
såklart bli traffic drops. Finns det något konfigurationsfel mellan
noderna så går inte Consistency Check igenom och då kommer endast den
primära noden att vara aktiv för forwardering. Beroende på typ av
mismatch så genereras syslog-meddelanden.

`show vpc consistency-parameters global`

Back to Back
------------

Man kan koppla ett vpc-par till ett annat vpc-par och köra en vpc på
varje sida, detta kallas back-to-back vPC. Detta kan t.ex. användas
mellan aggregation och access layer. Det går också att använda som
DCI-lösning om man inte använder någon overlay-teknik eller om man vill
ha alla länkar aktiva och avgränsa STP. Man kan stänga av att BPDU:er
skickas (portfast) och ha varje DC i egen STP-domän.

Det finns inga speciella kommandon eller hårdvarukrav för detta utan det
är en implementationsvariant, man konfar vpc på båda sidor. Dock måste
vPC domain ID skilja sig mellan paren.

[<File:Cisco_vPC_B2B.PNG>](/File:Cisco_vPC_B2B.PNG "wikilink")

[Category:Cisco](/Category:Cisco "wikilink")