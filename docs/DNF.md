---
title: DNF
permalink: /DNF/
---

DNF är en ersättare för yum. De flesta kommandon är likadana men det
finns även lite nya funktioner. Dokumentation:
<http://dnf.readthedocs.org/en/latest/index.html>
Grunder

`dnf search open-vm-tools`
`dnf install screen`
`dnf remove htop`
`dnf info firefox`

Repository

`dnf repolist`
`dnf repoquery --whatprovides `<command>

History

`dnf history list`

Rollback

`dnf history undo 7`

### System Upgrade

Uppgradera operativsystemet med hjälp av dnf.

`sudo dnf update --refresh`
`sudo dnf install dnf-plugin-system-upgrade`
`sudo dnf system-upgrade download --releasever=23  #`[`Fedora`](/Fedora "wikilink")
`sudo dnf system-upgrade reboot`

[Category:Tools](/Category:Tools "wikilink")