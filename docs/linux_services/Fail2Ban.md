---
title: Fail2Ban
permalink: /Fail2Ban/
---

[Category:Guider](/Category:Guider "wikilink") Fail2ban söker av log
filerna för olika tjänster som ssh, apache etc och letar efter tex
bruteforce attacker eller om en exploit försökt köras. Fail2ban
uppdaterar då brandväggen att blocka all trafik från den IP'n i ex antal
minuter.

Installation
============

**Deb baserad.**

`apt-get install fail2ban`

**RPM baserad**

`yum install fail2ban`

Konfiguration
=============

Fail2ban kommer med bra inställningar ifrån början. Vill man ändra dom
gör man det i `/etc/fail2ban/jail.conf`

|          |                                                                              |
|----------|------------------------------------------------------------------------------|
| maxretry | Antalet gånger något får hända. Tex 5 felaktiga lösenord.                    |
| findtime | Hur många gånger man får skriva tex felaktigt lösenord under en tidsperiod.  |
| bantime  | Hur länge en IP blir bannad. Skrivs i sekunder, **-1** ger en permanent ban. |

SSH Repeater permanent ban
--------------------------

Om en IP försöker bruteforca dig så kan det vara skönt att blocka IP'n
permanent istället.

Skapa följande fil `/etc/fail2ban/action.d/iptables-repeater.conf`

` # Fail2ban configuration file`
`#`
`# Author: Phil Hagen <phil@identityvector.com>`
`#`

`[Definition]`

`# Option:  actionstart`
`# Notes.:  command executed once at the start of Fail2Ban.`
`# Values:  CMD`
`#`
`actionstart = iptables -N fail2ban-REPEAT-`<name>
`              iptables -A fail2ban-REPEAT-`<name>` -j RETURN`
`              iptables -I INPUT -j fail2ban-REPEAT-`<name>
`              # set up from the static file`
`              cat /etc/fail2ban/ip.blocklist.`<name>` |grep -v ^\s*#|awk '{print $1}' | while read IP; do iptables -I fail2ban-REPEAT-`<name>` 1 -s $IP -j DROP; done`

`# Option:  actionstop`
`# Notes.:  command executed once at the end of Fail2Ban`
`# Values:  CMD`
`#`
`actionstop = iptables -D INPUT -j fail2ban-REPEAT-`<name>
`             iptables -F fail2ban-REPEAT-`<name>
`             iptables -X fail2ban-REPEAT-`<name>

`# Option:  actioncheck`
`# Notes.:  command executed once before each actionban command`
`# Values:  CMD`
`#`
`actioncheck = iptables -n -L INPUT | grep -q fail2ban-REPEAT-`<name>

`# Option:  actionban`
`# Notes.:  command executed when banning an IP. Take care that the`
`#          command is executed with Fail2Ban user rights.`
`# Tags:    `<ip>`  IP address`
`#          `<failures>`  number of failures`
`#          `<time>`  unix timestamp of the ban time`
`# Values:  CMD`
`#`
`actionban = iptables -I fail2ban-REPEAT-`<name>` 1 -s `<ip>` -j DROP`
`            # also put into the static file to re-populate after a restart`
`            ! grep -Fq `<ip>` /etc/fail2ban/ip.blocklist.`<name>` && echo "`<ip>` # fail2ban/$( date '+%%Y-%%m-%%d %%T' ): auto-add for repeat offender" >> /etc/fail2ban/ip.blocklist.`<name>

`# Option:  actionunban`
`# Notes.:  command executed when unbanning an IP. Take care that the`
`#          command is executed with Fail2Ban user rights.`
`# Tags:    `<ip>`  IP address`
`#          `<failures>`  number of failures`
`#          `<time>`  unix timestamp of the ban time`
`# Values:  CMD`
`#`
`actionunban = /bin/true`

`[Init]`

`# Defaut name of the chain`
`#`
`name = REPEAT`

Skapa sedan ett jail i `/etc/fail2ban/jail.conf`

`...`
`[ssh-repeater]`
`enabled  = true`
`filter   = sshd`
`action   = iptables-repeater[name=ssh]`
`           sendmail-whois[name=SSH-repeater, dest=root, sender=root]`
`logpath  = /var/log/auth`
`maxretry = 10`
`findtime = 7200`
`bantime  = -1`
`...`

Denna regeln gör att en IP blir permbannad om den skrivit fel lösenord
över SSH mer än 10 gånger dom senaste 2 timmarna.