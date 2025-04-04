---
title: Distributed Switch
permalink: /Distributed_Switch/
---

vSphere Distributed Switch (vDS) är en mer skalbar variant av virtuell
switch som är tillgänglig via Enterprise Plus-licensen.

Grundläggande om vDS
--------------------

Till skillnad från vSphere Standard Switchar är Distributed Switcharna
just distribuerade mellan de hostar i ett Datacenter som kopplats till
dem. Uplinks och Port Groups är därför också automatiskt distribuerade
till alla hostar. För att skapa en vDS, Högerklicka på
**Datacenter**-objektet -\> **Distributed Switch** -\> **New Distributed
Switch...**, konfigurera därefter grundinställningarna:

1.  Namn och lokation.
2.  Version, välj alltid senaste så länge dina hostar har stöd för det.
3.  Modifiera antalet Uplinks, slå på/av Network IO Control (NIOC) och
    skapa en default Port Group om så önskas.

Angående de olika vDS-versionerna, se nedan.

| Version   | Kompatibilitet | Nya features/förbättringar                                                                   |
|-----------|----------------|----------------------------------------------------------------------------------------------|
| vDS 6.5.0 | 6.5\<          | Port Mirroring Enhancements                                                                  |
| vDS 6.0.0 | 6.0\<          | NIOC v3 och IGMP/MLD Snooping                                                                |
| vDS 5.5.0 | 5.5\<          | Traffic Filtering & Marking och förbättrat LACP-stöd.                                        |
| vDS 5.1.0 | 5.1\<          | Management Network Rollback & Recovery, Health Check, Enhanced Port Mirroring och LACP-stöd. |
| vDS 5.0.0 | 5.0\<          | Användardefinierade resurspooler i NIOC, Netflow och Port Mirroring.                         |

För fortsatt konfiguration, klicka på din **vDS** -\> **Actions** -\>
**Settings**. Under **"Edit Settings"** kan allt som nämnts ovan ändras.
Under samma meny (Settings) finns även nedan inställningar.

-   Private VLAN
-   Netflow
-   Health Check
-   Export/Restore configuration

Under Advanced kan MTU, Multicast filtering (Basic eller IGMP/MLD
snooping), Discovery protocol (Type: CDP/LLDP/Disabled, Operation:
Listen/Advertise/Both) samt Administrator Contact ändras.

För att radera en vDS, ta först bort alla hostar och associerade
Uplinks, högerklicka sedan på din **vDS** och välj **Delete**.

### dvPort Groups

vNetwork Distributed Port Groups kallas portgrupperna som används av en
vDS. Lägg till en ny dvPort Group genom att högerklicka på din **vDS**
-\> **Distributed port group** -\> **New distributed port group**. Följ
wizarden och konfigurera de olika settings som finns:
**Port Binding** - Styr hur en virtuell port tilldelas till en VM. Det
finns tre olika möjligheter.
\* Static Binding: En port tilldelas då VM:en ansluts till dvPort
Group:en.
\* Dynamic Binding: Tilldelar en port första gången en VM startar efter
den kopplats till dvPort Group. Deprecated sedan 5.5.
\* Ephemeral - no binding: Ingen port binding alls, det går att tilldela
en VM till en dvPort Group med Ephemeral port binding även då man är
direktansluten till hosten.
**Port allocation** - Hur portar allokeras till en vDS.
\* Elastic - Default 8 portar, när alla portar tilldelats allokeras 8
nya portar till switchen. Denna allokering är default.
\* Static - Default 8 portar, inga nya portar allokeras när de
befintliga blivit tilldelade.
**Number of ports** - Antalet portar i dvPort Group:en.
**Network resource pool** - Används för att tilldela dvPort Group till
en network resource pool.
**VLAN** - Vilken sorts VLAN-teknik som skall användas:
\* None - Använd inte VLAN (otaggad trafik).
\* VLAN - Använd VLAN, 1-4094 (taggad trafik).
\* VLAN Trunking - Använd VLAN, range:ar tillåts, Virtual Guest Tagging
(taggad trafik).
\* Private VLAN - Använd ett Private VLAN som finns på switchen.

För att radera en dvPort Group, se först till att alla virtuella
nätverkskort och VMKernel-adaptrar migrerats till en annan portgrupp.
**vDS** -\> **Networks** -\> **Distributed Port Groups** -\> Välj
**dvPort Group** -\> i **Actions**-menyn, välj **Delete**.

