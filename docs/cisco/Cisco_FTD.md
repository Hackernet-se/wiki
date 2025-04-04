---
title: Cisco FTD
permalink: /Cisco_FTD/
---

Firepower Threat Defense (FTD) är Ciscos Next-Generation
Firewall-erbjudande. Denna serie kommer att vara i fokus framåt och på
sikt ersätta ASA-brandväggarna. Firepower-hårdvaran kan köras antingen
med ren ASA-kod eller med NGFW-koden; FTD. Alla ASA-brandväggar ur
5500-X-serien kan reimage:as till FTD också, förutom 5585-X.

Till skillnad från ASA är FTD inte CLI-drivet utan manageras via
antingen ett lokalt webbgränssnitt, FDM (2100-serien och mindre) eller
Firepower Management Center (FMC), en centraliserad management-server
för en eller flera brandväggar (motsvarande PAN Panorama och CheckPoint
Tracker). De CLI-kommandon som finns används för grundläggande
installation och debugging.

Grundkonfiguration av FTD
-------------------------

Logga in i konsolen med admin/Admin123 och fyll i IP, hostname m.m. i
setup-wizarden. För att sedan kunna managera enheten via FMC kör
följande kommando:

`configure manager add <hostname | IPv4_address | IPv6_address | DONTRESOLVE>  reg_key `<nat_id>

Exempel

`configure manager add 10.11.12.13 my_reg_key`

`Hostname/IP` används för att peka ut FMC.

`reg_key` är en sträng som används likt en shared secret för att ansluta
FTD och FMC (denna anges senare i FMC).

`nat_id` används bara om NAT används mellan FTD och FMC, ange då ett
unikt ID tillsammans med `DONTRESOLVE` istället för hostname.

Exempel med NAT

`configure manager add DONTRESOLVE my_reg_key my_nat_id`

Firepower Management Center
---------------------------

FMC används för att centralt managera FTD-brandväggar, FMC finns både
som virtuell och fysisk appliance. För de större FTD-brandväggarna krävs
FMC för management.

### Licensing & Evaluation Period

FMC kan testköras i 90 dagar, detta aktiveras under samma meny som
används för Smart Licenses. För att aktivera din Smart License eller
Evaluation Period, gör såhär:

`   1. Klicka eller hovra på System-fliken i övre höger hörn.`

`   2. Under Licenses-fliken, välj Smart Licenses.`

`   3. Aktivera din Evaluation Period eller registrera dina Smart Licenses.`

### Managera FTD

Logga in i FMC via din webbläsare och gör följande för att lägga till
din FTD-enhet för managering:

`   1. Klicka på Devices-fliken längst upp på sidan.`

`   2. Klicka på Add...-knappen längst till höger, välj Add Device.`

`   3. Fyll i IP/Hostname i Host-fältet.`

`   4. Fyll i samma registration key som konfigurerats på FTD-enheten.`

`   5. Tilldela/skapa en Access Control Policy till enheten.`

`   6. Bocka för önskade licenser under Smart Licensing.`

`   7. Om nat_id använts i FTD, fyll i detta efter Unique NAT ID under Advanced.`

`   8. Tryck Register.`

### Omstart av FMC

Under System -\> Configuration -\> Process finns möjlighet att starta om
FMC-konsolen eller FMC-servern samt stänga av FMC-servern.

### Packet Tracer

Finns under Devices -\> Device Management, klicka sedan på
"verktygsikonen" för att komma Health Monitor-vyn. Starta härifrån
Advanced Troubleshooting, så finner du Packet Tracer som en separat
flik. Det går även att nå Packet Tracer via System -\> Health -\>
Monitor, för att sedan klicka sig fram till enheten.

[Category:Cisco](/Category:Cisco "wikilink")