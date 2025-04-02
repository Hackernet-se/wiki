---
title: Cisco IOS
permalink: /Cisco_IOS/
---

IOS är den mjukvara som används av de flesta routrar och switchar av
märket Cisco. Se även [NX-OS](/Cisco_Nexus "wikilink") och [IOS
XR](/Cisco_IOS-XR "wikilink").

**IOS-XE**
IOS är ett monolithic operativsystem som är till åren därför har IOS-XE
utvecklats som är betydligt modernare uppbyggt. Det kör en linuxkärna i
botten och sedan ligger IOS som en daemon. Sedan kan ytterliggare
processer köras för sig. Denna moduläritet gör systemet mer feltolerant,
t.ex. ett fel i en process behöver inte påverka kärnan. IOS-XE har även
APIer för control plane processer. Se även [Cisco
CSR](/Cisco_CSR#Konfiguration "wikilink").

Konfiguration
=============

**Grundläggande**

`hostname [hostname]`
`enable secret [password]`
`service password-encryption`
`service nagle`
`no ip domain lookup`
`no ip http server`

Se även Cisco [Logging](/Cisco_Logging "wikilink"),
[Services](/Cisco_Services "wikilink") och
[Security](/Cisco_Security "wikilink").

Slå på loggmeddelanden i SSH terminal.

`terminal monitor`

**Resurser**

`show platform resources  `
`show platform hardware fed switch 1 fwd-asic resource tcam utilization`

**Line**

`line con 0`
` logging synchronous`
` exec-timeout [minutes] [seconds]`
` login`
`line vty 0 15`
` logging synchronous`
` exec-timeout [minutes] [seconds]`
` login #local`

`show line vty`

Reload

`reload in 3`
`reload cancel`

**NETCONF**

`netconf ssh`
`ssh -s cisco@10.0.0.10 netconf`

I nyare IOS-XE finns även restconf (XML eller JSON)

`restconf`

**Users**
Kolla vilka som är inloggade.

`show users  /  who`
`show tcp brief`

Auto enable

`line vty 0 15`
` privilege level 15`

CLI history, lägg till **all** för att se alla kommandon dvs det som
finns i crashinfo.

`show history   `

Disable Express Setup (mode button for 3 seconds)

`no setup express`

Conditional Debugging är bra på busy routers.

`debug condition int gi2`
`debug ip rip`

**COPP**

`cpp system-default`
`show policy-map control-plane`
`show policy-map system-cpp-policy`
`show platform hardware fed switch 1 qos queue stats internal cpu policer`

Inbyggda Funktioner
-------------------

**Meny**
Man kan skapa menyer med menu-kommandot och sedan binda users till
menyn.

`menu Menu01 line-mode`
`menu Menu01 prompt ^R1#^`
`menu Menu01 single-space`
`menu Menu01 title ^Actions for restricted user^`
`menu Menu01 text 1 Show routes`
`menu Menu01 command 1 show ip route`
`menu Menu01 text 2 Exit`
`menu Menu01 command 2 exit`

`username User01 autocommand menu Menu01`

**Macro**
Med macros kan konfigurera att ett kommando gör många saker.

`define interface-range SERVERPORTS gi 0/3-9`
`show parser macro`

**Schemaläggning**
Funkar endast med exec mode kommandon

`kron occurrence OCC in 1 recurring`
` policy-list TEST`
`kron policy-list TEST`
` cli show vers`

`show kron schedule`

**Views**

`enable view`
`parser view SHOWONLY`
`show parser view`

**Auto-install**
Auto-install är en feature som kan hämta konfiguration från en filserver
första gången en enhet startar. Det går att göra med
[DHCP](/Cisco_DHCP "wikilink") eller RARP, preference är: sname, option
66, option 150, siaddr. Det försöker på alla tillgängliga interface. OBS
för att auto-install ska triggas måste NVRAM vara helt tomt på
konfigurationsfiler, **erase nvram:**.

`show auto install status`

**Linux shell**
Man kan göra IOS lite mer likt ett Linux-skal och då får man tillgång
till några basic linuxkommandon. Detta är en IOS 15 feature.

`terminal shell`

Eller om man alltid vill ha det på.

`shell processing full`

Verify

`show terminal | grep Shell`

**XMCP**

`service-routing xmcp listen `
` client username username password password `
` domain domain-number {default | only}`
`show service-routing xmcp clients `
`show service-routing xmcp server `

Character Generator Protocol, port 19

`service tcp-small-servers`

EEM
---

Cisco IOS Embedded Event Manager är ett subsystem som möjliggör event
detection och onboard automation. Det är flexibelt och kan triggas vid
kommando, händelse eller klockslag, **show event manager version**.

Exempel:

`event manager applet CLI_logger`
` event cli pattern "show.*" sync no skip no`
` action 01 syslog msg "$_cli_host executed: $_cli_msg"`

`event manager applet NO_SH_RUN`
` event cli pattern "show run" sync yes`
` action 01 puts "CAN´T DO THAT"`

`event manager applet Never_Back_Down`
` event timer watchdog time 5`
` action 01 cli command "enable"`
` action 02 cli command "conf t"`
` action 03 cli command "interface gi2"`
` action 04 cli command "no shut"`

`debug event manager action cli `

Verify

`show event manager policy registered`

Trigga manuellt

`event manager run APPLET`

EEM kan använda sig utav environment variable, t.ex. för att konfigurera
en mailserver som flera applets kan dra nytta av.

`event manager environment _mail_server 172.22.0.10`

Kolla alla inbyggda variabler, det finns en hel del.

`show event manager detector all detailed | i \$_`

Konfigurationshantering
-----------------------

**Archive and rollback**

`archive`
` path `[`tftp://1.2.3.4/test`](tftp://1.2.3.4/test)
` write-memory `
` time-period 1440`
`show archive`

Kolla skillnad mellan running och startup config.

`show archive config differences`

`alias exec `**`diff`**` show archive config differences`
`alias configure `**`diff`**` do show archive config differences`

**Automatic Rollback**
Prereq.

`archive`
` path bootflash:/`
` maximum 1`

Ta en snapshot av konfigen när man går in i global configuration mode.
Tappar man konnektivitet så rullas konfigen tillbaka efter 1 minut.

`configure terminal revert timer idle 1`

`configure confirm`

**Parser**
Parser cache är påslaget default för att göra konfig-hantering snabbare.

`parser cache`
`show parser statistics`

Man kan reducera tiden det tar för ett kommando att exekvera.

`parser config cache interface`

Man kan begränsa så att endast en user i taget kan managera en enhet.

`parser command serializer`

**Resilient Configuration**

`secure boot-image`
`secure boot-config`
`show secure bootset`

Restore

`secure boot-config restore flash:archived-config`
`configure replace flash:archived-config`

Ethernet
========

`show controllers ethernet-controller`
`show interfaces counters errors`

Default är Ethernet autonegotiation påslaget på switchportar. För att
slå av det måste både speed och duplex ställas manuellt.

`int gi0/1`
` speed 1000`
` duplex full`

CDP kan upptäcka duplex mismatch men ej fixa det. Ifall fel kabel
(korsad eller rak) används finns Auto-MDIX för att upptäcka detta och
ändra rx och tx på switchporten.

Testa kabel, Time Domain Reflection

`test cable-diagnostics tdr interface gi 0/1`
`show cable-diagnostics tdr interface gi 0/1`

CDP
---

CDP är ett l2-protokoll för att upptäcka och utbyta information med
directly connected Cisco-enheter, destination address är
01:00:0c:cc:cc:cc och det skickas var 60:e sekund. CDP går att använda
för reliable policy routing och är ett prereq för Layer 2 traceroute.
Aktuell version är CDPv2.

`cdp run`
`cdp timer 60`
`cdp holdtime 180`

Slå på per interface

`interface gi2`
` cdp enable`

Verify

`show cdp`
`show cdp neighbor`

Det finns även stöd för den öppna standarden LLDP som använder
01:80:c2:00:00:0e. LLDP advertisements skickas var 30:e sekund och TTL
är 120 sekunder.

`lldp run`
`show lldp`

CDP/LLDP kan användas för att sätta interface descriptions automatiskt
utifrån neighbor hostname och port-id.

`event manager applet AUTOMATIC-PORT-DESCRIPTION`
` event neighbor-discovery interface regexp GigabitEthernet.* cdp add`
` action 10 cli command "enable"`
` action 11 cli command "config t"`
` action 12 cli command "interface $_nd_local_intf_name"`
` action 13 cli command "description $_nd_cdp_entry_name:$_nd_port_id"`
` action 14 syslog msg "Updated description $_nd_cdp_entry_name:$_nd_port_id on $_nd_local_intf_name"`

DNAC
====

Cisco DNA Center är en kontroller- och analysplattform för Catalystnät.

**Reset switch**
För att nollställa en switch som har varit managerad av DNAC måste man
ta bort de certifikat som DNAC har installerat.

`conf t`
` crypto key zeroize`
` yes`
` no crypto pki certificate pool`
` yes`
` end`
`delete /force vlan.dat`
`delete /force nvram:*.cer`
`delete /force nvram:pnp*`
`delete /force flash:pnp*`
`write erase`
`reload`

[Category:Cisco](/Category:Cisco "wikilink")