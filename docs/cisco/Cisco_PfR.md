---
title: Cisco PfR
permalink: /Cisco_PfR/
---

Performance Routing (PfR) är "Application Path Optimization". Det är en
vidareutveckling av Optimized Edge Routing (OER) som gav prefix-based
route optimization. PfR och OER använder sig av packet loss, response
time, path availability och traffic load distribution för att fatta
beslut. Det PfR också tar hänsyn till är application type och
application performance requirements. PfR kan klassificera trafik
utifrån IP-adresser, protokoll, portnummer, DSCP och i nyare versioner
av IOS även [NBAR](/Cisco_QoS#NBAR "wikilink"). Man behöver en Master
Controller (som fattar besluten) och en eller flera Border Routers.
Authentication är inbyggt för all kommunikation till och från MC och man
måste använda sig av key-chains (t.o.m. om MC och BR finns på samma
router). Kommunikation mellan MC och BR görs med TCP och performance
metrics samlas med [NetFlow](/Cisco_NetFlow "wikilink") and [IP
SLA](/Cisco_Routing#IP_SLA "wikilink") probes som konfigureras
automatiskt. PfR route-maps sätts på Internal Interface och för att
dynamiska route-maps ska fungera krävs L3-konnektivitet mellan BRs
annars möts inte PfR's PBR requirement och dynamiska route-maps fungerar
ej. Om Master Controller går ner så märker Border Routers att deras
kommunikation till MC inte längre är aktiv. Det som händer då är att de
kollar vilka routes som är från PfR och tar bort dessa och allt återgår
till normal routing. Nätverket blir som det var innan PfR slogs på. PfR
är inte VRF-aware.

Terminologi
-----------

**Master Controller:** monitorerar utgående trafikflöden för att kunna
optimera routingen med hjälp av policy. En MC kan ha hand om 10 border
routers eller 20 external interfaces. Den behöver inte finnas i data
plane forwarding path.

**Border Router:** har ett eller flera external interfaces. Dessa
rapporterar in prefix- och transit link measurements till MC som sedan
fattar policy beslut. MC berättar sedan för BR vad den ska göra.

**Internal interfaces:** är interface mot resten av nätet och används
för att kommunicera med control plane manager för PfR. MC dikterar vad
som är internal interfaces.

**External interfaces:** används för att skicka paket till det lokala
nätverket. Det är dessa som performance mäts på. MC dikterar vad som är
external interfaces.

**Local interfaces:** finns på routern och är source för kommunikationen
med Master Controller.

Operational Phases
------------------

PfR delas in i olika faser som fyller olika syften.

-   **Profile Phase:** Lära sig vilka flows som har hög latency och
    throughput. MTC list innehåller alla Monitored Traffic Classes.

<!-- -->

-   **Measure Phase:** Samla in och räkna på performance metrics för all
    trafik på MTC list.

<!-- -->

-   **Apply Policy Phase:** Skapa low och high thresholds för att veta
    vad som är in-policy och vad som är out-of-policy.

<!-- -->

-   **Control Phase:** Påverka trafik genom att manipulera routes eller
    använda PBR.

<!-- -->

-   **Verify Phase:** Kontrollera ifall något är out-of-policy för att
    isåfall rätta till det.

Konfiguration
-------------

Key chain måste skapas på alla enheter.

`key chain PFR`
` key 1`
`  key-string SECRET`

`show key chain`

**MC**
Det krävs minst 2 external interfaces (totalt) för att MC ska bli aktiv.

`pfr master`
` border 2.2.2.2 key-chain PFR`
`  interface gi2 internal`
`  interface gi3 external`
` border 3.3.3.3 key-chain PFR`
`  interface gi2 internal`
`  interface gi3 external`

Defaults

`pfr master`
` learn`
`  throughput`
`  periodic-interval 0`
`  monitor-period 1`

` border 2.2.2.2 key-chain PFR`
`  interface GigabitEthernet3 external`
`   max-xmit-utilization percentage 90`
`   maximum utilization receive percentage 100`

Verify

`show pfr master border`
`show pfr master exits`

**Border**

`pfr border`
` master 1.1.1.1 key-chain PFR`
` local loopback 0`
` logging`

Verify

`show pfr border`
`show ip sla summary`

[Category:Cisco](/Category:Cisco "wikilink")