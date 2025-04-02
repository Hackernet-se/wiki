---
title: EFI
permalink: /EFI/
---

EFI gör det möjligt att lägga till och utveckla en rad funktioner som
inte är möjligt med ett vanligt BIOS.

efibootmgr: a Linux user-space application to modify the Intel
Extensible Firmware Interface (EFI) Boot Manager.

`apt-get install efibootmgr`

Tips n Tricks
-------------

Ändra boot order utan att stänga av maskinen:

Kolla nuvarande boot entries

`efibootmgr -v`

Rensa bort nuvarande boot order i EFI NVRAM

`efibootmgr --delete-bootorder`

Ta bort oönskade entries

`efibootmgr --delete-bootnum --bootnum 0003`

Konfigurera boot menu timeout

`efibootmgr --timeout 10`

Konfigurera den ordning du vill ha, t.ex.

`efibootmgr -o 0000,0002,0003,0001`

Lägg boot entry högst endast för nästa omstart

`efibootmgr -n 0003`

[Category:Tools](/Category:Tools "wikilink")