---
title: Cisco Nexus
permalink: /Cisco_Nexus/
---

Cisco Nexus switchar är designade för datacenter. De kör NX-OS som
bygger på en nedbantad variant av Linux kernel. De har stöd för tekniker
som [FabricPath](/Nexus_FabricPath "wikilink") och
[vPC](/Nexus_vPC "wikilink") och går att konfigurera med CLI
(SSH/console) eller XML baserat på NETCONF. För virtuell instans se
[Nexus VDC](/Nexus_VDC "wikilink") och för virtuell switch se [Nexus
1000V](/Nexus_1000V "wikilink") och Nexus 9000v (nedan).

### Nexus 9000 Taxonomy

[790px](/File:CiscoNexusTaxonomy.jpg "wikilink")

Konfiguration
-------------

`hostname Nexus-01`
`service password-encryption`
`no ip domain-lookup`
`user admin password bigdog role vdc-admin`

Management

`interface mgmt0`
` ip address 10.0.0.10/24`

`vrf context management`
` ip route 0.0.0.0/0 10.0.0.1 `

Slå på loggmeddelanden och färgkodning i SSH terminal.

`terminal monitor`
`terminal color persist`

Slå på features görs efter behov.

`feature ssh`
`feature fex`
`feature lacp`
`feature vpc`

Global

`system default switchport shutdown`
`port-channel load-balance ethernet source-dest-port`
`clock timezone CET 1 0 `
`clock summer-time CEST 5 Sunday March 02:00 5 Sunday October 02:00 60`

Show

`show module`
`show system resources`
`show cli history unformatted`
`show cli history config-mode `

Alias, exempel

`cli alias name wr copy running-config startup-config`
`cli alias name diff show running diff`
`cli alias name changeto switchto vdc`

