---
title: ESXi Secure Boot
permalink: /ESXi_Secure_Boot/
---

Secure Boot
-----------

ESXi 6.5 har inbyggt stöd för Secure Boot, för att kunna säkerställa att
ESXi endast startar med en signerad bootloader. Osignerad kod kan inte
heller köras i hypervisorn. VMware:s implementation består av följande
komponenter:

#### Boot Loader

Som vid klassisk Secure Boot verifierar UEFI bootloaderns digitala
signatur. ESXi:s bootloader är signerad med Microsoft UEFI Public CA och
innehåller även en publik VMware-nyckel. Denna nyckel används för
validering av VMKernel och ett fåtal systemfunktioner, däribland Secure
Boot Verifier, som används för att validera VIB:ar.

#### VMKernel

VMKernel är signerad med VMware:s privata nyckel och valideras av
bootloadern mha ovan nämnda publika nyckel. Det första VMKernel själv
gör är att köra Secure Boot Verifier.

#### Secure Boot Verifier

Secure Boot Verifier validerar varje signerad VIB mot VMware:s publika
nyckel.

Man kan köra följande skript för att verifiera om Secure Boot kan slås
på eller inte:

`/usr/lib/vmware/secureboot/bin/secureboot.py -c`

VIB:ar & Secure Boot
--------------------

Vid uppgradering av vSphere uppdateras VIB:arnas signaturer, så länge de
finns med i nyare version bland uppgraderingspaketen. En uppgradering
via ESXCLI kommer dock inte att uppgradera bootloadern vilket kommer
resultera i fel ifall Secure Boot slås på, den enda workarounden är
ominstallation. Community-VIB:ar kan inte installeras på en host som
använder Secure Boot, då de inte signeras. Alla VIB-paket måste vara
minst PartnerSupported. En host som upptäckt en osignerad VIB efter
påslagning av Secure Boot kommer att få PSOD med ett meddelande om
vilken VIB som orsakat detta. För att lösa problemet måste VIB:en tas
bort eller uppdateras till en supporterad version. Secure Boot måste
först stängas av i UEFI, ESXi startas sedan för att administratören ska
kunna ta bort/uppdatera VIB-paketet. Efter detta slår man på Secure Boot
i UEFI igen och startar ESXi.

Virtuella Maskiner och Secure Boot
----------------------------------

Det finns vissa krav för att en virtuell maskin ska stödja Secure Boot:

-   VMware Tools 10.1 eller senare.
-   Linux-maskiner måste stänga av "VMware Host-Guest Filesystem" i
    VMware Tools.
-   Virtual Hardware 13 eller senare.
-   OS:et måste ha stöd för UEFI Secure Boot.

För att slå på VM Secure Boot: **Edit Settings** -\> **VM Options** -\>
ändra **Firmware** från "**BIOS**" till "**EFI**" och tryck **OK**.

[Category:VMware](/Category:VMware "wikilink")