---
title: Cisco NetFlow
permalink: /Cisco_NetFlow/
---

Netflow är ett Cisco-properitärt protokoll som används för att kunna
exportera data om vilka adresser och protokoll som används i ett nätverk
och hur mycket trafik de genererar. De vanligaste versioner som används
är 5 och 9. Den stora skillnaden är att v5 inte har stöd för IPv6 eller
MPLS. Samt att v5-paket har ett fixerat paketformat. Paket för version 9
kan se olika ut och man kan ändra det med templates. Det finns även
IETF-standard,
[IPFIX](https://en.wikipedia.org/wiki/IP_Flow_Information_Export). Se
även [Cisco SPAN](/Cisco_SPAN "wikilink").

Komponenter:

-   Flow exporter, t.ex. en router
-   Flow collector, t.ex. [Pmacct](/Pmacct "wikilink")
-   Analysis application, t.ex. [Ntopng](/Ntopng "wikilink"),
    [FastNetMon](/FastNetMon "wikilink")

### Paket

Ett NetFlow-paket skickas med UDP och kan innehålla metadata om flera
trafikflöden.

<div class="mw-collapsible mw-collapsed" style="width:310px">

-   NetFlow v9:

<div class="mw-collapsible-content">

[<File:Cisco_Netflow_v9.png>](/File:Cisco_Netflow_v9.png "wikilink")

</div>
</div>

Om man använder version 9 så skickar Cisco-enheter en NetFlow-template
var 20:e paket så mottagare vet vilken information NetFlow-paketen
innehåller.

<div class="mw-collapsible mw-collapsed" style="width:310px">

-   NetFlow template:

<div class="mw-collapsible-content">

[<File:Cisco_NetFlow_Template.png>](/File:Cisco_NetFlow_Template.png "wikilink")

</div>
</div>

Konfiguration
=============

Legacy IOS syntax

`int gi0/0`
` ip flow ingress`
` ip flow egress`

Top-talkers

`ip flow-top-talkers`
` sort-by bytes`
` top 5`

Show

`show ip flow top-talkers `
`show ip cache flow `

### ASR

IOS-XE använder den modernare syntaxen som kallas Flexible NetFlow. Man
kan även definiera och använda egna flow records, dvs vilken information
som ska exporteras.
OBS en ASR 1000 kan inte använda sitt management-interface som source
för NetFlow-exporten.

`flow exporter COLLECTOR`
` destination 10.0.0.10`
` transport udp 2055`
` source gi0/1`
` export-protocol netflow-v9`

`flow monitor FLOW-MONITOR`
` record netflow ipv4 original-input `
` exporter COLLECTOR`
` cache timeout active 60`

`interface gi0/3`
` ip flow monitor FLOW-MONITOR input`

"Random Sampled NetFlow is more statistically accurate than Sampled
NetFlow." - Cisco

`sampler SAMPLER-1`
` mode random 1 out-of 1000`
`interface gi0/3`
` ip flow monitor FLOW-MONITOR sampler SAMPLER-1 input`

Verify

`show flow exporter`
`show flow interface`
`show flow monitor`
`show flow exporter statistics`
`show flow record`
`show sampler`

**MPLS-aware NetFlow**

`interface gi2`
` mpls netflow egress`

### EzPM

Med Easy Performance Monitoring så autokonfas allt man behöver utifrån
en färdig profil, man kan välja mellan prestanda, upplevelse och
statistik. Man får tillgång till alla Application, Visibility and
Control (AVC) features.

`performance monitor context EzPM profile application-experience`
` exporter destination 10.0.0.10 source loopback0 transport udp port 2055 [vrf]`
` traffic-monitor all`

`interface Gi0/1`
` performance monitor context EzPM`

Verify

`show performance monitor context EzPM`

### Nexus

`feature netflow`

`flow exporter COLLECTOR`
` destination 10.0.0.10 use-vrf management`
` version 9`
` transport udp 2055`
` source mgmt 0`

`flow monitor FLOW-MONITOR`
` exporter COLLECTOR`
` record netflow-original`

Ska man samla in netflow på ett interface i ett F3-kort måste sampler
användas.

`sampler SAMPLER-1`
` mode 1 out-of 5`

Interface

`interface Ethernet1/1`
` ip flow monitor FLOW-MONITOR input sampler SAMPLER-1`

Verify

`show flow record netflow-original`
`show flow exporter`
`show flow monitor `
`show flow interface`

**Layer 2**
Man kan även exportera metadata för L2-trafik med netflow. Notera att
flow monitor måste ha flow records för L2, dvs Vlan, MAC och ethertype.

`interface e1/1`
` switchport`
` layer2-switched flow monitor FLOW-MONITOR input`

IP Accounting
=============

IP Accounting är en annan feature i IOS som också kan användas för att
kolla trafik lokalt, dock mindre populär än NetFlow.

`ip accounting-threshold 1200`
`ip accounting-list 10.0.10.0 0.0.0.255`
`int g2/0`
` ip accounting output-packets`

`show ip accounting`
`clear ip accounting`

Stores the old accounting database into a checkpoint

`show ip accounting checkpoint`

Det går även att kolla MAC-adresser.

`interface gi2`
` ip accounting mac-address input`
`show interface gi2 mac-accounting`

[Category:Cisco](/Category:Cisco "wikilink")