---
title: Cisco FC
permalink: /Cisco_FC/
---

Fibre channel är ett data transport protocol som ger in-order och
lossless transfer av blockdata. FC lämpar sig bra för block based
storage. Se även [Cisco FCoE](/Cisco_FCoE "wikilink").

**Termer**

-   pWWN/WWPN: 64-bitars portadress på HBA (typ MAC-adress fast finns ej
    i data plane)
-   nWWN/WWNN: 64-bitars HBA-adress
-   sWWN: Switch WWN
-   Sequence: en eller flera data frames som hör ihop (SEQ_ID) och
    skickas i en enkelriktad ström mellan två N ports
-   FCID: Logisk adress
-   Principal switch: har bl.a. hand om domain ID distribution och RSCN,
    finns en per SAN
-   FCNS: Fibre Channel Name Server (typ DNS), körs på den utvalda
    Principal switch
-   RSCN: Registered State Change Notification är en tjänst som N ports
    kan subscriba på för att få uppdateringar om vad som händer i
    fabricen
-   FSPF: Fabric Shortest Path First är det routingprotokoll som körs i
    fabricen (motsvarighet till OSPF för IP)

**Layers**
\* FC-0: physical layer

-   FC-1: enconding and error control
-   FC-2: signaling protocol med frame structure och byte sequences
-   FC-3: vilka services finns i fabricen, t.ex. time distribution och
    säkerhet
-   FC-4: Mappning mellan FC och det som körs ovanpå, t.ex. SCSI eller
    IP

Initiators och targets har Host Bus Adapters (HBA), dessa kallas Node
Ports. N ports kopplas till Fabric Ports (F ports) på FC-switcharna.
Switchportar som kopplas ihop med varandra kallas Expansion (E) Ports,
det är på dessa som FSPF körs. Default räknas FSPF cost: 1000 delat med
link speed i Gbps, t.ex. 10G = 100. FSPF har default stöd för ECMP. Har
man t.ex. Ciscoswitchar finns det stöd för VSAN (motsvarigheten till
[VLAN](/Cisco_VLAN "wikilink") + VRF) kan man trunka dem över dessa E
ports, då kallas det Trunking Expansion Ports (TE Ports).

Det första som händer när man kopplar in en server är att den skickar en
Fabric Login (FLOGI). Detta görs till FFFFFE (well-known fibre channel
address for a fabric F_Port). Switchen tar emot detta meddelande och
registrerar denna unika WWPN med FCNS. FCNS svarar tillbaka med en unik
24-bitars Fibre Channel Identifier (FC_ID eller N_Port_ID). FCID
består av Domain ID, Area ID, Port ID och är routbar inom FC-domänen.
Varje switch har ett eget domain ID som måste vara unikt i fabricen,
detta går att konfa manuellt och börjar då gälla när man startar om
processen (fcdomain restart). När en initiator har fått ett FCID så
skickar den Port Login (PLOGI). Detta görs till FFFFFC (well-known fibre
channel address for a directory server). Då registreras WWPN och det
assignade FCID till FCNS. FCNS svarar då tillbaka med FCID:n för de
targets som initiatorn har rätt att accessa enligt zoningpolicyn. När
PLOGI är klart kan initiatorn börja sin discovery process för att hitta
targets och deras capabilities och operating parameters. Detta görs
mellan upper layer protocols och kallas PRLI. Sedan kan man hitta
Logical Unit Numbers (LUNs).

FLOGI-databasen är alltså locally significant inom switchen. Där finns
endast WWPN och FCID:n för de directly connected initiators och targets.
FCNS-databasen är distribuerad över alla switchar i fabricen och där
finns alla nåbara WWPN och FC_ID:n.

Eftersom FC är lossless data transport så finns det inbyggd flow control
mekanismer. Detta är credit-based vilket betyder att mottagaren alltid
kontrollerar flödena och sändaren får endast skicka data om den vet att
mottagaren har tillräckligt med resurser för att ta emot det. Man
berättar för andra sidan hur mycket buffer som finns tillgängligt
(BB_Credit) och sändaren räknar sedan hur mycket som har skickats
(BB_Credit_CNT). Counten får ej överstiga BB_Credit. Varje gång en
buffer blir ledig så skickas ett R_RDY message över till sändaren som
då sänker BB_Credit_CNT. Detta görs hela tiden mellan alla portar i
fabricen.

