---
title: Fedora
permalink: /Fedora/
---

Fedora är en RPM-baserad linuxdistribution främst utvecklad av Red Hat.
Hela distributionen är fri programvara och används som en bas (läs PoC)
för den kommersiella distributionen Red Hat Enterprise Linux.
Kickstartfil: [Fedora](/Kickstart_Fedora "wikilink").

Pakethanterare
--------------

Se [Yum](/Yum "wikilink")
Se [DNF](/DNF "wikilink")

Network
-------

`systemctl stop NetworkManager.service && systemctl disable NetworkManager.service`
`systemctl enable network.service && systemctl start network.service`

Uppgradering
------------

Till 23 med hjälp av fedup som tankar alla nödvändiga filer.

`sudo dnf -y update && sudo dnf -y install fedup && sudo fedup --network 23`
`reboot`

Auto update
-----------

`sudo dnf -y install dnf-automatic`
`sudo systemctl enable dnf-automatic.timer`

*Default kollas det efter uppdateringar en gång per dygn*

SSH
---

`sudo systemctl enable sshd.service`

Gnome
-----

I det grafiska gränsnittet går det bara att sätta 15 minuter som max på
Blank screen under Power saving. Högre värde går att sätta med kommando.

`gsettings set org.gnome.desktop.session idle-delay 3600   #sekunder`
`gsettings set org.gnome.desktop.screensaver lock-delay 10`

Desktop

`gsettings set org.gnome.desktop.background show-desktop-icons true`
`gsettings set org.gnome.nautilus.desktop home-icon-visible false`

GRUB menu
---------

Fedora använder GRUB2 som bootloader och default visas menyn i 5
sekunder vid uppstart. Detta går att ta bort genom att ändra/lägga till
följande.

`sudo nano /etc/default/grub`
`GRUB_TIMEOUT=0`
`GRUB_HIDDEN_TIMEOUT=1`
`GRUB_HIDDEN_TIMEOUT_QUIET=true`

Hidden timeout 1 ger möjligheten att komma åt menyn med ESC i 1 sekund
under uppstart.

Uppdatera GRUB

`sudo grub2-mkconfig -o /boot/grub2/grub.cfg`

OBS Kör man UEFI kan filen heta /boot/efi/EFI/fedora/grub.cfg

[Category:Distar](/Category:Distar "wikilink")