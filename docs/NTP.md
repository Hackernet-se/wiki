---
title: NTP
permalink: /NTP/
---

Ställ klockan rätt, slipp problem.

**Ntpdate:** engångssynkroniseringar (deprecated sedan 2012)
**Ntpd:** automatisk tidssynkronisering
**SNTP:** Simple NTP är inte lika pålitligt eller noggrannt som NTP
Ntpd \>= ntpdate + crontab

`yum/apt-get install ntp`

Konfiguration

`nano /etc/ntp.conf`
`server 10.0.0.10`

Verifiera

`ntptrace`
`ntpq -pn`

### Time Zone

`timedatectl`
`sudo timedatectl set-timezone Europe/Stockholm`

[Category:Tools](/Category:Tools "wikilink")