**Zoning**
En zone är en samling N ports i fabricen som känner till varandra men
inget utanför zonen, ett slags VPN. Detta används för att få storage
access control. Varje medlem kan definieras av port på switch, WWN, FCID
eller ett operator configured alias. Zoning kan göras på två olika sätt,
soft och hard zoning. Soft betyder att members endast ser varandra i
name server queries medans hard görs med "ACL:er" i hårdvaran i hela
fabricen. Nuföritden finns endast hard zoning.

En eller flera zoner kan aktiveras som en grupp och kallas då zone set.
En fabric kan ha flera zone sets men endast en kan vara aktiv åt gången.
För att ha hand om detta finns det en Zone Server.

**VSAN**
Med virtuella SAN kan man köra flera SAN i samma hårdvara. VSAN är en
emulering av en FC fabric, dvs man partitionerar upp sitt SAN. Varje
VSAN kör sin egen Name Server, Zone Server, Login Server etc. VSAN
Manager är en NX-OS process som håller koll på VSAN attribut och
porttillhörighet. Alla portar på en Cisco-switch ligger default i VSAN
1. Man kan förlänga VSAN genom att trunka dem över E ports, som då
kallas TE_port. Alla frames taggas då med en VSAN header. Det går även
att aggregera länkar som trunkar VSAN. FSPF cost ändras inte när en
member i en port-channel går ner. Man kan låta PCP agera
kontrollprotokoll för länkaggregeringar likt LACP för ethernet. Man kan
modifiera MTU per VSAN, det kommer att förhandlas vid FLOGI.

### Konfiguration

Nexus 5000. Default pratar bara Nexus-switchar FC med Cisco FC-switchar,
detta går att ändra med interoperability mode.

Prereqs

`feature fcoe`

`slot 1 `
` port 44-48 type fc`

`copy run start`
`reload`

Verify

`show int br  `
`show int e1/44 trans`

VSAN och trunk

`feature fport-channel-trunk`

`vsan database`
` vsan 100`
` vsan 100 interface fc1/44 - 48`

`interface fc1/44 - 45`
` channel-group 10 `

`interface san-port-channel 10`
` channel mode active`
` switchport trunk mode on`
` switchport trunk allowed vsan 100`

Noter att båda sidor bör konfas klart innan man gör no shutdown på
port-channel.

`show san-port-channel database`

TE port

`interface fc1/1 - 2`
` switchport speed 8000`
` switchport mode E`
` switchport trunk allowed vsan 101`

TE Port-channel

`interface fc2/1 - 2`
` switchport speed 8000`
` switchport mode E`
` channel-group 11 force`
` no shutdown`

`interface san-port-channel 11`
` channel mode active`
` switchport mode E`
` switchport trunk allowed vsan 101`

**Verify**
show flogi database

`show fcns database`
`show fcdomain domain-list`
`show fcroute unicast`

Traffic Engineering

`interface fc1/24`
` fspf cost 50 vsan 100`

`show fspf vsan 100`

Persistent FC ID

`fcdomain fcid persistent vsan 100`
`fcdomain fcid database`
` vsan 100 wwn 11:22:11:22:33:44:33:44 fcid 0x66ee00`

`show fcdomain fcid persistent vsan 100`

#### Zoning

Zoning är en central del i FC, det är access control i fabricen. Ett
zoneset är en eller flera zones. Zone-rekommendation är single target,
single initiatior och att man använder pwwn eller alias. Det kan vara
bra att känna till att vissa system är case sensitive när det gäller
WWN:er. Hard zoning går ej att stänga av på Nexus.

`zoneset name PROD-A vsan 100`
` zone name Server1-to-SAN`
`  member pwwn 10:00:00:23:45:00:00:10`
`  member pwwn 10:00:00:23:45:00:00:20`

