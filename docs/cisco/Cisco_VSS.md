---
title: Cisco VSS
permalink: /Cisco_VSS/
---

Virtual Switching System används för att göra två stycken fysiska
switchar till en logisk enhet. Fysiskt är det två switchar och man kan
dra allt kablage redundant. Med detta behöver man inte använda
[HSRP](/Cisco_HSRP "wikilink") eller [VRRP](/Cisco_FHRP "wikilink") samt
att L2-topologin går att hålla loopfri. En fördel är att det blir färre
manageringspunkter, en nackdel att ett fel kan få större blast radius.
VSS har stöd för [EtherChannel](/Cisco_EtherChannel "wikilink") så detta
är en variant av MLAG. När switcharna bootar upp använder de Link
Management Protocol (LMP) och Role Resolution Protocol (RRP) för att
förhandla om vem som ska vara active och således blir den andra standby.
Båda switcharna står för data plane men endast den aktiva står för
management och control plane. Mellan switcharna har man en Virtual
Switch Link som all sorts trafik går på, däremot har control plane och
management högre prio på denna länk. Denna bör dimensioneras kraftigt.

Installation
------------

Man behöver 2st cisco 4500-x, 4500-e eller 6500-e. I e-modellerna så
behövs Cisco Catalyst Supervisor Engine 7-E eller 7-LE men i
x-modellerna är den inbyggd.

Konfiguration
-------------

sätt Virtual Switch domain samt switch nummer

`SW1#conf t`
`Enter configuration commands, one per line. End with CNTL/Z.`
`SW1(config)#switch virtual domain 10`
`Domain ID 10 config will take effect only`
`after the exec command 'switch convert mode virtual' is issued`
`SW1(config-vs-domain)#switch 1`
`SW1(config-vs-domain)#exit`
`SW1(config)#`

`SW2#conf t`
`Enter configuration commands, one per line. End with CNTL/Z.`
`SW2(config)#switch virtual domain 10`
`Domain ID 10 config will take effect only`
`after the exec command 'switch convert mode virtual' is issued`
`SW2(config-vs-domain)#switch 2`
`SW2(config-vs-domain)#exit`
`SW2(config)#`

Konfigurera VSL Port Channel

`SW1(config)#int port-channel 5`
`SW1(config-if)#switchport`
`SW1(config-if)#switch virtual link 1`
`SW1(config-if)#no shut`
`SW1(config-if)#exit`
`*Jan 24 05:19:57.092: %SPANTREE-6-PORTDEL_ALL_VLANS: Port-channel5 deleted from all Vlans`

`SW2(config)#int port-channel 10`
`SW2(config-if)#switchport`
`SW2(config-if)#switch virtual link 2`
`SW2(config-if)#no shut`
`SW2(config-if)#exit`
`SW2(config)#`
`*Jan 24 05:14:17.273: %SPANTREE-6-PORTDEL_ALL_VLANS: Port-channel10 deleted from all Vlans`

Konfigurera VSL portarna

`SW1(config)#int range gig7/3 - 4`
`SW1(config-if-range)#switchport mode trunk`
`SW1(config-if-range)#channel-group 5 mode on`
`WARNING: Interface GigabitEthernet7/3 placed in restricted config mode. All extraneous configs removed!`
`WARNING: Interface GigabitEthernet7/4 placed in restricted config mode. All extraneous configs removed!`
`SW1(config-if-range)#exit`

`SW2(config)#int range gig4/45 - 46`
`SW2(config-if-range)#switchport mode trunk`
`SW2(config-if-range)#channel-group 10 mode on`
`WARNING: Interface GigabitEthernet4/45 placed in restricted config mode. All extraneous configs removed!`
`WARNING: Interface GigabitEthernet4/46 placed in restricted config mode. All extraneous configs removed!`
`SW2(config-if-range)#exit`

Switcha över till VSS från vanlig

`SW1#switch convert mode virtual `

`SW2#switch convert mode virtual `

Kolla så att det fungerar

`SW1#show switch virtual `

`Executing the command on VSS member switch role = VSS Active, id = 1 `

`Switch mode                  : Virtual Switch`
`Virtual switch domain number : 10`
`Local switch number          : 1`
`Local switch operational role: Virtual Switch Active`
`Peer switch number           : 2`
`Peer switch operational role : Virtual Switch Standby `

`Executing the command on VSS member switch role = VSS Standby, id = 2  `

`Switch mode                  : Virtual Switch`
`Virtual switch domain number : 10`
`Local switch number          : 2`
`Local switch operational role: Virtual Switch Standby`
`Peer switch number           : 1`
`Peer switch operational role : Virtual Switch Active`

### Dual-Active Detection

Förhindra att båda supervisors blir aktiva vid VSL link failure.

`switch virtual domain 10`
` dual-active detection fast-hello`

`interface te1/1/24`
` description VSS Fast-Hello`
` no switchport`
` no ip address`
` no cdp enable`
` dual-active fast-hello`
` no shut`

Verify

`show switch virtual dual-active fast-hello`

### Felsökning

`show switch virtual `
`show switch virtual role`
`show switch virtual link`

**Giants**
Om man ser giants counter gå upp på VSL interface så är det normalt
eftersom VSL inter-switch control frame packets skickas som 1518 bytes +
32 byte DBUS header mellan switcharna.

### Tips N Trix

Man kan använda sig av 10ge interface också och inte enbart 1ge som står
i guiden. Kommando för att byta vilken switch som är aktiv.

`redundancy force-switchover`

StackWise
=========

För de lite mindre switchmodellerna finns StackWise för att koppla ihop
flera enheter till en logisk. Switcharna kopplas ihop med speciella
StackWise-kablar på baksidan. Man väljer en switch som man konfigurerar
som master och sedan kopplar man ihop dem och bootar upp dem.

`switch 1 priority 15`

Kolla status på stacken

`show switch`
`show switch stack-bandwidth`
`show switch stack-mode`

Firmware

`software auto-upgrade enable`

Reset the switch mode to N+1

`switch clear stack-mode`

[Category:Cisco](/Category:Cisco "wikilink")