**Jumbo frames Nexus 5K**
Detta gäller för L2 interface. Vill man vara någorlunda granulär kan man
köra jumbo frames per vlan. Show interface visar inte rätt eftersom
Nexus 5k inte har stöd för per interface MTU utan man får använda show
queuing. Se även [QoS](/Cisco_QoS#NX-OS "wikilink") för NX-OS för mer
info.

`policy-map type network-qos JUMBO-MTU`
` class type network-qos class-default`
`  mtu 9216`
`system qos`
` service-policy type network-qos JUMBO-MTU`

`show queuing interface e1/1`

Nexus 7K, denna globala inställning säger vad man max får konfa under
interfacen.

`system jumbomtu 9216`

**API**
NX-OS har stöd för flera olika API:er.

`feature netconf`
`feature restconf`
`feature grpc`

**Troubleshooting**
NX-OS har en on-device log file med de exec level configuration commands
som körts.

`show accounting log`

Visa historical event log för Layer 2 MAC-databasen.

`show system internal l2fm l2dbg macdb address 0011.2233.4455 vlan 100`

Routing and forwarding
show forwarding ip route <IP>

`show forwarding adjacency `<IP>
`show hardware mac address-table 1`

Verify ECMP

`show routing hash `<src-ip>` `<dst-ip>

Nexus 9K, för att smidigt se om t.ex. en counter räknar upp eller ej.

`watch differences interval 1 show interface e1/1`
`watch show interface counters table`

Alternativt

`show int eth1/10 | diff`
`show int eth1/10 | diff`

VLAN
Man kan kolla vilka VLAN som är reserverade och används internt.

`show vlan internal usage`

Sätt switchen i maintenance mode.

`system mode maintenance [dont-generate-profile] `
`show system mode`
`show config-profile`

Software Reload
Endast mjukvaran startar om. Data plane påverkas inte men control plane
är nere några minuter. OBS om detta failar av någon anledning så bootar
switchen om som vanligt.

`soft-reload`

Licens

`license grace-period`

`show license brief`
`show license usage`
`show license host-id`

**Shell**
Bash Access, här blir man root.

`feature bash-shell`
`run bash`

Secure Guest Shell är en kombination av bash och en secure Linux
environment med ett modifierbart root system. Detta körs i en Linux
Container. Man kan ändra resurstilldelning för en guestshell-contatiner
med *guestshell resize*.

`guestshell`
`show virtual-service list`

**Python**

`switch# python`
`from cli import *`
`import yaml`
`cli('configure terminal ; interface loopback 5 ; no shut')`
`intflist = yaml.safe_load(clid('show interface brief'))`

**Scheduler**
NX-OS har en inbyggd schemaläggare som kan användas för att köra
kommandon vid valda tidpunkter.

`feature scheduler`

`scheduler job name CLEAR-STATISTICS`
` clear counters interface all`
` exit`

`scheduler schedule name EVERYDAY`
` job name CLEAR-STATISTICS`
` time daily 23:30`
` exit`

`show scheduler schedule`

CoPP

`control-plane `
` service-policy input copp-system-policy-scaled-l2`

FIPS

`fips mode enable`
`show fips status`

**Git repo backup**

`event manager applet gitpush `
` event cli match "copy running-config startup-config" `
` action 1 cli copy running bootflash:running.latest `
` action 2 cli run guestshell python /home/admin/upload_git.py`
` action 3 event-default `

**Adjacency Manager**
Nexus adjacency manager finns på den aktiva supervisorn och håller
adjacency information för olika protokoll inklusive ARP, NDP och static
mappings. Adjacency Manager populerar t.ex. IPv4 RIB:en med routes lärda
från ARP. Dessa är host-routes och har Administrative Distance 250,
detta går dock att ställa om.

`ip adjacency route distance 250`
`ipv6 adjacency route distance 250`

**iCAM**
Nexus 9000 har stöd för Intelligent CAM Analytics and Machine-learning
feature. Man kan se traffic analytics per feature samt TCAM resources
och entries.

`feature icam`
`show icam scale`

**CLI variables**
cli var name MYINF interface e1/10

`show cli variables `
`tac-pac bootflash:$(SWITCHNAME)-$(TIMESTAMP)-show-tech-all.gz`

### PTP

PTP är ett time synchronization protocol för noder i ett nätverk.
Hardware timestamps används för att ge bättre noggrannhet än andra
protokoll som t.ex. [NTP](/Cisco_Services#NTP "wikilink"). PTP är ett
distribuerat protokoll och ett PTP-system kan bestå av en kombination av
PTP och icke-PTP devices. Ordinary clocks organiseras i en master-slave
synchronization hierarki med en grandmaster clock på toppen som
bestämmer referenstiden för hela systemet. PTP-processen består av två
faser: etablera master-slave hierarkin och synka klockorna. PTP
transporteras med UDP över multicast. För att hantera sin egen interna
queuing eller snarare delays in queues kan en switch agera enligt
transparent clock model eller boundary clock model. PTP är inte
supporterat på FEX interface.

<div class="mw-collapsible mw-collapsed" style="width:300px">

Sync message:

<div class="mw-collapsible-content">

[<File:Cisco-PTP-Sync.PNG>](/File:Cisco-PTP-Sync.PNG "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:300px">

Announce message:

<div class="mw-collapsible-content">

[<File:Cisco-PTP-Announce.PNG>](/File:Cisco-PTP-Announce.PNG "wikilink")

</div>
</div>

`feature ptp`
`ptp source `<ip-address>
`ptp domain 0    #Default`

`interface ethernet1/1`
` switchport`
` ptp`

Verify

`show ptp brief`
`show ptp clock`
`show ptp port interface ethernet 1/2`

Fabric Extender
---------------

FEXar är remote linjekort man sprider ut i sitt DC för att få fördelar
från både ToR-kabeldragning och EoR-management. Man kopplar in FEXar
till Nexus-switchar eller UCS FI:s och sedan strömsätter man dem och
associering görs automatiskt. För att upptäcka varandra använder FEX och
parent switch Satellite Discovery Protocol (SDP). Får en FEX svar så
startar den Satellite Registration Protocol (SRP). Därefter är FEXen
registrerad med parent. Med hjälp av control VLAN 4042 och interna
IP-adress 127.15.1.100 används Virtual Interface Configuration protocol
för att konfa FEXens portar. SDP skickas periodvis och fungerar även som
en keepalive mekanism. Om alla upplänkar går ner kommer FEXen att stänga
alla sina interface, detta gör att dual homed servrar kan faila över
till den andra FEXen.

Upplänkar på FEX kallas Fabric Interface. Server facing interfaces
kallas Host Interface. Varje HIF har ett Virtual Interface inuti FEXen,
detta får sin konfig ifrån parent switch. Varje VIF binds till ett
Logical Interface i parent switch, detta har VLAN membership, ACL:er,
etc. Mappningen mellan VIF och LIF görs med hjälp av en speciell tag i
Ethernet framesen som går mellan FEX och parent. Denna logiska länk
kallas VN-Link och taggen heter VNTag. Cisco VNTag har en egen ethertype
och innehåller bl.a. Direction bit, Pointer bit, Looped bit, Version och
Source och Destination Virtual Interface. Paket som kommer in på ett
Host Interface skickas alltid till parent även om t.ex. destination är
en annan port på samma FEX.

FEXar har INTE stöd för:

-   [STP](/Cisco_STP "wikilink"), (BPDUGuard enabled by default)
-   [VTP](/Cisco_VTP "wikilink")
-   QinQ
-   CDP, (Upplänkar undantag)

**Supported Topologies**
Man kan koppla in FEXar single homed eller dual homed beroende på om det
som ska ansluta till FEXarna ska vara single eller dual homed.

[600px](/File:Cisco_Nexus_FEX.PNG "wikilink")

**Konfiguration**
Notera att dual-homed FEXes måste ha identisk konfiguration, dvs
Nexus-switcharna ska ha matchande FEX-relaterad konfig. Detta kan
antingen göras manuellt eller med en configuration synchronization
service som finns inbyggd i NX-OS. Config sync kan dock ställa till med
konstiga fel så fördelaktigt görs detta med något externt
automationsverktyg. När man konfar en port-channel till FEXen (vilket
man bör) måste **pinning max-links 1** vara satt samt att *mode on*
måste köras eftersom FEX ej har stöd för LACP. MTU på FEXar styrs av
network QoS policy så för att ändra MTU på FEX-portar måste även MTU på
fabric portar ändras. Notera att FEXar kräver minst 1058 bytes annars
misslyckas registreringen med parent switch. Man kan konfa FEX innan den
är online med hjälp av pre-provision, se nedan. Man måste göra modelval
för att parent ska veta hur många och vilka sorts interface som finns på
FEXen. Giltiga FEX-nummer är 101-199.

Do not power on the FEX until all cabling and uplink port provisioning
on the uplinked Nexus has been completed.

Single homed FEX

`fex 101`
` pinning max-links 1`
` description "FEX101"`

`interface port-channel101`
` description FEX101`
` switchport mode fex-fabric`
` fex associate 101`

`interface Ethernet1/1`
` description FEX101, Uplink 1`
` switchport mode fex-fabric`
` fex associate 101`
` channel-group 101`
` no shutdown`

`interface Ethernet1/2`
` description FEX101, Uplink 2`
` switchport mode fex-fabric`
` fex associate 101`
` channel-group 101`
` no shutdown`

Dual homed FEX

`fex 111`
` pinning max-links 1`
` description "FEX111"`

`slot 111`
` provision model N2K-C2248TP-E-1GE`

`interface port-channel111`
` description FEX111 `
` switchport mode fex-fabric`
` fex associate 111`
` vpc 111`

`interface Ethernet1/1`
` description FEX111, Uplink 1`
` switchport mode fex-fabric`
` fex associate 111`
` channel-group 111`
` no shutdown`

`interface Ethernet1/2`
` description FEX111, Uplink 3`
` switchport mode fex-fabric`
` fex associate 111`
` channel-group 111`
` no shutdown`

Verify

`show fex detail`
`show module fex`
`show interface fex-fabric`

Om serienummer är satt i konfigen måste det stämma annars blir det
"Identity-Mismatch". Står det inget i konfigen accepteras vad som blir
connected.

Port Profiles
-------------

En port profile används för att skapa en mall med fördefinierad
konfiguration för portar. Istället för att manuellt kopiera befintlig
portkonfiguration till en ny port kan istället profilen appliceras på
porten för en färdig och enhetlig konfiguration.

Skapa port-profile

`port-profile ACCESS`
` switchport`
` switchport mode access`
` switchport access vlan 10`
` spanning-tree port type edge`
` spanning-tree bpdufilter enable`
` spanning-tree bpduguard enable`
` no shutdown`
` state enabled`

Applicera port-profile, kan t.ex. appliceras under port-channel eller
ethernet-interface.

`interface ethernet 1/1`
` inherit port-profile ACCESS`

Verifiering

`show run interface ethernet 1/1 expand-port-profile`
`show port-profile`

Checkpoint
----------

Nexusswitchar har en inbyggd funktion för Configuration Roll Back.
Checkpoint-featuren låter admins spara konfigurationssnapshots. Sedan
kan man rollbacka när man behöver. Exempelvis när man tar bort en
feature (*no feature xxx*) så skapar Feature Manager automatiskt en
checkpoint.

Skapa checkpoint

`checkpoint`

Show checkpoints

`show checkpoint summary`

Diff

`show diff rollback-patch checkpoint user-checkpoint-1 running-config`

Rollback

`rollback running-config checkpoint user-checkpoint-1`

Delete

`clear checkpoint database`

Portmode
--------

På vissa nexus-modeller kan man ställa olika portmodes, t.ex. 93180LC
och YC. I LC modellen så kan man sätta 18x100g isället för
4x100g+28x40g, man kan också köra 6x100g+24x40g.

För att ställa in 18x100g

`hardware profile portmode 18x100g `

För 6x100g+24x40g

`hardware profile portmode 6x100g+24x40g`

För 4x100g+28x40g

`hardware profile portmode 4x100g+28x40g`

Man måste sedan spara configen och starta om switchen för att detta
skall börja gälla.

Nexus 9000v
-----------

Nexus 9000v Switch är en virtuell maskin som man kan använda för att
testa NX-OS features. Nexus 9000v funkar t.ex. i
[EVE-NG](/EVE-NG "wikilink"). Dock funkar inte alla features, t.ex. QoS,
BFD, Storm-control, FCoE och MACsec.

Man måste lägga in i startup-config vilken image switchen ska boota
ifrån. Här följer lite grundkonfig.

`hostname N9K01`
`boot nxos bootflash:/nxos.7.0.3.I7.3.bin`
`feature lldp`
`terminal width 110`
`spanning-tree mode mst`
`line console`
`  exec-timeout 0`

`policy-map type control-plane COPP`
`control-plane`
`  service-policy input COPP`

Detta kommando används istället för show mac address-table på Nexus
9000v.

`show system internal l2fwder mac`

Ansible
-------

`ansible-galaxy collection install cisco.nxos`

nxos.yml

`---`
`ansible_connection: ansible.netcommon.httpapi`
`ansible_httpapi_use_ssl: true`
`ansible_httpapi_validate_certs: false`
`ansible_network_os: cisco.nxos.nxos`
`ansible_user: admin`
`ansible_password: password`

hosts.yml

`---`
`all: `
`  hosts:`
`    switch1: `
`      ansible_host: 10.0.0.40`
`    switch2:`
`      ansible_host: 10.0.0.41`

ansible.cfg

`[defaults]`
`collections_paths   = ./collections`
`inventory           = ./inventory`
`forks           = 15`
`stdout_callback = yaml`

[Category:Cisco](/Category:Cisco "wikilink")