### Uplinks

De fysiska NIC (pNIC) som kopplas till vDS:en mappas mot en Uplink, som
konfigureras identiskt på samtliga hostar. För att lägga till en Uplink,
gå till **vDS** -\> i **Actions**-menyn, välj **Add and Manage Hosts**
-\> **Manage host networking** -\> **Next**. Välj vilket/vilka pNIC som
ska mappas mot Uplink:en och tryck **Assign Uplink**. Därefter väljer
man manuellt vilken Uplink som ska användas, eller **Auto-assign**.
Efter du tryckt **Next** utvärderas om iSCSI kommer att påverkas eller
inte.

### VMkernel Adapters

VMkernel Adapters används för olika sorters tjänster/trafik i vSphere,
vilka följer nedan:

-   vMotion traffic
-   Provisioning traffic
-   Fault Tolerance (FT) traffic
-   Management traffic (HA Heartbeat, namnet är missvisande)
-   vSphere Replication Traffic (outgoing)
-   vSphere Replication NFC traffic (incoming)
-   vSAN traffic

En default VMkernel Port kan endast användas för IP Storage (iSCSI/NFS)
och management.

För att lägga till en VMkernel-adapter i en vDS, navigera till din
**vDS** -\> i **Actions**-menyn, välj **Add and Manage Hosts** -\>
**Manage host networking** -\> **Next**. Välj **Manage VMkernel
adapters**, och tryck **Next** -\> **New Adapter**. En wizard öppnas:

