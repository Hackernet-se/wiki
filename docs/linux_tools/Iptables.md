---
title: Iptables
permalink: /Iptables/
---

Källa och väldigt bra läsning:
<http://www.lysator.liu.se/~kjell-e/tekla/linux/security/iptables/>

Sätt upp en brandvägg för att begränsa och blockera oönskad inkommande
trafik till din server, detta är valfritt men rekommenderat. Kommandot
iptables används för att kontrollera netfilter, den underliggande
tekniken som funnits med i linuxkärnan sedan 2.4.

Komponenter
===========

### Tables

Tables är de stora delarna av netfilter, och består av FILTER, NAT, och
MANGLE. FILTER används för vanlig hantering av paket, och är
standardtabellen om ingen annan anges. NAT används för att skriva om
source och/eller destination för paket. MANGLE används för att på annat
sätt modifiera paket, t.ex. modifiera olika delar av en TCP header.

### Chains

Chains är sedan associerade med varje table. Chains är listor av regler
inom en table, och de är associerade med platser där man kan avlyssna
trafiken och vidta åtgärder.

Dessa chains finns:

**PREROUTING:** Immediately after being received by an interface.

**POSTROUTING:** Right before leaving an interface.

**INPUT:** Right before being handed to a local process.

**OUTPUT:** Right after being created by a local process.

**FORWARD:** For any packets coming in one interface and leaving out
another.

### Kombinationer

**FILTER**: Input, Output, Forward

**NAT**: PREROUTING, POSTROUING, Output

**MANGLE**: PREROUTING, POSTROUING, Input, Output, Forward

### Targets

Targets bestämmer vad som kommer att hända med ett paket i en kedja om
en matchning hittas med en av dess regler. De två vanligaste är DROP och
ACCEPT.

Regelverk
=========

Kolla regelverk

`sudo iptables -S`

Skapa regelverk

``` bash
sudo dd of=/etc/iptables.firewall.rules << EOF
*filter

# Standard
-A INPUT -i lo -j ACCEPT
-A INPUT -d 127.0.0.0/8 -j REJECT
-A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Portar och protokoll
-A INPUT -p tcp --dport 80 -j ACCEPT
-A INPUT -p tcp --dport 443 -j ACCEPT
-A INPUT -p tcp -m state --state NEW --dport 22 -j ACCEPT
-A INPUT -p icmp --icmp-type echo-request -j ACCEPT

# Catch all
-A INPUT -j DROP
-A FORWARD -j DROP
-A OUTPUT -j ACCEPT

COMMIT
EOF
```

Rules activate!

`sudo iptables-restore < /etc/iptables.firewall.rules`
`sudo iptables -L -n -v --line-numbers`

### Persistent

Behåll regler efter omstart, Debian/Ubuntu

``` bash
sudo dd of=/etc/network/if-pre-up.d/firewall << EOF
#!/bin/sh
/sbin/iptables-restore < /etc/iptables.firewall.rules
EOF
sudo chmod +x /etc/network/if-pre-up.d/firewall
```

Alternativt använd iptables-persistent

`apt-get install iptables-persistent`
`iptables-save > /etc/iptables/rules.v4`

Dynamisk IP
===========

Att ha dynamisk IP suger men så är det ibland. Som tur är kan iptables
uppdatera sina regler automatiskt även om en IP-adress ändras. Det som
behövs är ett DNS-namn mot IPn.

`iptables -N DYNDNS`
`iptables -A INPUT -p tcp -m tcp --dport 22 -j DYNDNS`

Sedan ett script som körs enligt schemaläggning

``` bash
sudo dd of=/etc/dyndns.sh << EOF
#!/bin/bash
iptables -F DYNDNS
iptables -A DYNDNS -s dyndns.exempel.se -j ACCEPT
EOF
sudo chmod +x /etc/dyndns.sh
echo "0 * * * * /etc/dyndns.sh" | sudo crontab -
```

Uppdatering en gång i timmen

IPset
=====

IPset är ett verktyg för att hantera regler. Det är en extension till
iptables som tillåter skapandet av regler som matchar mot grupper med
t.ex. IP-adresser, nätverk och portar. Med grupper kan man få ner
antalet regelrader vilket förenklar uppsättning och felsökning samt ökar
skalbarhet och prestanda.

`sudo apt-get install ipset`
`sudo dnf install ipset`

Exempelanvändning, skapa ett set.

`ipset -N myset nethash`
`ipset -A myset 1.1.1.1`
`ipset -A myset 2.2.2.2`
`iptables -A INPUT -p tcp -m set --set myset src --dport 22 -j ACCEPT`

Kolla grupper

`sudo ipset list`

### Exempelscript

``` bash
## Firewall script by Helikopter

# Flush old settings
iptables -F && iptables -t mangle -F && iptables -X && iptables -t mangle -X && iptables -Z && ipset destroy

#####################################################################################
### Standardregler och policy

iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p icmp -j ACCEPT
iptables -A INPUT -i lo -j ACCEPT

# Default policy
iptables -P INPUT DROP
iptables -P OUTPUT ACCEPT
iptables -P FORWARD DROP


#####################################################################################
### Allt gors med grupper som definieras langre ner.

# Skapa grupper
ipset -N SSH nethash
ipset -N TSM nethash
ipset -N HTTPS nethash


# Regler, detta ar alla regler.
iptables -A INPUT -p tcp -m set --match-set SSH src --dport 22 -j ACCEPT
iptables -A INPUT -p tcp -m set --match-set TSM src --dport 1501 -j ACCEPT
iptables -A INPUT -p tcp -m set --match-set HTTPS src --dport 443 -j ACCEPT


#####################################################################################
### Har definieras grupperna, lagg IP-adresser har under.

## SSH
ipset -A SSH 172.16.20.0/24


## TSM
ipset -A TSM 172.16.10.100


## HTTPS
ipset -A HTTPS 10.0.2.0/24
ipset -A HTTPS 10.0.0.0/23
ipset -A HTTPS 172.24.190.110
ipset -A HTTPS 192.168.0.10
```

[Category:Tools](/Category:Tools "wikilink")