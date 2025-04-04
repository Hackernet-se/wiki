---
title: Cisco CEF
permalink: /Cisco_CEF/
---

Cisco Express Forwarding är switchingteknik som är framtagen för att öka
prestandan på Ciscos routrar och L3-switchar. I tidernas begynnelse
fanns endast process switching, då behövde varenda paket kollas upp i
routingtabellen vart det skulle. L2-information för next-hop (som finns
i en annan tabell) behövde också tas fram. Ibland krävs rekursiva
iterationer av lookupen för att identifiera rätt next-hop och egress
interface. Detta kan vara väldigt intensivt för CPU så en variant med
cachefunktion utvecklades. Med fast switching behandlas det första paket
på samma sätt som med process switching men resultatet av lookupen
sparas i en route cache, designad för att vara snabb. Den innehåller
destination IP, next-hop information och L2 information till framen som
ska skickas. Route once, forward many times. Den stora nackdelen är att
om det kommer in många nya paket blir det ändå tungt för CPU och entries
i cachen timear ut ganska fort för annars skulle cachen kunna gå full
och allt skulle bli process switched igen. CEF löser detta genom att
proaktivt lägga entries i en cache som programmeras på ASIC.
Routing-information från Routing Information Base (RIB), Route Processor
(RP) och line card (LC) databases används för express forwarding. CEF
har även möjlighet att göra rekursiva uppslag i RIB, dvs när primary
path går ner kan next longest matching path användas, detta är
användbart om next-hop finns multipla hopp bort och det går att nå via
flera vägar. I nyare IOS:er finns det inte stöd för unicast fast
switching. When IPv6 routing is enabled, CEFv6 is automatically enabled.

`show cef state`

### FIB

CEF har två nyckelkomponenter, FIB och Adjacency. L2 address resolution
tas direkt från CEF med **ip cef optimize neighbor resolution**, det är
på default.

`show ip cef`
`show ipv6 cef`
`clear cef table ipv4`

Adjacency

`show adjacency`

Kolla en specifik route

`show ip cef exact-route `*`source`*` `*`destination`*
`show ip cef exact-route 10.0.0.5 172.16.1.2`

Consistency

`test cef table consistency`
`show cef table consistency-check `

### Load Sharing

Per-destination load balancing används default. Ett problem med att alla
använder samma metod för att välja väg uppstår när hash algoritmen på
flera noder väljer en viss väg och redundanta vägar därmed inte används,
detta kallas CEF polarization. För att undvika detta använder numera CEF
default en algoritm som väljer ett slumpat Universal ID som sedan
används som seed för hashen.

`ip cef load-sharing algorithm`
` include-ports  Algorithm that includes layer 4 ports`
` original       Original algorithm`
` tunnel         Algorithm for use in tunnel only environments`
` universal      Algorithm for use in most environments`

### Interface

CEF

`ip cef`
`show ip interface | i protocol|CEF`

Fast-switched

`int gi1`
` no ip route-cache cef`

Process-switched

`int gi1`
` no ip route-cache`

Debug

`debug ip packet detail`

För detta krävs att CEF stängs av, *no ip route-cache*

### dCEF

Med Distributed CEF så har alla line cards egna kopior av FIB och
adjacency table, på så sätt kan de göra express forwarding själva och
behöver inte fråga main processor.

`show cef linecard`

[Category:Cisco](/Category:Cisco "wikilink")