`zoneset activate name PROD-A vsan 100`

Show

`show zone status vsan 100`
`show zoneset active`

Permit all

`zone default-zone permit vsan 100`

**Enhanced Zoning**
Gör att varje gång man konfar det så låses konfen fabric wide av CFS. Om
t.ex. ett vsan isoleras på en länk kolla att zoning mode överenstämmer
(tänk VTP).

`zone mode enhanced vsan 100`
`zone confirm-commit`
`zoneset overwrite-control vsan 100`
`zone commit vsan 100`

Verify

`show zone status vsan 100`

Man kan även distribuera sitt zoneset över fabricen

`zoneset distribute full vsan 100`

**Smart Zoning**
För att förenkla sin konfig lite kan man använda taggar för att ange
vilka pwwn som är initiators kontra targets. Detta måste vara påslaget
på alla switchar i fabricen.

`zone smart-zone enable vsan 100`
`zone convert smart-zone vsan 100`

ACLTCAM usage MDS

`show system internal acl tcam-usage`
`show system internal acltcam-soc tcam-usage`

**Alias**
Man bör använda alias för att förenkla zonhantering och felsökning. Även
detta kan distribueras mha CFS, det kallas då enhanced device aliases
och valfri nod kan göra ändringar som propagerar genom nätet.

`device-alias mode enhanced `
`device-alias database`
` name Server1-HBA1 pwwn 00:11:11...`
` name SAN-Array1-port1 pwwn 00:22:22...`

`device-alias commit `
`show device-alias status`

**Zone Merge**
Om man ska koppla ihop två SAN kan man skydda sig mot felkonfad zoning
genom att ställa merge-control till restrict. Kopplar man ihop två SAN
med olika zonesets blir ISL:en isolated för de vsan som har mismatch.

`zone merge-control restrict vsan 100`

#### Port Security

FC Port Security är utökad säkerhet jämfört med zoning, man låter inte
ens obehöriga logga in i fabricen. Login requests från obehöriga FC
devices (Nx ports) och switchar (xE ports) nekas. Alla nekade
inloggningsförsök loggas genom system messages. Man kan använda pWWN,
nWWN eller sWWN för att vitlista vem som får vara med i fabricen.
Konfigurationen går att distribuera med hjälp av CFS, det är dock
avstängt default.

Man kan även låta switcharna lära sig port security konfigurationen
automatiskt över tid. Detta kan man använda när man aktiverar port
security första gången eftersom det sparar arbete genom att man inte
måste gå igenom alla portar manuellt, detta konfas per VSAN. När man
aktiverar port security så aktiveras auto-learn automatiskt.

`feature fc-port-security`
`fc-port-security activate vsan 1`

Lock vsan for new entries

`no fc-port-security auto-learn vsan 1`

Diff

`fc-port-security database diff active vsan 1`

Verify

`show fc-port-security status`
`show fc-port-security database active`
`show fc-port-security database config`
`show fc-port-security violations`

CFS

`fc-port-security distribute`

NPV
---

N-Port Virtualisation är en teknik för att öka skalbarhet och
simplicitet i FC-SAN. Man låter en enskild fysisk N_Port ha multipla
WWPN. NPV-enheten gör en FLOGI och sedan kan den registrera fler WWPN
och då få fler N_Port_ID. En NPV-enhet har F-portar downstream och
NP-port upstream. En NPV-switch kopplas till F-port i SAN. HBA:er märker
inte av NPV.

Det finns ingen funktionell skillnad mellan fysiska WWPN och virtuella,
man använder dem för zoning och LUN masking som vanligt. Däremot gör man
ingen zoning i NPV-enheten, den har ingen preferens i frågan utan
slussar bara vidare inlogg till ovanliggande switch. Notera att
ovanliggande switch måste ha NPIV enableat. Nested NPV är inte möjligt.
Notera att "feature npv" kräver en write erase och reload.

`feature fcoe-npv`
`feature npv`

Ovanliggande switch

`feature npiv`