---
title: Cisco Logging
permalink: /Cisco_Logging/
---

Ciscoenheter kan logga meddelanden lokalt och/eller remote. Se även
[Cisco IOS](/Cisco_IOS "wikilink").

### Format

Man kan använda lite olika format på sina loggmeddelanden, detta går
även ändra på debugmeddelanden. Vill man att tidsstämplarna ska utgå
ifrån den tidszon enheten är konfad med kan man lägga till **localtime**
efter datetime-kommandona.

`(Utan tidsstämpel)`
`%LINK-3-UPDOWN: Interface Port-channel1, changed state to up`

**`service`` ``timestamps`` ``log`` ``uptime`**
`00:00:46: %LINK-3-UPDOWN: Interface Port-channel1, changed state to up`

**`service`` ``timestamps`` ``log`` ``datetime`**
`*Feb  8 18:24:02: %LINK-3-UPDOWN: Interface Port-channel1, changed state to up`

**`service`` ``timestamps`` ``log`` ``datetime`` ``msec`**
`*Feb  8 18:24:02:355 %LINK-3-UPDOWN: Interface Port-channel1, changed state to up`

[NX-OS](/Cisco_Nexus "wikilink") har lite annan struktur på syslog

`2016 Feb  8 18:41:55.911853  DC01-SW02  %BGP-3-UNEXPECT:  the-message...`

### Diverse

Default har de flesta IOS-enheter en rätt liten logg-buffer men det går
att ställa upp.

`logging buffered 131072`

Count every log message and timestamp last occurance

`logging count`
`show logging count`

Persistent, no buffering

`logging persistent immediate`

Rate limit

`logging rate-limit console all 1`

Numrera loggrader, gör det svårare att manipulera lagrade loggar i
efterhand.

`service sequence-numbers`

**Message Discriminator**
Innan ett loggmeddelande levereras kan man ha det checkat mot en
manuellt definierad kriterielista. På så sätt kan man t.ex. specificera
om några speciella loggmeddelanden ska droppas.

`logging discriminator BLOCK msg-body drops Interface Port-channel1`

`logging monitor discriminator BLOCK`
`logging host 1.1.1.1 discriminator BLOCK`

Local Storage
=============

Man kan lagra loggar lokalt på flash.

`mkdir flash:/logs`
`logging persistent url flash:/logs`
`logging on`

Verify

`show logging`

Syslog
======

Syslog är en standard för message logging, även om inte strukturen på
meddelandena är standardiserad. Syslog använder default UDP port 514.
Syslog-meddelanden går även att skicka med
[SNMP](/Cisco_SNMP "wikilink")-traps, först skickas det lokalt till en
speciell history buffer och sedan replikerar SNMP agenten det till
traps.

`logging on`

Set syslog server logging level, 0-7.

`logging trap ?`

Source

`logging origin-id HOSTNAME`
`logging source-interface Loopback 0`

Bytt protokoll och port

`logging host 1.1.1.1 transport tcp port 5514`

Kommandologgning
================

`archive`
` log config`
`  logging enable`
`  notify syslog`
`  hidekeys`

Verify

`show archive log config all`

ACL
===

Förutom att öka hit count generera ett loggmeddelande när en ACL-regel
träffas.

`ip access-list extended Block_HTTP`
` 10 deny tcp any any eq 80 `**`log`**
` 20 permit ip any any`

För L2-info också använd *log-input* istället för log.

Access list logging interval (milliseconds) & log-update threshold
(number of hits)

`ip access-list logging interval 1000`
`ip access-list log-update threshold 10`

IOS kan generera och lägga på en MD5 hash på varje access-list entry.
Denna hash kan användas för att enklare söka och filtrera på
loggmeddelanden utifrån en viss regel. Hashen ligger kvar efter reboot.

`ip access-list logging hash-generation `

[Category:Cisco](/Category:Cisco "wikilink")