1.  Välj **dvPort Group** under **Select target device**.
2.  **Port properties**, här konfigureras **IP Settings**
    (IPv4/IPv6/Båda) samt vilka typer av trafik som tillåts på adaptern
    (vMotion etc). Det går även att byta TCP/IP-stack (Default, vMotion
    & Provisioning finns fördefinierade, dock kan fler läggas till via
    esxcli.
3.  På nästa sida konfigureras IP-adress & subnätmask.
4.  En review-sida visas innan du trycker **Finish**.

Konfiguration av vDS
--------------------

#### Koppla host till vDS

För att koppla på en host, gå till **vDS** -\> **Actions** -\> **Add and
Manage Hosts** -\> **Add Hosts** -\> **Next** -\> **New hosts** -\>
**OK**. Konfigurera sedan antalet fysiska NIC (pNIC) för Uplinks,
migrera VMKernel Adapters och VM Networking.

En host kan även användas som ett slags template för
nätverkskonfiguration av andra hostar på vDS:en. I **Add and Manage
Hosts**-menyn kan **Configure identical networking settings on multiple
hosts** väljas för att kopiera inställningarna från en host till övriga
hostar. Värden som måste vara unika, t ex IP-adresser fylls i som en
range, t ex 1.1.1.1\#3, så tilldelas de i tur och ordning till hostarna.

#### Ta bort host från vDS

Innan en host kan tas bort från en vDS måste alla fysiska adaptrar,
VMKernel-adaptrar och VM:ars nätverksadaptrar migreras till en annan
switch. Hosten tas sedan bort via **vDS** -\> **Actions** -\> **Add and
Manage Hosts** -\> **Remove Hosts** -\> **Next** -\> **Välj host(ar)**
-\> **Finish**.

#### Migrera VMs till/från vDS

Navigera till din **vDS** -\> i **Actions**-menyn, välj **Add and Manage
Hosts** -\> **Manage host networking** -\> **Next**. Välj **Migrate
virtual machine networking**, tryck **Next** -\> Välj **Source**
(specific/no network) och **Destination network**, dvs **dvPort Group**,
**Next** -\> Välj vilka VMs som ska migreras.

vDS Policies & Security
-----------------------

#### vDS Port Blocking

Under **Edit Settings** på en dvPort Group, i **Miscellaneous**-menyn
finns en inställning för **"Block all ports"**. Om den ställs in på
**Yes**, kommer samtliga virtuella portar i portgruppen att stängas ned.
Det går även att blockera enskilda portar och Uplinks under **Networks**
-\> Dubbelklicka på en **dvPort Group**/**Uplink** under **Distributed
Port Groups**/**Uplink Port Groups** -\> **Ports**-fliken.

1.  Välj en port i listan.
2.  Klicka på **Edit distributed port settings**.
3.  Under **Miscellaneous**, bocka för **Override**-rutan och välj om
    porten ska blockas eller inte.
4.  **OK**.

#### Load Balancing & Failover Policies

Förutom lastbalansering för LACP finns även fem olika val för Uplinks
och vanliga vSwitchar, de är:

-   Route based on IP hash
-   Route based on source MAC hash
-   Route based on originating virtual port
-   Use explicit failover order (ingen LB alls)
-   Route based on physical NIC load (endast tillgänglig för vDS)

Failover order använder sig av **Active**, **Standby** och
**Unused**-status. Om Active-NIC:arna är aktiva kommer de att användas,
i kombination med Load balancing-policyn. När inga portar från
Active-listan är aktiva längre, kommer portarna i Standby att användas.

De övriga inställningar som finns är: **Network Failure Detection** -
Hur ESXi känner av störningar i nätverket.
**Link status only** - Endast det fysiska NIC:ets länkstatus används för
att avgöra om nätet anses fungera.
**Beacon probing** - Beacons skickas ut via broadcast varje sekund och
registreras av övriga adaptrar. Denna info används tillsammans med
länkstatus för att avgöra om nätet fungerar optimalt. Använd inte detta
med färre än tre adaptrar i ditt failover team, annars kan inte ESXi
avgöra vilken enskild adapter som upplever problem.
**Failback** - Avgör huruvida en nätverksadapter som varit offline ska
sättas tillbaka som aktiv igen efter den kommit online.
**Notify switches** - Om detta är påslaget skickas RARP-meddelande ut
för att informera de fysiska switcharna om en failover för att de så
snabbt som möjligt ska uppdatera sina lookup tables. Detta används även
vid vMotion för att minska antalet tappade paket.

#### Private VLAN

Private VLAN fungerar "som vanligt", Primary/Promiscuous-VLAN:et
innehåller Secondary-VLAN:en som måste skicka sin trafik tillbaks till
Primary. Portarna i Secondary VLAN:en är antingen Isolated (kommunicerar
bara med Promiscuous-portar, dvs inte med "grann-VM:ar") eller Community
(kommunicerar med grann-VMs i samma secondary-VLAN och med
promiscuous-portar).

För att använda Private VLAN måste även den fysiska nätverksutrustingen
implementera detta korrekt.

#### Traffic Shaping

En traffic shaping policy appliceras per port i en portgrupp. Policyn
definieras med average bandwidth, peak bandwidth och burst size. På en
vDS sker shaping både inkommande och utgående, en standard vSwitch
shape:as endast ugående trafik. **Average Bandwidth** - Hur många kbit/s
som tillåts på en port, i genomsnitt över tid.
**Peak Bandwidth** - Maximalt antal kbit/s som tillåts vid en
trafik-burst.
**Burst Size** - Maximalt antal Kilobyte som tillåts i en burst. När en
port vill förbruka mer bandbredd än vad som angetts som Average kommer
den att använda denna s k Burst bonus, om den är tillgänglig.

vDS och LACP
------------

Med vDS kommer stöd för LACP och ett antal nya algoritmer för
lastbalansering. Högst 64 LAG-grupper kan konfigureras per vDS och en
host har stöd för 32 som mest. Som vanligt med LACP konfigureras Active
eller Passive Mode. De load balancing modes som finns är:

-   Source and destination IP address, TCP/UDP port and VLAN
-   Source and destination IP address and VLAN
-   Source and destination MAC address
-   Source and destination TCP/UDP port
-   Source port ID
-   VLAN

Endast en aktiv LAG kan användas per dvPort Group, till skillnad från
enskilda Uplinks, det går inte heller att blanda LAG:ar med vanliga
Uplinks. Att ha andra LAG:ar eller Uplinks som Standby är inte
supporterat, utan måste sättas som Unused i Failover Order. Under
migrering från Uplinks till LAG är det supporterat att en LAG sätts som
Standby före skiftet.

Skapa en LAG via **vDS** -\> **Configure** -\> **Settings** -\> **LACP**
-\> klicka på **Plustecknet**.

1.  Sätt ett namn på LACP-gruppen.
2.  Ange antal portar.
3.  Ange Active/Passive Mode för LACP.
4.  Sätt Load Balancing mode.
5.  VLAN och NetFlow policies kan överskridas här, om overrides
    tillåtits på vDS-nivå.
6.  Klicka OK för att skapa LAG:en.


För att flytta dvPort Groups till din LAG, gå till **vDS** -\> i
**Actions**-menyn, välj **Distributed Port Group** -\> **Manage
Distributed Port Groups** -\> Välj **Teaming and failover**, tryck
**Next**.

1.  Välj vilka dvPort Groups som ska använda LAG:en, Next.
2.  Under Failover Order, sätt LAG:en som Standby, Next.
3.  En review-sida visas, tryck Finish.


Efter detta ska fysiska NIC tilldelas LAG:en; gå till **vDS** -\> i
**Actions**-menyn, välj **Add and Manage Hosts** -\> **Manage host
networking** -\> **Next** -\> **Manage physical adapters** -\> **Next**
-\> Tilldela härifrån pNIC:ar till LAG:en från respektive host -\>
**OK**.

Nu återstår bara att gå tillbaks till **Failover Order** (se ovan) och
flytta LAG:en till **Active** och alla övriga Uplinks till **Unused**.
**Standby**-listan ska vara tom efter detta. Efter du tryckt på
**Finish** kommer trafiken flyttas till LAG:en, detta är non-disruptive.

#### Begränsningar med LACP

-   Inkompatibelt med iSCSI multipathing.
-   Finns inte settings för LACP i Host Profiles.
-   Ingen support för Nested ESXi.
-   Fungerar inte med ESXi dump collector.
-   Port mirroring fungerar inte.

vDS Auto-Rollback
-----------------

Som ett skydd mot att permanent tappa kontakt med vCenter pga
felkonfiguration utförs en rollback av konfigurationen på en vDS om
kontakten skulle försvinna efter en ändring. Denna funktion är påslagen
per default sedan version 5.1.

Det finns två typer av rollbacks, Host Networking Rollback och vDS
Rollback. En Host Networking Rollback sker då konfiguration ändrats på
en host som gör att kommunikationen med vCenter fallerar, exempel på
detta:

-   Ändring av speed/duplex på pNIC
-   DNS-/routing-ändringar.
-   Ändring av teaming & failover eller traffic shaping på en port group
    som innehåller management Vmkernel-adaptern.
-   Ändring av VLAN på portgruppen som innehåller management
    Vmkernel-adaptern.
-   Ändringar av MTU på managment Vmkernel-adaptern och dess switch till
    värden som inte stöds av den fysiska infrastrukturen.
-   Ändringar av IP-adressering på management Vmkernel-adaptern.
-   Borttagning av management Vmkernel-adaptern från en standard vSwitch
    eller vDS.
-   Borttagning av ett pNIC från en vDS/vSwitch som innehåller
    management Vmkernel-adaptern.
-   Migrering av management Vmkernel-adaptern från vSwitch till vDS.

En Distributed Switch Rollback sker när felaktiga ändringar görs på en
vDS, dvPort Group eller dvPort. Exempel på ändringar som kan trigga en
rollback:

-   Ändring av MTU på vDS-nivå.
-   Ändring av Teaming & Failover, VLAN eller Traffic Shaping på dvPort
    Group:en som innehåller management VMkernel-adaptern.
-   Blockering av alla portar i dvPort Group:en som innehåller
    management VMKernel-adaptern.

Det går också att återfå anslutningen för management via DCUI. Gå till
**Network Restore Options** -\> Välj **Restore vDS** -\> Konfigurera
uplinks och ev VLAN för management-nätet -\> **Apply**:a
konfigurationen. Vad som sker då är att DCUI skapar en lokal
ephemeral-port som konfigureras enligt de angivna värdena.
VMkernel-adaptern för management-nätet flyttas till den nya porten för
att återfå anslutning mot vCenter.

Under vissa omständigheter kan det vara önskvärt att inte ha rollback
påslaget, för att slå av rollback gör man följande: navigera till en
**vCenter**-instans -\> **Configure** -\> **Settings** -\> **Advanced
Settings** -\> **Edit** -\> Ändra värdet på
**config.vpxd.network.rollback**-nyckeln till **false** -\> **OK** -\>
Starta om vCenter för att applicera ändringen. Det går också att göra
detta via config-filen **vpxd.cfg** som ligger under
**C:\\ProgramData\\VMware\\CIS\\cfg\\** i Windows-varianten och under
**/etc/** i appliance-varianten. Under **<network>**-elementet, ändra
elementet **<rollback>** till false.
<code>

<config>
` `<vpxd>
`  `<network>
`    `<rollback>`false`</rollback>
`  `</network>
` `</vpxd>
</config>` `

</code>
Spara och stäng filen, och starta om vCenter.

[Category:VMware](/Category:VMware "wikilink")