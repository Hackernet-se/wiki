---
title: Realmd
permalink: /Realmd/
---

realmd är en tjänst som gör det möjligt att konfigurera
nätverksautentisering och domänmedlemskap på ett standardiserat sätt.
realmd upptäcker information om domänen automatiskt. För Active
Directory Backend används SSSD, det går även med winbind men SSSD är
rekommenderat. Några fördelar med SSSD:

-   Snabbare inloggning
-   Klienter kan uppdatera sitt eget DNS record
-   Klienter har stöd för sites-featuren i AD
-   Enterprise Principals (UPN) är supporterade default

Installation
============

*Ubuntu*

`apt-get install realmd`
`apt-get install sssd`

Konfiguration
=============

`nano /etc/sssd/sssd.conf`
`[nss]`
`filter_groups = root`
`filter_users = root`
`reconnection_retries = 3`

`[pam]`
`reconnection_retries = 3`

Filrättigheter

`chmod 0600 /etc/sssd/sssd.conf`

Joina domän

`realm --verbose join domain.local -U Administrator`

Om det inte funkar, lägg till följande i sssd.conf

`use_fully_qualified_names = True`

Reboota maskinen

Testa

`id LOCALDOMAIN\\username`
`su username@localdomain`

[Category:Guider](/Category:Guider "wikilink")