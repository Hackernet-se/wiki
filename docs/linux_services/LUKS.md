---
title: LUKS
permalink: /LUKS/
---

Linux Unified Key Setup är standarden för hårddiskkryptering i Linux.

Cryptsetup
==========

cryptsetup är ett verktyg som krypterar/avkrypterar blockenheter i
realtid baserat på dm-crypt kernelmodulen.

`apt-get install cryptsetup`
`yum install cryptsetup-luks`

### Nuke

Vill man radera sin data väldigt snabbt oavsett mängd kan man sätta upp
en kill-switch.

`cryptsetup luksAddNuke /dev/sda5`